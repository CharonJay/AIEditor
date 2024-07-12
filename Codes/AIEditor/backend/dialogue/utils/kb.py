from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.vectorstores import FAISS
import pickle
import os


# 相似性搜索
class FaissSearch:
    def __init__(self, db, embeddings):
        # 数据库实例self.db 中，embeddings方法
        self.db = db
        self.embeddings = embeddings

    def search(self, query: str, top_k: int = 10, **kwargs):
        docs = self.db.similarity_search(query, top_k)
        # 获取与查询最相关的文档
        para_result = self.embeddings.embed_documents([i.page_content for i in docs])
        # 进行相似性比较
        query_result = self.embeddings.embed_query(query)
        # 对查询字符串也进行嵌入
        similarities = cosine_similarity([query_result], para_result).reshape((-1,))
        # 计算查询嵌入和文档嵌入之间的余弦相似度
        retrieval_results = []
        for index, doc in enumerate(docs):
            retrieval_results.append(
                {"content": doc.page_content, "score": similarities[index], "title": doc.metadata}
            )
        # 遍历每个文档
        return retrieval_results


class KnowledgeBase:
    def __init__(self, splitter, embeddings, fpath):
        self.splitter = splitter  # 文本分割器
        self.embeddings = embeddings  # 嵌入模型
        self.user_kbs = {}  # 每个用户的FAISS索引
        self.document_mapping = {}  # 每个用户的文档映射
        self.fpath = fpath  # 所有用户的存储目录

    # 上传一个文档，并加入
    def add_documents(self, user_id, documents):
        docs = self.splitter.split_documents(documents)
        # print("splitter后的结果",docs)
        if user_id not in self.user_kbs:
            # 如果用户不在user_kbs中，则创建并加入
            self.user_kbs[user_id] = FAISS.from_documents(docs, self.embeddings)
            self.document_mapping[user_id] = docs
        else:
            # 如果存在，则更新文档映射和 FAISS 索引
            existing_docs = self.document_mapping[user_id]
            all_docs = existing_docs + docs
            self.user_kbs[user_id] = FAISS.from_documents(all_docs, self.embeddings)
            self.document_mapping[user_id] = all_docs

    # 删除一个文档
    def delete_document(self, user_id, document_metadata):
        if user_id not in self.user_kbs:
            raise ValueError(f"No knowledge base found for user {user_id}")
        if user_id not in self.document_mapping:
            raise ValueError(f"No documents found for user {user_id}")

        # 找到文档并从映射中移除
        # updated_docs = [doc for doc in self.document_mapping[user_id] if doc['content'] != document_content]
        updated_docs = [doc for doc in self.document_mapping[user_id] if doc.metadata != document_metadata]
        # print(updated_docs)
        # print('----------')
        # print(self.document_mapping[user_id])
        # print('-------------------------')
        # print(self.document_mapping)

        if len(updated_docs) == len(self.document_mapping[user_id]):
            raise ValueError(f"Document not found in user {user_id}'s knowledge base")

        # 更新
        self.document_mapping[user_id] = updated_docs

        if updated_docs:

            self.user_kbs[user_id] = FAISS.from_documents(updated_docs, self.embeddings)
        else:
            self.user_kbs[user_id] = FAISS.from_documents([kb_Document(' ', {})], self.embeddings)
            # del self.user_kbs[user_id]
            # del self.document_mapping[user_id]

    # 保存知识库
    def save_kb(self, user_id, filepath):
        if user_id not in self.user_kbs:
            raise ValueError(f"No knowledge base found for user {user_id}")
        self.user_kbs[user_id].save_local(self.fpath + f"/{filepath}")
        with open(self.fpath + f"/{filepath}" + "_mapping.pkl", 'wb') as f:
            pickle.dump(self.document_mapping[user_id], f)

    # 查看已有的知识
    def list_documents(self, user_id):
        if user_id not in self.document_mapping:
            raise ValueError(f"No documents found for user {user_id}")
        return self.document_mapping[user_id]

    # 加载知识库
    def load_kb(self, user_id, filepath):
        if not os.path.exists(self.fpath + '/' + filepath) or not os.path.exists(
                self.fpath + f"/{filepath}" + "_mapping.pkl"):
            self.user_kbs[user_id] = FAISS.from_documents([kb_Document(' ', {})], self.embeddings)
            self.document_mapping[user_id] = []
            self.user_kbs[user_id].save_local(self.fpath + f"/{filepath}")
            with open(self.fpath + f"/{filepath}" + "_mapping.pkl", 'wb') as f:
                pickle.dump(self.document_mapping[user_id], f)

        self.user_kbs[user_id] = FAISS.load_local(self.fpath + f"/{filepath}", self.embeddings,
                                                  allow_dangerous_deserialization=True)
        with open(self.fpath + f"/{filepath}" + "_mapping.pkl", 'rb') as f:
            self.document_mapping[user_id] = pickle.load(f)
        # print(self.document_mapping[user_id])

    # 查询指定 metadata 的所有文档
    def query_by_metadata(self, user_id, metadata):
        if user_id not in self.document_mapping:
            raise ValueError(f"No documents found for user {user_id}")
        result = [doc for doc in self.document_mapping[user_id] if doc.metadata == metadata]
        return result

    # 搜索部分，待定
    def search1(self, user_id, query, top_k=10):
        if user_id not in self.user_kbs:
            raise ValueError(f"No knowledge base found for user {user_id}")
        return self.user_kbs[user_id].similarity_search(query, top_k)


# 文档类，处理下文档
class kb_Document:
    def __init__(self, content, metadata):
        self.page_content = content
        self.metadata = metadata


# 合并相同source的文档
from collections import defaultdict


def merge_documents_by_metadata(documents):
    merged_docs_dict = defaultdict(list)
    for doc in documents:
        merged_docs_dict[doc.metadata["source"]].append(doc.page_content)

    merged_docs = []
    for source, contents in merged_docs_dict.items():
        combined_content = "\n".join(contents)
        merged_docs.append(kb_Document(combined_content, {"source": source}))

    return merged_docs
