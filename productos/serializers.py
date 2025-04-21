from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    imagen = serializers.CharField(source='imagen.url', read_only=True) # Asegúrate de tener esto o similar

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'categoria_nombre', 'proveedor', 'precio_compra', 'precio_venta', 'imagen', 'unidad_medida', 'fecha_creacion', 'fecha_actualizacion', 'stock']