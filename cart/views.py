from django.shortcuts import render
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
def update_cart(request):
    """
    This view is for managing the quantity of products in the card.
    
    Add a product to the cart if it does not exist in the cart 
    or increase the quantity of the product if the product already exist in the cart.
    
    Decrease the quantity of the product  in the cart.
    """
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
        'item_total_price': intcomma(cart.cart.get(product_id)["quantity"] * cart.cart.get(product_id)["price"]),
        'post_price': intcomma(cart.post_price()),
        'final_price': intcomma(cart.final_total_price()),
    }
    return JsonResponse(data)


@require_POST
def delete_item(request):
    """ Delete the product from the cart."""
    product_id = request.POST.get('product_id')
    cart = Cart(request)
    cart.delete(product_id)
    data = {
        'cart_count': cart.count_item(),
        'cart_total_price': intcomma(cart.total_price()),
        'post_price': intcomma(cart.post_price()),
        'final_price': intcomma(cart.final_total_price()),
    }
    return JsonResponse(data)


@require_POST
def clear_cart(request):
    """ Delete all products from the cart."""
    cart = Cart(request)
    cart.clear()
    data = {
        'success': True,
    }
    return JsonResponse(data)

