from django.contrib import admin
from coreapp.models import Book,Profile
from wishlist.models import Order,OrderItem
# Register your models here.

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
