from django.shortcuts import render
from .models import Producto, Categoria

# Create your views here.
def inicio(request):
    ordenar = request.GET.get('ordenar', 'destacado')
    categoria_id = request.GET.get('categoria', None)
    query = request.GET.get('q', '')
    
    productos = Producto.objects.all()
    
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
    ordenar = request.GET.get('ordenar', 'destacado')
    
    productos = Producto.objects.all()  # Obtener todos los productos

    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Buscar productos que coincidan

    if ordenar == 'menor-precio':
        productos = productos.order_by('precio')
    elif ordenar == 'mayor-precio':
        productos = productos.order_by('-precio')

    return render(request, 'buscar.html', {
        'productos': productos, 
        'query': query,
        'ordenar': ordenar
        })