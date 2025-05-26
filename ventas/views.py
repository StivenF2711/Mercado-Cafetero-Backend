from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer
from rest_framework.permissions import AllowAny
import mercadopago
from inventario.models import Inventario
from productos.models import Producto

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

            items_mp = []
            total_venta = 0

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

                total_venta += cantidad * precio_unitario

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
                "auto_return": "approved"
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response.get("response", {})

            if "id" not in preference:
                return Response(
                    {"error": "No se pudo crear la preferencia de pago."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Registrar la venta localmente (opcional, también puede hacerse en un webhook)
            venta = Venta.objects.create(
                id_cliente=None,
                total=total_venta,
                metodo_pago="mercadopago",
                preferencia_id=preference["id"]
            )

            # Crear los detalles de la venta y actualizar inventario
            for item in detalles:
                producto = Producto.objects.get(id=item["producto"])
                cantidad = int(item["cantidad"])
                precio_unitario = float(item["precio_unitario"])

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                )

                Inventario.objects.create(
                    producto=producto,
                    tipo='venta',
                    cantidad=cantidad,
                    observaciones=f"Venta registrada (ID venta: {venta.id})"
                )

            data_response = VentaSerializer(venta).data
            data_response["init_point"] = preference.get("init_point")
            return Response(data_response, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error al crear preferencia de pago:", e)
            return Response(
                {"error": "Error interno al comunicarse con Mercado Pago."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
