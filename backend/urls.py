"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from proveedores.views import ProveedorViewSet, CategoriaViewSet
from productos.views import ProductoViewSet
from inventario.views import InventarioViewSet
from usuarios.views import UsuarioViewSet
from pedidos.views import PedidoViewSet
from ventas.views import VentaViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventario', InventarioViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'pedidos', PedidoViewSet)  
router.register(r'ventas', VentaViewSet)  

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/login/", obtain_auth_token, name="api_login"),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)