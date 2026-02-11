from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password,
            email='test@example.com'
        )
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

    def test_get_token_success(self):
        """Teste para obter token JWT com credenciais válidas"""
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_token_invalid_credentials(self):
        """Teste de falha ao obter token com credenciais inválidas"""
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        """Teste para renovar o token de acesso"""
        # Primeiro obtém o token
        data = {
            'username': self.username,
            'password': self.password
        }
        login_response = self.client.post(self.token_url, data, format='json')
        refresh_token = login_response.data['refresh']

        # Tenta renovar
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
