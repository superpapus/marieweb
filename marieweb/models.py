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
        return f"#{self.pk} - {self.nombre}"

class Deuda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=False, null=False, related_name='deudas')
    productos = models.ManyToManyField(Producto)
    cantidad_productos = models.JSONField(default=dict)
    monto_total = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    pagado = models.BooleanField(default=False)
    fechaPago = models.DateTimeField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"#{str(self.pk)} - {self.usuario.username} - {self.fecha}"