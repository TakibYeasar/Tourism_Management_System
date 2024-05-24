from .models import Booking
from django import forms
from authapi.models import CustomUser
from django.core.exceptions import ValidationError


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current Password', 'required': 'required'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password', 'required': 'required'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'required': 'required'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError(
                "New Password and Confirm Password do not match.")

        return cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['from_date', 'to_date', 'comment']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


