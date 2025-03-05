from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    dia_visita = models.CharField(max_length=20)  # Ej: "Lunes, Miércoles"
    
    def __str__(self):
        return self.nombre
