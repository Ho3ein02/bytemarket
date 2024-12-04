from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'weight']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'first_name', 'last_name', 'postal_code', 'province', 'city', 'is_paid']
    inlines = [OrderItemInline]
