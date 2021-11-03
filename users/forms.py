from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.widgets import TextInput, Textarea
from shop.models import CancellationOrder

from .models import CustomUser


class CancellationOrderForm(forms.ModelForm):

    class Meta:
        model = CancellationOrder
        fields = ('comment',)
        widgets = {
            'comment': Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control-sm col-12 mt-0 pt-0 mb-3 border border-2",
                    "placeholder": "Вы можете оставить любой комментарий. Это не обязательно."
                }
            )
        }


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'phonenumber',
            'social_network',
            'address',
            'agreement',
        )
        widgets = {
            'username': TextInput(attrs={"class": "form-control"}),
            'first_name': TextInput(attrs={"class": "form-control"}),
            'last_name': TextInput(attrs={"class": "form-control"}),
            'social_network': TextInput(attrs={"class": "form-control"}),
            'address': TextInput(attrs={"class": "form-control"}),
            'phonenumber': TextInput(attrs={"class": "form-control"}),
            'password1': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
