from django.db import models
from productos.models import Producto
from proveedores.models import Proveedor

class EntradaInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='entradas')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='entradas')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Lógica para aumentar el stock del producto
        if self.pk is None:  # Solo si es una entrada nueva
            self.producto.stock += self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entrada de {self.cantidad} {self.producto.unidad_medida} de '{self.producto.nombre}' el {self.fecha.date()}"
