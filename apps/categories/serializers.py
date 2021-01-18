from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_recursive.fields import RecursiveField

from apps.categories.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class CategorySerializer(serializers.ModelSerializer):
    parents = CategoryModelSerializer(source="get_parents", many=True, read_only=True)
    children = CategoryModelSerializer(source="get_children", many=True, read_only=True)
    siblings = CategoryModelSerializer(source="get_siblings", many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parents",
            "children",
            "siblings",
        )


class CategoryTreeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=124, validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    children = serializers.ListField(child=RecursiveField(), required=False)

    class Meta:
        model = Category
        fields = (
            "name",
            "children",
        )
