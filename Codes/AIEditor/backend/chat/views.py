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

        response = asyncio.run(async_chat('请为以下内容续写一段文字,在续写的文字前加上以下内容，保证只有一个自然段' + text))

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
        prompt = f'我想让你充当{target_language}翻译员、拼写纠正员和改进员。我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答。我希望你用更优美优雅的高级{target_language}单词和句子替换我简化的单词和句子。保持相同的意思，但使它们更文艺。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它。我要你只回复更正、改进，不要写任何解释。'
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
        # 待修改内容中出现而模板中不存在的元素忽略修改保留原样式即可
        prompt = "我从tiptap在线编辑器中得到了一段html格式的文本，现在我希望你可以对我得到的文本重新进行排版和字体样式修改，模板参考:" + template_content + "请你根据待修改内容元素的类型，添加与模板元素类型严格一致样式。如果待修改内容中与模板中对应的元素内部还包括mark、u、strong、em、s等元素，也请严格按照顺序添加。修改完成后，直接返回修改后的HTML结果即可，除此之外不要添加任何解释、注意、说明、内容标识等类似的内容。绝对不要在输出中标识输出的结果是HTML。待修改内容如下："

        # 使用 asyncio.run 来运行异步函数
        response = asyncio.run(async_chat(prompt + html_content))
        print(response)

        return JsonResponse({'response': response}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
