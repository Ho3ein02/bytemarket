# Generated by Django 5.1.2 on 2024-11-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
