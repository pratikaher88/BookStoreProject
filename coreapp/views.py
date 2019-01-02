from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import UserCreationForm, NewEntryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

# @login_required
# def logoutpage(request):
#     return render(request,'registration/logout.html')


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

# def addforexchange(request):

class SearchListView(generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        book_name = self.request.GET.get('search')
        print(book_name)
        return Book.objects.filter(Q(book_name__icontains=book_name))


def add_to_list(request, item_id):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    book = Book.objects.filter(id=item_id).first()
    # check if the user already owns this product
    # if product in request.user.profile.ebooks.all():
    #     messages.info(request, 'You already own this ebook')
    #     return redirect(reverse('products:product-list'))
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(book=book)
    print(order_item)
    # create order associated with the user
    user_order = Order.objects.get_or_create(
        owner=user_profile)
    if order_item in user_order[0].items.all():
        messages.warning(request, 'Item Already in Wishlist!')
        return redirect(reverse('listentries'))
    # create orderItem of the selected product
    user_order[0].items.add(order_item)
    user_order[0].save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('listentries'))


def delete_from_list(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    print(item_to_delete)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('wish_list'))


def transaction(request):
    return render(request, 'transaction.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class BookListView(generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        return Book.objects.exclude(user=self.request.user)


class WishListView(generic.ListView):
    model = OrderItem
    template_name = 'wish_list_entries.html'
    context_object_name = 'orders'
    ordering = ['-date_added']


class UserBookListView(generic.ListView):
    model = Book
    template_name = 'user_books_listentries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user).order_by('-created_at')


class UserBookListViewForUser(generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.kwargs['username']
        return Book.objects.filter(user__username=user).order_by('-created_at')


class NewEntry(generic.CreateView):
    form_class = NewEntryForm
    success_url = reverse_lazy('listentries')
    template_name = 'new_entry.html'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.user = self.request.user
        book.save()
        return super(NewEntry, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    template_name = 'new_entry.html'
    success_url = reverse_lazy('userbooks')
    fields = ['book_name', 'description', 'price', 'condition']

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
    success_url = reverse_lazy('userbooks')
    template_name = 'book_confirm_delete.html'

    def test_func(self):

        book = self.get_object()
        if self.request.user == book.user:
            return True
        return False
