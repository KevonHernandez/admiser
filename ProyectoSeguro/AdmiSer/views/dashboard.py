from django.contrib import messages
from django.shortcuts import render, redirect
from AdmiSer.decorators import sesion_requerida
from AdmiSer.forms import ServicioForm
from ..views.session import limpiar_sesion_login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Servicio, Servidor
import paramiko


@sesion_requerida
def dashboard(request):
    if request.method == 'POST':
        # Caso para cerrar sesión
        if request.POST.get('cerrar_sesion') == 'true':
            limpiar_sesion_login(request)
            return redirect('AdmiSer:login')

        # Caso para agregar servicio desde dashboard
        servidor_id = request.POST.get('servidor_id')
        nombre_servicio = request.POST.get('nombre_servicio')

        if servidor_id and nombre_servicio:
            servidor = get_object_or_404(Servidor, id=servidor_id)
            form = ServicioForm({'nombre': nombre_servicio})
            if form.is_valid():
                # ✅ Verificamos si el servicio existe en el servidor
                comando_verificacion = f'systemctl status {nombre_servicio}'
                salida, error = ejecutar_comando_ssh(servidor, comando_verificacion)

                if error or 'not-found' in salida or 'could not be found' in salida or 'Loaded: not-found' in salida:
                    messages.error(request, f'El servicio "{nombre_servicio}" no existe o no se encontró en el servidor "{servidor.nombre}".')
                else:
                    servicio = form.save(commit=False)
                    servicio.servidor = servidor
                    servicio.save()
                    messages.success(request, f'Servicio "{servicio.nombre}" agregado al servidor "{servidor.nombre}".')
                    return redirect('AdmiSer:dashboard')
            else:
                messages.error(request, 'Nombre de servicio inválido.')

    # GET o cualquier otro caso
    servidores = Servidor.objects.all().prefetch_related('servicio_set')
    context = {
        'servidores': servidores,
    }
    return render(request, 'dashboard.html', context)

def ejecutar_comando_ssh(servidor, comando):
    try:
        cliente = paramiko.SSHClient()
        cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente.connect(hostname=servidor.ip,
                        username=servidor.usuario, password=servidor.password)
        stdin, stdout, stderr = cliente.exec_command(comando)
        salida = stdout.read().decode()
        error = stderr.read().decode()
        cliente.close()
        print(f"Comando: {comando}")
        print(f"Salida: {salida}")
        print(f"Error: {error}")
        if error:
            return None, error
        return salida, None
    except Exception as e:
        return None, str(e)


def accion_servicio(request, accion, servicio_id):
    try:
        servicio = Servicio.objects.get(id=servicio_id)
        servidor = servicio.servidor
        nombre_servicio = servicio.nombre

        if accion == 'levantar':
            comando = f'sudo systemctl start {nombre_servicio}'
        elif accion == 'reiniciar':
            comando = f'sudo systemctl restart {nombre_servicio}'
        elif accion == 'detener':
            comando = f'sudo systemctl stop {nombre_servicio}'
        elif accion == 'estado':
            comando = f'systemctl is-active {nombre_servicio}'
        else:
            return JsonResponse({'resultado': 'Acción no válida'}, status=400)

        salida, error = ejecutar_comando_ssh(servidor, comando)

        if error:
            return JsonResponse({'resultado': f'Error al ejecutar: {error}'}, status=500)

        if accion == 'estado':
            salida = salida.strip()
            if salida == 'active':
                estado = 'activo'
            elif salida in ['inactive', 'failed']:
                estado = 'inactivo'
            else:
                estado = 'desconocido'
            return JsonResponse({'servicio': nombre_servicio, 'estado': estado})

        return JsonResponse({'resultado': f'{accion.capitalize()} ejecutado correctamente.'})

    except Servicio.DoesNotExist:
        return JsonResponse({'resultado': 'Servicio no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'resultado': f'Error inesperado: {str(e)}'}, status=500)


@sesion_requerida
def listar_servidores(request):
    servidores = Servidor.objects.all()
    return render(request, 'listar_servidores.html', {'servidores': servidores})
