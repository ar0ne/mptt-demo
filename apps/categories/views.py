from dataclasses import dataclass
from typing import List, Optional

from dacite import from_dict
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mptt_demo.apps.categories.models import Category
from mptt_demo.apps.categories.serializers import CategorySerializer


@dataclass
class NodeItem:
    name: str
    children: Optional[List["NodeItem"]]


def add_node(item, parent=None):
    node_name = item.name

    if not Category.objects.filter(name=node_name).exists():
        node = Category.add_node(node_name, parent)
    else:
        node = Category.objects.get(name=node_name)

    if item.children and len(item.children):
        for it in item.children:
            add_node(it, node)


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
        item = from_dict(data_class=NodeItem, data=request.data)

        add_node(item)

        return Response()
