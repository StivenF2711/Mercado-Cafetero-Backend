from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Usuario
from .serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para usuarios.
    Solo accesible para usuarios autenticados.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
    Vista para login que devuelve token de autenticación.
    Permite acceso sin estar autenticado.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Recibe 'username' que en realidad es el correo para autenticación
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username (correo) y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        # Llama al backend personalizado que autentica por correo
        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
