from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('clientes/', views.Lista_clientes, name='Lista_clientes'),
    path('empleados/', views.Lista_empleados, name='Lista_empleados'),
    path('mesas/', views.Lista_mesas, name='Lista_mesas'),
    path('platos/', views.Lista_platos, name='Lista_platos'),
    path('ordenes/', views.Lista_ordenes, name='Lista_ordenes'),
    path('facturas/', views.Lista_facturas, name='Lista_facturas'),
]

