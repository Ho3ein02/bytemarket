# Generated by Django 5.1.2 on 2024-12-10 19:35

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_product_created_alter_product_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
