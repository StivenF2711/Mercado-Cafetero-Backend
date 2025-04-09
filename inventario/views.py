from rest_framework import viewsets
from .models import EntradaInventario
from .serializers import EntradaInventarioSerializer

class EntradaInventarioViewSet(viewsets.ModelViewSet):
    queryset = EntradaInventario.objects.all().order_by('-fecha')
    serializer_class = EntradaInventarioSerializer
