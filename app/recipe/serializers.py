from rest_framework import serializers

from core.models import Recipe, Ingredient

from ingredient.serializers import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_ingredients(self, ingredients, recipe):
        user = self.context['request'].user

        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=user, **ingredient
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe


class DetailRecipeSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
