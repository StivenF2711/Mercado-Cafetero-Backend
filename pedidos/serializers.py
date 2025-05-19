from rest_framework import serializers
from .models import Pedido, DetallePedido, Producto

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')  # útil en respuestas

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'producto_nombre', 'cantidad_pedida', 'cantidad_recibida', 'productos_danados', 'observaciones']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'fecha_pedido', 'estado', 'observaciones', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        pedido = Pedido.objects.create(**validated_data)
        for detalle in detalles_data:
            DetallePedido.objects.create(pedido=pedido, **detalle)
        return pedido

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.observaciones = validated_data.get('observaciones', instance.observaciones)
        instance.save()

        if detalles_data:
            instance.detalles.all().delete()
            for detalle in detalles_data:
                DetallePedido.objects.create(pedido=instance, **detalle)
        return instance
