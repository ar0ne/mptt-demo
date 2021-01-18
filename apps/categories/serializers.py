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
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()

    def get_parents(self, obj):
        return CategoryModelSerializer(obj.get_parent(), many=True).data

    def get_children(self, obj):
        return CategoryModelSerializer(obj.get_children(), many=True).data

    def get_siblings(self, obj):
        return CategoryModelSerializer(obj.get_siblings(), many=True).data

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
