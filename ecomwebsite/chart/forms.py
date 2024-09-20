from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import User  
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import *
#from django_countries.fields import CountryField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget





class Userregisterform(UserCreationForm):
    email=forms.EmailField(required=True)
    phone_fields=forms.IntegerField(max_value=12)
    class Meta:

        model=User 
        fields=['username','email','password1','password2','phone_fields']


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product 
        fields='__all__'


class CheckoutForm(forms.Form):
  
    street_address=forms.CharField(widget=forms.TextInput())
    Apparment_address=forms.CharField(widget=forms.TextInput())
    country=CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget())
    zip_code=forms.CharField(widget=forms.TextInput())
       
class CardForm(forms.Form):
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    expiration_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))