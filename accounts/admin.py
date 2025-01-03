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
        "password_changed",
        "level",
    )
    list_filter = ("password_changed", "level")
    search_fields = (
        "username",
        "first_name",
        "last_name",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "phone",
                    "email",
                    "password_changed",
                    "entry_date",
                    "level",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "phone",
                    "entry_date",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    # fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("middle_name",)}),)
    # add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("middle_name",)}),)
