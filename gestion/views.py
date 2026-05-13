from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden


@login_required
def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesa': Mesa.objects.count(),
        'total_plato': Plato.objects.count(),
        'total_orden': Orden.objects.count(),
        'total_factura': Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)


@login_required
def lista_clientes(request):
    # CREAR
    if request.method == 'POST' and 'crear' in request.POST:
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            telefono=request.POST['telefono'],
            correo=request.POST['correo'],
        )
        return redirect('lista_clientes')

    # EDITAR
    if request.method == 'POST' and 'editar' in request.POST:
        cliente = get_object_or_404(Cliente, pk=request.POST['id'])
        cliente.nombre = request.POST['nombre']
        cliente.telefono = request.POST['telefono']
        cliente.correo = request.POST['correo']
        cliente.save()
        return redirect('lista_clientes')

    # ELIMINAR
    if request.method == 'POST' and 'eliminar' in request.POST:
        cliente = get_object_or_404(Cliente, pk=request.POST['id'])
        cliente.delete()
        return redirect('lista_clientes')

    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})


@login_required
def lista_empleados(request):
    # CREAR
    if request.method == 'POST' and 'crear' in request.POST:
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            cargo=request.POST['cargo'],
            telefono=request.POST['telefono'],
            correo=request.POST['correo'],
        )
        return redirect('lista_empleados')

    # EDITAR
    if request.method == 'POST' and 'editar' in request.POST:
        empleado = get_object_or_404(Empleado, pk=request.POST['id'])
        empleado.nombre = request.POST['nombre']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST['telefono']
        empleado.correo = request.POST['correo']
        empleado.save()
        return redirect('lista_empleados')

    # ELIMINAR
    if request.method == 'POST' and 'eliminar' in request.POST:
        empleado = get_object_or_404(Empleado, pk=request.POST['id'])
        empleado.delete()
        return redirect('lista_empleados')

    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})


@login_required
def lista_mesas(request):
    if request.method == 'POST' and 'crear' in request.POST:
        Mesa.objects.create(
            numero_mesa=request.POST['numero_mesa'],
            capacidad=request.POST['capacidad'],
            estado_mesa=request.POST['estado_mesa'],
        )
        return redirect('lista_mesas')

    if request.method == 'POST' and 'editar' in request.POST:
        mesa = get_object_or_404(Mesa, pk=request.POST['id'])
        mesa.numero_mesa = request.POST['numero_mesa']
        mesa.capacidad = request.POST['capacidad']
        mesa.estado_mesa = request.POST['estado_mesa']
        mesa.save()
        return redirect('lista_mesas')

    if request.method == 'POST' and 'eliminar' in request.POST:
        mesa = get_object_or_404(Mesa, pk=request.POST['id'])
        mesa.delete()
        return redirect('lista_mesas')

    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})


@login_required
def lista_platos(request):
    if request.method == 'POST' and 'crear' in request.POST:
        Plato.objects.create(
            nombre_plato=request.POST['nombre_plato'],
            descripcion=request.POST['descripcion'],
            precio=request.POST['precio'],
            categoria=request.POST['categoria'],
            disponible='disponible' in request.POST,
        )
        return redirect('lista_platos')

    if request.method == 'POST' and 'editar' in request.POST:
        plato = get_object_or_404(Plato, pk=request.POST['id'])
        plato.nombre_plato = request.POST['nombre_plato']
        plato.descripcion = request.POST['descripcion']
        plato.precio = request.POST['precio']
        plato.categoria = request.POST['categoria']
        plato.disponible = 'disponible' in request.POST
        plato.save()
        return redirect('lista_platos')

    if request.method == 'POST' and 'eliminar' in request.POST:
        plato = get_object_or_404(Plato, pk=request.POST['id'])
        plato.delete()
        return redirect('lista_platos')

    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})


@login_required
def lista_ordenes(request):
    if request.method == 'POST' and 'crear' in request.POST:
        Orden.objects.create(
            cliente_id=request.POST['cliente_id'],
            empleado_id=request.POST['empleado_id'],
            mesa_id=request.POST['mesa_id'],
            estado_orden=request.POST['estado_orden'],
        )
        return redirect('lista_ordenes')

    if request.method == 'POST' and 'editar' in request.POST:
        orden = get_object_or_404(Orden, pk=request.POST['id'])
        orden.cliente_id = request.POST['cliente_id']
        orden.empleado_id = request.POST['empleado_id']
        orden.mesa_id = request.POST['mesa_id']
        orden.estado_orden = request.POST['estado_orden']
        orden.save()
        return redirect('lista_ordenes')

    if request.method == 'POST' and 'eliminar' in request.POST:
        orden = get_object_or_404(Orden, pk=request.POST['id'])
        orden.delete()
        return redirect('lista_ordenes')

    # AGREGAR DETALLE
    if request.method == 'POST' and 'agregar_detalle' in request.POST:
        orden = get_object_or_404(Orden, pk=request.POST['orden_id'])
        plato = get_object_or_404(Plato, pk=request.POST['plato_id'])
        cantidad = int(request.POST['cantidad'])
        DetalleOrden.objects.create(
            orden=orden,
            plato=plato,
            cantidad=cantidad,
        )
        return redirect('lista_ordenes')

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
    })


@login_required
def lista_facturas(request):
    if request.method == 'POST' and 'crear' in request.POST:
        orden = get_object_or_404(Orden, pk=request.POST['orden_id'])
        subtotal = orden.total
        impuesto = subtotal * Decimal('0.19')  # IVA 19%
        total_factura = subtotal + impuesto
        Factura.objects.create(
            orden=orden,
            subtotal=subtotal,
            impuesto=impuesto,
            total_factura=total_factura,
            metodo_pago=request.POST['metodo_pago'],
        )
        return redirect('lista_facturas')

    if request.method == 'POST' and 'editar' in request.POST:
        factura = get_object_or_404(Factura, pk=request.POST['id'])
        factura.metodo_pago = request.POST['metodo_pago']
        factura.save()
        return redirect('lista_facturas')

    if request.method == 'POST' and 'eliminar' in request.POST:
        factura = get_object_or_404(Factura, pk=request.POST['id'])
        factura.delete()
        return redirect('lista_facturas')

    facturas = Factura.objects.all()
    ordenes_sin_factura = Orden.objects.filter(factura__isnull=True)
    return render(request, 'gestion/facturas.html', {
        'facturas': facturas,
        'ordenes': ordenes_sin_factura,
    })
