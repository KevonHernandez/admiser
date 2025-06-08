from django.shortcuts import redirect

def sesion_requerida(vista):
    def interna(request, *args, **kargs):
        # Verificar si el usuario está autenticado por la variable 'ha_iniciado_sesion'
        if not request.session.get('ha_iniciado_sesion', False):
            return redirect('AdmiSer:login')  # Redirigir a la página de login
        return vista(request, *args, **kargs)
    return interna
