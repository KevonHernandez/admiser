from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import docker
from ..models import Servicio

@csrf_exempt
def accion_servicio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nombre_contenedor = data.get("contenedor")
        nombre_servicio = data.get("servicio")
        accion = data.get("accion")

        try:
            cliente = docker.from_env()
            contenedor = cliente.containers.get(nombre_contenedor)
            contenedor.reload()

            # Verificar si el contenedor está corriendo
            if contenedor.status != 'running':
                return JsonResponse({
                    "mensaje": f"El contenedor '{nombre_contenedor}' no está corriendo."
                }, status=400)

            # Verificar si el binario existe
            verificacion = contenedor.exec_run(f"which {nombre_servicio}", user="root", demux=True)
            if verificacion.exit_code != 0:
                return JsonResponse({
                    "mensaje": f"El servicio '{nombre_servicio}' no está instalado en el contenedor."
                }, status=400)

            # Comando específico según el servicio
            if nombre_servicio == "apache" or nombre_servicio == "apache2":
                comando = f"apachectl -k {'restart' if accion == 'reiniciar' else 'stop'}"
            else:
                if accion not in ["reiniciar", "detener"]:
                    return JsonResponse({"mensaje": "Acción no válida."}, status=400)
                comando = f"service {nombre_servicio} {'restart' if accion == 'reiniciar' else 'stop'}"

            # Ejecutar el comando
            salida = contenedor.exec_run(cmd=comando, user="root", demux=True)

            if salida.exit_code == 0:
                # Actualizar el estado del servicio en la base de datos
                servicio = Servicio.objects.filter(
                    nombre=nombre_servicio,
                    servidor__nombre_contenedor=nombre_contenedor
                ).first()
                if servicio:
                    servicio.status_servicio = "activo" if accion == "reiniciar" else "no activo"
                    servicio.save()

                return JsonResponse({"mensaje": f"Servicio '{nombre_servicio}' {accion} correctamente."})
            else:
                stdout = salida.output[0].decode() if salida.output and salida.output[0] else ''
                stderr = salida.output[1].decode() if salida.output and salida.output[1] else ''
                return JsonResponse({
                    "mensaje": f"No se pudo {accion} el servicio '{nombre_servicio}'.",
                    "stdout": stdout,
                    "stderr": stderr
                }, status=500)

        except docker.errors.NotFound:
            return JsonResponse({"mensaje": f"Contenedor '{nombre_contenedor}' no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"mensaje": f"Error interno: {str(e)}"}, status=500)

    return JsonResponse({"mensaje": "Método no permitido."}, status=405)
