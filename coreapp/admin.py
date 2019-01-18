from django.contrib import admin
from coreapp.models import Book, Profile, UserCollection, Order, Requests, Transaction, ShippingAddress, FinalBuyOrder, OldRequests
# Register your models here.

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OldRequests)
admin.site.register(UserCollection)
admin.site.register(Requests)
admin.site.register(Transaction)
admin.site.register(ShippingAddress)
admin.site.register(FinalBuyOrder)


class SystemAdmin(admin.ModelAdmin):
    form = Order
    filter_horizontal = ('items',)
