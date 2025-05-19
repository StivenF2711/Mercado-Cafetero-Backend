from rest_framework import viewsets, permissions
from .models import Pedido
from .serializers import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha_pedido')
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]  # ajusta si es necesario
