import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auto_login_user(db, create_user, api_client):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(username='testuser', password='password')
        api_client.force_authenticate(user=user)
        return api_client, user
    return make_auto_login
