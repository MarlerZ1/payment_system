from django.contrib import admin
from django.core.exceptions import ValidationError

from payments.forms import OrderForm
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
    readonly_fields = ['created_at']
    form = OrderForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            super().save_model(request, obj, form, change)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']
    readonly_fields = ['stripe_id']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    readonly_fields = ['stripe_id']
