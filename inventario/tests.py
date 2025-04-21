from django.test import TestCase
from inventario.models import Inventario
from productos.models import Producto
from proveedores.models import Proveedor, Categoria

class InventarioModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Abarrotes")
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Central",
            categoria=self.categoria,
            telefono="3201234567",
            email="central@proveedor.com",
            dias_visita="Lunes y Jueves"
        )
        self.producto = Producto.objects.create(
            nombre="Arroz Diana",
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra=2000,
            precio_venta=2500,
            unidad_medida="kg",
            stock=10
        )

    def test_entrada_aumenta_stock(self):
        """Una entrada de inventario debe aumentar el stock del producto."""
        Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=5
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_salida_disminuye_stock(self):
        """Una salida de inventario debe disminuir el stock del producto."""
        Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='salida',
            cantidad=3
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)

    def test_actualizacion_movimiento_ajusta_stock_correctamente(self):
        """Actualizar un movimiento ya existente debe ajustar el stock correctamente."""
        movimiento = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=8
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 18)

        movimiento.cantidad = 5
        movimiento.save()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_eliminar_movimiento_revierte_ajuste_stock(self):
        """Eliminar un movimiento de inventario debe revertir el ajuste de stock."""
        movimiento = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=6
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 16)

        movimiento.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
