from django.contrib import admin

from payments.models import Item, User


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']


@admin.register(User)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', "email", "is_staff"]