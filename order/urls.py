from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('order-create/', views.order_create, name='order_create'),
    path('confirm-order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('order-edit/<int:order_id>/', views.order_edit, name='order_edit')
]
