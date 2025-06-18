from django.shortcuts import render, redirect
from django.contrib import messages
from AdmiSer.models import Servidor, Servicio
import docker
import random
import string

def generar_nombre_contenedor(nombre_servidor):
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{nombre_servidor.lower().replace(' ', '_')}_{sufijo}"

def instalar_servicios_comando(servicios, sistema):
    comandos = []

    if sistema in ["ubuntu", "debian"]:
        comandos.append("apt-get update")

        for servicio in servicios:
            if servicio == "apache2":
                comandos.append("apt-get install -y apache2")
            elif servicio == "nginx":
                comandos.append("apt-get install -y nginx")
            else:
                # Servicio desconocido: solo avisamos que se intentará instalar
                comandos.append(f"apt-get install -y {servicio}")
    
    return " && ".join(comandos)

def asignar_puerto(servicio):
    puertos = {
        'apache2': 80,
        'nginx': 8080
    }
    # Si el servicio no es conocido, asignamos un puerto ficticio 0
    return puertos.get(servicio, 0)

def registrarservidor(request):
    if request.method == "POST":
        nombre_servidor = request.POST["nombre_servidor"]
        ip = request.POST["ip"]
        sistema = request.POST["sistema_operativo"]
        servicios = request.POST.getlist("servicios")

        # El campo de texto con servicio personalizado (si fue marcado)
        otro_servicio = request.POST.get("otro_servicio_input", "").strip()
        if otro_servicio:
            servicios.append(otro_servicio.lower())

        nombre_contenedor = generar_nombre_contenedor(nombre_servidor)

        try:
            client = docker.from_env()
            comandos = instalar_servicios_comando(servicios, sistema)

            if not comandos:
                raise Exception("No se generaron comandos para los servicios.")

            contenedor = client.containers.run(
                image=sistema,
                name=nombre_contenedor,
                command=["bash", "-c", comandos + " && tail -f /dev/null"],
                detach=True,
                tty=True,
            )

            nuevo_servidor = Servidor.objects.create(
                nombre_servidor=nombre_servidor,
                ip=ip,
                sistema_operativo=sistema,
                lista_servicios=",".join(servicios),
                nombre_contenedor=nombre_contenedor,
            )

            for nombre_servicio in servicios:
                Servicio.objects.create(
                    nombre=nombre_servicio,
                    puerto=asignar_puerto(nombre_servicio),
                    servidor=nuevo_servidor,
                    status_servicio='Desconocido'
                )

            messages.success(request, "Servidor registrado y contenedor creado exitosamente.")
            return redirect("AdmiSer:dashboard")

        except docker.errors.ImageNotFound:
            messages.error(request, "Imagen no encontrada para el sistema operativo seleccionado.")
        except Exception as e:
            messages.error(request, f"Error al crear el contenedor: {e}")

        return redirect("AdmiSer:registrarservidor")

    return render(request, "registrarservidor.html")
