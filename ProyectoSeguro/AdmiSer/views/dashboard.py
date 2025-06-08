from django.shortcuts import render, redirect

from AdmiSer.decorators import sesion_requerida
from ..views.session import limpiar_sesion_login

@sesion_requerida
def dashboard(request):
    # logica para el boton cerrar sesion
    if request.method == 'POST' and request.POST.get('cerrar_sesion') == 'true':
        # Limpiar la sesión
        limpiar_sesion_login(request)

        return redirect('AdmiSer:login')
    

    return render(request, 'dashboard.html', {})