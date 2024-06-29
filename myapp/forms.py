from django import forms
from .models import *

class ImageForm(forms.Form):
    image = forms.ImageField()

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
