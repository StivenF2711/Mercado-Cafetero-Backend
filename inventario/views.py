from rest_framework import viewsets
from .models import Inventario
from .serializers import InventarioSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all().order_by('-fecha_actualizacion')
    serializer_class = InventarioSerializer
