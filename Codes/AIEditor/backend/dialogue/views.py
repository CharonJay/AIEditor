from django.shortcuts import render

import os
import asyncio
from django.http import JsonResponse, StreamingHttpResponse
from asgiref.sync import async_to_sync

from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import HumanMessage, AIMessage
from erniebot_agent.tools import RemoteToolkit

import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.views.decorators.csrf import csrf_exempt

# 大模型的memory
from erniebot_agent.memory import AIMessage, HumanMessage, WholeMemory
from erniebot_agent.memory import LimitTokensMemory
from erniebot_agent.memory import SlidingWindowMemory
from langchain_community.document_loaders import PyPDFLoader

# 数据库
from .models import Helper
from user.models import CustomUser
from asgiref.sync import sync_to_async
from dialogue.utils.crypto_AES import encrypt, decrypt

# 缓存
from django.core.cache import cache

# 知识库
from dialogue.utils.kb import FaissSearch, kb_Document, KnowledgeBase, merge_documents_by_metadata
from dialogue.utils.read_file import read_pdf_pymupdf
from erniebot_agent.extensions.langchain.embeddings import ErnieEmbeddings

from langchain.text_splitter import SpacyTextSplitter

from langchain_community.vectorstores import FAISS
from dialogue.instantiation_kb import kb

from backend import settings

# Create your views here.
os.environ["EB_AGENT_ACCESS_TOKEN"] = "667595ca971e8228418f477dd45e78444b88c14e"


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    async def post(self, request, user_id):
        try:
            body_unicode = request.body.decode('utf-8')  # 解码请求体
            data = json.loads(body_unicode)  # 解析JSON数据
            prompt = data.get('message')
            if not prompt:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # 去读缓存
            user_model = cache.get(f'user_model_{user_id}')
            user_messages = cache.get(f'user_messages_{user_id}')
            # user_memory=cache.get(f'user_memory_{user_id}')

            user_messages.append(HumanMessage(prompt))
            ai_message = await user_model.chat(messages=user_messages, stream=True)
            result = ''

            async for chunk in ai_message:
                result += chunk.content
            user_messages.append(AIMessage(result))
            response_message = result
            # print(response_message)

            uId = user_id

            # 加密相关内容，加入新的记忆在数据库中
            IV = os.urandom(16)
            # print(IV)
            encrypted_question = encrypt(IV, prompt)
            encrypted_answer = encrypt(IV, response_message)
            user = await sync_to_async(CustomUser.objects.get)(pk=uId)
            helper = Helper(uId=user, hQuestion=encrypted_question, hAnswer=encrypted_answer, IV=IV)
            await sync_to_async(helper.save)()


            return JsonResponse({'response': response_message}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# 获取知识库中所有内容
@csrf_exempt
def get_kb(request, user_id):
    try:
        # kb.load_kb(f'user{user_id}',f'user{user_id}')
        docs = kb.list_documents(f'user{user_id}')
        if not docs:
            return JsonResponse({'resonse': '知识库中无内容'}, status=200)
        merged_docs = merge_documents_by_metadata(docs)
        response_data = [
            {"content": doc.page_content, "source": doc.metadata["source"]}
            for doc in merged_docs
        ]
        return JsonResponse({'知识库的内容': response_data}, status=200)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=404)

    except Exception as e:
        return JsonResponse({'error': '服务器内部错误', '详情': str(e)}, status=500)


# 在知识库中加入新内容_pdf
@csrf_exempt
def add_new_pdf(request, user_id):
    # 获取上传的文件
    if request.method == 'POST':
        # try:
            # 读取文件,需要文件保存的路径和文件名
            uploaded_file = request.FILES.get('file')
            filename = uploaded_file.name
            file_path = os.path.join(settings.MEDIA_ROOT_CHAT, 'file', 'save', uploaded_file.name)
            # 保存到知识库中
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            text = ""
            new_document = []
            for doc in documents:
                text = doc.page_content
                new_document.append(kb_Document(text, {"source": filename}))
            print(text)
            kb.add_documents(f'user{user_id}', new_document)
            print("2222")
            kb.save_kb(f'user{user_id}', f'user{user_id}')

            return JsonResponse({'success': '加入成功'}, status=200)
        # except Exception as e:
        #     # 捕获异常并返回错误信息
        #     return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'No file provided'}, status=400)


