from django.contrib import admin
from .models import Book,Profile,Order,OrderItem
# Register your models here.

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
