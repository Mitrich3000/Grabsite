from django import forms
from django.forms import TextInput


class MyForm(forms.Form):
    url = forms.URLField(label='Адрес', min_length=5, max_length=100, widget=TextInput(attrs={'size': 60}))
    email = forms.EmailField(label='Email', max_length=100, widget=TextInput(attrs={'size': 60}))
