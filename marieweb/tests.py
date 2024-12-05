from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from marieweb.models import Categoria, Encargo, Producto
from django.contrib.auth.models import User
from datetime import date
from time import time
from rest_framework.test import APITestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class EncargoModelTest(TestCase):
    def setUp(self):
        self.encargo = Encargo.objects.create(
            encargo_nombre_producto="Producto de prueba",
            encargo_cantidad_producto=10,
            encargo_fecha=date(2024, 12, 10),  # Aquí aseguramos usar un objeto 'date'
            encargo_comentario_extra="Comentario de prueba",
            encargo_estado="en_proceso"
        )

    def test_encargo_creation(self):
        print(f"Tipo de encargo_fecha: {type(self.encargo.encargo_fecha)}")
        print(f"Valor de encargo_fecha: {self.encargo.encargo_fecha}")

        fecha = self.encargo.encargo_fecha
        if isinstance(fecha, str): 
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date() 

        self.assertEqual(self.encargo.encargo_nombre_producto, "Producto de prueba")
        self.assertEqual(self.encargo.encargo_cantidad_producto, 10)
        self.assertEqual(fecha.strftime('%Y-%m-%d'), "2024-12-10") 
        self.assertEqual(self.encargo.encargo_comentario_extra, "Comentario de prueba")
        self.assertEqual(self.encargo.encargo_estado, "en_proceso")
        

    def test_encargo_estado_choices(self):
        choices = dict(Encargo.ESTADOS)
        self.assertIn(self.encargo.encargo_estado, choices.keys())


class CrearEncargoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_crear_encargo_view_get(self):
        response = self.client.get(reverse('crear_encargo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crear_encargo.html')

    def test_crear_encargo_view_post(self):
        response = self.client.post(reverse('crear_encargo'), {
            'encargo_nombre_producto': 'Producto de prueba',
            'encargo_cantidad_producto': 5,
            'encargo_fecha': '2024-12-15',
            'encargo_comentario_extra': 'Comentario adicional'
        })
        self.assertEqual(response.status_code, 302)  # Redirección exitosa
        self.assertTrue(Encargo.objects.filter(encargo_nombre_producto='Producto de prueba').exists())


class MisEncargosViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Encargo.objects.create(
            encargo_nombre_producto="Producto de prueba",
            encargo_cantidad_producto=10,
            encargo_fecha="2024-12-10",
            encargo_comentario_extra="Comentario de prueba",
            encargo_estado="en_proceso"
        )

    def test_mis_encargos_view(self):
        response = self.client.get(reverse('mis_encargos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mis_encargos.html')
        self.assertContains(response, "Producto de prueba")


#Pruebas unitest de katy a ashley
class AuthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="SecurePass123"
        )
        self.login_url = reverse("login")  
        self.logout_url = reverse("logout") 
        self.password_reset_url = reverse("password_reset")  

    def test_valid_authentication(self):
        """
        Validar autenticación exitosa con credenciales válidas.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "SecurePass123"
        })
        self.assertEqual(response.status_code, 302)  
        self.assertIn("_auth_user_id", self.client.session)  

    def test_invalid_authentication(self):
        """
        Probar manejo de credenciales inválidas y mostrar mensajes de error.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "WrongPass123"
        })
        self.assertEqual(response.status_code, 200)  
        self.assertNotIn("_auth_user_id", self.client.session) 

    def test_password_reset_flow(self):
        """
        Verificar el flujo completo de recuperación de contraseña.
        """
        response = self.client.post(self.password_reset_url, {
            "email": "testuser@example.com"
        })
        self.assertEqual(response.status_code, 302)  

    def test_logout_clears_session(self):
        """
        Confirmar que el cierre de sesión elimina la sesión del usuario.
        """
        self.client.login(username="testuser", password="SecurePass123")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  
        self.assertNotIn("_auth_user_id", self.client.session)  


#-------Tests #21 Gestionar Existencia de Productos--------#

class TestAgregarProducto(APITestCase):
    def setUp(self):
        # Crear un usuario y autenticarse
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Crear una categoría para pruebas
        self.categoria = Categoria.objects.create(nombre="Libros")
    
    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'jpeg')
        file.seek(0)
        return SimpleUploadedFile('test_image.jpg', file.read(), content_type='image/jpeg')

    def test_agregar_producto(self):
        url = reverse('add_producto')
        data = {
            "nombre": "Babel",
            "precio": 100,
            "descripcion": "Babel libro",
            "stock": 5,
            "categoria": self.categoria.id,
            "enabled": True,
            "imagen": self.create_test_image(),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre='Babel').exists())
        

class TestEliminarProducto(APITestCase):
    def setUp(self):
        # Crear un usuario y autenticarse
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Crear una categoría para pruebas
        self.categoria = Categoria.objects.create(nombre="Libros")
        
        # Crear un producto para eliminar
        self.producto = Producto.objects.create(
            nombre="Producto de Prueba",
            descripcion="Descripción de prueba",
            precio=100,
            stock=10,
            categoria=self.categoria,
            enabled=True
        )

    def test_eliminar_producto(self):
        url = reverse('gestionar_productos', args=[self.producto.id])
        response = self.client.post(url, data={"delete": "delete"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())


class TestModificarProducto(APITestCase):
    def setUp(self):
        # Crear un usuario y autenticarse
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Crear una categoría para pruebas
        self.categoria = Categoria.objects.create(nombre="Ropa")
        
        # Crear un producto para modificar
        self.producto = Producto.objects.create(
            nombre="Camisa de algodón",
            descripcion="Camisa blanca de algodón",
            precio=20,
            stock=100,
            categoria=self.categoria,
            enabled=True
        )

    def test_modificar_producto(self):
        url = reverse('gestionar_productos', args=[self.producto.id])

        # Datos actualizados
        nuevos_datos = {
            "nombre": "Camisa de lino",
            "descripcion": "Camisa gris de lino",
            "precio": 25,
            "stock": 80,
            "enabled": True
        }

        inicio_tiempo = time()

        response = self.client.post(url, data=nuevos_datos)

        tiempo_transcurrido = time() - inicio_tiempo
        self.assertLessEqual(tiempo_transcurrido, 5, "El tiempo de respuesta superó los 5 segundos")

        self.assertEqual(response.status_code, 302)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Camisa de lino")
        self.assertEqual(self.producto.precio, 25)
        self.assertEqual(self.producto.stock, 80)
        self.assertEqual(self.producto.descripcion, "Camisa gris de lino")
