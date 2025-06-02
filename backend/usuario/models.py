# Importación de módulos necesarios de Django
from django.db import models  # Importa el módulo para manejar modelos en Django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # Importa las clases para crear un usuario personalizado y su administrador

# Creamos un Manager personalizado para el modelo Usuario
class UsuarioManager(BaseUserManager):
    """
    Manager para el modelo de Usuario personalizado.
    Define métodos para crear usuarios y superusuarios.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Método para crear un usuario con un correo electrónico y contraseña.
        """
        if not email:
            # Si el correo no es proporcionado, se lanza un error
            raise ValueError("El email debe ser proporcionado.")
        
        email = self.normalize_email(email)  # Normaliza el correo electrónico (asegurando que esté en minúsculas)
        user = self.model(email=email, **extra_fields)  # Crea una nueva instancia del usuario con el email y los campos extra
        user.set_password(password)  # Establece la contraseña (utiliza el método set_password que la cifra)
        user.save(using=self._db)  # Guarda el usuario en la base de datos
        return user  # Devuelve el usuario creado

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Método para crear un superusuario.
        """
        # Establece valores por defecto para un superusuario
        extra_fields.setdefault('is_staff', True)  # El superusuario debe tener permisos de staff
        extra_fields.setdefault('is_superuser', True)  # El superusuario debe ser considerado como superusuario
        # Llama al método `create_user` para crear el usuario con los parámetros proporcionados
        return self.create_user(email, password, **extra_fields)

# Creamos el modelo de Usuario personalizado
class Usuario(AbstractBaseUser):
    """
    Modelo de Usuario Personalizado:
    Usamos el e-mail como la credencial principal.
    Incluye un rol y otros campos básicos de autenticación.
    """

    # 1️⃣ Credencial principal (email)
    email = models.EmailField(unique=True)  # El campo de correo electrónico es único para cada usuario

    # 2️⃣ Roles de los usuarios
    # Definimos diferentes roles para los usuarios: cliente, administrador, supervisor
    ROLE_CLIENTE = "cliente"
    ROLE_ADMIN = "admin"
    ROLE_SUPERVISOR = "supervisor"

    # Las opciones posibles para el rol
    ROLE_CHOICES = [
        (ROLE_CLIENTE, "Cliente"),
        (ROLE_ADMIN, "Administrador"),
        (ROLE_SUPERVISOR, "Supervisor"),
    ]
    
    # El campo 'role' se utiliza para asignar el rol de cada usuario
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ROLE_CLIENTE)  # Por defecto, el rol es 'cliente'

    # 3️⃣ Campos básicos de autenticación
    # Estos campos permiten controlar el estado del usuario y sus permisos
    is_active = models.BooleanField(default=True)  # Define si el usuario está activo (puede iniciar sesión)
    is_staff = models.BooleanField(default=False)  # Define si el usuario tiene permisos de administración
    is_superuser = models.BooleanField(default=False)  # Define si el usuario es un superusuario (tiene todos los permisos)

    # 4️⃣ Configuración de autenticación
    USERNAME_FIELD = 'email'  # El campo principal para la autenticación es el email
    REQUIRED_FIELDS = ['role']  # Otros campos necesarios cuando se crea un superusuario

    # 5️⃣ Configuración del manager personalizado para el modelo Usuario
    objects = UsuarioManager()  # Asociamos el manager personalizado que maneja la creación de usuarios

    # 6️⃣ Métodos adicionales para la clase Usuario

    def __str__(self):
        """
        Método que define cómo se representa el objeto Usuario cuando se imprime o se muestra.
        """
        return f"{self.email} ({self.role})"  # Devuelve el correo electrónico y el rol del usuario

    def set_password(self, password):
        """
        Sobrescribe el método set_password de AbstractBaseUser para cifrar la contraseña.
        """
        super().set_password(password)  # Llama al método de la clase base para cifrar la contraseña

    def check_password(self, password):
        """
        Sobrescribe el método check_password de AbstractBaseUser para verificar la contraseña.
        """
        return super().check_password(password)  # Llama al método de la clase base para verificar la contraseña
