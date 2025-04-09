
from rest_framework import serializers
from .models import EntradaInventario

class EntradaInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaInventario
        fields = '__all__'
        read_only_fields = ['fecha']  # Evita que te la pidan al crear
