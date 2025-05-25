from django.db import models
from django.core.exceptions import ValidationError
from productos.models import Producto
from pedidos.models import Pedido, DetallePedido

class Inventario(models.Model):
    TIPO_MOVIMIENTO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste de precios'),
        ('vencimiento', 'Salida por vencimiento'),
        ('daño', 'Salida por daño'),              
        ('pérdida', 'Salida por pérdida'),        
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=15, choices=TIPO_MOVIMIENTO, default='entrada')
    cantidad = models.PositiveIntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    observaciones = models.TextField(blank=True, null=True)

    @staticmethod
    def obtener_precios_actuales(producto):
        ultimo_ajuste = Inventario.objects.filter(producto=producto, tipo='ajuste').order_by('-fecha_creacion').first()
        if ultimo_ajuste:
            return {
                'precio_compra': ultimo_ajuste.precio_compra,
                'precio_venta': ultimo_ajuste.precio_venta,
            }
        return {
            'precio_compra': None,
            'precio_venta': None,
        }

    @staticmethod
    def obtener_stock_actual(producto):
        movimientos = Inventario.objects.filter(producto=producto).exclude(tipo='ajuste')
        stock = 0
        for movimiento in movimientos:
            if movimiento.tipo == 'entrada':
                stock += movimiento.cantidad
            elif movimiento.tipo in ['salida', 'vencimiento', 'daño', 'pérdida']:
                stock -= movimiento.cantidad
        return stock

    def clean(self):
        if self.tipo == 'ajuste':
            if self.cantidad != 0:
                raise ValidationError("El ajuste de precios no debe tener cantidad distinta de cero.")

        if self.precio_compra and self.precio_venta:
            if self.precio_venta < self.precio_compra:
                raise ValidationError("El precio de venta no puede ser menor al precio de compra.")

        if self.tipo in ['salida', 'vencimiento', 'daño', 'pérdida'] and not self.pk:
            stock_actual = self.obtener_stock_actual(self.producto)
            if stock_actual - self.cantidad < 0:
                raise ValidationError("La salida dejaría el stock en negativo.")

    def save(self, *args, **kwargs):
        self.clean()

        if self.tipo == 'ajuste':
            if self.precio_compra is not None:
                self.producto.precio_compra = self.precio_compra
            if self.precio_venta is not None:
                self.producto.precio_venta = self.precio_venta
            self.producto.save()
            return super().save(*args, **kwargs)

        # Movimiento de stock normal
        if self.pk:
            movimiento_anterior = Inventario.objects.get(pk=self.pk)
            ajuste = self.cantidad if self.tipo == 'entrada' else -self.cantidad
            ajuste_anterior = movimiento_anterior.cantidad if movimiento_anterior.tipo == 'entrada' else -movimiento_anterior.cantidad
            diferencia = ajuste - ajuste_anterior
        else:
            diferencia = self.cantidad if self.tipo == 'entrada' else -self.cantidad

        stock_actual = self.obtener_stock_actual(self.producto)
        nuevo_stock = stock_actual + diferencia

        if self.tipo in ['salida', 'vencimiento', 'daño', 'pérdida'] and nuevo_stock < 0:
            raise ValidationError("Esta modificación dejaría el stock en negativo.")

        super().save(*args, **kwargs)

        # Generar pedido automático por bajo stock
        stock_actual = self.obtener_stock_actual(self.producto)
        if stock_actual < 10:
            proveedor = self.producto.proveedor  # Asume que existe
            if proveedor is not None:
                pedidos_pendientes = Pedido.objects.filter(proveedor=proveedor, estado='pendiente')
                pedido_existente = None
                for pedido in pedidos_pendientes:
                    if pedido.detalles.filter(producto=self.producto).exists():
                        pedido_existente = pedido
                        break

                if not pedido_existente:
                    pedido = Pedido.objects.create(
                        proveedor=proveedor,
                        estado='pendiente',
                        observaciones='Generado automáticamente por bajo stock',
                    )
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=self.producto,
                        cantidad_pedida=20,
                        cantidad_recibida=0,
                    )

    def delete(self, *args, **kwargs):
        if self.tipo != 'ajuste':
            ajuste = -self.cantidad if self.tipo == 'entrada' else self.cantidad
            stock_actual = self.obtener_stock_actual(self.producto)
            nuevo_stock = stock_actual + ajuste
            if self.tipo in ['salida', 'vencimiento', 'daño', 'pérdida'] and nuevo_stock < 0:
                raise ValidationError("Eliminar esta salida dejaría el stock en negativo.")

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.cantidad} {self.producto.unidad_medida} de '{self.producto.nombre}' el {self.fecha_creacion.date()}"

    @staticmethod
    def obtener_productos_disponibles():
        """
        Retorna productos con stock > 0, incluyendo nombre, id, stock y precios actuales.
        """
        from productos.models import Producto  # Para evitar import circular

        productos = Producto.objects.all()
        disponibles = []

        for producto in productos:
            stock = Inventario.obtener_stock_actual(producto)
            if stock > 0:
                precios = Inventario.obtener_precios_actuales(producto)
                disponibles.append({
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'stock': stock,
                    'precio_compra': float(precios['precio_compra']) if precios['precio_compra'] else 0.0,
                    'precio_venta': float(precios['precio_venta']) if precios['precio_venta'] else 0.0,
                })

        return disponibles