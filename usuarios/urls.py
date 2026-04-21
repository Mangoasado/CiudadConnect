from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('usuarios/login/', views.vista_login, name='login'),
    path('usuarios/registro/', views.vista_registro, name='registro'),
    path('usuarios/logout/', views.vista_logout, name='logout'),
    path('usuarios/perfil/', views.vista_perfil, name='perfil'),
    path('usuarios/perfil/password/', views.cambiar_password, name='cambiar_password'),
]