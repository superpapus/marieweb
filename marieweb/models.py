from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    icon_image = models.ImageField(upload_to='icons/', blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Deuda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=False, null=False, related_name='deudas')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    monto = models.IntegerField(default=0)
    cantidad = models.PositiveIntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)
    fechaPago = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.usuario.username + ' - ' + self.producto.nombre