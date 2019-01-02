from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from .forms import UserCreationForm, NewEntryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

class SearchListView(generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        book_name = self.request.GET.get('search')
        print(book_name)
        return Book.objects.filter(Q(book_name__icontains=book_name))

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
