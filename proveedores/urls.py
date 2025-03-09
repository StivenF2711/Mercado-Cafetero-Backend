from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet, CategoriaProveedorViewSet, CustomAuthToken, UserViewSet

# 🔹 Crear el router y registrar los ViewSets
router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaProveedorViewSet)
router.register(r'usuarios', UserViewSet, basename='usuarios')  # 🔹 Agregar usuarios

urlpatterns = [
    path('', include(router.urls)),  # 🔹 Esto incluirá todas las rutas del router
    path('login/', CustomAuthToken.as_view(), name='api_login'),  # Mantiene el login personalizado
]
