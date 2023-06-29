from django.db import models
from shop.models import Product


class Order(models.Model):
    firstname = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=60)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname
    

    def get_total_cost(self):     # pour recuperer le cout total du panier
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    

    def get_cost(self):     # qui permet de recuperer le cout
        return self.price * self.quantity

