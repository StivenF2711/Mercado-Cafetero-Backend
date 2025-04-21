from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', include(router.urls)),
]