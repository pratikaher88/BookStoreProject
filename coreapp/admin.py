from django.contrib.admin import actions
from django.contrib import admin
from coreapp.models import Book, Profile, UserCollection, Order, Requests, Transaction, ShippingAddress, FinalBuyOrder, OldRequests, CompletedBuyOrder, CompletedTransaction
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
# Register your models here.

admin.site.register(CompletedBuyOrder)
admin.site.register(CompletedTransaction)

# class TransactionAdmin(ImportExportModelAdmin):
#     pass

def delete_selected_exchange_order(modeladmin, request, queryset):
    for obj in queryset:
        CompletedTransaction.objects.create(requester=obj.requester, offerrer=obj.offerrer, requester_book_name=obj.requester_book.book_name, offerrer_book_name=obj.offerrer_book.book_name, requester_author_name=obj.requester_book.author_name, offerrer_author_name=obj.offerrer_book.author_name, requester_address=obj.requester_address, offerrer_address=obj.offerrer_address)
        obj.requester_book.delete()
        obj.offerrer_book.delete()
        obj.delete()
delete_selected_exchange_order.short_description = "Delete Exchange Order(Select This)"


class TransactionAdmin(admin.ModelAdmin):
    actions = [delete_selected_exchange_order]


admin.site.register(Transaction, TransactionAdmin)


def delete_selected_buy_order(modeladmin, request, queryset):
    for obj in queryset:
        CompletedBuyOrder.objects.create(user=obj.user,book_name=obj.book.book_name, author_name=obj.book.author_name, seller=obj.seller,
                                         useraddress=obj.useraddress, selleraddress=obj.selleraddress, total_price=obj.total_price)
        obj.book.delete()
        obj.delete()
delete_selected_buy_order.short_description = "Delete Selected Buy Order(Select This)"


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

