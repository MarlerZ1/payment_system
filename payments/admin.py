import stripe
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

    def delete_queryset(self, request, queryset):
        for tax in queryset:
            if tax.stripe_id:
                try:
                    stripe.TaxRate.modify(tax.stripe_id, active=False)
                except stripe.error.StripeError as e:
                    self.message_user(request, f"Ошибка удаления налога в Stripe: {tax.stripe_id}: {e}", level='error')

        super().delete_queryset(request, queryset)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    readonly_fields = ['stripe_id']


    def delete_queryset(self, request, queryset):
        for discount in queryset:
            if discount.stripe_id:
                try:
                    stripe.Coupon.delete(discount.stripe_id)
                except stripe.error.StripeError as e:
                    self.message_user(request, f"Ошибка удаления Discount в Stripe: {discount.stripe_id}: {e}", level='error')

        super().delete_queryset(request, queryset)