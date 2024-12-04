from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'first_name', 'last_name', 'postal_code', 'address',
                  'province', 'city']

