from django.urls import path

from payments.views import ItemView, buy_item

app_name = 'payments'

urlpatterns = [
    path('item/<int:item_id>', ItemView.as_view()),
    path('buy/<int:item_id>', buy_item),
]