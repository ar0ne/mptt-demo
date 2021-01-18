from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from mptt_demo.apps.categories.models import Category
from mptt_demo.apps.categories.serializers import CategorySerializer


class CategoryViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
