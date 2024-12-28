from shop.models import Product


class Cart:
    """ 
    A class to manager cart in the session.

    In the session we create a variable called 'cart' that contains the products that the user has selected.
    
    The structure of the cart is dictionary. The keys of this dictionary are 
    products id and the values of them are also a dictionary that contains 
    the 'quantity', 'price', and 'weight' of each product.
    
    Example:
    cart = {
        '12': {'quantity': 5, 'price': 1200000, 'weight': 2},
        '3': {'quantity': 1, 'price': 500000, 'weight': 1.5},
        ...
    }
    """
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        
        # Check that the cart is exists in the session
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        """ Method to add product to the cart """
        product_id = str(product.id)
        
        # Check whether we should add the product to the card for the first time or increase its number
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            # Check that the product's inventory is available to increase the quantity
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()
        
    def decrease(self, product):
        """ Method to deacrese the qunatity of the product in the cart """
        product_id = str(product.id)
        
        # Check that the product exists in the cart and the quantity of the product is greater than 1
        if product_id in self.cart and self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()
        
    def delete(self, product_id):
        """ Method to delete the product from the cart """
        del self.cart[product_id]
        self.save()
        
    def clear(self):
        """ Method to delete all products in the cart """
        del self.session['cart']
        self.save()
    
    def count_item(self):
        """ Returns the total quantity of all products in cart """
        return sum([item['quantity'] for item in self.cart.values()])
    
    def total_price(self):
        """ Returns the total price of all products """
        return sum([item['price'] * item['quantity'] for item in self.cart.values()])
    
    def total_weight(self):
        """ Returns the total weight of all products """
        return sum([item['weight'] for item in self.cart.values()])
    
    def post_price(self):
        """ Returns the posting price based on the total weight """
        weight = self.total_weight()
        if weight == 0:
            return 0
        elif weight < 500:
            return 20000
        elif weight < 1200:
            return 35000
        elif weight < 2000:
            return 50000
        else:
            return 75000
        
    def final_total_price(self):
        """ Returns sum of posting price and the total price of all products """
        return self.total_price() + self.post_price()
    
    def save(self):
        """ Method that save the session """
        self.session.modified = True
    
    def __iter__(self):
        """ Method to add product object to the cart dictionary in the session """
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            item['total_price'] = item['quantity'] * item['price']
            item['product'] = product
            yield item

