# Generated by Django 5.1.2 on 2024-12-23 23:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_city_remove_order_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_orders', to='order.city'),
        ),
        migrations.AddField(
            model_name='order',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='province_orders', to='order.province'),
        ),
    ]
