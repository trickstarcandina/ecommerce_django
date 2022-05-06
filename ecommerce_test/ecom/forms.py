from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']

class DrinkForm(forms.ModelForm):
    class Meta:
        model=models.Drink
        fields=['name','size','type', 'expiry']

class CakeForm(forms.ModelForm):
    class Meta:
        model=models.Cake
        fields=['name','type','expiry']


#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class CakeItemForm(forms.ModelForm):
    class Meta:
        model=models.Cakeitem
        fields= '__all__'


class DrinkItemForm(forms.ModelForm):
    class Meta:
        model=models.Drinkitem
        fields= '__all__'