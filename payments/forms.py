from django import forms
from django.core.exceptions import ValidationError
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['items', 'discount', 'taxes']

    def clean_items(self):
        items = self.cleaned_data.get('items')


        item_currency = None
        for item in items:
            if item_currency is None:
                item_currency = item.currency
            elif item.currency != item_currency:
                raise ValidationError("Все товары в заказе должны иметь одинаковую валюту.")

        return items

