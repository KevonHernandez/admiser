from django import forms
from AdmiSer.models import Servicio, Servidor
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    nick = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',

            'placeholder': ''

        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',

            'placeholder': ''
        })
    )
    captcha = CaptchaField(label='Captcha')

class OTPForm(forms.Form):
    otp = forms.CharField(
        label='Código OTP',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': 'Ingresa aqui el código OTP'
        })
    )

class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nombre', 'ip', 'usuario', 'password', 'puerto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'puerto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ServicioForm(forms.ModelForm):
        class Meta:
            model = Servicio
            fields = ['nombre']  # Solo el nombre, el servidor se asigna en la vista
            widgets = {
                'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del servicio'})
            }