from django.db import models

class Venta(models.Model):
    id_cliente = models.CharField(max_length=50, blank=True, null=True, help_text="ID o referencia del cliente")

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('mercadopago', 'Mercado Pago'),
    ]
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO
    )

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('anulada', 'Anulada'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    # Campos específicos de Mercado Pago
    preferencia_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="ID de preferencia de Mercado Pago"
    )

    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="ID del pago en Mercado Pago"
    )

    estado_pago = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Estado real del pago en Mercado Pago (approved, rejected, etc.)"
    )

    def __str__(self):
        cliente = self.id_cliente if self.id_cliente else "Anónimo"
        return f"Venta #{self.id} - Cliente: {cliente} - Total: {self.total} - Estado: {self.estado}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Venta #{self.venta.id}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
