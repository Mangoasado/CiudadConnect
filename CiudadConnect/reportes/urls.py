from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),
    path('nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('<int:pk>/', views.detalle_reporte, name='detalle_reporte'),
    path('<int:pk>/editar/', views.editar_reporte, name='editar_reporte'),
    path('<int:pk>/actualizar/', views.actualizar_estado, name='actualizar_estado'),
    path('<int:pk>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),
]