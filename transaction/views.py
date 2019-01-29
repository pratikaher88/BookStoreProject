from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from coreapp.models import Book, Requests, Transaction, UserCollection, FinalBuyOrder, OldRequests, Profile, ShippingAddress, CompletedTransaction, CompletedBuyOrder
from coreapp.models import Requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from coreapp.forms import ShippingAddressForm
from django.db.models import Q
from django.utils import timezone
import datetime

ordered_books = FinalBuyOrder.objects.values_list('book')
requester_books = Transaction.objects.values_list('requester_book')
offerrer_books = Transaction.objects.values_list('offerrer_book')

@login_required
def final_transaction(request, offer_id, book_id):
    offerrer_book = get_object_or_404(Book, id=book_id)
    new_request = get_object_or_404(Requests,id=offer_id)
    address_form = ShippingAddressForm(
        request.POST, instance=request.user.profile.address)

    if request.method == "POST" and 'Yes' in request.POST:
        offerrer_address = get_object_or_404(ShippingAddress, profile=request.user.profile)

        # requester_profile = get_object_or_404(
        #     Profile, user=new_request.requester)
        requester_address = get_object_or_404(
            ShippingAddress, profile=new_request.requester.profile)

        new_order = Transaction(requester=new_request.requester, offerrer=new_request.offerrer,
                                requester_book=new_request.requester_book, offerrer_book=offerrer_book, requester_address=requester_address, offerrer_address=offerrer_address)
        old_request = OldRequests(requester=new_request.requester, offerrer=new_request.offerrer,
                                  requester_book=new_request.requester_book)



        # print(collection_items.exclude(books__id__in=ordered_books).exclude(books__id__in=requester_books).exclude(books__id__in=offerrer_books))

        # delete entry from requests
        new_request.delete()
        
        # save old request
        # save new order
        new_order.save()
        old_request.save()

        if not UserCollection.objects.get(
                owner=new_request.requester.profile).books.filter(
                sell_or_exchange='Exchange').exclude(id__in=offerrer_books).exclude(id__in=requester_books):
                Requests.objects.filter(requester=new_request.requester).delete()

        return redirect('transaction:orders_view')

    if request.method == 'POST' and 'updateadd' in request.POST:
        if address_form.is_valid():
            address_form.save()
            messages.success(request, ('Address successfully updated!'))

    offer = get_object_or_404(Requests,id=offer_id)
    address = get_object_or_404(ShippingAddress, profile=request.user.profile)
    context = {'offer': offer, 'book': offerrer_book,
               'address': address, 'address_form': address_form}
    return render(request,'transaction_final.html',context)

@login_required
def add_request(request,book_id):
    book = get_object_or_404(Book, id=book_id)
    new_request = Requests(requester=request.user, offerrer=book.user , requester_book=book)

    address = ShippingAddress.objects.get(profile=request.user.profile)
    if address.status():
        messages.info(request, "You need to add  address in profile to make request !")
    else:
        if (UserCollection.objects.get(
            owner=request.user.profile).books.exclude(
                id__in=requester_books).exclude(id__in=offerrer_books).filter(sell_or_exchange="Exchange").exists()):
            if Requests.objects.filter(requester=request.user, offerrer=book.user, requester_book=book).exists():
                messages.info(request,"Request for this book already made!")
            else:
                date_from = datetime.datetime.now(
                    tz=timezone.utc) - datetime.timedelta(days=1)

                no_of_requests_made_in_one_day = Requests.objects.filter(requester=request.user, timestamp__gte=date_from).count()

                if no_of_requests_made_in_one_day>6:
                    messages.warning(request,"Maximum requests exceeded for one day : you can make maximum of 7 requests")
                else:
                    messages.info(
                        request, "New Request made!")

                    new_request.save()
                    return redirect('transaction:requests_view')
        else:
            messages.info(request, ('You need to add "Exchange" items to your collection to make a request!'))

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
        self.object.delete()
        return redirect(self.get_success_url())

class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'transaction_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Transaction.objects.filter(Q(offerrer=self.request.user) | Q(requester=self.request.user)).order_by('timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buy_order'] = FinalBuyOrder.objects.filter(
            user=self.request.user).order_by('-date_ordered')
        return context


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction:orders_view')
    template_name = 'transaction_order_confirm_delete.html'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.requester or self.request.user == transaction.offerrer:
            return True
        return False    


class TransactionCompletedExchangeOrder(LoginRequiredMixin, generic.ListView):
    model = CompletedTransaction
    template_name = 'transaction_completed_exchange_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return CompletedTransaction.objects.filter(Q(offerrer=self.request.user) | Q(requester=self.request.user)).order_by('timestamp')


class TransactionCompletedBuyOrder(LoginRequiredMixin, generic.ListView):
    model = CompletedBuyOrder
    template_name = 'transaction_completed_buy_order.html'
    context_object_name = 'buy_order'

    def get_queryset(self):
        return CompletedBuyOrder.objects.filter(user=self.request.user).order_by('date_ordered')
