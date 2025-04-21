from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    imagen = serializers.ImageField(required=False) # Permite la subida de imágenes, no es requerida

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'categoria_nombre', 'proveedor', 'precio_compra', 'precio_venta', 'imagen', 'unidad_medida', 'fecha_creacion', 'fecha_actualizacion', 'stock']