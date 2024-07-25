from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import CustomUser

# Create your views here.
from .forms import CustomUserCreationForm, AddVoterForm


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.request.user.password_changed = True
        self.request.user.save()

        return super().form_valid(form)


@staff_member_required
def add_new_voters(request):
    # form = CustomUserCreationForm()
    form = AddVoterForm()
    if request.method == "POST":
        # form = CustomUserCreationForm(request.POST)
        username = request.POST.get("phone_number")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        level = request.POST.get("level")

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            level=level,
            password="gmsa2024",
        )
        messages.success(request, f"You've added {username} to the voter register.")
        return redirect("add-voters")

        # if form.is_valid():
        #     form.save()
        #     messages.success(request, f"You've added {username} to the voter register.")
        #     return redirect("add-voters")
    context = {"form": form}
    return render(request, "accounts/add_voter.html", context)


# def logout(request):
#     if request.method == 'POST':
#         selected_candidates = request.session.get("selected_candidates")
#         if selected_candidates:
#             request.session['selected_candidates'] = {}
#         logout(request)
#         return redirect('login')
#     return redirect('home')
