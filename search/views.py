from django.shortcuts import render
from dal import autocomplete
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from search.forms import SearchForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from coreapp.models import Book, Profile, Transaction, FinalBuyOrder
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q


class SearchListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'list_entries.html'
    context_object_name = 'books'
    ordering = ['-created_at']

    def get_queryset(self):
        book_name = self.request.GET.get('search')

        ordered_books = FinalBuyOrder.objects.values_list('book')
        requester_books = Transaction.objects.values_list('requester_book')
        offerrer_books = Transaction.objects.values_list('offerrer_book')

        print(self.request.user)

        print(Book.objects.exclude(user=self.request.user))

        return Book.objects.exclude(user=self.request.user).exclude(id__in=ordered_books).exclude(id__in=requester_books).exclude(id__in=offerrer_books).filter(Q(book_name__icontains=book_name) | Q(author_name__icontains=book_name))

        # return Book.objects.filter(Q(book_name__icontains=book_name)) | Book.objects.filter(Q(author_name__icontains=book_name))

# def search_form(request):

# 	if request.method == 'POST':
# 		form = SearchForm(request.POST)

# 		if form.is_valid():

# 			form.save()
# 			request.session['home_request'] = True
# 			return redirect('coreapp:list_entries')
# 	else:

# 		form = SearchForm()

# 	return render(request, 'list_entries.html', {'form': form})


# class SearchAutoComplete(FormView):
#     template_name = 'list_entries.html'
#     form_class = SearchForm
#     success_url = reverse_lazy('coreapp:list_entries')


class ContentAutoComplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):

		qs = Book.objects.all()

		if self.q:
			qs = qs.filter(book_name__istartswith=self.q)
			return qs
