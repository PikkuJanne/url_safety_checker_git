from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import URL
from unittest.mock import patch

class URLCheckerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = 'https://www.google.com/'

    def test_user_registration(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_user_login(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_302_FOUND])

    @patch('url_checker.views.check_url_with_google_safe_browsing')
    def test_submit_url(self, mock_check_url):
        
        mock_check_url.return_value = False
        self.client.force_authenticate(user=self.user)
    
        data = {"url": "https://www.google.com/"}  
    
        response = self.client.post(reverse('submit_url'), data, format='json', follow = True)
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    


