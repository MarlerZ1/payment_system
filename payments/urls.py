from django.urls import path

from payments.views import ItemView

app_name = 'payments'

urlpatterns = [
    path('item/<int:item_id>', ItemView.as_view()),
]