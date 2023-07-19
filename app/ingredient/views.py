from rest_framework import viewsets
from rest_framework import permissions, authentication

from ingredient.serializers import IngredientSerializer

from core.models import Ingredient


class IngredientApiViewset(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
