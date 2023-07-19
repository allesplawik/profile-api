from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

from decimal import Decimal


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_recipe(user, **params):
    defaults = {
        'title': 'Lazagne',
        'time_minutes': 60,
        'price': Decimal('5.30'),
        'description': 'Italiaz lazagne'

    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=(recipe_id,))


class PublicRecipeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_recipe_unauthorized(self):
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email='user@example.com',
            name='user',
            password='pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipe(self):
        create_recipe(
            user=self.user,
            title='Potato soup',
        )

        create_recipe(
            user=self.user,
            title='Spaggethi',
        )

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_limited_recipe(self):
        new_user = create_user(
            email='new_user@example.com',
            name="New User",
            password="userpass123"
        )
        create_recipe(
            user=self.user,
            title='Potato soup'
        )
        create_recipe(
            user=new_user,
            title='Pasta'
        )

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        payload = {
            'title': "Soup",
            'time_minutes': 60,
            'price': Decimal('5.25'),
            'description': 'Test soup'
        }

        res = self.client.post(RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(user=self.user)

        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.title, payload['title'])

    def test_partial_update_recipe(self):
        origin_price = Decimal('13.50')
        recipe = create_recipe(
            user=self.user,
            price=origin_price
        )
        payload = {
            'title': 'Italian lazagne',
            'time_minutes': 100,
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, origin_price)

    def test_update_user_error(self):
        new_user = create_user(
            email='new_user@example.com',
            name="New User",
            password="userpass123"
        )

        recipe = create_recipe(
            user=self.user
        )
        payload = {
            'user': new_user.id
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload, format='json')
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        recipe = create_recipe(
            user=self.user
        )

        payload = {
            'title': "Updated recipe",
            'time_minutes': 10,
            'price': Decimal('10.00'),
            'description': 'Italiaz lazagne updated'
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload, format='json')
        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

    def test_delete(self):
        recipe = create_recipe(
            user=self.user
        )

        url = detail_url(recipe.id)

        res = self.client.delete(url)
        recipes_exists = Recipe.objects.filter(user=self.user).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(recipes_exists)

    def test_delete_error(self):
        new_user = create_user(
            email='newuser@example.com',
            name='New User',
            password='testpass123'
        )
        recipe = create_recipe(
            user=new_user
        )

        url = detail_url(recipe.id)
        self.client.delete(url)

        recipes_exists = Recipe.objects.filter(user=new_user).exists()
        self.assertTrue(recipes_exists)

    def test_create_recipe_create_ingredient(self):
        payload = {
            'title': 'Pizza',
            'time_minutes': 15,
            'price': Decimal('5.75'),
            'description': 'Pizza italiana from Florence',
            'ingredients': [
                {
                    'name': 'potato',
                },
                {
                    'name': 'cheese',
                }
            ]
        }

        res = self.client.post(RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(user=self.user)
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertEqual(recipe.user, self.user)
