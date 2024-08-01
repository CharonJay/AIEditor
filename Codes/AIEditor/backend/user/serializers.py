from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Files, DocumentTemplate, Documents

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Remove password field from validated_data if present
        if 'password' in validated_data:
            del validated_data['password']

        return super().update(instance, validated_data)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

    def create(self, validated_data):
        file = Files.objects.create(
            name=validated_data['name'],
            creator=validated_data['creator'],
            status=validated_data['status']
        )
        return file


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'

    def create(self, validated_data):
        document = Documents.objects.create(
            name=validated_data['name'],
            content=validated_data['content'],
            fid=validated_data['fid']
        )
        return document


class DocumentTemplateSerlizer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplate
        fields = '__all__'

    def create(self, validated_data):
        docTemplate = DocumentTemplate.objects.create(
            name=validated_data['name'],
            content=validated_data['content'],
            image_path=validated_data['image_path'],
            username=validated_data['username']
        )
        return docTemplate

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.img_path = validated_data['img_path']
        instance.username = validated_data['username']
        instance.save()
        return instance

    def delete(self, instance, validated_data):
        instance.delete()
        return instance
