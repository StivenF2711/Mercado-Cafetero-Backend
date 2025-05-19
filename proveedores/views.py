from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Proveedor, Categoria
from .serializers import ProveedorSerializer, CategoriaProveedorSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]  # Solo usuarios autenticados

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaProveedorSerializer
    permission_classes = [permissions.AllowAny]  # Solo usuarios autenticados



class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def filtrar_por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')  # o usa 'nombre' si filtras por nombre

        if categoria_id:
            proveedores = Proveedor.objects.filter(categoria_id=categoria_id)
        else:
            proveedores = Proveedor.objects.all()

        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)
