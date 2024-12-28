from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products_list, name='products_list_all'),
    path('products/category/<category_slug>/', views.products_list, name='products_list'),
    path('product/<id>/<slug>/', views.product_detail, name='product_detail'),
    path('products/search', views.product_search, name='product_search'),
    path('product/add/comment/<product_id>', views.add_comment, name='add_comment'),
    path('products/<portion>/', views.products_portion, name='products_portion'),
]
