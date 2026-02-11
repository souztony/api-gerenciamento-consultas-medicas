from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.professionals.models import Professional


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.username = 'authuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.professionals_url = reverse('professional-list')

        Professional.objects.create(
            social_name='Dra. Maria Lopes',
            profession='Clínica Geral',
            address='Rua A, 100',
            contact='maria@email.com',
        )

    def test_obtain_jwt_token_success(self):
        response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_jwt_token_invalid_credentials(self):
        response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': 'senha-incorreta'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_jwt_token_success(self):
        token_response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        response = self.client.post(
            self.refresh_url,
            {'refresh': token_response.data['refresh']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_jwt_token_invalid_token(self):
        response = self.client.post(
            self.refresh_url,
            {'refresh': 'token-invalido'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_requires_authentication(self):
        response = self.client.get(self.professionals_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_accepts_valid_jwt(self):
        token_response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json',
        )
        access_token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.professionals_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_security_headers_are_present(self):
        response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['Referrer-Policy'], 'strict-origin-when-cross-origin')
        self.assertEqual(response['Cross-Origin-Opener-Policy'], 'same-origin')

    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ),
            'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.UserRateThrottle',
                'rest_framework.throttling.AnonRateThrottle',
            ],
            'DEFAULT_THROTTLE_RATES': {'user': '2/min', 'anon': '2/min'},
        }
    )
    def test_authenticated_requests_are_throttled(self):
        token_response = self.client.post(
            self.token_url,
            {'username': self.username, 'password': self.password},
            format='json',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")

        first = self.client.get(self.professionals_url, format='json')
        second = self.client.get(self.professionals_url, format='json')
        third = self.client.get(self.professionals_url, format='json')

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(third.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
