from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def requestsview(request):

    return render(request,'transaction_request.html')

# class RequestListView(ListView):
# class OfferListView(ListView):
# class OrderListView(ListView):
