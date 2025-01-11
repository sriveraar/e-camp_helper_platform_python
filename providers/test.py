from django.test import TestCase
from django.contrib.auth.models import User
from .models import Provider, Service

class ProviderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.provider = Provider.objects.create(
            user=self.user,
            phone='123456789',
            description='Proveedor de prueba'
        )
        self.service = Service.objects.create(name='Limpieza general')

    def test_provider_creation(self):
        self.assertEqual(self.provider.user.username, 'testuser')

    def test_service_addition(self):
        self.provider.services.add(self.service)
        self.assertIn(self.service, self.provider.services.all())
