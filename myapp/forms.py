from django import forms
from .models import RegisterData
from .models import Car
from .models import MyReserve
from .models import LoginData
from .models import message
from .admin import timezone
from django.contrib.auth.forms import PasswordResetForm

# class CustomPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
class MyRegistrationForm(forms.ModelForm):
    class Meta:
        model = RegisterData
        fields = ["username","age","contact","email","address","password","confirm_password"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.com' not in email:  # Example custom validation
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match. Please try again.")


class MyCar(forms.ModelForm):
    class Car:
        model = Car
        field = ["car_name","image","additional_image1","additional_image2","additional_image3","price","kilometer","Luggage","Seats","status"]

class MyReserveForm(forms.ModelForm):
    picktime = forms.TimeField(
        widget=forms.TimeInput(
            format='%I:%M %p',
            attrs={'placeholder': '12:00 AM'}
        ),
        input_formats=['%I:%M %p']
    )
    droptime = forms.TimeField(
        widget=forms.TimeInput(
            format='%I:%M %p',
            attrs={'placeholder': '12:45 PM'}
        ),
        input_formats=['%I:%M %p']
    )
    class Meta:
        model = MyReserve
        fields = ['Car','price','name', 'age', 'phone_number', 'email', 'pickup', 'dropoff', 'pickdate','dropdate','picktime', 'droptime']
        widgets = {
            'pickdate': forms.DateInput(attrs={'type': 'date'}),
            'dropdate': forms.DateInput(attrs={'type': 'date'}),
            'picktime': forms.TimeInput(attrs={'type': 'time'}),
            'droptime': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.com' not in email:  # Example custom validation
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        pickdate = cleaned_data.get('pickdate')
        dropdate = cleaned_data.get('dropdate')

        if dropdate < pickdate:
            raise forms.ValidationError("Drop date should be after pick date.")

        if pickdate < timezone.now().date():
            raise forms.ValidationError("Pick date must be in the future.")

class MyLoginForm(forms.ModelForm):
    class LoginData:
        model = LoginData
        field = ["username","password"]


class MyMessage(forms.ModelForm):
    class Usermessage:
        model = message
        field = ["fullname","email","tellme"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.com' not in email:  # Example custom validation
            raise forms.ValidationError("Please enter a valid email address.")
        return email