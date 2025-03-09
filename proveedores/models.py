from django.db import models

class CategoriaProveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaProveedor, on_delete=models.CASCADE, related_name="proveedores")
    telefono = models.CharField(max_length=20)
    email = models.EmailField(default="example@email.com")
    dias_visita = models.CharField(max_length=255, default="Lunes")  # Podrías mejorar con un campo ManyToMany si es necesario

    def __str__(self):
        return self.nombre

