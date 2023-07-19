from django.test import TestCase

from core.models import UserProfile, Ingredient, Recipe

from django.contrib.auth import get_user_model

from decimal import Decimal


def create_user(email: str, name: str, password: str) -> UserProfile:
    return get_user_model().objects.create_user(email=email, name=name, password=password)


def create_superuser(email: str, name: str, password: str) -> UserProfile:
    return get_user_model().objects.create_superuser(email=email, name=name, password=password)


def create_ingriedient(name: str, user: UserProfile):
    return Ingredient.objects.create(name=name, user=user)


def create_recipe(**params) -> Recipe:
    return Recipe.objects.create(**params)


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


class IngredientsModelTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )

    def test_create_ingredient_object(self):
        ingredient_details = {
            'name': 'potato',
            'user': self.user
        }

        ingredient = create_ingriedient(**ingredient_details)

        self.assertEqual(str(ingredient), ingredient_details['name'])
        self.assertEqual(ingredient.user, self.user)


class RecipeModelTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )

    def test_create_recipe(self):
        recipe_details = {
            'user': self.user,
            'title': 'Spaghetti',
            'time_minutes': 45,
            'price': Decimal('5.50'),
            'description': 'Spaghetti description'
        }
        recipe = create_recipe(**recipe_details)

        self.assertEqual(recipe.user, self.user)
        self.assertEqual(str(recipe), recipe.title)
