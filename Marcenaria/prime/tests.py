from django.test import TestCase
from .models import Cliente
from django.urls import reverse

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Henrique",
            email="henrique@example.com",
            telefone1="(11) 99999-9999"  
        )

    def test_cliente_criado(self):
        cliente = Cliente.objects.get(nome="Henrique")
        self.assertEqual(cliente.email, "henrique@example.com")
        self.assertEqual(cliente.telefone1, "(11) 99999-9999")

class ClienteViewTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Maria",
            email="maria@example.com",
            telefone1="(11)8888-8888"
        )

    def test_lista_clientes(self):
        response = self.client.get(reverse('lista_clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria")

class ClienteFormTest(TestCase):
    def test_criar_cliente_formulario(self):
        response = self.client.post(reverse('clientes'), {
            'nome': 'João',
            'email': 'joao@example.com',
            'telefone1': '(11)7777-7777'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertTrue(Cliente.objects.filter(nome="João").exists())

