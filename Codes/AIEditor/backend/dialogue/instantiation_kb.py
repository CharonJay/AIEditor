#知识库实例化
from dialogue.utils.kb import KnowledgeBase
from erniebot_agent.extensions.langchain.embeddings import ErnieEmbeddings

from langchain.text_splitter import SpacyTextSplitter
import os

os.environ["EB_AGENT_ACCESS_TOKEN"] = "667595ca971e8228418f477dd45e78444b88c14e"

aistudio_access_token = os.environ.get("EB_AGENT_ACCESS_TOKEN", "")
embeddings = ErnieEmbeddings(aistudio_access_token=aistudio_access_token, chunk_size=16)
text_splitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=320, chunk_overlap=0)

fpath='faiss_index'
kb = KnowledgeBase(text_splitter, embeddings,fpath)