import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from .models import Producto, Categoria, Deuda, Encargo, Usuario
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, timedelta
from .forms import EncargoForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def inicio(request):
    ordenar = request.GET.get('ordenar', 'destacado')
    categoria_id = request.GET.get('categoria', None)
    query = request.GET.get('q', '')
    
    productos = Producto.objects.filter(enabled=True)
    
    if query != '':
        productos = productos.filter(nombre__icontains=query)


    if ordenar == 'menor-precio':
        productos = productos.order_by('precio')
    elif ordenar == 'mayor-precio':
        productos = productos.order_by('-precio')
    
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    username = request.user.username if request.user.is_authenticated else None

    return render(request, 'inicio/inicio.html', {
        'productos': productos, 
        'ordenar': ordenar, 
        'categorias': categorias, 
        'categoria_actual': categoria_id,
        'query': query,
        'username': username
        })

def gestionar_productos(request, producto_id=None):
    producto = None
    if producto_id:
        producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            if producto:
                producto.delete()
                messages.success(request, 'Producto eliminado exitosamente.')
            return redirect('inicio')

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        enabled = request.POST.get('enabled') == 'on'

        if not nombre or not precio or not stock:
            messages.error(request, 'Complete todos los campos.')
            categorias = Categoria.objects.all()
            return render(request, 'gestionar_productos.html', {
                'producto': producto,
                'categorias': categorias,
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'stock': stock,
                'enabled': enabled,
            })
        
        if producto:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.stock = stock
            producto.enabled = enabled
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente.')
        return redirect('gestionar_productos', producto_id=producto.id if producto else None)
    
    return render(request, 'gestionar_productos.html', {
        'producto': producto
    })

def add_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        categoria_id = request.POST.get('categoria')
        enabled = request.POST.get('enabled') == 'on'
        imagen = request.FILES.get('imagen')

        if not imagen or not nombre or not precio or not stock:
            messages.error(request, 'Complete todos los campos.')
            categorias = Categoria.objects.all()
            return render(request, 'add_producto.html', {
                'categorias': categorias,
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'stock': stock,
                'categoria_id': categoria_id,
                'enabled': enabled,
            })
        
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            enabled=enabled,
            imagen=imagen
        )
        messages.success(request, 'Producto creado exitosamente.')
        return redirect('inicio')
    
    categorias = Categoria.objects.all()
    return render(request, 'add_producto.html', {
        'categorias': categorias
    })

def deudas(request):
    ruta = request.path.split('/')
    if not request.user.is_authenticated:
        return redirect('login')
    if ruta[2] == 'admin':
        if not request.user.is_staff:
            return redirect('deudas')
    
    busqueda = request.GET.get('q', '')
    ordenarPor = request.GET.get('ordenarPor', 'fecha-agregado')

    if ruta[2] == 'admin':
        deudas = Deuda.objects.all()
        productos = Producto.objects.all()
        usuarios = User.objects.all()
    else:
        deudas = request.user.deudas.all()
        productos = None
        usuarios = None

    if busqueda != '':
        if ruta[2] == 'admin':
            deudas = deudas.filter(usuario__username__icontains=busqueda)
        else:
            deudas = deudas.filter(productos__nombre__icontains=busqueda)
    
    if ordenarPor == 'fecha-agregado':
        deudas = deudas.order_by('-fecha')
    elif ordenarPor == 'fecha-antiguo':
        deudas = deudas.order_by('fecha')
    elif ordenarPor == 'monto-mayor':
        deudas = deudas.order_by('-monto_total')
    elif ordenarPor == 'monto-menor':
        deudas = deudas.order_by('monto_total')
    
    if ruta[2] == 'admin':
        titulo = 'Deudas de los usuarios'
        descripcion = 'Aquí puedes ver todas las deudas de los usuarios.'
    else:
        titulo = 'Mis deudas'
        descripcion = 'Aquí puedes ver todas tus deudas pendientes.'

    return render(request, 'deudas.html', {
        'username': request.user.username,
        'is_admin': request.user.is_staff,
        'mostrarAdmin': ruta[2] == 'admin',
        'mostrar_agregar_deuda': not ("admin/ver" in request.path),
        'mostrar_filtro': True,
        'deudas': deudas,
        'busqueda': busqueda,
        'ordenarPor': ordenarPor,
        'titulo': titulo,
        'descripcion': descripcion,
        'productos': productos,
        'usuarios': usuarios
    })

def ver_deuda(request, id):
    if not request.user.is_authenticated:
        return redirect('inicio')
    elif not request.user.is_staff and not Deuda.objects.get(pk=id).usuario == request.user:
        return redirect('deudas')
    
    mostrarAdmin = request.user.is_staff and request.path.split('/')[2] == 'admin'
    if mostrarAdmin:
        titulo = 'Detalles de la deuda'
        descripcion = 'Aquí puedes ver los detalles de la deuda.'
    else:
        titulo = 'Detalles de tu deuda'
        descripcion = 'Aquí puedes ver los detalles de tu deuda.'
    return render(request, 'deudas.html', {
        'username': request.user.username,
        'is_admin': request.user.is_staff,
        'mostrarAdmin': mostrarAdmin,
        'mostrar_filtro': False,
        'productos': Producto.objects.all(),
        'deuda': Deuda.objects.get(pk=id),
        'titulo': titulo,
        'descripcion': descripcion
    })
