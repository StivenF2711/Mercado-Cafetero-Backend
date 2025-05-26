from django.urls import path
from .views import UsuarioViewSet, LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls

