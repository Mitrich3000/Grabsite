from django import forms


class MyForm(forms.Form):
    url = forms.URLField(label='Адрес для анализа', max_length=30)
    email = forms.EmailField(label='Email для получения данных', max_length=30)

