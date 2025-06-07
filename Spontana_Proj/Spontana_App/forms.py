# Spontana_App/forms.py
from django import forms
import re

class FullRegisterForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'border p-2 rounded w-full mb-2', 'placeholder': 'Username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'border p-2 rounded w-full mb-2', 'placeholder': 'Enter your Gmail address'
    }))
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'border p-2 rounded w-full mb-2', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'border p-2 rounded w-full mb-2', 'placeholder': 'Confirm Password'
    }))
    code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'border p-2 rounded w-full mb-2', 'placeholder': 'Enter Verification Code'
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            raise forms.ValidationError("Only valid Gmail addresses are allowed.")
        return email
