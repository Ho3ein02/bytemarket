# Generated by Django 5.1.2 on 2024-12-06 19:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_user_created_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 6, 19, 33, 28, 348878, tzinfo=datetime.timezone.utc)),
        ),
    ]
