# productos/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from proveedores.models import Categoria, Proveedor
from productos.models import Producto

class ProductoTests(APITestCase):

    def setUp(self):
        # Crear una categoría y un proveedor para asociarlos al producto
        self.categoria = Categoria.objects.create(nombre="Lácteos")
        self.proveedor = Proveedor.objects.create(nombre="Proveedor 1", categoria=self.categoria)

        # Crear un producto de prueba
        self.producto_data = {
            'nombre': 'Leche',
            'categoria': self.categoria.id,
            'proveedor': self.proveedor.id,
            'precio_compra': 1.5,
            'precio_venta': 2.0,
            'stock': 50,
            'unidad_medida': 'litro',
            'activo': True,
        }

    def test_crear_producto(self):
        url = '/api/productos/'
        response = self.client.post(url, self.producto_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Leche')

    def test_actualizar_producto(self):
        # Crear un producto
        producto = Producto.objects.create(
            nombre='Yogurt',
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra=1.0,
            precio_venta=1.5,
            stock=20,
            unidad_medida='unidad',
        )
        
        url = f'/api/productos/{producto.id}/'
        updated_data = {'stock': 25}
        response = self.client.patch(url, updated_data, format='json')
        producto.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(producto.stock, 25)

    def test_crear_producto_sin_datos_requeridos(self):
        url = '/api/productos/'
        incomplete_data = {
            'nombre': 'Leche',
            # Faltan 'categoria', 'proveedor', 'precio_compra', 'precio_venta'
            'stock': 50
        }
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_inventario(self):
        # Crear productos
        Producto.objects.create(
            nombre='Leche',
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra=1.5,
            precio_venta=2.0,
            stock=50,
            unidad_medida='litro',
            activo=True,
        )
        
        url = '/api/productos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica que haya al menos un producto
