# Generated by Django 5.1.2 on 2024-12-10 19:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 10, 19, 35, 37, 526375, tzinfo=datetime.timezone.utc)),
        ),
    ]