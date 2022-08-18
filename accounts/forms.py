from enum import unique
import imp
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)	


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}))
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}), label="Confirm Password")
    is_staff = forms.BooleanField(label="Are you a staff?", required=False)
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'full_name',
            'password',
            'password2',
            "is_staff"
        ]

    
    def clean_full_name(self):
        data = self.cleaned_data.get('full_name')
        if len(data) < 5:
            raise ValidationError("Full name must be at least 5 characters!")
        return data 

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        #check for password length at least 8 characters.
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters!")
        return password
    
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        #check for password and password2 is match.
        if password != password2:
            raise ValidationError("Confirm password must be same!")
        
        return password2


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'type': 'password'}))
    
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'password',
        ]

    
    def clean_full_name(self):
        data = self.cleaned_data.get('full_name')
        if len(data) < 5:
            raise ValidationError("Full name must be at least 5 characters!")
        return data 

    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        #check for password length.
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters!")
        return password


class EditUserForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=False)
    
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
        ]

    
    def clean_full_name(self):
        data = self.cleaned_data.get('full_name')
        if len(data) <= 5:
            raise ValidationError("Full name must be at least 5 characters!")
        return data 


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'address',
            'phone',
            'photo',
        ]
