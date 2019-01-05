from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coreapp.models import Book, Profile
from dal import autocomplete


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'description', 'image', 'price', 'condition']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', ]