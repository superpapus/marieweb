from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import crear_encargo

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('deudas/', views.deudas, name='deudas'),
    path('deudas/admin/', views.deudas, name='deudas_admin'),
    path('deudas/ver/<int:id>/', views.ver_deuda, name='ver_deuda'),
    path('deudas/admin/ver/<int:id>/', views.ver_deuda, name='ver_deuda_admin'),
    path('login/', views.login, name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('crear/', crear_encargo, name='crear_encargo'),
    path('mis_encargos/', views.mis_encargos, name='mis_encargos'),
]