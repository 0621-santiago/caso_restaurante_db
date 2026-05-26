from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden
from .decorators import tiene_rol


# ─────────────────────────────────────────────────────────────────────────────
# INICIO  (panel por rol)
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def inicio(request):
    context = {}
    if tiene_rol(request.user, 'Administrador'):
        context.update({
            'total_clientes': Cliente.objects.count(),
            'total_empleados': Empleado.objects.count(),
            'total_mesa': Mesa.objects.count(),
            'total_plato': Plato.objects.count(),
            'total_orden': Orden.objects.count(),
            'total_factura': Factura.objects.count(),
            'total_usuarios': User.objects.count(),
        })
    elif tiene_rol(request.user, 'Mesero'):
        context.update({
            'mesas_disponibles': Mesa.objects.filter(estado_mesa='Disponible').count(),
            'mesas_ocupadas': Mesa.objects.filter(estado_mesa='Ocupada').count(),
            'mesas_reservadas': Mesa.objects.filter(estado_mesa='Reservada').count(),
            'ordenes_activas': Orden.objects.filter(estado_orden__in=['Activa', 'En preparación']).count(),
            'total_platos': Plato.objects.filter(disponible=True).count(),
        })
    elif tiene_rol(request.user, 'Cajero'):
        context.update({
            'ordenes_pendientes': Orden.objects.filter(
                factura__isnull=True, estado_orden='Entregada'
            ).count(),
            'total_facturas': Factura.objects.count(),
        })
    return render(request, 'gestion/inicio.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# CLIENTES  — Admin: CRUD | Mesero: solo lectura | Cajero: sin acceso
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_clientes(request):
    es_admin = tiene_rol(request.user, 'Administrador')
    es_mesero = tiene_rol(request.user, 'Mesero')

    if not (es_admin or es_mesero):
        return redirect('acceso_denegado')

    if request.method == 'POST':
        if not es_admin:
            return redirect('acceso_denegado')

        if 'crear' in request.POST:
            Cliente.objects.create(
                nombre=request.POST['nombre'],
                telefono=request.POST['telefono'],
                correo=request.POST['correo'],
            )
            return redirect('lista_clientes')

        if 'editar' in request.POST:
            cliente = get_object_or_404(Cliente, pk=request.POST['id'])
            cliente.nombre = request.POST['nombre']
            cliente.telefono = request.POST['telefono']
            cliente.correo = request.POST['correo']
            cliente.save()
            return redirect('lista_clientes')

        if 'eliminar' in request.POST:
            cliente = get_object_or_404(Cliente, pk=request.POST['id'])
            cliente.delete()
            return redirect('lista_clientes')

    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {
        'clientes': clientes,
        'es_admin': es_admin,
    })


# ─────────────────────────────────────────────────────────────────────────────
# EMPLEADOS  — Solo Administrador
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_empleados(request):
    if not tiene_rol(request.user, 'Administrador'):
        return redirect('acceso_denegado')

    if request.method == 'POST' and 'crear' in request.POST:
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            cargo=request.POST['cargo'],
            telefono=request.POST['telefono'],
            correo=request.POST['correo'],
        )
        return redirect('lista_empleados')

    if request.method == 'POST' and 'editar' in request.POST:
        empleado = get_object_or_404(Empleado, pk=request.POST['id'])
        empleado.nombre = request.POST['nombre']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST['telefono']
        empleado.correo = request.POST['correo']
        empleado.save()
        return redirect('lista_empleados')

    if request.method == 'POST' and 'eliminar' in request.POST:
        empleado = get_object_or_404(Empleado, pk=request.POST['id'])
        empleado.delete()
        return redirect('lista_empleados')

    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})


