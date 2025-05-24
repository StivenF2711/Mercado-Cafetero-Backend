from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pedido, DetallePedido  # asumiendo que tienes el modelo detalle
from .serializers import PedidoSerializer
from inventario.models import Inventario
from productos.models import Producto
from django.db import transaction

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha_pedido')
    serializer_class = PedidoSerializer
    permission_classes = [permissions.AllowAny]  # ajusta si es necesario

    @action(detail=True, methods=['put'])
    def recibir(self, request, pk=None):
        pedido = self.get_object()
        datos_detalles = request.data.get('detalles', [])
    
        try:
            with transaction.atomic():
                estado_pedido = 'recibido'  # por defecto
    
                total_unidades_buenas = 0
                total_unidades_pedidas = 0
    
                for item in datos_detalles:
                    detalle_id = item.get('id')
                    cantidad_recibida = item.get('cantidad_recibida', 0)
                    productos_danados = item.get('productos_danados', 0)
    
                    detalle = pedido.detalles.get(id=detalle_id)
                    detalle.cantidad_recibida = cantidad_recibida
                    detalle.productos_danados = productos_danados
                    detalle.save()
    
                    cantidad_buena = cantidad_recibida - productos_danados
                    total_unidades_buenas += cantidad_buena
                    total_unidades_pedidas += detalle.cantidad_pedida
    
                    if cantidad_buena > 0:
                        Inventario.objects.create(
                            producto=detalle.producto,
                            tipo='entrada',
                            cantidad=cantidad_buena,
                            precio_compra=None,
                            precio_venta=None,
                            observaciones=f'Entrada por recepción pedido {pedido.id}',
                        )
    
                if total_unidades_buenas == 0:
                    estado_pedido = 'cancelado'  # o un estado que decidas para "todo malo"
                elif total_unidades_buenas < total_unidades_pedidas:
                    estado_pedido = 'incompleto'
                else:
                    estado_pedido = 'recibido'
    
                pedido.estado = estado_pedido
                pedido.save()
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'mensaje': f'Pedido recibido y stock actualizado. Estado: {pedido.estado}'}, status=status.HTTP_200_OK)
    