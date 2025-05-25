from rest_framework import serializers
from productos.models import Producto
from .models import Venta, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['subtotal']  # subtotal se calcula en save

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'id_cliente', 'fecha', 'total', 'metodo_pago', 'estado', 'observaciones', 'detalles']
        read_only_fields = ['fecha', 'estado', 'total']

    def validate(self, data):
        usuario_actual = self.context['request'].user.username  # o el identificador correcto
        id_cliente = data.get('id_cliente')

        if id_cliente == usuario_actual:
            raise serializers.ValidationError("No puedes pagarte a ti mismo.")

        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        total = 0

        for detalle in detalles_data:
            cantidad = detalle['cantidad']
            precio_unitario = detalle['precio_unitario']
            total += cantidad * precio_unitario

        venta = Venta.objects.create(total=total, **validated_data)

        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)

        return venta
