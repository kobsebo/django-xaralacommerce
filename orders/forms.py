from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    firstname = forms.CharField(
        label="Prénoms", widget=forms.TextInput({"class": "form-control", "placeholder": "Prénoms"}))
    
    name = forms.CharField(
        label="Nom", widget=forms.TextInput({"class": "form-control", "placeholder": "Nom"}))
    
    email = forms.EmailField(
        label="Votre email", widget=forms.TextInput({"class": "form-control", "placeholder": "Votre email"}))
    
    address = forms.CharField(
        label="Adresse de Livraison", widget=forms.TextInput({"class": "form-control", "placeholder": "Adresse de Livraison"}))
    
    phone = forms.CharField(
        label="Téléphone", widget=forms.TextInput({"class": "form-control", "placeholder": "Téléphone"}))
    
    class Meta:
        model = Order
        fields = ("firstname", "name", "email", "phone", "address")