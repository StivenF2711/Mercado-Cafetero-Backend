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

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        # No uses total de validated_data, lo calculamos aquí
        total = 0

        # Calculamos total sumando subtotal de cada detalle
        for detalle in detalles_data:
            cantidad = detalle['cantidad']
            precio_unitario = detalle['precio_unitario']
            total += cantidad * precio_unitario

        # Creamos la venta con el total calculado
        venta = Venta.objects.create(total=total, **validated_data)

        # Creamos los detalles y los asociamos a la venta
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)

        return venta
