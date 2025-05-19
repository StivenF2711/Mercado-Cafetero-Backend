from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    correo = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    es_activo = models.BooleanField(default=True)

    ROL_CHOICES = (
        ('administrador', 'Administrador'),
        ('jefe_bodega', 'Jefe de Bodega'),
        ('empleado', 'Empleado'),
    )
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='empleado')

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username']  # requerido por AbstractUser

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"
