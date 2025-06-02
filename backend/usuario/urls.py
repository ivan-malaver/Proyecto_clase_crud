from django.urls import path
from . import views  # Importa las vistas de tu archivo views.py

urlpatterns = [
    # Ruta para listar todos los usuarios o crear un nuevo usuario
    path('usuarios/', views.usuario_list, name='usuario_list'),  # Manejamos GET y POST

    # Ruta para obtener, actualizar o eliminar un usuario específico
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),  # Manejamos GET, PUT y DELETE
]
