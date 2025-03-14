from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser

class AuthTestCase(APITestCase):
    def test_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'strongpass123',
            'password2': 'strongpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_login(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='strongpass123'
        )
        data = {'email': 'test@example.com', 'password': 'strongpass123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)