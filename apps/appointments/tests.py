from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.professionals.models import Professional
from .models import Appointment
from django.utils import timezone

class AppointmentTests(APITestCase):
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

        self.professional = Professional.objects.create(
            social_name="Dr. Alex Lima",
            profession="Endocrinologista",
            address="Av. Paulista, 1000",
            contact="alex@email.com"
        )
        self.appointment_data = {
            "date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "professional": self.professional.id
        }
        self.url = reverse('appointment-list')

    def test_create_appointment(self):
        """
        Garantir que podemos criar uma nova consulta (Autenticado).
        Simula também o acionamento do mock da Asaas (verificável via logs).
        """
        response = self.client.post(self.url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.get().professional, self.professional)

    def test_create_appointment_unauthenticated(self):
        """
        Garantir que não podemos criar consulta sem autenticação.
        """
        self.client.credentials()
        response = self.client.post(self.url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_appointments_by_professional_id(self):
        """
        Garantir que podemos buscar consultas pelo ID do profissional.
        """
        Appointment.objects.create(
            date=timezone.now() + timezone.timedelta(days=1),
            professional=self.professional
        )
        # Buscar filtrando por professional_id
        response = self.client.get(f"{self.url}?professional_id={self.professional.id}", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_appointment_missing_professional(self):
        """
        Garantir que falha ao tentar criar consulta sem profissional.
        """
        invalid_data = {"date": (timezone.now() + timezone.timedelta(days=1)).isoformat()}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_appointment(self):
        """
        Garantir que podemos atualizar a data de uma consulta.
        """
        appointment = Appointment.objects.create(
            date=timezone.now() + timezone.timedelta(days=1),
            professional=self.professional
        )
        update_url = reverse('appointment-detail', args=[appointment.id])
        new_date = (timezone.now() + timezone.timedelta(days=2)).isoformat()
        
        response = self.client.patch(update_url, {"date": new_date}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
    
    def test_create_appointment_past_date(self):
        """
        Garantir que não podemos criar consulta com data no passado.
        """
        invalid_data = self.appointment_data.copy()
        invalid_data['date'] = (timezone.now() - timezone.timedelta(days=1)).isoformat()
        
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
    
    def test_create_appointment_invalid_professional(self):
        """
        Garantir que criar consulta com profissional inexistente retorna erro.
        """
        invalid_data = self.appointment_data.copy()
        invalid_data['professional'] = 9999
        
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_appointment_not_found(self):
        """
        Garantir que buscar consulta inexistente retorna 404.
        """
        url = reverse('appointment-detail', args=[9999])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_appointment(self):
        """
        Garantir que podemos deletar uma consulta.
        """
        appointment = Appointment.objects.create(
            date=timezone.now() + timezone.timedelta(days=1),
            professional=self.professional
        )
        delete_url = reverse('appointment-detail', args=[appointment.id])
        
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
    
    def test_delete_appointment_unauthenticated(self):
        """
        Garantir que não podemos deletar consulta sem autenticação.
        """
        appointment = Appointment.objects.create(
            date=timezone.now() + timezone.timedelta(days=1),
            professional=self.professional
        )
        delete_url = reverse('appointment-detail', args=[appointment.id])
        self.client.credentials()
        
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_appointments_unauthenticated(self):
        """
        Garantir que não podemos listar consultas sem autenticação.
        """
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
