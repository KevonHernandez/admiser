from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Servidor, Servicio, Usuario

def registrarservidor(request):
    if not request.session.get('ha_iniciado_sesion'):
        messages.error(request, 'Debes iniciar sesión primero.')
        return redirect('AdmiSer:login')

    if request.method == 'POST':
        nombre_servidor = request.POST.get('nombre_servidor')
        descripcion_servidor = request.POST.get('descripcion_servidor')
        ip_servidor = request.POST.get('ip')
        puerto_servidor = request.POST.get('puerto')
        so_servidor = request.POST.get('sistema_operativo')

        nombre_servicio = request.POST.get('nombre_servicio')
        descripcion_servicio = request.POST.get('descripcion_servicio')
        puerto_servicio = request.POST.get('puerto_servicio')

        if all([nombre_servidor, ip_servidor, puerto_servidor, so_servidor, nombre_servicio, puerto_servicio]):
            nick_usuario = request.session.get('nick')
            try:
                administrador = Usuario.objects.get(nick=nick_usuario)
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado en la sesión.')
                return redirect('AdmiSer:login')

            # Simulación de estados (comentario con solución real debajo)
            status_servidor = 'Activo'
            status_servicio = 'Corriendo'

            servidor = Servidor.objects.create(
                administrador=administrador,
                nombre=nombre_servidor,
                ip=ip_servidor,
                puerto=puerto_servidor,
                sistema_operativo=so_servidor,
                status_servidor=status_servidor,
                descripcion=descripcion_servidor
            )

            Servicio.objects.create(
                nombre=nombre_servicio,
                descripcion=descripcion_servicio,
                puerto=puerto_servicio,
                servidor=servidor,
                status_servicio=status_servicio
            )

            messages.success(request, f'Servidor "{nombre_servidor}" y servicio "{nombre_servicio}" registrados correctamente.')
            return redirect('AdmiSer:registrarservidor')
        else:
            messages.error(request, 'Completa todos los campos obligatorios.')

    return render(request, 'registrarServidor.html')