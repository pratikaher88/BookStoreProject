from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, Order, ShippingAddress, FinalBuyOrder
from coreapp.forms import ShippingAddressForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum


@login_required
def add_to_cart(request, item_id):
    book = get_object_or_404(Book,id=item_id)
    user_order, status = Order.objects.get_or_create(
        owner=request.user.profile)
    if book in user_order.get_cart_items():
        messages.warning(request, 'Item Already in Cart!')
        return redirect(reverse('coreapp:buy_entries'))
    user_order.items.add(book)
    user_order.save()
    messages.info(request, "Item added to cart!")
    return redirect(reverse('coreapp:buy_entries'))

@login_required
def delete_from_cart(request, item_id):
    book = get_object_or_404(Book,id=item_id)
    orders = Order.objects.get(owner=request.user.profile)
    orders.items.remove(book)

    messages.info(request, "Item has been deleted")
    return redirect(reverse('cart:cart_items'))

@login_required
def cart_list_entries_view(request):
    orders = Order.objects.get(owner=request.user.profile)

    address_form = ShippingAddressForm(
        request.POST, instance=request.user.profile.address)

    user_address = get_object_or_404(
        ShippingAddress, profile=request.user.profile)
    orderitems = Order.objects.get(owner=request.user.profile)
    orders = orderitems.get_cart_items()

    total_price = Order.objects.filter(
        owner=request.user.profile).aggregate(Sum('items__price'))

    total_price = (list(total_price.values())[0])

    if request.method == "POST" and 'Yes' in request.POST:

        for order in orders:

            seller_profile = get_object_or_404(Profile, user=order.user)
            seller_address = get_object_or_404(
                ShippingAddress, profile=seller_profile)

            FinalBuyOrder.objects.create(user=request.user, book=order, seller=order.user,
                                         useraddress=user_address, selleraddress=seller_address, total_price=total_price+20)
            orderitems.items.remove(order)

        messages.success(request, ('Item successfully Ordered!'))
        return redirect('transaction:orders_view')

    if request.method == 'POST' and 'updateadd' in request.POST:
        if address_form.is_valid():
            address_form.save()
            messages.success(request, ('Address successfully updated!'))
            return redirect('cart:cart_items')

    context = {'orders': orders, 'address': user_address,
               'address_form': address_form, 'total_price': total_price}
    return render(request, 'cart_list_entries.html', context)


class FinalBuyOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = FinalBuyOrder
    success_url = reverse_lazy('transaction:orders_view')
    template_name = 'final_order_confirm_delete.html'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False
