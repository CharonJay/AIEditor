# Generated by Django 5.0.6 on 2024-07-10 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Helper",
            fields=[
                (
                    "hId",
                    models.AutoField(
                        db_column="hId",
                        primary_key=True,
                        serialize=False,
                        verbose_name="AI对话流水号",
                    ),
                ),
                (
                    "hQuestion",
                    models.TextField(db_column="hQuestion", verbose_name="对话提问"),
                ),
                ("hAnswer", models.TextField(db_column="hAnswer", verbose_name="对话回答")),
                ("IV", models.BinaryField(db_column="IV", verbose_name="初始向量")),
            ],
            options={
                "verbose_name": "AI编辑助手",
                "verbose_name_plural": "AI编辑助手",
                "db_table": "Helper",
            },
        ),
    ]
