import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Producto, Categoria
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, timedelta

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
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        enabled = request.POST.get('enabled') == 'on'
        
        if producto:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.stock = stock
            producto.enabled = enabled
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente.')
        else:
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                enabled=enabled
            )
            messages.success(request, 'Producto creado exitosamente.')
        return redirect('gestionar_productos', producto_id=producto.id if producto else None)
    
    return render(request, 'gestionar_productos.html', {
        'producto': producto
    })

def buscar_productos(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL
    categoria_id = request.GET.get('categoria', None)
    
    productos = Producto.objects.filter(enabled=True)

    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Buscar productos que coincidan


    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'buscar.html', {
        'productos': productos, 
        'query': query,
        'categorias': categorias, 
        'categoria_actual': categoria_id,
        })

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