from rest_framework import serializers
from .models import Proveedor, CategoriaProveedor

class CategoriaProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProveedor
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "categoria", "categoria_nombre"]


