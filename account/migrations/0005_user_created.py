# Generated by Django 5.1.2 on 2024-11-27 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_user_address_remove_user_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
