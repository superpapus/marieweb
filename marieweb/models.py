from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
import re  # Para la validación personalizada de contraseñas

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

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")  # Email único
    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de Usuario")  # Nombre de usuario único
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