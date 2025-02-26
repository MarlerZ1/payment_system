import stripe
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('RUB', 'RUB'), ('EUR', 'EUR')], default='USD')

    def __str__(self):
        return str(self.currency) + "\t|\t" + str(self.name)


class User(AbstractUser):
    pass


class Discount(models.Model):
    code = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    stripe_id = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_id:
            try:
                coupon = stripe.Coupon.create(
                    duration="forever",
                    percent_off=self.amount,
                )
                self.stripe_id = coupon.id

                super().save(*args, force_insert=False, force_update=False, using=None, update_fields=None)
            except Exception as e:
                print(e)

    def __str__(self):
        return str(self.amount)


class Tax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    stripe_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.rate)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_id:
            try:
                tax = stripe.TaxRate.create(
                    display_name=self.name,
                    percentage=self.rate,
                    inclusive=False,
                )
                self.stripe_id = tax.id

                super().save(*args, force_insert=False, force_update=False, using=None, update_fields=None)
            except Exception as e:
                print(e)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(to=Discount, on_delete=models.CASCADE, blank=True, null=True)
    taxes = models.ManyToManyField(Tax, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
