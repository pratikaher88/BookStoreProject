from django.contrib import admin
from coreapp.models import Book,Profile , UserCollection, Order,Requests,Transaction
# Register your models here.

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(UserCollection)
admin.site.register(Requests)
admin.site.register(Transaction)


class SystemAdmin(admin.ModelAdmin):
    form = Order
    filter_horizontal = ('items',)
