from django.db import models

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
