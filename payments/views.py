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
                    'currency': item.currency,
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
                    'currency': item.currency,
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
            }, ] if order.discount else [],
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        return JsonResponse({
            'id': checkout_session.id,
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


class OrderView(TitleMixin, TemplateView):
    template_name = 'payments/order.html'
    title = "PaymentSystem - Order"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order_id = kwargs.get('order_id')

            order = Order.objects.get(id=order_id)

            context["taxes"] = order.taxes.all()
            context["items"] = order.items.all()
            context["discount"] = order.discount
            context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
            return context
        except Order.DoesNotExist as e:
            print(e)
            return context
        except Exception as e:
            print(e)
            return context

class MainView(TitleMixin, TemplateView):
    template_name = 'payments/main.html'
    title = 'PaymentSystem - Main'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        context['orders'] = Order.objects.all()
        return context