from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import requests

from .models import Payment, DuesRegister, Donation


def payments_home(request):
    return render(request, "payments/homePage.html")


@login_required
def dues_payment(request):
    user = request.user
    if request.method == "POST":
        request.session["index"] = request.POST.get("index-no")
        request.session["momo"] = request.POST.get("momo-no")
        request.session["amount"] = request.POST.get("amount")
        request.session["academic-year"] = request.POST.get("academic-year")
        return redirect("dues_preview")
    context = {"academic_years": user.get_academic_years}
    return render(request, "payments/duesForm.html", context)


@login_required
def details_preview(request):
    print("index", request.session["index"])
    print("momo", request.session["momo"])
    print("amount", request.session["amount"])
    print("academic-year", request.session["academic-year"])
    print(request.session.get("index"))
    return render(request, "payments/duesPreview.html")


def initiate_payment(request):
    if request.method == "POST":
        momo_number = request.session["momo"]
        amount = request.session["amount"]
        academic_year = request.session["academic-year"]
        provider = request.session["provider"]

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "email": f"user_{momo_number}@example.com",
            "amount": amount,
            "currency": "GHS",
            "mobile_money": {"phone": momo_number, "provider": provider},
            "callback_url": "http://127.0.0.1:8000/payments/verify",
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            payment_url = data["data"]["authorization_url"]
            return redirect(payment_url)
        else:
            messages.error(request, "Payment initialization failed!")
            return redirect("payments_home")


def verify_payment(request):
    reference = request.GET.get("reference")

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["data"]["status"] == "success":
            success(request)
        else:
            failed(request)
    else:
        messages.error(request, "An error occurred during verification.")
        return redirect("payments_home")


def donation_payment(request):
    return render(request, "payments/donationForm.html")


def waiting(request):
    return render(request, "payments/waitingPage.html")


def success(request):
    return render(request, "payments/successPage.html")


def failed(request):
    return render(request, "payments/failedPage.html")
