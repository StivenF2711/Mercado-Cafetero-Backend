from django.urls import path
from .views import UsuarioListCreateView

urlpatterns = [
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuarios'),
    path('login/', UsuarioListCreateView.as_view(), name='login'),
]
