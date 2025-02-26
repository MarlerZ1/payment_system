from django.contrib import admin
from django.core.exceptions import ValidationError

from payments.models import Item, User, Order, Tax, Discount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'description']
    fieldsets = [
        (None, {
            'fields': ('name', ('price', 'currency'), 'description')
        }),
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', "email", "is_staff"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at']

    def save_model(self, request, obj, form, change):
        try:
            new_items = form.cleaned_data.get('items', [])
            self.validate(new_items)
        except ValidationError as e:
            form.add_error('items', e)
            self.message_user(request, e.message, level='error')
            return
        else:
            super().save_model(request, obj, form, change)


    def validate(self, new_items):
        item_currency = None
        for item in new_items:
            if item_currency is None:
                item_currency = item.currency
            elif item.currency != item_currency:
                raise ValidationError("Все товары в заказе должны иметь одинаковую валюту.")

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']
    readonly_fields = ['stripe_id']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    readonly_fields = ['stripe_id']
