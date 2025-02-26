from django.urls import path

from payments.views import ItemView, buy_item, buy_order, OrderView, MainView

app_name = 'payments'

urlpatterns = [
    path('item/<int:item_id>', ItemView.as_view(), name="item"),
    path('buy/<int:item_id>', buy_item, name="buy"),
    path('buy_order/<int:order_id>', buy_order, name="buy_order"),
    path('order/<int:order_id>', OrderView.as_view(), name="order"),
    path('', MainView.as_view(), name="main"),
]
