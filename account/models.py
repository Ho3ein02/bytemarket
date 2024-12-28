from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('phone must exist.')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Check that the is_staff equal True
        if not extra_fields.get('is_staff'):
            raise ValueError('is_staff must be True')
        # Check that the is_superuser equal True
        if not extra_fields.get('is_superuser'):
            raise ValueError('is_superuser must be True')

        user = self.create_user(phone, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=55, null=True, blank=True)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone' # Set phone as the unique identifier for authentication

    objects = UserManager()
    
    # Method to check if the user has both first and last names
    def has_full_name(self):
        if self.first_name and self.last_name:
            return True
        return False
    
    # Method to get the user's full name
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.phone

