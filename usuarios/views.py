from rest_framework.viewsets import ModelViewSet
from .models import Usuario
from .serializer import UsuarioSerializer
from .permissions import EsAdministrador
from rest_framework.views import APIView
from rest_framework.response import Response

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdministrador]

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validar campos
        if not username or not password:
            return Response({'error': 'Username y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        # Autenticación
        user = authenticate(username=username, password=password)
        if user:
            return Response({'message': 'Login exitoso'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)