from django.contrib import admin
from .models import Categoria, Producto, Deuda, Encargo

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Deuda)
admin.site.register(Encargo)