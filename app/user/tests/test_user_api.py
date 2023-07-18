"""Test user API."""

from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

CREATE_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(email: str, name: str, password: str):
    return get_user_model().objects.create_user(email, name, password)


class PublicUserApiTest(TestCase):
    """Testing public user API."""

    def test_create_user(self):
        payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'test123'
        }

        res = self.client.post(CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email='test@example.com')

        self.assertEqual(str(user), payload['email'])
        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_email(self):
        payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'test123'
        }

        create_user(**payload)

        res = self.client.post(CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'test'
        }

        res = self.client.post(CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):

        user_details = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload, format='json')

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_details_unauthorized(self):
        """Get user details for unauthorized users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_details(self):
        """Test retrieving user details."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Post to me not allowed."""

        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile(self):
        payload = {
            'name': 'Admin updated',
            'password': 'password updated'
        }

        res = self.client.patch(ME_URL, payload, format='json')
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