# ─────────────────────────────────────────────────────────────────────────────
# MESAS  — Admin: CRUD | Mesero: solo lectura | Cajero: solo lectura
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_mesas(request):
    es_admin = tiene_rol(request.user, 'Administrador')
    es_mesero = tiene_rol(request.user, 'Mesero')
    es_cajero = tiene_rol(request.user, 'Cajero')

    if not (es_admin or es_mesero or es_cajero):
        return redirect('acceso_denegado')

    if request.method == 'POST':
        if not es_admin:
            return redirect('acceso_denegado')

        if 'crear' in request.POST:
            num_mesa = int(request.POST.get('numero_mesa', 0))
            capacidad = int(request.POST.get('capacidad', 0))
            if num_mesa < 1 or capacidad < 1:
                return render(request, 'gestion/mesas.html', {
                    'mesas': Mesa.objects.all(),
                    'error': 'El número de mesa y la capacidad deben ser mayores a 0.',
                    'es_admin': es_admin,
                })
            Mesa.objects.create(
                numero_mesa=num_mesa,
                capacidad=capacidad,
                estado_mesa=request.POST['estado_mesa'],
            )
            return redirect('lista_mesas')

        if 'editar' in request.POST:
            num_mesa = int(request.POST.get('numero_mesa', 0))
            capacidad = int(request.POST.get('capacidad', 0))
            if num_mesa < 1 or capacidad < 1:
                return render(request, 'gestion/mesas.html', {
                    'mesas': Mesa.objects.all(),
                    'error': 'El número de mesa y la capacidad deben ser mayores a 0.',
                    'es_admin': es_admin,
                })
            mesa = get_object_or_404(Mesa, pk=request.POST['id'])
            mesa.numero_mesa = num_mesa
            mesa.capacidad = capacidad
            mesa.estado_mesa = request.POST['estado_mesa']
            mesa.save()
            return redirect('lista_mesas')

        if 'eliminar' in request.POST:
            mesa = get_object_or_404(Mesa, pk=request.POST['id'])
            mesa.delete()
            return redirect('lista_mesas')

    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {
        'mesas': mesas,
        'es_admin': es_admin,
    })


# ─────────────────────────────────────────────────────────────────────────────
# PLATOS  — Admin: CRUD | Mesero: solo lectura (ver menú) | Cajero: sin acceso
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_platos(request):
    es_admin = tiene_rol(request.user, 'Administrador')
    es_mesero = tiene_rol(request.user, 'Mesero')

    if not (es_admin or es_mesero):
        return redirect('acceso_denegado')

    if request.method == 'POST':
        if not es_admin:
            return redirect('acceso_denegado')

        if 'crear' in request.POST:
            Plato.objects.create(
                nombre_plato=request.POST['nombre_plato'],
                descripcion=request.POST['descripcion'],
                precio=request.POST['precio'],
                categoria=request.POST['categoria'],
                disponible='disponible' in request.POST,
            )
            return redirect('lista_platos')

        if 'editar' in request.POST:
            plato = get_object_or_404(Plato, pk=request.POST['id'])
            plato.nombre_plato = request.POST['nombre_plato']
            plato.descripcion = request.POST['descripcion']
            plato.precio = request.POST['precio']
            plato.categoria = request.POST['categoria']
            plato.disponible = 'disponible' in request.POST
            plato.save()
            return redirect('lista_platos')

        if 'eliminar' in request.POST:
            plato = get_object_or_404(Plato, pk=request.POST['id'])
            plato.delete()
            return redirect('lista_platos')

    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {
        'platos': platos,
        'es_admin': es_admin,
    })


# ─────────────────────────────────────────────────────────────────────────────
# ORDENES  — Admin: CRUD | Mesero: crear/leer/actualizar | Cajero: solo lectura
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_ordenes(request):
    es_admin = tiene_rol(request.user, 'Administrador')
    es_mesero = tiene_rol(request.user, 'Mesero')
    es_cajero = tiene_rol(request.user, 'Cajero')

    if not (es_admin or es_mesero or es_cajero):
        return redirect('acceso_denegado')

    if request.method == 'POST':
        if not (es_admin or es_mesero):
            return redirect('acceso_denegado')

        if 'crear' in request.POST:
            Orden.objects.create(
                cliente_id=request.POST['cliente_id'],
                empleado_id=request.POST['empleado_id'],
                mesa_id=request.POST['mesa_id'],
                estado_orden=request.POST['estado_orden'],
            )
            return redirect('lista_ordenes')

        if 'editar' in request.POST:
            orden = get_object_or_404(Orden, pk=request.POST['id'])
            orden.cliente_id = request.POST['cliente_id']
            orden.empleado_id = request.POST['empleado_id']
            orden.mesa_id = request.POST['mesa_id']
            orden.estado_orden = request.POST['estado_orden']
            orden.save()
            return redirect('lista_ordenes')

        if 'eliminar' in request.POST:
            if not es_admin:
                return redirect('acceso_denegado')
            orden = get_object_or_404(Orden, pk=request.POST['id'])
            orden.delete()
            return redirect('lista_ordenes')

        if 'agregar_detalle' in request.POST:
            orden = get_object_or_404(Orden, pk=request.POST['orden_id'])
            plato = get_object_or_404(Plato, pk=request.POST['plato_id'])
            cantidad = int(request.POST['cantidad'])
            DetalleOrden.objects.create(orden=orden, plato=plato, cantidad=cantidad)
            return redirect('lista_ordenes')

    # Cajero solo ve órdenes Entregadas (pendientes de cobro)
    if es_cajero and not es_admin:
        ordenes = Orden.objects.filter(estado_orden='Entregada')
    else:
        ordenes = Orden.objects.all()

    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    mesas = Mesa.objects.all()
    platos = Plato.objects.filter(disponible=True)
    return render(request, 'gestion/ordenes.html', {
        'ordenes': ordenes,
        'clientes': clientes,
        'empleados': empleados,
        'mesas': mesas,
        'platos': platos,
        'es_admin': es_admin,
        'es_mesero': es_mesero,
        'es_cajero': es_cajero,
    })


