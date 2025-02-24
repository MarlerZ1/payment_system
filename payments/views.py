from lib2to3.fixes.fix_input import context

from django.conf import settings
import stripe
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from common.mixins.mixins import TitleMixin
from payments.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemView(TitleMixin, TemplateView):
    template_name = "payments/item.html"
    title = "PaymentSystem - Item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            item_id = kwargs.get('item_id')
            item = Item.objects.get(id=item_id)

            context["item"] = item
            context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
            return context
        except BaseException as e:
            print(e)
            return JsonResponse({}, status=400)

def buy_item(request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id,
                'url': checkout_session.url,
            })
        except BaseException as e:
            print(e)
            return JsonResponse({}, status=400)