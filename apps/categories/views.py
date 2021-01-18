from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer, CategoryTreeSerializer


def add_node(item, parent=None):
    node = Category.add_node(item["name"], parent)

    if "children" in item and len(item["children"]):
        for child_item in item["children"]:
            add_node(child_item, node)


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        Category.objects.all().delete()
        return Response()

    def create(self, request, *args, **kwargs):
        serializer = CategoryTreeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        add_node(serializer.validated_data)

        return Response()
