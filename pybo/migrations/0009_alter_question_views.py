# Generated by Django 4.0.3 on 2023-02-09 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0008_question_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
