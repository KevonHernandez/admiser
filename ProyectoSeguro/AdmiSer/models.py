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
    nombre = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    puerto = models.PositiveIntegerField(default=22)
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # cifrada
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='Desconocido')

    def __str__(self):
        return f'{self.nombre} en {self.servidor.nombre}'