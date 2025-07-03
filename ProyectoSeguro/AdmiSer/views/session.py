# AdmiSer/utils/sesion.py

from django.contrib import messages
from django.shortcuts import redirect


def iniciar_sesion_segura(request, usuario):
    """
    Establece una sesión autenticada
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        usuario (Usuario): El objeto Usuario que se está autenticando.
    Returns:
        None: Establece los datos de sesión necesarios para el usuario.    
    """
    request.session.flush()
    request.session['usuario_id'] = usuario.id
    request.session['nick'] = usuario.nick
    request.session['ha_iniciado_sesion'] = True

def establecer_pendiente_otp(request, usuario):
    """
    Guarda que el usuario debe pasar OTP
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        usuario (Usuario): El objeto Usuario que se está autenticando.  
        """
    request.session.flush()
    request.session['usuario_otp'] = usuario.id

def limpiar_sesion_login(request):
    """
    Limpia la sesión de login/OTP
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        """
    request.session.flush()

def sesion_autenticada(request):
    """
    Verifica si hay una sesión activa
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        """
    return request.session.get('ha_iniciado_sesion') is True


def logout(request):
    """ 
    Cierra la sesión del usuario y redirige al login.
    Args:   
        request (HttpRequest): La solicitud HTTP del usuario.
    Returns:
        HttpResponse: Redirige al usuario a la página de inicio de sesión.
    """
    limpiar_sesion_login(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('AdmiSer:login')