# 在知识库中加入新内容_orc等
@csrf_exempt
def add_new_str(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get('content')
            title = data.get('title')

            if not content or not title:
                return JsonResponse({'error': '内容和标题不能为空'}, status=400)

            # 添加新内容到知识库
            new_document = kb_Document(content, {"source": title})
            kb.add_documents(f'user{user_id}', [new_document])

            # 更新缓存中的知识库，跟新本地的知识库
            kb.save_kb(f'user{user_id}', f'user{user_id}')

            return JsonResponse({'success': '新内容已添加到知识库'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': '服务器内部错误', '详情': str(e)}, status=500)

    return JsonResponse({'error': '仅支持POST请求'}, status=405)


# 删除知识库中的文档
@csrf_exempt
def de_document(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            document_name = data.get('name')
            if not document_name:
                return JsonResponse({'error': '文档名称不能为空'}, status=400)
            # print(document_name)
            # 删除指定名称的文档
            kb.delete_document(f'user{user_id}', {"source": document_name})
            kb.save_kb(f'user{user_id}', f'user{user_id}')
            return JsonResponse({'success': '文档已从知识库中删除'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': '服务器内部错误', '详情': str(e)}, status=500)

    return JsonResponse({'error': '仅支持POST请求'}, status=405)


# 获取知识库中某个文件的内容
@csrf_exempt
def get_document(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            document_name = data.get('name')
            if not document_name:
                return JsonResponse({'error': '文档名称不能为空'}, status=400)

            docs = kb.query_by_metadata(f'user{user_id}', {"source": document_name})
            if not docs:
                return JsonResponse({'resonse': '知识库中无内容'}, status=200)
            merged_docs = merge_documents_by_metadata(docs)
            response_data = [
                {"content": doc.page_content, "source": doc.metadata["source"]}
                for doc in merged_docs
            ]
            return JsonResponse({'文档内容': response_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': '服务器内部错误', '详情': str(e)}, status=500)
    return JsonResponse({'error': ''}, status=500)


# 知识库和大模型结合的对话
from erniebot_agent.agents.function_agent_with_retrieval import FunctionAgentWithRetrieval

llm = ERNIEBot(model='ernie-4.0')
aistudio_access_token = os.environ.get("EB_AGENT_ACCESS_TOKEN", "")
embeddings = ErnieEmbeddings(aistudio_access_token=aistudio_access_token, chunk_size=16)
tts_tool = RemoteToolkit.from_aistudio("texttospeech").get_tools()


@csrf_exempt
def kb_chat(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')

            if not prompt:
                return JsonResponse({'error': '对话内容不能为空'}, status=400)

            # 从缓存中获取用户知识库和模型
            db = FAISS.load_local(kb.fpath + f'/user{user_id}', embeddings, allow_dangerous_deserialization=True)
            # print(db)
            faiss_search = FaissSearch(db=db, embeddings=embeddings)
            # res = faiss_search.search(query=prompt)
            agent = FunctionAgentWithRetrieval(llm=llm, tools=tts_tool, knowledge_base=faiss_search, threshold=0.5)

            async def demo():
                response = await agent.run(prompt)
                return response

            response = asyncio.run(demo())
            # messages = response.chat_history
            # for item in messages:
            #    print(item.to_dict())

            return JsonResponse({'response': response.text}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': '服务器内部错误', '详情': str(e)}, status=500)

    return JsonResponse({'error': '仅支持POST请求'}, status=405)
