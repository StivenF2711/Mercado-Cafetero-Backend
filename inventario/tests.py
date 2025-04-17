from django.test import TestCase
from productos.models import Producto
from proveedores.models import Proveedor
from inventario.models import Inventario

class InventarioModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(nombre='Leche 1L', stock=10, unidad_medida='unidad')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor X', telefono='1234567890', correo='proveedorx@mail.com')

    def test_crear_entrada_aumenta_stock(self):
        entrada = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=5
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_crear_salida_disminuye_stock(self):
        salida = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='salida',
            cantidad=3
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)

    def test_actualizar_movimiento_ajusta_stock(self):
        entrada = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=5
        )
        entrada.cantidad = 10
        entrada.save()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 20)  # 10 original + 10 actualizada

    def test_eliminar_entrada_resta_stock(self):
        entrada = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=5
        )
        entrada.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)  # stock vuelve al original

    def test_eliminar_salida_suma_stock(self):
        salida = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='salida',
            cantidad=5
        )
        salida.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)  # stock vuelve al original
