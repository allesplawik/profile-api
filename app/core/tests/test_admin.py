"""Admin for managing models."""
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model

from django.urls import reverse

from core.models import Ingredient


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_ingredient(**params):
    return Ingredient.objects.create(**params)


class UserAdmin(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email='user@example.com',
            name='User Test',
            password='test123'
        )
        self.admin = create_superuser(
            email='test@example.com',
            name='Test Admin',
            password='test123'
        )
        self.client = Client()
        self.client.force_login(self.admin)

    def test_user_list(self):
        """Testing if user list is displayed."""
        url = reverse('admin:core_userprofile_changelist')

        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_add_user_objects(self):
        """Testing if user detail is shown."""
        url = reverse('admin:core_userprofile_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_change(self):
        """Testing edit page."""
        url = reverse('admin:core_userprofile_change', args=(self.user.id,))
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)


class IngredientAdminTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email='user@example.com',
            name='User Test',
            password='test123'
        )
        self.admin = create_superuser(
            email='test@example.com',
            name='Test Admin',
            password='test123'
        )
        self.client = Client()
        self.client.force_login(self.admin)

    def test_ingredients_list(self):
        ingredient = create_ingredient(
            name='Onion',
            amount=100,
            user=self.user
        )
        url = reverse('admin:core_ingredient_changelist')

        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, ingredient.name)
        self.assertContains(res, ingredient.amount)
