from django.shortcuts import render
from .models import Producto

# Create your views here.
def inicio(request):
    return render(request, 'inicio/inicio.html')

def buscar_productos(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL
    productos = []  # Inicializar con una lista vacía

    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Buscar productos que coincidan

    return render(request, 'buscar.html', {'productos': productos, 'query': query})