from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet, CategoriaViewSet, UserViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('', include(router.urls)),
]
