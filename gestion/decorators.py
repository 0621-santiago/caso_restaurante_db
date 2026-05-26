from functools import wraps
from django.shortcuts import redirect
from django.conf import settings


def tiene_rol(user, *roles):
    """Verifica si el usuario tiene alguno de los roles indicados."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=roles).exists()


def rol_requerido(*roles):
    """Decorador que restringe el acceso a una vista según el rol del usuario."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            return redirect('acceso_denegado')
        return _wrapped
    return decorator
