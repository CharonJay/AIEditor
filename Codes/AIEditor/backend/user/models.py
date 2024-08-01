from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    # 在这里定义你的自定义字段，例如：
    information = models.TextField(default="这个人什么也没有留下~")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_member = models.BooleanField(default=False)
    membership_expiration = models.DateTimeField(blank=True, null=True)

    def is_membership_active(self):
        if self.is_member and self.membership_expiration:
            return self.membership_expiration > timezone.now()
        return False

    def __str__(self):
        return self.username


class Files(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(CustomUser, to_field='username', related_name='files', on_delete=models.CASCADE)
    status = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Documents(models.Model):
    name = models.CharField(max_length=255, default='Untitled')
    content = models.TextField(default='Hello World', blank=False, null=False)
    fid = models.IntegerField(default=0)

    def __str__(self):
        return f'Content for {self.name}'


class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255, default='Untitled')
    content = models.TextField()
    image_path = models.CharField(max_length=255, default='/')
    username = models.CharField(max_length=255)

    def __str__(self):
        return f'Content for {self.name}'
