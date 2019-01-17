from coreapp.models import Transaction, ShippingAddress ,Requests ,Profile , Order
from django.shortcuts import get_object_or_404
from coreapp.forms import ShippingAddressForm

def add_variable_to_context(request):
    if request.user.id:
        return {
            'requestscount': Requests.objects.filter(requester=request.user).count(),
            'offercount' : Requests.objects.filter(offerrer=request.user).count(),
            'orderscount': Transaction.objects.filter(offerrer=request.user).count(),
            # 'cartitemscount': Order.objects.filter(owner=request.user.profile).items.count(),
            'addresscheck': get_object_or_404(ShippingAddress, profile=get_object_or_404(Profile, user=request.user)).address1
            # 'addressformal': get_object_or_404(ShippingAddress, profile=get_object_or_404(Profile, user=request.user))
            
            }
    else:
        return {}
