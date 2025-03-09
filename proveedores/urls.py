from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet, CategoriaProveedorViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaProveedorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
]
