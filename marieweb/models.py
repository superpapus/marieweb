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
