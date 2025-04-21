# inventario/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from proveedores.models import Categoria, Proveedor
from productos.models import Producto
from inventario.models import Inventario

class InventarioTests(APITestCase):

    def setUp(self):
        # Crear una categoría, proveedor y producto para asociarlos al inventario
        self.categoria = Categoria.objects.create(nombre="Lácteos")
        self.proveedor = Proveedor.objects.create(nombre="Proveedor 1", categoria=self.categoria)
        self.producto = Producto.objects.create(
            nombre="Leche",
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra=1.5,
            precio_venta=2.0,
            stock=50,
            unidad_medida="litro",
            activo=True
        )

        # Datos para agregar al inventario
        self.movimiento_data_entrada = {
            'producto': self.producto.id,
            'proveedor': self.proveedor.id,
            'tipo': 'entrada',
            'cantidad': 10,
        }
        
        self.movimiento_data_salida = {
            'producto': self.producto.id,
            'proveedor': self.proveedor.id,
            'tipo': 'salida',
            'cantidad': 5,
        }

    def test_agregar_entrada_al_inventario(self):
        # Verificar el stock inicial del producto
        self.assertEqual(self.producto.stock, 50)
        
        # Crear un movimiento de entrada
        url = '/api/inventario/'
        response = self.client.post(url, self.movimiento_data_entrada, format='json')
        
        # Verificar que el stock se haya incrementado correctamente
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 60)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registrar_salida_del_inventario(self):
        # Primero agregar una entrada para que haya stock
        Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=10,
        )
        
        # Verificar el stock antes de la salida
        self.assertEqual(self.producto.stock, 60)
        
        # Crear un movimiento de salida
        url = '/api/inventario/'
        response = self.client.post(url, self.movimiento_data_salida, format='json')
        
        # Verificar que el stock se haya decrementado correctamente
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 55)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_eliminar_movimiento_inventario(self):
        # Crear un movimiento de entrada
        movimiento = Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=10,
        )
        
        # Verificar el stock antes de la eliminación
        self.assertEqual(self.producto.stock, 60)
        
        # Eliminar el movimiento de inventario
        url = f'/api/inventario/{movimiento.id}/'
        response = self.client.delete(url)
        
        # Verificar que el stock se haya ajustado correctamente
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 50)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ver_movimientos_inventario(self):
        # Crear algunos movimientos de inventario
        Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='entrada',
            cantidad=10,
        )
        
        Inventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo='salida',
            cantidad=5,
        )
        
        url = '/api/inventario/'
        response = self.client.get(url)
        
        # Verificar que los movimientos fueron recuperados correctamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Debería haber 2 movimientos
