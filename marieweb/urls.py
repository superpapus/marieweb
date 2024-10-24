from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
]
