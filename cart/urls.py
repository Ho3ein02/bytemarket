from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('delete/', views.delete_item, name='delete_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
]
