from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import (
    Account,
)

class SignInForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            try:
                if not Account.objects.get(email__iexact = email).is_active:
                    raise forms.ValidationError('you must validate your account!')
            except Account.DoesNotExist:
                raise forms.ValidationError("Invalid Login!")

            if not authenticate(email = email, password = password):
                raise forms.ValidationError("Invalid Login!")

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label='old password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='new password', required=True, widget=forms.PasswordInput)
    password3 = forms.CharField(label='new password', required=True, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.is_valid():
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            password3 = self.cleaned_data['password3']
            if not authenticate(email = self.user.email, password=password1):
                raise forms.ValidationError("old password is incorrect!")
            if password2 != password3:
                raise forms.ValidationError("new password don't match!")

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('email', 'username', 'is_protected', 'hide_email', 'profile_image', 'cover_image')
