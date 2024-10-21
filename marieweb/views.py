from django.shortcuts import render
from .models import Producto


# Create your views here.
def inicio(request):
    ordenar = request.GET.get('ordenar', 'destacado')
    
    if ordenar == 'menor-precio':
        productos = Producto.objects.all().order_by('precio')
    elif ordenar == 'mayor-precio':
        productos = Producto.objects.all().order_by('-precio')
    else:
        productos = Producto.objects.all()  # Default order uwu



    return render(request, 'inicio/inicio.html', {'productos': productos, 'ordenar': ordenar})