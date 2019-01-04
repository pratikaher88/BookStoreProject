from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from .forms import UserCreationForm, NewEntryForm ,UserForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

class SignUp(SuccessMessageMixin,generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    success_message = 'Account Created! You can now Login!'

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        return Book.objects.exclude(user=self.request.user)

class UserBookListView(generic.ListView):
    model = Book
    template_name = 'user_books_list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user).order_by('-created_at')


class UserBookListViewForUser(generic.ListView):
    model = Book
    template_name = 'collection_user_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.kwargs['username']
        return Book.objects.filter(user__username=user).order_by('-created_at')


class NewEntry(generic.CreateView):
    form_class = NewEntryForm
    success_url = reverse_lazy('coreapp:list_entries')
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
            return redirect('coreapp:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
