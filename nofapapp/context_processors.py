from coreapp.models import Transaction, ShippingAddress, Requests, Profile, Order, FinalBuyOrder, UserCollection
from django.shortcuts import get_object_or_404
from coreapp.forms import ShippingAddressForm
from django.db.models import Q


def add_variable_to_context(request):
    if request.user.id:

        requester_books = Transaction.objects.values_list('requester_book')
        offerrer_books = Transaction.objects.values_list('offerrer_book')

        # addressformcontext=ShippingAddressForm(
        #     request.POST, instance=request.user.profile.address)
        orderitems = Order.objects.get(owner=request.user.profile)
        return {
            'requestscount': Requests.objects.filter(requester=request.user).count(),
            'offercount' : Requests.objects.filter(offerrer=request.user).count(),
            'orderscount': Transaction.objects.filter(Q(offerrer=request.user) | Q(requester=request.user)).count()+FinalBuyOrder.objects.filter(user=request.user).count(),
            'cartitemscount': orderitems.items.count(),
            'addresscheck': get_object_or_404(ShippingAddress, profile=get_object_or_404(Profile, user=request.user)).address1,
            # 'addressformcontext':  addressformcontext
            'exchangeitemexists': UserCollection.objects.get(
                owner=request.user.profile).books.exclude(
                id__in=requester_books).exclude(id__in=offerrer_books).filter(sell_or_exchange="Exchange").exists(),
            }
    else:
        return {}
