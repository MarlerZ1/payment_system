from django.urls import path

from payments.views import ItemView, buy_item, buy_order

app_name = 'payments'

urlpatterns = [
    path('item/<int:item_id>', ItemView.as_view(), name="item"),
    path('buy/<int:item_id>', buy_item, name="buy"),
    path('buy_order/<int:order_id>', buy_order, name="buy_order"),
]
