from rest_framework import serializers

from mptt_demo.apps.categories.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "lft",
            "rgt",
            "parent_id",
        )


class CategorySerializer(serializers.ModelSerializer):
    parents = CategoryModelSerializer(source="get_parents", many=True)
    children = CategoryModelSerializer(source="get_children", many=True)
    siblings = CategoryModelSerializer(source="get_siblings", many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parents",
            "children",
            "siblings",
            "lft",
            "rgt",
            "parent_id",
        )
