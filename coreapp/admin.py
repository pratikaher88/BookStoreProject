from django.contrib.admin import actions
from django.contrib import admin
from coreapp.models import Book, Profile, UserCollection, Order, Requests, Transaction, ShippingAddress, FinalBuyOrder, OldRequests, CompletedBuyOrder, CompletedTransaction
# Register your models here.

# class SystemAdmin(admin.ModelAdmin):
#     form = Order
#     filter_horizontal = ('items',)

# def delete_model(modeladmin, request, obj):
#         # do something with the user instance
#         print("Request", request)
#         obj.delete()


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        print("Request", obj)
        CompletedTransaction.objects.create(requester=obj.requester, offerrer=obj.offerrer, requester_book=obj.requester_book, offerrer_book=obj.offerrer_book, requester_address=obj.requester_address, offerrer_address=obj.offerrer_address)
        # obj.requester_book.delete()
        # obj.offerrer_book.delete()
        obj.delete()
delete_selected.short_description = "Delete Exchange Order"

class TransactionAdmin(admin.ModelAdmin):
    actions = [delete_selected]

admin.site.register(Transaction, TransactionAdmin)


def delete_selected_buy_order(modeladmin, request, queryset):
    for obj in queryset:
        print("Request", obj)
        CompletedBuyOrder.objects.create(user=obj.user, book=obj.book,
                                         seller=obj.seller, useraddress=obj.useraddress, selleraddress=obj.selleraddress, total_price=obj.total_price)
        # obj.requester_book.delete()
        # obj.offerrer_book.delete()
        obj.delete()
delete_selected_buy_order.short_description = "Delete Selected Buy Order"


class FinalBuyOrderAdmin(admin.ModelAdmin):
    actions = [delete_selected_buy_order]


admin.site.register(FinalBuyOrder, FinalBuyOrderAdmin)

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OldRequests)
admin.site.register(UserCollection)
admin.site.register(Requests)
# admin.site.register(Transaction)
admin.site.register(ShippingAddress)
# admin.site.register(FinalBuyOrder)
admin.site.register(CompletedBuyOrder)
admin.site.register(CompletedTransaction)
