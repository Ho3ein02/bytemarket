from .cart import Cart


def cart_items_count(request):
    cart = Cart(request)
    return {'cart_count': cart.count_item(), 'cart_total_price': cart.total_price()}
