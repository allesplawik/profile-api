from rest_framework import serializers

from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'amount']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return Ingredient.objects.create(**validated_data, user=user)

    def update(self, instance, validated_data):

        """Custom approach"""
        # for key, value in validated_data.items():
        #     setattr(instance, key, value)
        # instance.save()
        # return instance
        return super().update(instance, validated_data)
