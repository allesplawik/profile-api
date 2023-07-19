from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import UserProfile, Ingredient
from ingredient.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('ingredient:ingredient-list')


def detail_url(ingredient_id):
    return reverse('ingredient:ingredient-detail', args=(ingredient_id,))


def create_user(email: str, name: str, password: str) -> UserProfile:
    return get_user_model().objects.create_user(email=email, name=name, password=password)


def create_ingriedient(name: str, user: UserProfile):
    return Ingredient.objects.create(name=name, user=user)


class IngredientApiTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            name='Test User',
            password='test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_ingredients(self):
        new_user = create_user(
            email='user@example.com',
            name='User Test',
            password='testpass123'
        )
        create_ingriedient(
            name='potato',
            user=self.user
        )
        create_ingriedient(
            name='tomato',
            user=new_user
        )

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertEqual(ingredients.count(), 1)
        ingredient = ingredients[0]
        self.assertEqual(ingredient.user, self.user)

    def test_list_ingredients_limited_for_user(self):
        create_ingriedient(
            name='potato',
            user=self.user
        )
        create_ingriedient(
            name='tomato',
            user=self.user
        )

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.filter(user=self.user).order_by('-id')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient(self):
        ingredient_details = {
            'name': 'lemon',
            'user': self.user
        }

        ingredient = create_ingriedient(**ingredient_details)
        url = detail_url(ingredient.id)
        payload = {
            'name': 'lemon updated',
        }

        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])
        self.assertEqual(ingredient.user, self.user)

    def test_ingredient_partial_update(self):
        ingredient_details = {
            'name': 'lemon',
            'user': self.user
        }
        ingredient = create_ingriedient(**ingredient_details)
        url = detail_url(ingredient.id)
        payload = {
            'name': 'lemon updated',
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()

        self.assertEqual(ingredient.name, payload['name'])

    def test_update_not_owned_ingredients(self):
        user = create_user(
            email='user@example.com',
            name='User Test',
            password='testpass123'
        )

        ingredient = create_ingriedient(
            name='garlic',
            user=user
        )

        payload = {
            'name': 'garlic updated',
        }

        url = detail_url(ingredient.id)
        res = self.client.put(url, payload, format='json')
        ingredient.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ingredient.user, user)
