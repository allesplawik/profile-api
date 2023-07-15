from django.test import TestCase

from core.models import UserProfile

from django.contrib.auth import get_user_model


def create_user(email: str, name: str, password: str) -> UserProfile:
    return get_user_model().objects.create_user(email=email, name=name, password=password)


def create_superuser(email: str, name: str, password: str) -> UserProfile:
    return get_user_model().objects.create_superuser(email=email, name=name, password=password)


class UserProfileTest(TestCase):
    """Testsing UserProfile model."""

    def setUp(self) -> None:
        self.creds = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123'
        }
        self.user = create_user(**self.creds)

    def test_create_user(self):
        self.assertEqual(str(self.user), self.creds['email'])
        self.assertTrue(self.user.check_password(self.creds['password']))

    def test_create_user_with_error(self):
        with self.assertRaises(ValueError):
            create_user(
                email='',
                name='User',
                password='test123'
            )

    def test_create_user_with_normalize_email(self):
        emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['test3@Example.Com', 'test3@example.com'],
            ['Test4@example.COM', 'Test4@example.com']
        ]

        for email, expacted in emails:
            user = create_user(email=email, name=email.split('@')[0].lower(), password='test123')
            self.assertEqual(str(user), expacted)

    def test_short_name_of_user(self):
        name = self.user.get_short_name()
        self.assertEqual(name, self.creds['name'])

    def test_full_name_of_user(self):
        full_name = self.user.get_full_name()
        self.assertEqual(full_name, self.creds['name'])

    def test_create_superuser(self):
        """Test creating a super user in the system."""
        creds = {
            'email': 'admin@example.com',
            'name': 'admin',
            'password': 'test123',
        }

        user = create_superuser(**creds)

        self.assertEqual(str(user), creds['email'])
        self.assertTrue(user.check_password(creds['password']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
