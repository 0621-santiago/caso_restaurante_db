# Restaurante Pasta La Vista — Sistema de Gestión

## Sistema de Roles

El sistema maneja tres roles a través de los **Groups** de Django:

| Rol           | Acceso                                                                 |
|---------------|------------------------------------------------------------------------|
| Administrador | CRUD completo, gestión de usuarios, roles y reportes                   |
| Mesero        | Leer clientes/mesas/menú; crear y actualizar órdenes                   |
| Cajero        | Ver órdenes entregadas; generar y consultar facturas; ver mesas        |

---

## Flujo de Ramas Git

```
main
 └── feature/login-crud        ← CRUD + login ya implementados
        │
        ▼  (merge → develop)
      develop
        │
        ▼  (crear desde develop)
      feature/roles-manager     ← implementación de roles (esta rama)
        │
        ▼  (merge → develop)
      develop
```

### Comandos paso a paso

```bash
# 1. Fusionar feature/login-crud → develop
git checkout develop
git merge feature/login-crud --no-ff -m "merge: integrar login y CRUD base"

# 2. Crear la rama de roles desde develop
git checkout -b feature/roles-manager

# 3. Trabajar en la rama y hacer commits
git add .
git commit -m "feat: agregar sistema de roles (Administrador, Mesero, Cajero)"

# 4. Fusionar feature/roles-manager → develop cuando esté lista
git checkout develop
git merge feature/roles-manager --no-ff -m "merge: integrar gestión de roles y permisos"
```

---

## Instalación y primeros pasos

```bash
# Aplicar migraciones (crea los 3 grupos automáticamente)
python manage.py migrate

# Crear superusuario administrador
python manage.py createsuperuser

# Desde el panel /usuarios/ (logueado como admin), crear usuarios
# y asignar el rol correspondiente.
```

---

## Archivos nuevos / modificados

| Archivo                                      | Descripción                          |
|----------------------------------------------|--------------------------------------|
| `gestion/decorators.py`                      | `tiene_rol()` y `@rol_requerido()`   |
| `gestion/context_processors.py`              | Inyecta `{{ rol_usuario }}` globalmente |
| `gestion/migrations/0002_create_roles.py`    | Crea los 3 grupos en la BD           |
| `gestion/views.py`                           | Todas las vistas con control de rol  |
| `gestion/urls.py`                            | Añade `/usuarios/` y `/acceso-denegado/` |
| `config/settings.py`                         | Registra el context processor        |
| `gestion/templates/gestion/base.html`        | Sidebar dinámico por rol             |
| `gestion/templates/gestion/inicio.html`      | Dashboard por rol                    |
| `gestion/templates/gestion/usuarios.html`    | Gestión de usuarios (solo admin)     |
| `gestion/templates/gestion/acceso_denegado.html` | Página 403 personalizada         |
| `gestion/templates/gestion/clientes.html`    | Oculta CRUD si no es admin           |
| `gestion/templates/gestion/mesas.html`       | Oculta CRUD si no es admin           |
| `gestion/templates/gestion/platos.html`      | Oculta CRUD si no es admin           |
| `gestion/templates/gestion/ordenes.html`     | Adapta botones por rol               |
| `gestion/templates/gestion/facturas.html`    | Adapta botones por rol               |
