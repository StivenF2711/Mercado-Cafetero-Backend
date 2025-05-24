from django.db import models
from productos import serializers
from proveedores.models import Proveedor
from productos.models import Producto

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('recibido', 'Recibido'),
        ('incompleto', 'Incompleto'),
        ('cancelado', 'Cancelado'),
        ('en proceso', 'En Proceso'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.proveedor.nombre}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_pedida = models.PositiveIntegerField()
    cantidad_recibida = models.PositiveIntegerField(default=0)
    productos_danados = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad_pedida} unid.) - Pedido #{self.pedido.id}"

def create(self, validated_data):
    detalles_data = validated_data.pop('detalles')
    proveedor = validated_data['proveedor']

    for detalle in detalles_data:
        producto = detalle['producto']
        if producto.proveedor != proveedor:
            raise serializers.ValidationError(
                f"El producto '{producto.nombre}' no pertenece al proveedor '{proveedor.nombre}'."
            )

    pedido = Pedido.objects.create(**validated_data)
    for detalle in detalles_data:
        DetallePedido.objects.create(pedido=pedido, **detalle)
    return pedido
