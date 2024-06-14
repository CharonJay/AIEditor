from django.shortcuts import render
from django.shortcuts import HttpResponse

import os
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.memory import HumanMessage, AIMessage

import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

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


"""@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    try:
        data = request.POST.get('message', '')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(chat_with_bot(data))
        return JsonResponse({'response': response}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    try:
        # 确保可以解析JSON数据
        data = json.loads(request.body.decode('utf-8'))  # 确保正确解码
        message = data.get('message', '')  # 提供默认值避免NoneType错误

        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        reply = f"收到了你的消息：{message}"
        return JsonResponse({'response': reply}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)"""


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