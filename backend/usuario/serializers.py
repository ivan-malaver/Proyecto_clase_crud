# Importamos los módulos necesarios de Django Rest Framework
from rest_framework import serializers  # Importa la clase 'serializers' que se usa para transformar objetos complejos (como los modelos) en formatos que puedan ser fácilmente renderizados en JSON o XML.
from .models import Usuario  # Importa el modelo 'Usuario', que es el modelo que vamos a serializar (convertir a un formato adecuado para la API)

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    Este serializador permite realizar las operaciones básicas de crear, leer, actualizar y eliminar usuarios.
    """

    class Meta:
        # La clase Meta es donde configuramos el serializador para usar el modelo 'Usuario'.
        model = Usuario  # Definimos el modelo de datos a serializar, en este caso el modelo Usuario.
        
        # Los campos que queremos incluir en la serialización (es decir, los que serán representados en JSON o en otro formato).
        fields = ['id', 'email', 'role', 'is_active', 'is_staff', 'is_superuser']  
        # Especificamos que solo los campos mencionados (id, email, role, is_active, is_staff, is_superuser) se incluirán en la salida del serializador.

        # 'extra_kwargs' se utiliza para personalizar el comportamiento de ciertos campos.
        extra_kwargs = {
            'password': {'write_only': True},  # La contraseña es un campo de solo escritura. Esto significa que la contraseña se podrá enviar para crear o actualizar un usuario, pero nunca será incluida en las respuestas API.
        }

    # Sobrescribimos el método 'create' para crear un nuevo usuario.
    def create(self, validated_data):
        """
        Sobrescribimos el método create para asegurarnos de que la contraseña se cifre antes de guardar al usuario.
        """
        # Creamos un nuevo usuario utilizando los datos validados (todos los campos excepto 'password' que se tratará de forma especial).
        user = Usuario.objects.create(**validated_data)
        
        # Aquí ciframos la contraseña antes de guardarla en la base de datos. Django proporciona este método para manejar el cifrado.
        user.set_password(validated_data['password'])
        
        # Guardamos el usuario con la contraseña cifrada.
        user.save()
        
        # Finalmente, devolvemos el usuario recién creado.
        return user

    # Sobrescribimos el método 'update' para actualizar un usuario existente.
    def update(self, instance, validated_data):
        """
        Sobrescribimos el método update para que se pueda actualizar la contraseña de manera segura.
        """
        # Intentamos obtener la nueva contraseña del diccionario de datos validados.
        password = validated_data.get('password', None)
        
        # Si hay una nueva contraseña, la ciframos antes de actualizar el usuario.
        if password:
            instance.set_password(password)
        
        # Llamamos al método 'update' de la clase base (que es el serializador base) para actualizar los demás campos.
        return super().update(instance, validated_data)
