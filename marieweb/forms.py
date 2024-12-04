from django import forms
from .models import Encargo

class EncargoForm(forms.ModelForm):
    class Meta:
        model = Encargo
        fields = ['encargo_nombre_producto', 'encargo_cantidad_producto', 'encargo_fecha', 'encargo_comentario_extra']
        labels = {
            'encargo_nombre_producto': 'Nombre del Producto',
            'encargo_cantidad_producto': 'Cantidad',
            'encargo_fecha': 'Día en que lo necesita',
            'encargo_comentario_extra': 'Comentarios extra',
        }
        widgets = {
            'encargo_fecha': forms.DateInput(attrs={'type': 'date'}),
            'encargo_comentario_extra': forms.Textarea(attrs={'rows': 4}),
        }