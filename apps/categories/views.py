""" Category app's views """
from typing import Dict, Optional

from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer, CategoryTreeSerializer


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def add_node(self, item: Dict, parent: Optional[Category] = None) -> None:
        """ Walks through dictionary and creates child nodes """
        node = Category.add_node(item["name"], parent)

        if "children" in item and len(item["children"]):
            for child_item in item["children"]:
                self.add_node(child_item, node)

    def create(self, request, *args, **kwargs):
        """ Create category tree """
        serializer = CategoryTreeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.add_node(serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)
