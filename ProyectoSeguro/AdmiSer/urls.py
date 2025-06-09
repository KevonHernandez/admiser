from django.urls import path, include
from .views.session import logout
from .views.otp import verificar_otp
from .views.login import login
from .views.registro import registro
from .views.dashboard import dashboard
from .views.registrarservidor import registrarservidor

app_name = 'AdmiSer'

urlpatterns = [
    path('', login, name='home'), 
    path('login', login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('registro/', registro, name='registro'),
    path('registrarservidor/', registrarservidor, name='registrarservidor'),
    path('otp/', verificar_otp, name='verificar_otp'),
    path('logout/', logout, name='logout'),

    

]



