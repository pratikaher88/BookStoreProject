from coreapp.models import Transaction, ShippingAddress, Requests, Profile, Order, FinalBuyOrder
from django.shortcuts import get_object_or_404
from coreapp.forms import ShippingAddressForm



def add_variable_to_context(request):
    if request.user.id:
        # addressformcontext=ShippingAddressForm(
        #     request.POST, instance=request.user.profile.address)
        orderitems = Order.objects.get(owner=request.user.profile)
        return {
            'requestscount': Requests.objects.filter(requester=request.user).count(),
            'offercount' : Requests.objects.filter(offerrer=request.user).count(),
            'orderscount': Transaction.objects.filter(offerrer=request.user).count()+FinalBuyOrder.objects.filter(user=request.user).count(),
            'cartitemscount': orderitems.items.count(),
            'addresscheck': get_object_or_404(ShippingAddress, profile=get_object_or_404(Profile, user=request.user)).address1,
            # 'addressformcontext':  addressformcontext
            
            }
    else:
        return {}
