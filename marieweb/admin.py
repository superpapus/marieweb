from django.contrib import admin
from .models import Categoria, Producto, Deuda, Encargo, Usuario

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Deuda)
admin.site.register(Encargo)