from django.db import models
from coreapp.models import Book,Profile

# Create your models here.


class OrderItem(models.Model):
    book = models.OneToOneField(
        Book, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.book_name


class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def __str__(self):
        return self.owner.user.username
