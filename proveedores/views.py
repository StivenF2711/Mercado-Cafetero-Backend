from rest_framework import viewsets
from .models import Proveedor, CategoriaProveedor
from .serializers import ProveedorSerializer, CategoriaProveedorSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class CategoriaProveedorViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProveedor.objects.all()
    serializer_class = CategoriaProveedorSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})