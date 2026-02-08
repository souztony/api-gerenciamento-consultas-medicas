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
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.professional = Professional.objects.create(
            social_name="Dr. Alex Lima",
            profession="Endocrinologista",
            address="Av. Paulista, 1000",
            contact="alex@email.com"
        )
        self.appointment_data = {
            "date": timezone.now().isoformat(),
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
            date=timezone.now(),
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
        invalid_data = {"date": timezone.now().isoformat()}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_appointment(self):
        """
        Garantir que podemos atualizar a data de uma consulta.
        """
        appointment = Appointment.objects.create(
            date=timezone.now(),
            professional=self.professional
        )
        update_url = reverse('appointment-detail', args=[appointment.id])
        new_date = (timezone.now() + timezone.timedelta(days=1)).isoformat()
        
        response = self.client.patch(update_url, {"date": new_date}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
