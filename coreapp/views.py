from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from .forms import UserCreationForm, NewEntryForm, UserForm, ProfileForm, ShippingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, UserCollection, ShippingAddress, FinalBuyOrder, Transaction, CompletedBuyOrder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from nofapapp.settings import GOOGLE_BOOKS_URL

ordered_books = FinalBuyOrder.objects.values_list('book')
requester_books = Transaction.objects.values_list('requester_book')
offerrer_books = Transaction.objects.values_list('offerrer_book')


@login_required
def profile(request):
    address = ShippingAddress.objects.get(profile=request.user.profile)
    return render(request, 'profile.html', {'profile': request.user.profile, 'address': address})


class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_message = 'Account Created! You can now Login!'


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    paginate_by = 15

    def get_queryset(self):
        # ordered_books = FinalBuyOrder.objects.values_list('book')
        # requester_books = Transaction.objects.values_list('requester_book')
        # offerrer_books = Transaction.objects.values_list('offerrer_book')
        return Book.objects.exclude(user=self.request.user).exclude(id__in=ordered_books).exclude(id__in=requester_books).exclude(id__in=offerrer_books).order_by('-created_at')
        # if self.request.user.is_authenticated:
        #     return Book.objects.exclude(user=self.request.user).order_by('?')
        # else:
        #     return Book.objects.all().order_by('?')


class BuyListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    paginate_by = 15

    def get_queryset(self):
        # ordered_books = FinalBuyOrder.objects.values_list('book')
        return Book.objects.exclude(user=self.request.user).exclude(id__in=ordered_books).filter(sell_or_exchange='Sell').order_by('-created_at')


class ExchangeListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    paginate_by = 15

    def get_queryset(self):
        # requester_books = Transaction.objects.values_list('requester_book')
        # offerrer_books = Transaction.objects.values_list('offerrer_book')
        return Book.objects.exclude(user=self.request.user).exclude(id__in=requester_books).exclude(id__in=offerrer_books).filter(sell_or_exchange='Exchange').order_by('-created_at')


class UserBookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'user_books_list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        # ordered_books = FinalBuyOrder.objects.values_list('book')
        # requester_books = Transaction.objects.values_list('requester_book')
        # offerrer_books = Transaction.objects.values_list('offerrer_book')
        collection_items = UserCollection.objects.get(
            owner=self.request.user.profile)

        return collection_items.books.exclude(id__in=ordered_books).exclude(
            id__in=requester_books).exclude(id__in=offerrer_books)


class UserBookSoldItemsView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'user_books_sold_list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        # ordered_books = FinalBuyOrder.objects.values_list('book')
        # requester_books = Transaction.objects.values_list('requester_book')
        # offerrer_books = Transaction.objects.values_list('offerrer_book')
        # collection_items = UserCollection.objects.get(
        #     owner=self.request.user.profile)

        # return collection_items.books.filter(id__in=ordered_books).exclude(
        #     id__in=requester_books).exclude(id__in=offerrer_books)
        return CompletedBuyOrder.objects.filter(seller=self.request.user).order_by('date_ordered')


class UserBookListViewForUser(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'collection_user_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.kwargs['username']

        user_profile = get_object_or_404(Profile, user__username=user)
        collection_items = UserCollection.objects.get(
            owner=user_profile)

        # ordered_books = FinalBuyOrder.objects.values_list('book')
        # requester_books = Transaction.objects.values_list('requester_book')
        # offerrer_books = Transaction.objects.values_list('offerrer_book')
        return collection_items.books.exclude(id__in=ordered_books).exclude(
            id__in=requester_books).exclude(id__in=offerrer_books)


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail_view.html'


class NewEntry(LoginRequiredMixin, generic.CreateView):
    form_class = NewEntryForm
    success_url = reverse_lazy('coreapp:userbooks')
    template_name = 'new_entry.html'

    def form_valid(self, form):

        # if self.request.method == 'POST' and 'check' in self.request.POST:
        #     print("POST request")
        #     return red

        address = get_object_or_404(
            ShippingAddress, profile=self.request.user.profile)

        if address.address1 == '':
            messages.info(
                self.request, 'You need to update address in profile to make a Sell request!')
            return redirect('coreapp:new_entry')

        book = form.save(commit=False)
        book.user = self.request.user
        book.save()

        collection, status = UserCollection.objects.get_or_create(
            owner=self.request.user.profile)

        collection.books.add(book)
        collection.save()

        return super(NewEntry, self).form_valid(form)


@login_required
def new_entry(request):
    if request.method == 'POST' and 'check' in request.POST:
        new_entry_form = NewEntryForm(request.POST, instance=request.user)
        book_name = new_entry_form.data['book_name']
        if book_name:
            parms = {"q": book_name, "printType": "books", "projection": "lite"}
            r = requests.get(
                url=GOOGLE_BOOKS_URL, params=parms)
            items = json.loads(r.text)
            return render(request, 'new_entry.html', {'form': new_entry_form, 'items': items['items']})
        else:
           return render(request, 'new_entry.html', {'form': new_entry_form})

    if request.method == 'POST' and 'submitentry' in request.POST:
        new_entry_form = NewEntryForm(request.POST, instance=request.user)
        if new_entry_form.is_valid():

            address = get_object_or_404(
                ShippingAddress, profile=request.user.profile)
            if address.address1 == '':
                messages.info(
                    request, 'You need to update address in profile to make a Sell request!')
                return redirect('coreapp:new_entry')
            
            book = Book()
            book.user = request.user
            book.book_name = new_entry_form.cleaned_data['book_name']
            book.author_name = new_entry_form.cleaned_data['author_name']
            book.price = new_entry_form.cleaned_data['price']
            book.description = new_entry_form.cleaned_data['description']
            book.sell_or_exchange = new_entry_form.cleaned_data['description']
            book.image_url = new_entry_form.cleaned_data['image_url']
            book.save()
            collection, status = UserCollection.objects.get_or_create(
                owner=request.user.profile)
            collection.books.add(book)
            collection.save()
            return redirect('coreapp:userbooks')
        else:
           return render(request, 'new_entry.html', {'form': new_entry_form})

    new_entry_form = NewEntryForm(instance=request.user)

    return render(request, 'new_entry.html', {
        'form': new_entry_form,
    })


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    form_class = NewEntryForm
    template_name = 'new_entry_update.html'
    success_url = reverse_lazy('coreapp:userbooks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):

        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('coreapp:userbooks')
    template_name = 'book_confirm_delete.html'

    def test_func(self):

        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
            return redirect('coreapp:profile')
    else:
        user_form = UserForm(instance=request.user)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,

    })


@login_required
def update_address(request):
    if request.method == 'POST':
        address_form = ShippingAddressForm(
            request.POST, instance=request.user.profile.address)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, ('Address successfully updated!'))
            return redirect('coreapp:profile')

    else:
        address_form = ShippingAddressForm(
            instance=request.user.profile.address)
    return render(request, 'address_edit.html', {
        'address_form': address_form
    })


@login_required
def aboutus(request):
    return render(request, 'aboutus.html')
