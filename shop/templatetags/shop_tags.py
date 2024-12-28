from django import template
from shop.models import Product
from order.models import OrderItem
from django.db.models import Sum
from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag('partials/latest_products.html')
def latest_products(count=10):
    products = Product.objects.filter(inventory__gt=0).order_by('-created')[:count]
    context = {
        'products': products,
    }
    return context


@register.inclusion_tag('partials/suggestion_products.html')
def suggestion_products(count=10):
    products = Product.objects.filter(off_percent__gt=0, inventory__gt=0).order_by('-off_percent')[:count]
    context = {
        'products': products,
    }
    return context


@register.inclusion_tag('partials/best_seller.html')
def best_seller_products(count=10):
    # Get the products that have been bought and the is_paid field of their order is equal True
    order_items = OrderItem.objects.filter(order__is_paid=True)
    # Filter the products that have been bought and count the number of them
    products = Product.objects.filter(order_items__in=order_items, inventory__gt=0).annotate(sell_count=Sum('order_items__quantity')).order_by('-sell_count')[:count]
    context = {
        'products': products,
    }
    return context


@register.simple_tag
def custom_get_elided_page_range(p, number, on_each_side=1, on_ends=1):
    return Paginator.get_elided_page_range(p, number, on_each_side=on_each_side, on_ends=on_ends)

