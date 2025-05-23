from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Proveedor, Categoria
from .serializers import ProveedorSerializer, CategoriaProveedorSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]  # Solo usuarios autenticados

    @action(detail=False, methods=['get'])
    def filtrar_por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')

        if categoria_id:
            proveedores = Proveedor.objects.filter(categoria_id=categoria_id)
        else:
            proveedores = Proveedor.objects.all()

        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]
