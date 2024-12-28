from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.verify_phone, name='verify_phone'),
    path('login/verify-code/', views.verify_code, name='verify_code'),
    path('login/resend-code/', views.resend_code, name='resend_code'),
    path('logout/', views.user_logout, name='logout'),
    path('my-account/', views.profile, name='profile'),
    path('user-info/edit/', views.user_info_edit, name='user_info_edit'),
]
