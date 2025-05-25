from rest_framework import viewsets
from .models import Inventario
from .serializers import InventarioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all().order_by('-fecha_actualizacion')
    serializer_class = InventarioSerializer

    @action(detail=False, methods=['get'], url_path='productos-disponibles')
    def productos_disponibles(self, request):
        disponibles = Inventario.obtener_productos_disponibles()
        return Response(disponibles)