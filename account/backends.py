from django.contrib.auth.backends import BaseBackend
from .models import User


# Custom authentication backend
class CustomBackend(BaseBackend):
    # Method to authenticate a user based on phone number
    def authenticate(self, request, phone=None, **kwargs):
        try:
            # Try to get the user with the given phone number
            user = User.objects.get(phone=phone)
            return user
        except User.DoesNotExist:
            # Return None if the user does not exist
            return None
        
    # Method to get user by their user id
    def get_user(self, user_id):
        try:
            # Try to get the user with the given user id
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Return None if the user does not exist
            return None
