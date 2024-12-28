from .cart import Cart


def cart_items_count(request):
    """
    Returns the count of the quantity and the total price of all products in the cart.
    """
    cart = Cart(request)
    return {'cart_count': cart.count_item(), 'cart_total_price': cart.total_price()}
