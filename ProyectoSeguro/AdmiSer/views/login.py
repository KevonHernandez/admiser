from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
import base64

from ..views.session import establecer_pendiente_otp, limpiar_sesion_login
from ..models import Usuario
from ..forms import LoginForm
from ..cripto.hasheo import password_valido

MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 5  # segundos


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def esta_bloqueada(ip):
    return cache.get(f'intentos_login_{ip}', 0) >= MAX_INTENTOS


def registrar_intento(ip):
    intentos = cache.get(f'intentos_login_{ip}', 0) + 1
    cache.set(f'intentos_login_{ip}', intentos, timeout=TIEMPO_BLOQUEO)
    print(f"Intentos de inicio de sesión para {ip}: {intentos}")


def reset_intentos(ip):
    cache.delete(f'intentos_login_{ip}')


def login(request):
    ip = get_client_ip(request)

    if esta_bloqueada(ip):
        messages.error(
            request, 'Demasiados intentos fallidos. Intenta más tarde.')
        
        return render(request, 'login.html', {'form': LoginForm()})

    form = LoginForm(request.POST or None)
    
    if request.method == 'GET':
        limpiar_sesion_login(request)

    if esta_bloqueada(ip):
        messages.error(
            request, 'Demasiados intentos fallidos. Intenta más tarde.')
        return render(request, 'login.html', {'form': LoginForm()})

    if request.method == 'POST' and form.is_valid():
        nick = form.cleaned_data['nick']
        password = form.cleaned_data['password']

        try:
            usuario = Usuario.objects.get(nick=nick)
            salt = base64.b64decode(usuario.salt)
            
            if password_valido(password, usuario.password, salt):
                request.session['usuario_otp'] = usuario.id
                reset_intentos(ip)
                establecer_pendiente_otp(request, usuario)
                return redirect('AdmiSer:verificar_otp')
            else:
                registrar_intento(ip)
                messages.error(request, 'Usuario o contraseña incorrectos.')

        except Usuario.DoesNotExist:
            registrar_intento(ip)
            limpiar_sesion_login(request)
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        registrar_intento(ip)
        limpiar_sesion_login(request)

    return render(request, 'login.html', {'form': form})
