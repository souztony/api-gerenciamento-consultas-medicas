from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Professional

class ProfessionalTests(APITestCase):
    def setUp(self):
        # Criar usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Obter token JWT
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'password123'
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.professional_data = {
            "social_name": "Dr. Joane Silva",
            "profession": "Psicóloga",
            "address": "Rua das Flores, 123",
            "contact": "joanesilva@email.com"
        }
        self.url = reverse('professional-list')

    def test_create_professional(self):
        """
        Garantir que podemos criar um novo profissional (Autenticado).
        """
        response = self.client.post(self.url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)
        self.assertEqual(Professional.objects.get().social_name, 'Dr. Joane Silva')

    def test_create_professional_unauthenticated(self):
        """
        Garantir que não podemos criar profissional sem autenticação.
        """
        self.client.credentials() # Limpar tokens
        response = self.client.post(self.url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_professionals(self):
        """
        Garantir que podemos listar profissionais.
        """
        Professional.objects.create(**self.professional_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_professional(self):
        """
        Garantir que podemos atualizar um profissional.
        """
        professional = Professional.objects.create(**self.professional_data)
        update_url = reverse('professional-detail', args=[professional.id])
        updated_data = self.professional_data.copy()
        updated_data['social_name'] = "Dr. Joane Santos"
        
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(professional.social_name, 'Dr. Joane Santos')

    def test_delete_professional(self):
        """
        Garantir que podemos deletar um profissional.
        """
        professional = Professional.objects.create(**self.professional_data)
        delete_url = reverse('professional-detail', args=[professional.id])
        
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_create_professional_invalid_data(self):
        """
        Garantir que dados inválidos retornam erro.
        """
        invalid_data = self.professional_data.copy()
        invalid_data['social_name'] = "" # Campo obrigatório vazio
        
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_professional_short_name(self):
        """
        Garantir que nome muito curto retorna erro de validação.
        """
        invalid_data = self.professional_data.copy()
        invalid_data['social_name'] = "Dr"
        
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('social_name', response.data)
    
    def test_create_professional_invalid_contact(self):
        """
        Garantir que contato inválido retorna erro.
        """
        invalid_data = self.professional_data.copy()
        invalid_data['contact'] = "contato-invalido"
        
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact', response.data)
    
    def test_create_professional_valid_phone(self):
        """
        Garantir que telefone válido é aceito.
        """
        valid_data = self.professional_data.copy()
        valid_data['contact'] = "(11) 98888-7777"
        
        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_professional_not_found(self):
        """
        Garantir que buscar profissional inexistente retorna 404.
        """
        url = reverse('professional-detail', args=[9999])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_professional_unauthenticated(self):
        """
        Garantir que não podemos atualizar sem autenticação.
        """
        professional = Professional.objects.create(**self.professional_data)
        update_url = reverse('professional-detail', args=[professional.id])
        self.client.credentials()
        
        response = self.client.put(update_url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_professional_unauthenticated(self):
        """
        Garantir que não podemos deletar sem autenticação.
        """
        professional = Professional.objects.create(**self.professional_data)
        delete_url = reverse('professional-detail', args=[professional.id])
        self.client.credentials()
        
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