# ─────────────────────────────────────────────────────────────────────────────
# FACTURAS  — Admin: CRUD | Cajero: crear/leer | Mesero: sin acceso
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_facturas(request):
    es_admin = tiene_rol(request.user, 'Administrador')
    es_cajero = tiene_rol(request.user, 'Cajero')

    if not (es_admin or es_cajero):
        return redirect('acceso_denegado')

    if request.method == 'POST':
        if 'crear' in request.POST:
            orden = get_object_or_404(Orden, pk=request.POST['orden_id'])
            subtotal = orden.total
            impuesto = subtotal * Decimal('0.19')
            total_factura = subtotal + impuesto
            Factura.objects.create(
                orden=orden,
                subtotal=subtotal,
                impuesto=impuesto,
                total_factura=total_factura,
                metodo_pago=request.POST['metodo_pago'],
            )
            # Cerrar mesa al facturar
            if orden.mesa:
                orden.mesa.estado_mesa = 'Disponible'
                orden.mesa.save()
            orden.estado_orden = 'Facturada'
            orden.save()
            return redirect('lista_facturas')

        if 'editar' in request.POST:
            if not es_admin:
                return redirect('acceso_denegado')
            factura = get_object_or_404(Factura, pk=request.POST['id'])
            factura.metodo_pago = request.POST['metodo_pago']
            factura.save()
            return redirect('lista_facturas')

        if 'eliminar' in request.POST:
            if not es_admin:
                return redirect('acceso_denegado')
            factura = get_object_or_404(Factura, pk=request.POST['id'])
            factura.delete()
            return redirect('lista_facturas')

    facturas = Factura.objects.all()
    ordenes_sin_factura = Orden.objects.filter(factura__isnull=True, estado_orden='Entregada')
    return render(request, 'gestion/facturas.html', {
        'facturas': facturas,
        'ordenes': ordenes_sin_factura,
        'es_admin': es_admin,
        'es_cajero': es_cajero,
    })


# ─────────────────────────────────────────────────────────────────────────────
# USUARIOS  — Solo Administrador
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def lista_usuarios(request):
    if not tiene_rol(request.user, 'Administrador'):
        return redirect('acceso_denegado')

    roles_disponibles = Group.objects.all()

    if request.method == 'POST' and 'crear' in request.POST:
        username = request.POST['username'].strip()
        password = request.POST['password']
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        rol_id = request.POST.get('rol_id')

        if User.objects.filter(username=username).exists():
            usuarios = User.objects.all().prefetch_related('groups')
            return render(request, 'gestion/usuarios.html', {
                'usuarios': usuarios,
                'roles': roles_disponibles,
                'error': f'El nombre de usuario «{username}» ya existe.',
            })

        nuevo = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        if rol_id:
            grupo = get_object_or_404(Group, pk=rol_id)
            nuevo.groups.set([grupo])
        return redirect('lista_usuarios')

    if request.method == 'POST' and 'asignar_rol' in request.POST:
        usuario = get_object_or_404(User, pk=request.POST['user_id'])
        rol_id = request.POST.get('rol_id')
        if rol_id:
            grupo = get_object_or_404(Group, pk=rol_id)
            usuario.groups.set([grupo])
        else:
            usuario.groups.clear()
        return redirect('lista_usuarios')

    if request.method == 'POST' and 'eliminar' in request.POST:
        usuario = get_object_or_404(User, pk=request.POST['user_id'])
        if usuario != request.user and not usuario.is_superuser:
            usuario.delete()
        return redirect('lista_usuarios')

    usuarios = User.objects.all().prefetch_related('groups').order_by('username')
    return render(request, 'gestion/usuarios.html', {
        'usuarios': usuarios,
        'roles': roles_disponibles,
    })


# ─────────────────────────────────────────────────────────────────────────────
# ACCESO DENEGADO
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def acceso_denegado(request):
    return render(request, 'gestion/acceso_denegado.html', status=403)
