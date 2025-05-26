from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Venta
from .serializers import VentaSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import mercadopago
from inventario.models import Inventario
from productos.models import Producto
from ventas.models import Venta, DetalleVenta  # Ajusta si lo tienes en otra app
from datetime import datetime

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="crearpreferencia")
    def crear_preferencia(self, request):
        sdk = mercadopago.SDK("APP_USR-3350272912119402-052516-fd717a318adaae1d10fe6b3a59a3f431-2456479427")
    
        try:
            data = request.data
            detalles = data.get("detalles", [])
            if not detalles:
                return Response({"error": "No se proporcionaron productos para la venta."}, status=400)
    
            # Crear preferencia en MercadoPago (con todos los productos)
            items_mp = []
            for item in detalles:
                producto_id = item.get("producto")
                producto = Producto.objects.get(id=producto_id)
                cantidad = int(item.get("cantidad", 1))
                precio_unitario = float(item.get("precio_unitario", item.get("precio_venta", 0.0)))
    
                items_mp.append({
                    "id": str(producto.id),
                    "title": producto.nombre,
                    "quantity": cantidad,
                    "currency_id": "COP",
                    "unit_price": precio_unitario,
                })
    
            preference_data = {
                "items": items_mp,
                "payer": {
                    "email": "test_user_123456@testuser.com"
                },
                "back_urls": {
                    "success": "https://mercado-cafetero-frontend-production.up.railway.app/pago-exitoso",
                    "failure": "https://mercado-cafetero-frontend-production.up.railway.app/pago-fallido",
                    "pending": "https://mercado-cafetero-frontend-production.up.railway.app/pago-pendiente"
                },
                "auto_return": "approved",
            }
    
            preference_response = sdk.preference().create(preference_data)
    
            # 💾 Crear la venta localmente (puedes mover esto a un webhook si prefieres después del pago)
            venta = Venta.objects.create(
             
                id_cliente=None,  # O puedes usar request.user.id o un email si tienes auth
                total=sum(item["quantity"] * item["unit_price"] for item in items_mp),
            

            )
    
            for item in detalles:
                producto = Producto.objects.get(id=item["producto"])
                cantidad = int(item["cantidad"])
                precio_unitario = float(item["precio_unitario"])

                # Crear detalle de venta
                movimiento = DetalleVenta( 
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                )

                # Crear instancia de Inventario
                movimiento = Inventario(
                    producto=producto,
                    tipo='venta',
                    cantidad=cantidad,
                    observaciones=f"Venta registrada (ID venta: {venta.id})"
                )
                # Llamar al método save explícitamente
                movimiento.save()
    
            return Response(preference_response["response"], status=status.HTTP_201_CREATED)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['patch'])
    def devolver(self, request, pk=None):
        venta = self.get_object()
        if venta.estado == 'devuelta':
            return Response({"detail": "Venta ya fue devuelta"}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica para hacer la devolución de inventario aquí o en frontend

        venta.estado = 'devuelta'
        venta.save()
        return Response({"detail": "Venta marcada como devuelta"})