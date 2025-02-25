from django import forms
from .models import CustomUser, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

class RegistrationForm(UserCreationForm):
    model = CustomUser
    email = forms.EmailField()

    class Meta:
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']