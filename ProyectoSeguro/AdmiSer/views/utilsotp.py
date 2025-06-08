# utils/otp.py
import random
import uuid
from django.utils import timezone
from ..models import OTPToken


def generar_codigo_otp(longitud=6):
    """Genera un OTP numérico."""
    return ''.join(str(random.randint(0, 9)) for _ in range(longitud))

def crear_otp_unico(usuario):
    """Borra cualquier OTP previo del usuario y genera uno nuevo."""
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
