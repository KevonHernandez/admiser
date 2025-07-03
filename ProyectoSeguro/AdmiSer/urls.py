from django.urls import path, include
from .views.session import logout
from .views.otp import verificar_otp
from .views.login import login
from .views.registro import registro
from .views.dashboard import accion_servicio, dashboard, listar_servidores, validar_password, verificar_estados_servicios
from .views.registrarservidor import registrar_servidor
from . import views

app_name = 'AdmiSer'

urlpatterns = [
    path('', login, name='home'), 
    path('login', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('registro/', registro, name='registro'),
    path('registrarservidor/', registrar_servidor, name='registrarservidor'),
    path('otp/', verificar_otp, name='verificar_otp'),
    path('logout/', logout, name='logout'),
    path('servicio/<str:accion>/<int:servicio_id>/', accion_servicio, name='accion_servicio'),
    path('servidores/', listar_servidores, name='listar_servidores'),
    path('validar-password/', validar_password, name='validar_password'),
    path('verificar_estados/', verificar_estados_servicios, name='verificar_estados_servicios'),
]



