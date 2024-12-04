from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.humanize.templatetags.humanize import intcomma
from shop.models import Product
from .cart import Cart


def index(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def add_product(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product)
    data = {
        'cart_count': cart.count_item(),
        'cart_total_price': intcomma(cart.total_price()),
    }
    return JsonResponse(data)


@require_POST
def decrease_product(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.deacrese(product)
    data = {
        'cart_count': cart.count_item(),
        'cart_total_price': intcomma(cart.total_price()),
    }
    return JsonResponse(data)


@require_POST
def update_cart(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    if action == "add":
        cart.add(product)
    elif action == "decrease":
        cart.decrease(product)
    data = {
        'cart_count': cart.count_item(),
        'cart_total_price': intcomma(cart.total_price()),
        'product_quantity': cart.cart.get(product_id)["quantity"],
        'item_total_price': cart.cart.get(product_id)["quantity"] * cart.cart.get(product_id)["price"],
    }
    return JsonResponse(data)


@require_POST
def delete_item(request):
    product_id = request.POST.get('product_id')
    cart = Cart(request)
    cart.delete(product_id)
    data = {
        'cart_count': cart.count_item(),
        'cart_total_price': intcomma(cart.total_price()),
    }
    return JsonResponse(data)


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shop:index')

