from django.db import models
from proveedores.models import CategoriaProveedor, Proveedor  # Asegúrate de importar bien según tu estructura

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaProveedor, on_delete=models.CASCADE, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    unidad_medida = models.CharField(max_length=20, default='unidad')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
