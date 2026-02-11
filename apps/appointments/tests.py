from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.professionals.models import Professional
from .models import Appointment

class AppointmentTests(APITestCase):
    def setUp(self):
        # Usuário para autenticação
        self.user = User.objects.create_user(username='patient', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Profissional necessário para a consulta
        self.professional = Professional.objects.create(
            social_name='Dr. Strange',
            profession='Sorcerer Supreme',
            contact='strange@sanctum.com',
            address='177A Bleecker Street'
        )
        
        self.url = reverse('appointment-list')
        self.future_date = timezone.now() + timedelta(days=1)

    def test_create_appointment(self):
        """Teste de agendamento de consulta"""
        data = {
            'professional': self.professional.id,
            'date': self.future_date
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_create_appointment_past_date(self):
        """Teste de validação: impedir agendamento no passado"""
        past_date = timezone.now() - timedelta(days=1)
        data = {
            'professional': self.professional.id,
            'date': past_date
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)

    def test_create_appointment_invalid_professional(self):
        """Teste de validação: profissional inexistente"""
        data = {
            'professional': 9999, # ID inexistente
            'date': self.future_date
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_appointments_filter_by_professional(self):
        """Teste de listagem com filtro por profissional"""
        # Cria consulta para este profissional
        Appointment.objects.create(professional=self.professional, date=self.future_date)
        
        # Cria outro profissional e consulta para testar filtro
        other_prof = Professional.objects.create(
            social_name='Dr. Who', 
            profession='Time Lord', 
            contact='tardis@bbc.com'
        )
        Appointment.objects.create(professional=other_prof, date=self.future_date)
        
        # Filtra pelo primeiro profissional
        response = self.client.get(f'{self.url}?professional_id={self.professional.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['professional'], self.professional.id)
