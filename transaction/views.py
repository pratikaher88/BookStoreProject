from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.


def requestsview(request):

    return render(request,'transaction_request.html')

# class RequestListView(ListView):
# class OfferListView(ListView):
# class OrderListView(ListView):
