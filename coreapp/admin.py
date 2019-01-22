from django.contrib.admin.actions import delete_selected as django_delete_selected
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
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


# class TransactionAdmin(DjangoUserAdmin):
#     actions = ['delete_selected']

#     def delete_model(modeladmin, request, obj):
#         # do something with the user instance
#         print("Request",request)
#         obj.delete()

#     def delete_selected(modeladmin, request, queryset):
#         # do something with the users in the queryset

#         return django_delete_selected(modeladmin, request, queryset)
#     delete_selected.short_description = django_delete_selected.short_description


# admin.site.unregister(Transaction)
# admin.site.register(Transaction, TransactionAdmin)
