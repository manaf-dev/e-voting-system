from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

# admin.site.register(CustomUser)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "username",
        "first_name",
        "last_name",
    )
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("token",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("token",)}),)
