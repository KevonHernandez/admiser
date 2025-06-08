from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    nick = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )
    captcha = CaptchaField(label='Captcha')

class OTPForm(forms.Form):
    otp = forms.CharField(
        label='Código OTP',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el código OTP'
        })
    )