def guardar_deuda(request):
    if request.user.is_staff and request.method == 'POST':
        usuario_id = request.POST.get('deuda-usuario')
        productos_json = request.POST.get('productos_json')
        deuda_pagada = request.POST.get('deuda-pagada') == 'on'
        if usuario_id == "-1" or not productos_json:
            messages.error(request, 'Complete todos los campos.')
            return redirect('deudas_admin')

        productos_dict = json.loads(productos_json)  # Convertir el JSON a un diccionario

        deuda = Deuda.objects.create(usuario=User.objects.get(pk=usuario_id))

        productos_seleccionados = Producto.objects.filter(pk__in=productos_dict.keys())
        deuda.productos.add(*productos_seleccionados)
        deuda.cantidad_productos = productos_dict
        deuda.pagado = deuda_pagada

        # Calcular el monto total
        total = 0
        for producto_id, cantidad in productos_dict.items():
            producto = Producto.objects.get(pk=producto_id)
            total += producto.precio * cantidad

        deuda.monto_total = total
        deuda.save()

    return redirect('deudas_admin')

def modificar_deuda(request):
    if request.user.is_staff and request.method == 'POST':
        deuda_id = request.POST.get('deuda-id')
        productos_json = request.POST.get('productos_json')
        deuda_pagada = request.POST.get('deuda-pagada') == 'on'
        print(deuda_id, productos_json, deuda_pagada)
        if not deuda_id or not productos_json:
            messages.error(request, 'Complete todos los campos.')
            return redirect('deudas_admin')

        deuda = Deuda.objects.get(pk=deuda_id)
        productos_dict = json.loads(productos_json)  # Convertir el JSON a un diccionario

        productos_seleccionados = Producto.objects.filter(pk__in=productos_dict.keys())
        deuda.productos.set(productos_seleccionados)
        deuda.cantidad_productos = productos_dict
        deuda.pagado = deuda_pagada

        # Calcular el monto total
        total = 0
        for producto_id, cantidad in productos_dict.items():
            producto = Producto.objects.get(pk=producto_id)
            total += producto.precio * cantidad

        deuda.monto_total = total
        deuda.save()
    
    return redirect('deudas_admin')


MAX_ATTEMPTS = 6
BLOCK_TIME = 10

def login(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    failed_attempts = request.session.get('failed_attempts', 0)
    block_time = request.session.get('block_time', None)
    if block_time:
        block_time = parse_datetime(block_time)

    if failed_attempts >= MAX_ATTEMPTS and block_time:
        if now() < block_time:
            remaining_time = block_time - now()
            minutes, seconds = divmod(remaining_time.seconds, 60)
            messages.error(
                request, f"Has alcanzado el máximo de intentos fallidos. Intenta nuevamente en {minutes} minutos y {seconds} segundos."
            )
            return render(request, 'login.html', {
                'failed_attempts': failed_attempts,
                'remaining_time': remaining_time,
            })
        else:
            request.session['failed_attempts'] = 0
            request.session['block_time'] = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['failed_attempts'] = 0
            request.session['block_time'] = None
            auth_login(request, user)
            return redirect('inicio')
        else:
            if failed_attempts < MAX_ATTEMPTS:
                request.session['failed_attempts'] = failed_attempts + 1
                messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')
            
            if request.session['failed_attempts'] >= MAX_ATTEMPTS:
                block_time = now() + timedelta(seconds=BLOCK_TIME)
                request.session['block_time'] = block_time.isoformat()
                messages.error(request, 'Has alcanzado el máximo de intentos fallidos. Tu cuenta está bloqueada por 5 minutos.')

    remaining_attempts = max(0, MAX_ATTEMPTS - request.session.get('failed_attempts', 0))

    return render(request, 'login.html', {
        'failed_attempts': request.session.get('failed_attempts', 0),
        'remaining_attempts': remaining_attempts
    })

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('inicio')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validar contra
        if not Usuario.validate_password(password):
            messages.error(request, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return redirect('registro')

        # Verificar si ya existe apodo o email registrando
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('registro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect('registro')

        # Si todo se verifico Crear el usuario
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.")
        return redirect('login')

    return render(request, 'registro.html')

def crear_encargo(request):
    if request.method == 'POST':
        form = EncargoForm(request.POST)
        if form.is_valid():
            encargo = form.save(commit=False)
            encargo.user = request.user  
            encargo.save()
            return redirect('mis_encargos')  
    else:
        form = EncargoForm()

    return render(request, 'crear_encargo.html', {'form': form})

def mis_encargos(request):
    encargos = Encargo.objects.all()  
    return render(request, 'mis_encargos.html', {'encargos': encargos})
