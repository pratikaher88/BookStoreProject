from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coreapp.models import Book, Profile, ShippingAddress
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
        fields = ['book_name','author_name', 'description',
                  'sell_or_exchange', 'price', 'condition','image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(NewEntryForm, self).__init__(*args, **kwargs)
        # self.fields['sell_or_exchange'].widget = forms.ChoiceField(attrs={
        #         'id': 'sellorexchangeid',
        # })

        self.fields['price'].widget = forms.TextInput(attrs={
                'type': 'number',
                'id': 'priceid',
        })

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ('profile',)

    field_order = ['flatnumber', 'address1',
                   'address2', 'zip_code','city', 'phone_number']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', ]
