from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        # fields = UserCreationForm.Meta.fields + ("middle_name",)
        fields = (
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "level",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class AddVoterForm(forms.Form):
    LEVEL = [("100", "100"), ("200", "200"), ("300", "300")]
    phone_number = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=True)
    level = forms.CharField(max_length=3, required=True)
    # level = forms.ChoiceField(choices=[LEVEL], required=True)
