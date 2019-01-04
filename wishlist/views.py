from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile
from wishlist.models import OrderItem, Order
from django.db.models import Q

def add_to_list(request, item_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    book = Book.objects.get(id=item_id)
    order_item, status = OrderItem.objects.get_or_create(book=book)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(
        owner=user_profile)
    # print(user_order.items.all())
    if order_item in user_order.items.all():
        messages.warning(request, 'Item Already in Wishlist!')
        return redirect(reverse('coreapp:list_entries'))
    # create orderItem of the selected product
    user_order.items.add(order_item)
    user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('coreapp:list_entries'))


def delete_from_list(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    print(item_to_delete)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('wishlist:wish_list'))


class WishListView(generic.ListView):
    model = Order
    template_name = 'wish_list_entries.html'
    context_object_name = 'orders'
    ordering = ['-date_ordered']

    def get_queryset(self):
        orders=Order.objects.get(owner=self.request.user.profile)
        print(orders)
        print(orders.get_cart_items())
        return orders.get_cart_items()
