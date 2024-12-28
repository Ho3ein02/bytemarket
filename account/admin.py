from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm
from .models import User


# Register the User model
@admin.register(User)
class ShopUserAdmin(UserAdmin):
    # Order the users by their phone number
    ordering = ['phone']
    # Specify the model to be used
    model = User
    # Form to be used for changing an existing user
    form = ShopUserChangeForm
    # Form to be used for adding a new user
    add_form = ShopUserCreationForm
    # Fields to be displayed
    list_display = ['phone', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
    
    # Define the fieldsets for the change user form
    fieldsets = [
        (None, {'fields': ['phone', 'password']}),
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email']}),
        ('Permissions', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']})
    ]
    
    # Define the fieldsets for the add user form
    add_fieldsets = [
        (None, {'fields': ['phone', 'password1', 'password2']}),
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email']}),
        ('Permissions', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']})
    ]
