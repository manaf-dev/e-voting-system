from django.urls import path

from . import views

urlpatterns = [
    path("", views.payments_home, name="payments_home"),
    path("pay-dues/", views.dues_payment, name="pay_dues"),
    path("donate/", views.donation_payment, name="donate"),
    path("preview-payment/", views.details_preview, name="details_preview"),
    path("initiate-payment/", views.initiate_payment, name="payment_initiate"),
    path("verify/", views.verify_payment, name="verify"),
    path("waiting/", views.waiting, name="waiting"),
    path("success/", views.success, name="success"),
    path("failed/", views.failed, name="failed"),
]
