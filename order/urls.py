from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('order-create/', views.order_create, name='order_create'),
    path('confirm-order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('order-edit/<int:order_id>/', views.order_edit, name='order_edit'),
    path('order/detail/<order_id>/', views.order_detail, name='order_detail'),
    path('get/cities/', views.get_cities, name='get_cities'),
]
