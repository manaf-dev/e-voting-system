from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class ForcePasswordChangeMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if request.user.is_authenticated and not request.user.password_changed:
            # change_password_url = reverse("password_change")
            # change_password_done_url = reverse("password_change_done")
            if request.path != reverse("change_password"):
                print(f"Redirecting {request.user} to change password")
                return redirect("change_password")
        return self.get_response(request)
