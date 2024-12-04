from django import template
from shop.models import Product
from order.models import OrderItem, Order
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('partials/latest_products.html')
def latest_products(count=10):
    products = Product.objects.all().order_by('-created')[:count]
    context = {
        'products': products,
    }
    return context


@register.inclusion_tag('partials/suggestion_products.html')
def suggestion_products(count=10):
    products = Product.objects.filter(off_percent__gt=0).order_by('-off_percent')[:count]
    context = {
        'products': products,
    }
    return context


@register.inclusion_tag('partials/best_seller.html')
def best_seller_products(count=10):
    products = Product.objects.annotate(sell_count=Count('order_items')).filter(sell_count__gt=0).order_by('-sell_count')
    order_items = OrderItem.objects.filter(order__is_paid=True).annotate(sell_count=Count('product'))

