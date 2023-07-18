from django.urls import path, include

from rest_framework.routers import DefaultRouter

from ingredient import views

router = DefaultRouter()
router.register('ingredients', views.IngredientApiViewset)

app_name = 'ingredient'

urlpatterns = [
    path('', include(router.urls))
]
