from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Venta
from .serializers import VentaSerializer
from rest_framework.permissions import AllowAny
import mercadopago

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Procesar la venta normalmente
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venta = serializer.save()

        # Si el método de pago es Mercado Pago, crear la preferencia
        if venta.metodo_pago == "mercadopago":
            sdk = mercadopago.SDK("TEST-8609422720499282-052501-36f788859347967d7a684ced096b79a2-2458297528")

            items = []
            for detalle in venta.detalles.all():
                items.append({
                    "title": detalle.producto.nombre,
                    "quantity": detalle.cantidad,
                    "unit_price": float(detalle.precio_unitario),
                })

            preference_data = {
                "items": items,
                "back_urls": {
                    "success": "http://localhost:5173/pago-exitoso",
                    "failure": "http://localhost:5173/pago-fallido",
                    "pending": "http://localhost:5173/pago-pendiente"
                },
                "auto_return": "approved"
            }

            try:
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response.get("response", {})
                print("Preferencia creada:", preference_response)

                if "id" in preference:
                    venta.preferencia_id = preference["id"]
                    venta.save()
                else:
                    return Response(
                        {"error": "No se pudo crear la preferencia de pago."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                data = serializer.data
                data["init_point"] = preference.get("init_point")
                return Response(data, status=status.HTTP_201_CREATED)

            except Exception as e:
                print("Error al crear preferencia de pago:", e)
                return Response(
                    {"error": "Error interno al comunicarse con Mercado Pago."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Si no es MercadoPago, simplemente devolver la venta registrada
        return Response(serializer.data, status=status.HTTP_201_CREATED)
