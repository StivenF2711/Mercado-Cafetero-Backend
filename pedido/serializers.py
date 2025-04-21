from rest_framework import serializers
from .models import Pedido, DetallePedido
from productos.models import Producto

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'fecha_creacion', 'estado', 'total', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        pedido = Pedido.objects.create(**validated_data)
        total = 0

        for detalle in detalles_data:
            producto = detalle['producto']
            cantidad = detalle['cantidad']
            precio = detalle['precio_unitario']
            subtotal = cantidad * precio

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            )
            total += subtotal

        pedido.total = total
        pedido.save()
        return pedido
