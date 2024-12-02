from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('deudas/', views.deudas, name='deudas'),
    path('deudas/admin/', views.deudas, name='deudas_admin'),
    path('deudas/ver/<int:id>/', views.ver_deuda, name='ver_deuda'),
    path('deudas/admin/ver/<int:id>/', views.ver_deuda, name='ver_deuda_admin'),
]
