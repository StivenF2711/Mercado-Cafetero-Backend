from rest_framework import serializers
from .models import Inventario

class InventarioSerializer(serializers.ModelSerializer):
    stock_actual = serializers.SerializerMethodField()
    ultimo_precio_venta = serializers.SerializerMethodField()
    ultimo_precio_compra = serializers.SerializerMethodField()

    class Meta:
        model = Inventario
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'stock_actual', 'ultimo_precio_venta', 'ultimo_precio_compra']

    def get_stock_actual(self, obj):
        return Inventario.obtener_stock_actual(obj.producto)

    def get_ultimo_precio_venta(self, obj):
        precios = Inventario.obtener_precios_actuales(obj.producto)
        return precios.get('precio_venta')

    def get_ultimo_precio_compra(self, obj):
        precios = Inventario.obtener_precios_actuales(obj.producto)
        return precios.get('precio_compra')
