from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'password']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=255)
    phone_num = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    amount = forms.CharField(max_length=255)
