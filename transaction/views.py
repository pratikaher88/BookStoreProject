from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from coreapp.models import Book, Requests, Transaction, UserCollection
from coreapp.models import Requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy, reverse
# Create your views here.

def make_transaction(request,offer_id, book_id):
    book = get_object_or_404(Book, id=book_id)
    print(offer_id)
    # old_request = get_object_or_404(Requests,offer_id)
    print(book)
    messages.success(request, ('Transaction successful'))
    return redirect('transaction:offers_view')

@login_required
def add_request(request,book_id):
    book = get_object_or_404(Book, id=book_id)
    new_request = Requests(requester=request.user, offerrer=book.user , requester_book=book)

    if (UserCollection.objects.get(owner=request.user.profile).get_collection_items()):
        if Requests.objects.filter(requester=request.user, offerrer=book.user, requester_book=book).exists():
            messages.info("Requests already made!")
        else:
            messages.info("New Request")
            # request.save()
    else:
        messages.info(request, ('You need to add items to your collection to make a request!'))

    return redirect('coreapp:list_entries')


class RequestListView(LoginRequiredMixin, generic.ListView):
    model = Requests
    template_name = 'transaction_request.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Requests.objects.filter(requester=self.request.user).order_by('timestamp')


class RequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Requests
    success_url = reverse_lazy('transaction:requests_view')
    template_name = 'transaction_request_confirm_delete.html'

    def test_func(self):
        request_object = self.get_object()
        if self.request.user == request_object.requester:
            return True
        return False

class OfferListView(LoginRequiredMixin, generic.ListView):
    model = Requests
    template_name = 'transaction_offer.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Requests.objects.filter(offerrer=self.request.user).order_by('timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['collection_all'] = UserCollection.objects.all()
        return context

        # user_profile = get_object_or_404(Profile, user__username=user)
        # collection_items = UserCollection.objects.get(
        #     owner=user_profile)


class OfferDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Requests
    success_url = reverse_lazy('transaction:offers_view')
    template_name = 'transaction_offer_confirm_delete.html'

    def test_func(self):
        offer = self.get_object()
        if self.request.user == offer.offerrer:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # self.object.delete()
        print(self.object)
        return redirect(self.get_success_url())

class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'transaction_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Transaction.objects.filter(offerrer=self.request.user).order_by('timestamp')


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction:orders_view')
    template_name = 'transaction_order_confirm_delete.html'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.requester or self.request.user == transaction.offerrer:
            return True
        return False    
