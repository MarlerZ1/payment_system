from lib2to3.fixes.fix_input import context

from django.conf import settings
import stripe
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
            return context
        except BaseException as e:
            print(e)
