from rest_framework import viewsets, permissions, authentication

from recipe.serializers import RecipeSerializer, DetailRecipeSerializer

from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = DetailRecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class
