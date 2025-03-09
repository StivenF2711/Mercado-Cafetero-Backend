from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from .models import Proveedor, CategoriaProveedor
from .serializers import ProveedorSerializer, CategoriaProveedorSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados

class CategoriaProveedorViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProveedor.objects.all()
    serializer_class = CategoriaProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        })

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # Solo admins pueden crear superusuarios

    @action(detail=False, methods=['post'])
    def crear_superusuario(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Todos los campos son obligatorios'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'El usuario ya existe'}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Encripta la contraseña
            is_superuser=True,
            is_staff=True
        )
        return Response({'mensaje': 'Superusuario creado correctamente'}, status=201)
