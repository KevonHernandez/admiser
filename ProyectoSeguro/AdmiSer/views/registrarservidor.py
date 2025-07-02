# views.py (añade estas vistas)
from django.shortcuts import render, redirect, get_object_or_404
from AdmiSer.models import Servidor
from ..forms import ServidorForm, ServicioForm
import paramiko
from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import ServidorForm




def registrar_servidor(request):
    if request.method == 'POST':
        form = ServidorForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            usuario = form.cleaned_data['usuario']  
            password = form.cleaned_data['password'] 

            conectado, error = probar_conexion_ssh(ip, usuario, password)
            if conectado:
                form.save()
                messages.success(request, "Servidor registrado y conexión SSH exitosa.")
                return redirect('AdmiSer:dashboard')  # O donde quieras
            else:
                messages.error(request, f"No se pudo conectar vía SSH: {error}")

    else:
        form = ServidorForm()
    return render(request, 'registrar_servidor.html', {'form': form})

# Agregar servicio a un servidor (desde dashboard, ajax o form simple)
def agregar_servicio(request, servidor_id):
    servidor = get_object_or_404(Servidor, id=servidor_id)
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.servidor = servidor
            servicio.save()
            return redirect('AdmiSer:dashboard')
    else:
        form = ServicioForm()
    return render(request, 'agregar_servicio.html', {'form': form, 'servidor': servidor})

def probar_conexion_ssh(ip, usuario, password, puerto=22):
    try:
        cliente = paramiko.SSHClient()
        cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente.connect(hostname=ip, username=usuario, password=password, port=puerto, timeout=5)
        cliente.close()
        return True, None
    except paramiko.AuthenticationException:
        return False, "Error de autenticación: Usuario o contraseña incorrectos."
    except paramiko.SSHException as e:
        return False, f"Error en SSH: {str(e)}"
    except Exception as e:
        return False, f"No se pudo conectar: {str(e)}"
