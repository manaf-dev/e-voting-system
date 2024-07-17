from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .models import CustomUser

# Create your views here.


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.request.user.password_changed = True
        self.request.user.save()

        return super().form_valid(form)


# def logout(request):
#     if request.method == 'POST':
#         selected_candidates = request.session.get("selected_candidates")
#         if selected_candidates:
#             request.session['selected_candidates'] = {}
#         logout(request)
#         return redirect('login')
#     return redirect('home')
