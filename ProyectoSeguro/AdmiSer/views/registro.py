# AdmiSer/views/registro.py
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from ..cripto.passvalidation import password_check
from ..models import Usuario
from ..cripto.hasheo import generar_salt, hashear_password, convertir_binario_texto64

def registro(request):
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        nick = request.POST['nick']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        correo = request.POST['email']

        mensajesPassword = password_check(password)

        if not nick or not correo or not password or not confirm_password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('AdmiSer:registro')

        if Usuario.objects.filter(nombre_completo=nombre_completo).exists():
            messages.error(request, 'El nombre ya está registrado.')
            return redirect('AdmiSer:registro')

        if Usuario.objects.filter(nick=nick).exists():
            messages.error(request, 'El nick o nombre ya está registrado.')
            return redirect('AdmiSer:registro')

        if Usuario.objects.filter(email=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('AdmiSer:registro')

        if mensajesPassword != "":
            messages.error(request, mensajesPassword)
            return redirect('AdmiSer:registro')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('AdmiSer:registro')

        # Hashear la contraseña con salt
        salt = generar_salt()
        hash_password, salt = hashear_password(password, salt)

        # Crear el usuario sin llaves
        nuevo_usuario = Usuario(
            nombre_completo=nombre_completo,
            nick=nick,
            password=hash_password,
            email=correo,
            salt=convertir_binario_texto64(salt)
        )

        nuevo_usuario.save()

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('AdmiSer:login')

    return render(request, 'registro.html')
