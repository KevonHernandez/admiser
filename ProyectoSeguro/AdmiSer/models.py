from django.db import models
from django.utils import timezone
import uuid

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=255)
    nick = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    salt = models.TextField() 
    
    def __str__(self):
        return self.nick
    
class OTPToken(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    session_id = models.UUIDField(default=uuid.uuid4)

    def is_valid(self):
        return not self.used and (timezone.now() - self.created_at).total_seconds() < 180

class Servidor(models.Model):
    administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servidores')
    nombre = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    puerto = models.PositiveIntegerField()
    sistema_operativo = models.CharField(max_length=100)
    status_servidor = models.CharField(max_length=50, default='Desconocido')  # ejemplo: Activo, Inactivo
    descripcion = models.TextField(blank=True, null=True)  # opcional

    def _str_(self):
        return f"{self.nombre} ({self.ip}:{self.puerto})"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # opcional
    puerto = models.PositiveIntegerField()
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name='servicios')
    status_servicio = models.CharField(max_length=50, default='Desconocido')  # ejemplo: Activo, Inactivo

    def _str_(self):
        return f"{self.nombre} en {self.servidor.nombre}"