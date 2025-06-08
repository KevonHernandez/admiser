# AdmiSer/utils/sesion.py

from django.contrib import messages
from django.shortcuts import redirect


def iniciar_sesion_segura(request, usuario):
    """Establece una sesión autenticada"""
    request.session.flush()  # Limpia cualquier dato previo
    request.session['usuario_id'] = usuario.id
    request.session['nick'] = usuario.nick
    request.session['ha_iniciado_sesion'] = True

def establecer_pendiente_otp(request, usuario):
    """Guarda que el usuario debe pasar OTP"""
    request.session.flush()
    request.session['usuario_otp'] = usuario.id

def limpiar_sesion_login(request):
    """Limpia la sesión de login/OTP"""
    request.session.pop('usuario_otp', None)
    request.session.pop('usuario_id', None)
    request.session.pop('nick', None)
    request.session.pop('ha_iniciado_sesion', None)

def sesion_autenticada(request):
    """Verifica si hay una sesión activa"""
    return request.session.get('ha_iniciado_sesion') is True


def logout(request):
    limpiar_sesion_login(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('AdmiSer:login')