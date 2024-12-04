from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm
from .models import User


@admin.register(User)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    model = User
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    list_display = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']

    fieldsets = [
        (None, {'fields': ['phone', 'password']}),
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email']}),
        ('Permissions', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']})
    ]

    add_fieldsets = [
        (None, {'fields': ['phone', 'password1', 'password2']}),
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email']}),
        ('Permissions', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']})
    ]
