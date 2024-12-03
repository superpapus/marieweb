import datetime
from django.shortcuts import redirect, render
from .models import Producto, Categoria, Deuda, Encargo
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, timedelta
from .forms import EncargoForm


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

def deudas(request):
    ruta = request.path.split('/')
    if not request.user.is_authenticated:
        return redirect('inicio')
    if ruta[2] == 'admin':
        if not request.user.is_staff:
            return redirect('deudas')
    
    busqueda = request.GET.get('q', '')
    ordenarPor = request.GET.get('ordenarPor', 'fecha-agregado')

    if ruta[2] == 'admin':
        deudas = Deuda.objects.all()
    else:
        deudas = request.user.deudas.all()

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
        'mostrar_filtro': True,
        'deudas': deudas,
        'busqueda': busqueda,
        'ordenarPor': ordenarPor,
        'titulo': titulo,
        'descripcion': descripcion
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
        'deuda': Deuda.objects.get(pk=id),
        'titulo': titulo,
        'descripcion': descripcion
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
