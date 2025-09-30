from django.db import models

class Cart(models.Model):
    
    user_id = models.IntegerField(unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина для пользователя {self.user_id}"

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        self.items.all().delete()
        
class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = 'items')
    product_id = models.IntegerField()
    quantity = models.IntegerField(default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    product_name = models.CharField(max_length = 100, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Товар: {self.product_name}, Количество: {self.quantity}"
    
    @property
    def subtotal(self):
        """Подсумма для данного товара"""
        return self.price * self.quantity