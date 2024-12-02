from django.shortcuts import redirect, render
from .models import Producto, Categoria, Deuda

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

    return render(request, 'inicio/inicio.html', {
        'productos': productos, 
        'ordenar': ordenar, 
        'categorias': categorias, 
        'categoria_actual': categoria_id,
        'query': query
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

    deudas = deudas.filter(pagado=False)
    
    if busqueda != '':
        deudas = deudas.filter(productos__nombre__icontains=busqueda) # | Q(usuario__username__icontains=busqueda)
    
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
        'mostrarAdmin': request.user.is_staff,
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
    
    if request.user.is_staff:
        titulo = 'Detalles de la deuda'
        descripcion = 'Aquí puedes ver los detalles de la deuda.'
    else:
        titulo = 'Detalles de tu deuda'
        descripcion = 'Aquí puedes ver los detalles de tu deuda.'
    return render(request, 'deudas.html', {
            'mostrarAdmin': request.user.is_staff,
            'mostrar_filtro': False,
            'deuda': Deuda.objects.get(pk=id),
            'titulo': titulo,
            'descripcion': descripcion
    })