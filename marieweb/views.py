from django.shortcuts import render
from .models import Producto, Categoria

# Create your views here.
def inicio(request):
    ordenar = request.GET.get('ordenar', 'destacado')
    categoria_id = request.GET.get('categoria', None)
    
    if ordenar == 'menor-precio':
        productos = Producto.objects.all().order_by('precio')
    elif ordenar == 'mayor-precio':
        productos = Producto.objects.all().order_by('-precio')
    else:
        productos = Producto.objects.all()  # Default order uwu
    
    categorias = Categoria.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'inicio/inicio.html', {
        'productos': productos, 
        'ordenar': ordenar, 
        'categorias': categorias, 
        'categoria_actual': categoria_id
        })

def buscar_productos(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL
    productos = []  # Inicializar con una lista vacía

    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Buscar productos que coincidan

    return render(request, 'buscar.html', {'productos': productos, 'query': query})