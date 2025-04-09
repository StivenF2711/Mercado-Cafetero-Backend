from rest_framework.routers import DefaultRouter
from .views import EntradaInventarioViewSet

router = DefaultRouter()
router.register(r'entradas', EntradaInventarioViewSet, basename='entrada-inventario')

urlpatterns = router.urls
