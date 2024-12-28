from django.db import models
from shop.models import Product
from account.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    phone = models.CharField(max_length=11)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    address = models.TextField()
    province = models.ForeignKey("Province", on_delete=models.CASCADE, related_name='province_orders', null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.CASCADE, related_name='city_orders', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    
    def final_price(self):
        return sum([item.price * item.quantity for item in self.items.all()])

    def __str__(self):
        return f"order{self.id}: {self.phone}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    def __str__(self):
        return f"order_item: {self.product.name}"


class Province(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    
    def __str__(self):
        return self.name
