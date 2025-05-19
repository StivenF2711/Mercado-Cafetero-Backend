from rest_framework import serializers
from .models import Proveedor, Categoria

class CategoriaProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    dias_visita = serializers.CharField()  # ✅ Ahora se puede leer y escribir

    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "categoria", "categoria_nombre", "telefono", "email", "dias_visita"]


    def get_dias_visita(self, obj):
        return obj.dias_visita.split(", ")  # Convierte la cadena en lista separada por comas
