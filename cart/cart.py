from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart and self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def delete(self, product_id):
        del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def count_item(self):
        return sum([item['quantity'] for item in self.cart.values()])

    def total_price(self):
        return sum([item['price'] * item['quantity'] for item in self.cart.values()])

    def post_price(self):
        return 50000

    def final_total_price(self):
        return self.total_price() + self.post_price()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            item['total_price'] = item['quantity'] * item['price']
            item['product'] = product
            yield item

