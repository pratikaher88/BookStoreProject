from django.shortcuts import render

# Create your views here.
from dal import autocomplete
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from search.forms import SearchForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


class SearchListView(generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        book_name = self.request.GET.get('search')
        print(book_name)
        return Book.objects.filter(Q(book_name__icontains=book_name))


class SearchAutoComplete(FormView):
    template_name = 'list_entries.html'
    form_class = SearchForm
    success_url = reverse_lazy('coreapp:list_entries')


class ContentAutoComplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):

		qs = Book.objects.all()

		if self.q:
			qs = qs.filter(book_name__istartswith=self.q)
			return qs
