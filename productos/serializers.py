from rest_framework import serializers
from .models import Producto, Proveedor, Categoria


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    proveedor_categoria_nombre = serializers.CharField(source='proveedor.categoria.nombre', read_only=True)
    proveedor_email = serializers.EmailField(source='proveedor.email', read_only=True)  # ← nuevo campo
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'categoria', 'categoria_nombre',
            'proveedor', 'proveedor_nombre', 'proveedor_email', 'proveedor_categoria_nombre',
            'imagen', 'imagen_url', 'unidad_medida',
            'fecha_creacion', 'fecha_actualizacion',
        ]

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return request.build_absolute_uri(obj.imagen.url) if request else obj.imagen.url
        return None
