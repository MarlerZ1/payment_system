import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView

from common.mixins.mixins import TitleMixin
from payments.models import Item, Order

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
        except Order.DoesNotExist as e:
            print(e)
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=500)


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
    except Order.DoesNotExist as e:
        print(e)
        return JsonResponse({'error': 'Order not found'}, status=404)
    except stripe.error.StripeError as e:
        print(e)
        return JsonResponse({}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def buy_order(request, order_id):
    try:

        order = Order.objects.get(id=order_id)

        item_taxes = []
        for tax in order.taxes.all():
            item_taxes.append(tax.stripe_id)

        line_items = []
        for item in order.items.all():
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
                "tax_rates": item_taxes
            }

            line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            discounts=[{
                'coupon': order.discount.stripe_id
            }, ],
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        return JsonResponse({'url': checkout_session.url})

    except Order.DoesNotExist as e:
        print(e)
        return JsonResponse({'error': 'Order not found'}, status=404)
    except stripe.error.StripeError as e:
        print(e)
        return JsonResponse({}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)
