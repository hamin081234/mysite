# Generated by Django 4.0.3 on 2023-02-07 00:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0003_answer_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 7, 0, 24, 29, 852370, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
