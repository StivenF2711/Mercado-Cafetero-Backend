# proveedores/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from proveedores.models import Categoria, Proveedor

class ProveedorTests(APITestCase):

    def setUp(self):
        # Crear categorías para los proveedores
        self.categoria_lacteos = Categoria.objects.create(nombre="Lácteos")
        self.categoria_aseo = Categoria.objects.create(nombre="Aseo")

        # Crear proveedores para cada categoría
        self.proveedor_1 = Proveedor.objects.create(
            nombre="Proveedor 1",
            categoria=self.categoria_lacteos,
            telefono="123456789",
            email="proveedor1@example.com",
            dias_visita="Lunes, Miércoles, Viernes"
        )

        self.proveedor_2 = Proveedor.objects.create(
            nombre="Proveedor 2",
            categoria=self.categoria_aseo,
            telefono="987654321",
            email="proveedor2@example.com",
            dias_visita="Martes, Jueves"
        )

        self.proveedor_data = {
            "nombre": "Proveedor 3",
            "categoria": self.categoria_lacteos.id,
            "telefono": "555123456",
            "email": "proveedor3@example.com",
            "dias_visita": "Lunes, Martes"
        }

    def test_crear_proveedor(self):
        url = '/api/proveedores/'  # Asumiendo que esta es la URL para crear proveedores
        response = self.client.post(url, self.proveedor_data, format='json')

        # Verificar que el proveedor se haya creado correctamente
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proveedor.objects.count(), 3)  # Verificar que hay tres proveedores
        self.assertEqual(Proveedor.objects.last().nombre, "Proveedor 3")

    def test_relacion_proveedor_categoria(self):
        # Verificar que los proveedores están correctamente asociados a su categoría
        self.assertEqual(self.proveedor_1.categoria.nombre, "Lácteos")
        self.assertEqual(self.proveedor_2.categoria.nombre, "Aseo")
        self.assertIn(self.proveedor_1, self.categoria_lacteos.proveedores.all())
        self.assertIn(self.proveedor_2, self.categoria_aseo.proveedores.all())

    def test_consultar_proveedores_por_categoria(self):
        # Verificar que podemos consultar los proveedores de una categoría
        url = f'/api/proveedores/?categoria={self.categoria_lacteos.id}'  # Endpoint para filtrar por categoría
        response = self.client.get(url)

        # Verificar que los proveedores de la categoría "Lácteos" estén en la respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Deberían estar los proveedores 1 y 3

    def test_proveedor_sin_datos_requeridos(self):
        # Intentar crear un proveedor sin los datos requeridos
        url = '/api/proveedores/'
        proveedor_incompleto = {
            "nombre": "Proveedor Incompleto",
            "telefono": "123456789",
            "email": "incompleto@example.com",
        }
        response = self.client.post(url, proveedor_incompleto, format='json')

        # Verificar que se devuelva un error debido a la falta de la categoría
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
