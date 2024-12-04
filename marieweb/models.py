from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import re # Para la validación personalizada de contraseñas

from django.conf import settings

class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de Usuario")  # Nombre de usuario único
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")  # Email único
    password = models.CharField(max_length=128, verbose_name="Contraseña")  # Contraseña

    def clean(self): # Verificaciones de usuario y contraseña, respectivamenteeee
        if not self.email or not self.username or not self.password:
            raise ValidationError("Todos los campos deben estar completos para guardar un usuario.")

        if not self.validate_password(self.password):
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres, una letra mayúscula y un número."
            )

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):  # Verifica si contiene al menos una mayúscula
            return False
        if not re.search(r'[0-9]', password):  # Verifica si contiene al menos un número
            return False
        return True

    def __str__(self):
        return self.username
    pass
    
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
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=False, null=False, related_name='deudas')
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

class Encargo(models.Model):
    ESTADOS = [
        ('en_proceso', 'En Proceso'),
        ('en_camino', 'En Camino'),
        ('listo_para_recoger', 'Listo para Recoger'),
    ]
    encargo_nombre_producto = models.CharField(max_length=255, verbose_name="Nombre del producto")
    encargo_cantidad_producto = models.PositiveIntegerField(verbose_name="Cantidad")
    encargo_fecha = models.DateField(verbose_name="Día en que lo necesita")
    encargo_comentario_extra = models.TextField(blank=True, verbose_name="Comentarios extra")
    encargo_estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='en_proceso',
    )

    def __str__(self):
        return self.encargo_nombre_producto
