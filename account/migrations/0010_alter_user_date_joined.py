# Generated by Django 5.1.2 on 2024-12-09 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 9, 20, 21, 22, 366223, tzinfo=datetime.timezone.utc)),
        ),
    ]
