from django.db import models
from oscar.core.loading import get_class, get_model
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()
Product = get_model('catalogue', 'Product')
Basket = get_model('basket', 'Basket')

class ProductPurchased(models.Model):
    owner = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    dateOfPurchase = models.DateTimeField(auto_now_add=True)
    basket = models.ForeignKey(Basket)
    validated = models.BooleanField(default=True) #TODO Only in demo phase

    def __str__(self):
        return self.name