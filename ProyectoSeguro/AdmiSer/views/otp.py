# AdmiSer/views/otp.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from ..views.login import get_client_ip, registrar_intento
from ..views.session import iniciar_sesion_segura, limpiar_sesion_login
from ..models import Usuario, OTPToken
from ..forms import OTPForm
from ..views.utilsotp import crear_otp_unico  # <--- importante

def verificar_otp(request):
    """
    Verifica el OTP enviado al usuario y permite el inicio de sesión seguro.\
    Si el OTP es válido, inicia sesión y redirige al dashboard.
    Si no es válido, muestra un mensaje de error y redirige al login.
    """
    # Verifica si el usuario ya está autenticado
    if request.user.is_authenticated:
        messages.info(request, 'Ya estás autenticado.')
        return redirect('AdmiSer:dashboard')    

    usuario_id = request.session.get('usuario_otp')
    if not usuario_id:
        limpiar_sesion_login(request)
        messages.error(request, 'Sesión de verificación inválida.')
        return redirect('AdmiSer:login')

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        limpiar_sesion_login(request)
        messages.error(request, 'Usuario no encontrado.')
        ip = get_client_ip(request)
        registrar_intento(ip)
        return redirect('AdmiSer:login')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            otp = OTPToken.objects.filter(user=usuario, token=otp_code).last()  # no importa si used=True

            # Invalida cualquier OTP anterior
            OTPToken.objects.filter(user=usuario).update(used=True)
            # 🔐 Verifica que el session_id del OTP coincida con el de la sesión
            session_id_actual = request.session.get('otp_session_id')
            print(f"Session ID actual: {session_id_actual}")  # Para depuración
            if otp and otp.is_valid() and str(otp.session_id) == session_id_actual:
                iniciar_sesion_segura(request, usuario)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('AdmiSer:dashboard')
            else:
                request.session.pop('usuario_otp', None)
                messages.error(request, 'OTP inválido o expirado.')
                registrar_intento(ip)
                limpiar_sesion_login(request)

                return redirect('AdmiSer:login')
        else:
            limpiar_sesion_login(request)
            messages.error(request, 'Código OTP mal formado.')
            ip = get_client_ip(request)
            registrar_intento(ip)

            return redirect('AdmiSer:login')
    else:
        # Evita reenvíos frecuentes
        ultimo = OTPToken.objects.filter(user=usuario).order_by('-created_at').first()
        if ultimo and (timezone.now() - ultimo.created_at).total_seconds() < 30:
            messages.warning(request, 'Espera unos segundos antes de solicitar un nuevo OTP.')
            return render(request, 'login.html', {'form': OTPForm(), 'otp_required': True})

        # 🔐 Generar OTP único y enviar
        codigo, session_id = crear_otp_unico(usuario)
        request.session['otp_session_id'] = session_id  # ✅ Guardar session_id en la sesión

        send_mail(
            subject='Tu código OTP',
            message=f'Tu código de acceso es: {codigo}',
            from_email='tuapp@correo.com',
            recipient_list=[usuario.email],
            fail_silently=False,
        )
        messages.info(request, 'Se envió un código OTP a tu correo.')

    return render(request, 'login.html', {'form': OTPForm(), 'otp_required': True})
