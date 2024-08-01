from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.conf import settings

import os
import asyncio
from django.http import JsonResponse, StreamingHttpResponse
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import HumanMessage, AIMessage
from erniebot_agent.file import GlobalFileManagerHandler
from erniebot_agent.agents import FunctionAgent

from erniebot_agent.tools import RemoteToolkit

import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

import cv2
import numpy as np
import os
import paddle
from paddleocr import PaddleOCR, draw_ocr
import re

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# Create your views here.
app_name = "chat"

os.environ["EB_AGENT_ACCESS_TOKEN"] = "667595ca971e8228418f477dd45e78444b88c14e"

model = ERNIEBot(model='ernie-4.0')
messages = []


async def get_ernie_response(prompt):
    messages.append(HumanMessage(prompt))
    ai_message = await model.chat(messages=messages, stream=True)

    result = ''
    async for chunk in ai_message:
        result += chunk.content
    messages.append(AIMessage(result))
    return result


async def async_chat(human_message_content):
    human_message = HumanMessage(content=human_message_content)
    ai_message = await model.chat(messages=[human_message])

    return ai_message.content

async def async_chat_format(human_message_content):
    human_message = HumanMessage(content=human_message_content)
    format_model = ERNIEBot(model='ernie-4.0')
    ai_message = await format_model.chat(messages=[human_message])

    return ai_message.content

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    async def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')  # 解码请求体
            data = json.loads(body_unicode)  # 解析JSON数据
            prompt = data.get('message')
            if not prompt:
                return JsonResponse({'error': 'No message provided'}, status=400)

            response_message = await get_ernie_response(prompt)
            return JsonResponse({'response': response_message}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def AI_summary(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')  # 解码请求体
        data = json.loads(body_unicode)  # 解析JSON数据
        text = data.get('message')
        if not text:
            return JsonResponse({"error": "No message provided"}, status=400)

        response = asyncio.run(async_chat('请为以下内容写出简要的摘要，请不要输出注释的内容，只输出结果：' + text))
        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def AI_polish(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')  # 解码请求体
        data = json.loads(body_unicode)  # 解析JSON数据
        text = data.get('message')
        if not text:
            return JsonResponse({"error": "No message provided"}, status=400)

        response = asyncio.run(async_chat('请修饰以下内容，使其更优美流畅，请只输出文本内容，不加入格式：' + text))

        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def AI_continuation(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')  # 解码请求体
        data = json.loads(body_unicode)  # 解析JSON数据
        text = data.get('message')
        if not text:
            return JsonResponse({"error": "No message provided"}, status=400)

        response = asyncio.run(
            async_chat('请为以下内容续写一段文字,在续写的文字前加上以下内容，保证只有一个自然段' + text))

        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def AI_correction(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')  # 解码请求体
        data = json.loads(body_unicode)  # 解析JSON数据
        text = data.get('message')
        if not text:
            return JsonResponse({"error": "No message provided"}, status=400)

        response = asyncio.run(async_chat(
            '请改正以下内容中的病句，使其语法正确、通顺，请根据将结果输出为与输入文本的相同的语言，无需任何格式和备注，如果原句没有语病，请直接输出原句，不要用括号写出注释：' + text))

        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def AI_translation(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')  # 解码请求体
        data = json.loads(body_unicode)  # 解析JSON数据
        text = data.get('message')
        target_language = request.GET.get("target_language", "英语")
        if not text:
            return JsonResponse({"error": "No message provided"}, status=400)
        prompt = f'我想让你充当{target_language}翻译员、拼写纠正员和改进员。我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它。我要你只回复更正、改进，不要写任何解释。'
        response = asyncio.run(async_chat(prompt + text))

        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def handle_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Construct the file path using MEDIA_ROOT_CHAT
        file_path = os.path.join(settings.MEDIA_ROOT_CHAT, 'file', 'save', uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        url = f"http://localhost:8000/chat/file/save/{uploaded_file.name}"

        # Return a JSON response indicating success
        return JsonResponse({'message': 'File uploaded successfully.'})

    # Return an error message if no file was uploaded
    return JsonResponse({'error': 'No file uploaded.'}, status=400)


@csrf_exempt
def AI_ocr(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        filename = uploaded_file.name
        file1_path = "./chat/file/save/"
        file_path = file1_path + filename
        # ocr
        result = ocr.ocr(file_path, cls=True)
        text = ''
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                txts = line[1][0]
                text = text + '\n' + txts

        # 处理识别到的文字
        response = asyncio.run(async_chat(
            '这些句子是从图像中提取的零散文本行，请重新排列并重写它们，形成一个连贯且逻辑流畅的段落。确保最终文本在语法上正确，内容上准确，并易于理解。原始文本行为：' + text))
        # print(response)
        return JsonResponse({'text': response})

    return JsonResponse({'error': 'No file uploaded.'}, status=400)


@csrf_exempt
async def AI_asr(request):
    if request.method == 'POST':
        # 创建ASR识别智能体
        asr_tool = RemoteToolkit.from_aistudio("asr").get_tools()[0]
        agent = FunctionAgent(
            llm=ERNIEBot(model="ernie-4.0"),
            tools=[asr_tool],
        )

        uploaded_file = request.FILES.get('file')
        filename = uploaded_file.name
        file1_path = "./chat/file/save/"
        file_path = file1_path + filename

        file_manager = GlobalFileManagerHandler().get()
        local_file = await file_manager.create_file_from_path(file_path=file_path, file_type="local")

        agent_response = await agent.run("这个音频讲了什么", files=[local_file])
        result_text = agent_response.text
        return JsonResponse({'text': result_text})

    return JsonResponse({'error': 'No file uploaded.'}, status=400)


@csrf_exempt
def delete_multi_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        filename = uploaded_file.name
        file1_path = "./chat/file/save/"
        file_path = file1_path + filename
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return JsonResponse({'message': 'File deleted successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)


@csrf_exempt
def AI_Format(request):
    if request.method == 'POST':

        html_content = request.POST.get('htmlContent')

        template_content = request.POST.get('templateContent')
        print(template_content)

        # 待修改内'容中出现而模板中不存在的元素忽略修改保留原样式即可
        role = """你现在是一名专业的格式排版大师，能够轻松胜任格式排版工作。用户将输入一个模板和待排版文档，他们都是html格式的。根据待排版文档中文本的内容类型识别应该使用模板中的对应类型的样式，如自动调整字体字号、字体颜色、分段、换行、修改标点符号、加重加粗关键词、下划线等。最后返回排版后的html代码即可，无需任何额外对话,也不要输出任何解释。"""
        prompt = role + "模板参考:" + template_content + "。待修改内容如下："

        # 使用 asyncio.run 来运行异步函数
        response = asyncio.run(async_chat_format(prompt + html_content))
        print(response)
        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def AI_mind_map(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        html_content = data.get('htmlContent')

        mindmap_format = """{
            data: {
              text: '我是自动生成的节点'
            },
            children: [
              {
                data: {
                  text: '子节点'
                },
                children: []
              },
              {
                data: {
                  text: '子节点2'
                },
                children: []
              }
            ]
          }"""

        prompt = "你是一名高级文秘，仔细阅读下面的文章后给出这篇文章的摘要，请你根据以下Tiptap编辑器中编辑得到的内容" + html_content + "，总结其中的要点，并输出根节点(data)及其对应的子节点(children),输出模板如下" + mindmap_format + "，结果必须用json代码的格式输出"

        # 使用 asyncio.run 来运行异步函数
        response = asyncio.run(async_chat(prompt + html_content))
        mind_map_data = response
        # 使用正则表达式删除输出文本中的代码标柱
        pattern = r'^```json\s*([\s\S]*)\s*```$'
        match = re.search(pattern, mind_map_data, re.MULTILINE)
        if match:
            mind_map_data = match.group(1)
            # 解析为 JSON 对象
            mind_map_json = json.loads(mind_map_data)
            return JsonResponse(mind_map_json, status=200)
        else:
            mind_map_json = json.loads(mind_map_data)
            return JsonResponse(mind_map_json, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


import json
import time
import requests
from django.http import JsonResponse

API_KEY = "A9W8WBdQQrEjtVl5YnrNZhBq"
SECRET_KEY = "UbR7EYBlwnSfNj2Y5oXNrkZCPCNbs5tH"


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 绘图
def draw(text):
    url = "https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/textToImage?access_token=" + get_access_token()

    payload = json.dumps({
        "text": text,
        "resolution": "512*512"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)

    # 提取 taskId
    task_id = response_data["data"]["taskId"]
    return task_id


# 读图
def read_picture(taskId):
    url = "https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/getImg?access_token=" + get_access_token()

    payload = json.dumps({
        "taskId": taskId
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = json.loads(response.text)

        # 检查 status
        status = response_data["data"]["status"]
        if status == 1:
            return response_data["data"]["img"]
        elif status == 0:
            time.sleep(5)  # 等待 5 秒后再次检查状态
        else:
            return None


@method_decorator(csrf_exempt, name='dispatch')
class ImageGeneratorView(View):
    def post(self, request, *args, **kwargs):
        # try:
            body = json.loads(request.body)
            text = f"{body.get('style', '')} {body.get('subject', '')} {', '.join(body.get('description', []))} {body.get('effect', '')} {body.get('otherContent', '')}"
            if not text.strip():
                return JsonResponse({"error": "缺少必要的描述信息"}, status=400)

            task_id = draw(text)
            img_url = read_picture(task_id)
            print(img_url)
            if img_url:
                # 下载图片并保存到本地
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    print("111")
                    img_path = os.path.join(settings.MEDIA_ROOT, f"{task_id}.png")
                    print("222")
                    print(img_path)
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)
                    return JsonResponse({"img_url": request.build_absolute_uri(settings.MEDIA_URL + f"{task_id}.png")})
                else:
                    return JsonResponse({"error": "下载图片失败"}, status=500)
            else:
                return JsonResponse({"error": "图片生成失败"}, status=500)
        # except Exception as e:
        #     return JsonResponse({"error": str(e)}, status=500)