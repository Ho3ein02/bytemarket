from django.contrib import admin
from .models import *


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class CityInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'weight']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'first_name', 'last_name', 'postal_code', 'province', 'city', 'is_paid']
    list_editable = ['is_paid']
    inlines = [OrderItemInline]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [CityInline]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']