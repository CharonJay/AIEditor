from django.db import models

from user.models import CustomUser


# Create your models here.
class Helper(models.Model):
    hId = models.AutoField(primary_key=True, db_column='hId', verbose_name='AI对话流水号')
    uId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='uId', verbose_name='用户id')
    hQuestion = models.TextField(db_column='hQuestion', verbose_name='对话提问')
    hAnswer = models.TextField(db_column='hAnswer', verbose_name='对话回答')
    # dId = models.ForeignKey(Document, on_delete=models.CASCADE, db_column='dId',verbose_name='文档Id')
    IV = models.BinaryField(db_column='IV', verbose_name='初始向量')

    class Meta:
        db_table = 'Helper'
        verbose_name = 'AI编辑助手'
        verbose_name_plural = 'AI编辑助手'

    def __str__(self):
        return f"Helper {self.hId}"
