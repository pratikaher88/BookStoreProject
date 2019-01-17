from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, Order, ShippingAddress
from coreapp.forms import ShippingAddressForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum


@login_required
def add_to_list(request, item_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    book = get_object_or_404(Book,id=item_id)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(
        owner=user_profile)
    if book in user_order.get_cart_items():
        messages.warning(request, 'Item Already in Wishlist!')
        return redirect(reverse('coreapp:list_entries'))
    # # create orderItem of the selected product
    user_order.items.add(book)
    user_order.save()
    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('coreapp:list_entries'))

@login_required
def delete_from_list(request, item_id):
    book = get_object_or_404(Book,id=item_id)
    orders = Order.objects.get(owner=request.user.profile, items=book)
    item_to_delete = Order.objects.get(items=book)
    
    print("Book",book)
    print("Delete a item", item_to_delete.items)
    print("Filtered item", item_to_delete)
    # item_to_delete.delete()
    messages.info(request, "Item has been deleted")
    return redirect(reverse('wishlist:wish_list'))



# class WishListView(LoginRequiredMixin,generic.ListView):
#     model = Order
#     template_name = 'wish_list_entries.html'
#     context_object_name = 'orders'
#     ordering = ['-date_ordered']

#     # def get_context_data(self, **kwargs):
#     #     context = super(WishListView, self).get_context_data(**kwargs)
#     #     context['total_price'] = Order.objects.aggregate(Sum('items__price'))


#     def get_queryset(self):
#         orders=Order.objects.get(owner=self.request.user.profile)
#         return orders.get_cart_items()


@login_required
def wish_list_entries_view(request):
    orders = Order.objects.get(owner=request.user.profile)

    address_form = ShippingAddressForm(
        request.POST, instance=request.user.profile.address)

    if request.method == "POST" and 'Yes' in request.POST:
        print("POST REQUEST")
        orderitems = Order.objects.get(owner=request.user.profile)
        orders = orderitems.get_cart_items()
        
        for order in orders:
            user_profile = get_object_or_404(Profile, user=request.user)
            user_address = get_object_or_404(
                ShippingAddress, profile=user_profile)
            seller_profile = get_object_or_404(Profile, user=order.user)
            seller_address = get_object_or_404(
                ShippingAddress, profile=seller_profile)
            print(user_address)
            print(seller_address)
            # FinalBuyOrder.create(user=request.user,book=order, seller=order.user ,useraddress=user_address,selleraddres=seller_address )
        # delete entry from requests
        # new_request.delete()
        # save old request
        # save new order
        # new_order.save()
        # old_request.save()
        # return redirect('transaction:orders_view')

    if request.method == 'POST' and 'updateadd' in request.POST:
        if address_form.is_valid():
            address_form.save()
            messages.success(request, ('Address successfully updated!'))

    user_profile = get_object_or_404(Profile, user=request.user)
    address = get_object_or_404(ShippingAddress, profile=user_profile)
    orderitems = Order.objects.get(owner=request.user.profile)
    orders = orderitems.get_cart_items()
    total_price = Order.objects.filter(
        owner=request.user.profile).aggregate(Sum('items__price'))
    # total_price = 0
    # for item in orders:
    #     total_price+=item.price

    total_price=(list(total_price.values())[0])

    context = {'orders': orders, 'address': address, 'address_form': address_form,'total_price':total_price }
    return render(request, 'wish_list_entries.html', context)
