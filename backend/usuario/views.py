# Importamos los módulos necesarios de Django Rest Framework
from rest_framework import status  # Para los códigos de estado HTTP
from rest_framework.decorators import api_view  # Para crear vistas basadas en funciones
from rest_framework.response import Response  # Para devolver respuestas a las solicitudes
from .models import Usuario  # Importamos el modelo Usuario
from .serializers import UsuarioSerializer  # Importamos el serializador para Usuario

# Vista para listar todos los usuarios o crear un nuevo usuario
@api_view(['GET', 'POST'])
def usuario_list(request):
    """
    Lista todos los usuarios o crea un nuevo usuario.
    """

    if request.method == 'GET':
        # Si la solicitud es GET, obtenemos todos los usuarios de la base de datos
        usuarios = Usuario.objects.all()
        # Serializamos los usuarios
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)  # Retorna la lista de usuarios como JSON

    elif request.method == 'POST':
        # Si la solicitud es POST, creamos un nuevo usuario con los datos proporcionados
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():  # Verificamos si los datos son válidos
            serializer.save()  # Guardamos el nuevo usuario en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retorna el nuevo usuario con código 201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna un error si los datos no son válidos


# Vista para obtener, actualizar o eliminar un usuario específico
@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail(request, pk):
    """
    Obtiene, actualiza o elimina un usuario específico.
    """
    try:
        usuario = Usuario.objects.get(pk=pk)  # Intentamos obtener un usuario por su ID (pk)
    except Usuario.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)  # Si no existe, retornamos un 404

    if request.method == 'GET':
        # Si la solicitud es GET, obtenemos los detalles del usuario
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)  # Retorna los detalles del usuario

    elif request.method == 'PUT':
        # Si la solicitud es PUT, actualizamos los detalles del usuario
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():  # Verificamos si los datos son válidos
            serializer.save()  # Actualizamos el usuario
            return Response(serializer.data)  # Retorna los datos actualizados
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Si hay errores, retornamos un 400

    elif request.method == 'DELETE':
        # Si la solicitud es DELETE, eliminamos el usuario
        usuario.delete()  # Eliminamos el usuario
        return Response(status=status.HTTP_204_NO_CONTENT)  # Retornamos un 204 (sin contenido)
