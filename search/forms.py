from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coreapp.models import Book, Profile
from dal import autocomplete

class SearchForm(forms.Form):

    search = forms.CharField(
        max_length=100, widget=autocomplete.ModelSelect2(url='country-autocomplete'))

    # class Meta:
    #     widgets = {'search': autocomplete.ListSelect2(
    #         url='content-autocomplete')}

    # def __init__(self, *args, **kwargs):
    #     super(FeedbackInfoInputModelForm, self).__init__(*args, **kwargs)
    #     self.fields['search'].widget = forms.TextInput(attrs={
    #         'id': 'search',
    #     })
