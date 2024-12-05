from django.test import TestCase, Client
from django.urls import reverse
from marieweb.models import Encargo
from django.contrib.auth.models import User
from datetime import date 

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
