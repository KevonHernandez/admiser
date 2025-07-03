# utils/otp.py
import random
import uuid
from django.utils import timezone
from ..models import OTPToken


def generar_codigo_otp(longitud=6):
    """
    Genera un OTP numérico.
    Args:
        longitud (int): Longitud del código OTP a generar. Por defecto es 6.    
    Returns:
        str: Un código OTP numérico de la longitud especificada.
    """
    return ''.join(str(random.randint(0, 9)) for _ in range(longitud))

def crear_otp_unico(usuario):
    """
    Borra cualquier OTP previo del usuario y genera uno nuevo.
    Args:
        usuario (Usuario): El objeto Usuario para el cual se generará el OTP.
    Returns:
        tuple: Un código OTP y un ID de sesión único.
    """
    OTPToken.objects.filter(user=usuario).delete()

    codigo = generar_codigo_otp()
    session_id = uuid.uuid4() #guardar el ID de sesión para rastrear el OTP

    OTPToken.objects.create(
        user=usuario,
        token=codigo,
        used=False,
        session_id=session_id
    )

    return codigo, str(session_id)
