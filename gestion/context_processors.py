def rol_usuario(request):
    """
    Inyecta el rol del usuario autenticado en el contexto de cada template.
    Disponible como {{ rol_usuario }} en cualquier plantilla.
    """
    if request.user.is_authenticated:
        grupos = list(request.user.groups.values_list('name', flat=True))
        if request.user.is_superuser or 'Administrador' in grupos:
            rol = 'Administrador'
        elif 'Mesero' in grupos:
            rol = 'Mesero'
        elif 'Cajero' in grupos:
            rol = 'Cajero'
        else:
            rol = 'Sin rol'
        return {
            'rol_usuario': rol,
            'usuario_nombre': request.user.get_full_name() or request.user.username,
        }
    return {'rol_usuario': None, 'usuario_nombre': ''}
