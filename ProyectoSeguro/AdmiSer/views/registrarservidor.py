import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Servidor
from ..forms import ServidorForm, ServicioForm
from ..utils.hasheo import hashear_password, convertir_binario_texto64, convertir_texto64_binario, password_valido, generar_salt
import paramiko

def probar_conexion_ssh(ip, usuario, password, puerto=22):
    """
    Prueba la conexión SSH a un servidor.
    Args:
        ip (str): Dirección IP del servidor.
        usuario (str): Nombre de usuario para la conexión SSH.
        password (str): Contraseña para la conexión SSH.
        puerto (int, optional): Puerto SSH. Por defecto es 22.
    Returns:
        tuple: (bool, str) donde el primer elemento indica si la conexión fue exitosa
        y el segundo elemento es un mensaje de error si la conexión falló.
    """
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
    
def registrar_servidor(request):
    """
    Vista para registrar un nuevo servidor.
    Permite ingresar la IP, usuario, contraseña y una descripción opcional.
    Valida la conexión SSH antes de guardar el servidor en la base de datos.
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
    Returns:    
        HttpResponse: Renderiza el formulario de registro de servidor o redirige al dashboard
        si el registro es exitoso.
    """
    if request.method == 'POST':
        form = ServidorForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']
            descripcion = form.cleaned_data.get('descripcion', '')

            # Probar conexión SSH
            conectado, error = probar_conexion_ssh(ip, usuario, password)
            if not conectado:
                messages.error(request, f"Conexión SSH fallida: {error}")
                return redirect('AdmiSer:registrarservidor')
            
            nuevo_servidor = Servidor(
                ip=ip,
                usuario=usuario,
                password=password,
                descripcion=descripcion
            )

            nuevo_servidor.save()

            messages.success(request, 'Servidor registrado exitosamente.')
            return redirect('AdmiSer:dashboard')
    else:
        form = ServidorForm()
    
    return render(request, 'registrar_servidor.html', {'form': form})

def agregar_servicio(request, servidor_id):
    """
    Vista para agregar un nuevo servicio a un servidor existente.
    Permite ingresar el nombre del servicio y lo guarda en la base de datos.
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        servidor_id (int): ID del servidor al que se le agregará el servicio.
    Returns:
        HttpResponse: Renderiza el formulario de agregar servicio o redirige al dashboard
        si el servicio es agregado exitosamente.
    """

    servidor = get_object_or_404(Servidor, id=servidor_id)

    if not request.session.get('password_validada', False):
        messages.error(request, "Debes validar tu contraseña antes de realizar esta acción.")
        return redirect('AdmiSer:validar_password')  # Crea esta url/vista o muestra modal

    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.servidor = servidor
            servicio.save()
            messages.success(request, "Servicio agregado correctamente.")
            return redirect('AdmiSer:dashboard')
    else:
        form = ServicioForm()
    return render(request, 'agregar_servicio.html', {'form': form, 'servidor': servidor})


def validar_password_sesion(request, password_ingresada):
    """ 
    Verifica si la contraseña ingresada por el usuario es válida
    comparándola con el hash y salt guardados en la sesión. 
    Args:
        request (HttpRequest): La solicitud HTTP del usuario.
        password_ingresada (str): La contraseña ingresada por el usuario.
    Returns:
        bool: True si la contraseña es válida, False en caso contrario.
    """

    hash_guardado = request.session.get('hash_password')
    salt_guardado64 = request.session.get('salt')

    if not hash_guardado or not salt_guardado64:
        return False

    salt_guardado = convertir_texto64_binario(salt_guardado64)

    return password_valido(password_ingresada, hash_guardado, salt_guardado)
