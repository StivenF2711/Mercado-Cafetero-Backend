from django.db import models
from productos.models import Producto

class Inventario(models.Model):
    TIPO_MOVIMIENTO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO, default='entrada')
    cantidad = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            entrada_anterior = Inventario.objects.get(pk=self.pk)
            diferencia = self.cantidad if self.tipo == 'entrada' else -self.cantidad
            diferencia_anterior = entrada_anterior.cantidad if entrada_anterior.tipo == 'entrada' else -entrada_anterior.cantidad
            ajuste = diferencia - diferencia_anterior
        else:
            ajuste = self.cantidad if self.tipo == 'entrada' else -self.cantidad

        self.producto.stock += ajuste
        self.producto.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ajuste = -self.cantidad if self.tipo == 'entrada' else self.cantidad
        self.producto.stock += ajuste
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.cantidad} {self.producto.unidad_medida} de '{self.producto.nombre}' el {self.fecha_creacion.date()}"
