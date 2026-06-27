from django.urls import path
from .views import (
    StripeCreatePaymentIntentView, StripeWebhookView,
    CODConfirmView, PaymentHistoryView,
)

app_name = "payments"

urlpatterns = [
    path("stripe/create-intent/", StripeCreatePaymentIntentView.as_view(), name="stripe-intent"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("cod/confirm/", CODConfirmView.as_view(), name="cod-confirm"),
    path("history/", PaymentHistoryView.as_view(), name="payment-history"),
]
