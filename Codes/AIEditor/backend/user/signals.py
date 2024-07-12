from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Files, Documents

User = get_user_model()


@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        if request:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])


@receiver(post_save, sender=Files)
def create_documents(sender, instance, created, **kwargs):
    if created:
        Documents.objects.create(name=f"{instance.name}",
                                 content=f'<h1>Hi for {instance.name}</h1>',
                                 fid=instance.id)


@receiver(post_delete, sender=Files)
def delete_documents(sender, instance, **kwargs):
    try:
        document = Documents.objects.get(fid=instance.id)
        document.delete()
    except Documents.DoesNotExist:
        pass


# @receiver(post_save, sender=Documents)
# def update_files_updated_at(sender, instance, created, **kwargs):
#     # 更新关联的 Files 数据的 updated_at 字段
#     try:
#         instance.file.updated_at = timezone.now()
#         instance.file.save()
#     except Files.DoesNotExist:
#         pass
