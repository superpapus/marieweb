from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('deudas/', views.deudas, name='deudas'),
]
