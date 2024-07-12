from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.core.cache import cache

import os

# 大模型
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import HumanMessage, AIMessage

# 大模型的memory
from erniebot_agent.memory import AIMessage, HumanMessage, WholeMemory
from erniebot_agent.memory import LimitTokensMemory
from erniebot_agent.memory import SlidingWindowMemory

# 数据库
from .models import Helper
from asgiref.sync import sync_to_async
from dialogue.utils.crypto_AES import encrypt, decrypt

from langchain_community.vectorstores import FAISS
from erniebot_agent.extensions.langchain.embeddings import ErnieEmbeddings

from langchain.text_splitter import SpacyTextSplitter

from dialogue.instantiation_kb import kb

os.environ["EB_AGENT_ACCESS_TOKEN"] = "667595ca971e8228418f477dd45e78444b88c14e"

aistudio_access_token = os.environ.get("EB_AGENT_ACCESS_TOKEN", "")
embeddings = ErnieEmbeddings(aistudio_access_token=aistudio_access_token, chunk_size=16)

text_splitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=320, chunk_overlap=0)


def create_user_ai_model(user):
    user_id = user.id
    helpers = Helper.objects.filter(uId=user_id).order_by('hId')

    user_model = ERNIEBot(model='ernie-4.0')
    user_messages = []
    user_memory = SlidingWindowMemory(max_round=20, retained_round=0)

    # 加入记忆
    for helper in helpers:
        user_messages.append(HumanMessage(decrypt(helper.IV, helper.hQuestion)))
        user_messages.append(AIMessage(decrypt(helper.IV, helper.hAnswer)))

    user_memory.add_messages(user_messages)
    # print(user_messages)
    # print(user_memory)

    kb.load_kb(f'user{user_id}', f'user{user_id}')

    # 读取知识库
    # user_kb = FAISS.load_local('faiss_index'+f'/user{user_id}', embeddings,allow_dangerous_deserialization=True)

    # 加入到缓存中
    print(user_messages)
    DEFAULT_TIMEOUT = 7200  # 2 hours in seconds
    timeout = DEFAULT_TIMEOUT

    cache.set(f'user_model_{user_id}', user_model, timeout)
    cache.set(f'user_messages_{user_id}', user_messages, timeout)
    cache.set(f'user_memory_{user_id}', user_memory, timeout)
    # cache.set(f'user_kb_{user_id}',user_kb)


# 退出登录删除缓存
def delete_user_ai_model(user_id):
    cache.delete(f'user_model_{user_id}')
    cache.delete(f'user_messages_{user_id}')
    cache.delete(f'user_memory_{user_id}')
    # cache.delete(f'user_kb_{user_id}')
