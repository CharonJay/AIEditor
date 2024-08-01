import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomUserSerializer, FileSerializer, DocumentTemplateSerlizer, DocumentSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, response
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Files, DocumentTemplate, Documents, CustomUser
from django.db.models import Q
from django.views import View
from django.core.files.storage import default_storage
import os
from backend.settings import MEDIA_URL, MEDIA_ROOT
from rest_framework.parsers import MultiPartParser, FormParser
import uuid

app_name = "user"
User = get_user_model()


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("此用户名已被占用。")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("此邮箱已被占用。")
        return value

    def validate_unique_username(self, username, user_id):
        # Check if username exists for users other than the current user
        if CustomUser.objects.exclude(id=user_id).filter(username=username).exists():
            raise serializers.ValidationError("此用户名已被占用。")

    def validate_unique_email(self, email, user_id):
        # Check if username exists for users other than the current user
        if CustomUser.objects.exclude(id=user_id).filter(email=email).exists():
            raise serializers.ValidationError("此邮箱已被占用。")

    def create(self, request, *args, **kwargs):
        self.validate_username(request.data["username"])
        self.validate_email(request.data["email"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        mutable_data = request.data.copy()

        instance.last_login = timezone.now()
        if 'username' in mutable_data:
            self.validate_unique_username(mutable_data["username"], instance.id)
        if 'email' in mutable_data:
            self.validate_unique_email(mutable_data["email"], instance.id)
        serializer = self.get_serializer(instance, data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


class GetFilesCreateByUserView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        creator = self.kwargs['creator']
        creator = get_object_or_404(User, username=creator)
        return Files.objects.filter(creator=creator, status__in=[0, 1])


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
        self.user.last_login = timezone.now()
        self.user.save(update_fields=['last_login'])
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

from rest_framework.decorators import api_view, permission_classes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    print(request.FILES)
    user = request.user
    avatar_file = request.FILES.get('file')

    if avatar_file:
        user.avatar = avatar_file
        user.save()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'No avatar file received'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_avatar(request):
    user = request.user
    avatar_url = user.avatar.url if user.avatar else None
    return Response({'avatar': avatar_url})
