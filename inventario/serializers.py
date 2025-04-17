
from rest_framework import serializers
from .models import Inventario

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
