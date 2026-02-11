from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Professional

class ProfessionalTests(APITestCase):
    def setUp(self):
        # Usuário para autenticação
        self.user = User.objects.create_user(username='doctor', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Dados de exemplo
        self.professional_data = {
            'social_name': 'Dr. House',
            'profession': 'Diagnostician',
            'contact': 'house@princeton.edu',
            'address': '221B Baker Street' # Just joking with address mixing
        }
        self.url = reverse('professional-list')

    def test_create_professional(self):
        """Teste de criação de profissional"""
        response = self.client.post(self.url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)
        self.assertEqual(Professional.objects.get().social_name, 'Dr. House')

    def test_create_professional_invalid_data(self):
        """Teste de validação na criação (campos vazios)"""
        invalid_data = {
            'social_name': '',
            'profession': '',
            'contact': 'invalid-email'
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', response.data)
        self.assertIn('profession', response.data)
        self.assertIn('contact', response.data)

    def test_list_professionals(self):
        """Teste de listagem de profissionais"""
        Professional.objects.create(**self.professional_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_professional(self):
        """Teste de atualização de profissional"""
        professional = Professional.objects.create(**self.professional_data)
        detail_url = reverse('professional-detail', args=[professional.id])
        
        update_data = {
            'social_name': 'Dr. Gregory House',
            'profession': 'Medical Doctor',
            'contact': 'house@plainsboro.com',
            'address': 'Princeton-Plainsboro'
        }
        
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['social_name'], 'Dr. Gregory House')

    def test_delete_professional(self):
        """Teste de remoção de profissional"""
        professional = Professional.objects.create(**self.professional_data)
        detail_url = reverse('professional-detail', args=[professional.id])
        
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_unauthenticated_access(self):
        """Teste de acesso negado sem autenticação"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
