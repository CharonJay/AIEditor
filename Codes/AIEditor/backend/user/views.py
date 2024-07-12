from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, FileSerializer, DocumentTemplateSerlizer, DocumentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Files, DocumentTemplate, Documents

app_name = "user"
User = get_user_model()


# Create your views here.
class LoginView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({'message': 'Hello, user.'})


class RegisterView(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'detail': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data.get('username')).exists():
            return Response({'detail': 'Username already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFilesCreateByUserView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        creator = self.kwargs['creator']
        creator = get_object_or_404(User, username=creator)
        return Files.objects.filter(creator=creator, status=0)


class GetFilesTrashByUserView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        creator = self.kwargs['creator']
        creator = get_object_or_404(User, username=creator)
        return Files.objects.filter(creator=creator, status=2)


class CreateFilesView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFilesView(APIView):
    def patch(self, request, pk):
        try:
            file = Files.objects.get(pk=pk)
            serializer = FileSerializer(file, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Files.DoesNotExist:
            return JsonResponse({'error': 'File does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteFilesView(APIView):
    def delete(self, request, id):
        try:
            file = get_object_or_404(Files, id=id)
            file.delete()
            return JsonResponse({'message': 'Document deleted successfully'}, status=200)
        except Files.DoesNotExist:
            return JsonResponse({'error': 'Document does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GetDocumentView(generics.ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        fid = self.kwargs['fid']
        return Documents.objects.filter(fid=fid)


class UpdateDocumentView(generics.ListAPIView):
    def patch(self, request, fid):
        try:
            document = Documents.objects.get(fid=fid)
            name = request.data['name']
            content = request.data['content']
            document.name = name
            document.content = content
            document.save()
            return JsonResponse({'success': True}, status=200)
        except Documents.DoesNotExist:
            return JsonResponse({'error': 'Document does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status)


class DocumentTemplateViewSet(viewsets.ModelViewSet):
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerlizer

    def get_queryset(self):
        queryset = DocumentTemplate.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            try:
                user = User.objects.get(username=username)
                queryset = queryset.filter(username=user)
            except User.DoesNotExist:
                queryset = DocumentTemplate.objects.none()
        return queryset


from dialogue.signals import create_user_ai_model, delete_user_ai_model


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 可以在此添加额外的token信息
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user_id': self.user.id})  # 添加user_id到响应数据中
        create_user_ai_model(self.user)
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    def delete(self, request, user_id):
        # 删除用户模型和对话缓存
        delete_user_ai_model(user_id)
        return Response({'detail': 'Cache cleared'}, status=status.HTTP_204_NO_CONTENT)
