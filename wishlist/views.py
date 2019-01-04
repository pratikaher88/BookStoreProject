from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile
from wishlist.models import OrderItem, Order
from django.db.models import Q


# Create your views here.


def add_to_list(request, item_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    book = Book.objects.filter(id=item_id).first()
    order_item, status = OrderItem.objects.get_or_create(book=book)
    print(order_item)
    # create order associated with the user
    user_order = Order.objects.get_or_create(
        owner=user_profile)
    if order_item in user_order[0].items.all():
        messages.warning(request, 'Item Already in Wishlist!')
        return redirect(reverse('coreapp:list_entries'))
    # create orderItem of the selected product
    user_order[0].items.add(order_item)
    user_order[0].save()

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
    model = OrderItem
    template_name = 'wish_list_entries.html'
    context_object_name = 'orders'
    ordering = ['-date_added']
