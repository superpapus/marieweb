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
    if not request.user.is_authenticated:
        return redirect('inicio')
    
    busqueda = request.GET.get('q', '')
    ordenarPor = request.GET.get('ordenarPor', 'fecha-agregado')

    deudas = request.user.deudas.all()

    if busqueda != '':
        deudas = deudas.filter(producto__nombre__icontains=busqueda)
    
    if ordenarPor == 'fecha-agregado':
        deudas = deudas.order_by('-fecha')
    elif ordenarPor == 'fecha-antiguo':
        deudas = deudas.order_by('fecha')
    elif ordenarPor == 'monto-mayor':
        deudas = deudas.order_by('-monto')
    elif ordenarPor == 'monto-menor':
        deudas = deudas.order_by('monto')
    
    return render(request, 'deudas.html', {
        'deudas': deudas,
        'ordenarPor': ordenarPor
    })