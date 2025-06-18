from django.shortcuts import render, redirect
from AdmiSer.decorators import sesion_requerida
from ..models import Servidor, Servicio
import docker

@sesion_requerida
def dashboard(request):
    if request.method == 'POST' and request.POST.get('cerrar_sesion') == 'true':
        from ..views.session import limpiar_sesion_login
        limpiar_sesion_login(request)
        return redirect('AdmiSer:login')

    servidores_db = Servidor.objects.all()
    cliente = docker.from_env()

    lista_servidores = []

    for servidor in servidores_db:
        try:
            contenedor = cliente.containers.get(servidor.nombre_contenedor)
            estado = contenedor.status
        except docker.errors.NotFound:
            estado = 'No creado'
        except docker.errors.APIError as e:
            estado = f'Error: {str(e)}'

        # Obtener servicios relacionados y su estado
        servicios = Servicio.objects.filter(servidor=servidor)
        servicios_info = []
        for s in servicios:
            servicios_info.append({
                'nombre': s.nombre,
                'estado': s.status_servicio
            })

        lista_servidores.append({
            'nombre': servidor.nombre_servidor,
            'ip': servidor.ip,
            'sistema': servidor.sistema_operativo,
            'contenedor': servidor.nombre_contenedor,  # para uso en AJAX
            'servicios': servicios_info,
            'estado': estado
        })

    return render(request, 'dashboard.html', {
        'servidores': lista_servidores
    })
