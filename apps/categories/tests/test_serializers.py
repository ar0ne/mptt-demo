""" Unit tests for serializers """
from rest_framework.exceptions import ValidationError

from apps.categories.serializers import (
    CategoryModelSerializer,
    CategorySerializer,
    CategoryTreeSerializer,
)
from apps.categories.tests.conftest import BaseTestCase


class TestCategoryModelSerializer(BaseTestCase):
    """ Tests for CategoryModelSerializer """

    def test_serialization(self):
        ser = CategoryModelSerializer(self.root)
        self.assertDictEqual({"id": self.root.id, "name": self.root.name}, ser.data)


class TestCategorySerializer(BaseTestCase):
    """ Tests for CategorySerializer """

    def test_serialization(self):
        ser = CategorySerializer(self.cat1)
        self.assertDictEqual(
            {
                "id": self.cat1.id,
                "name": self.cat1.name,
                "parents": [{"id": self.root.id, "name": self.root.name}],
                "children": [
                    {
                        "id": self.cat11.id,
                        "name": self.cat11.name,
                    },
                    {"id": self.cat12.id, "name": self.cat12.name},
                ],
                "siblings": [{"id": self.cat2.id, "name": self.cat2.name}],
            },
            ser.data,
        )


class TestCategoryTreeSerializer(BaseTestCase):
    """ Tests for CategoryTreeSerializer """

    def test_not_unique_name_validation(self):
        cases = (
            {"name": self.root.name},
            {"name": "unique", "children": [{"name": self.cat2.name}]},
            {
                "name": "unique",
                "children": [
                    {"name": "unique-child", "children": [{"name": self.cat12.name}]}
                ],
            },
            {
                "name": "unique",
                "children": [
                    {
                        "name": "unique-child",
                        "children": [
                            {"name": "unique-child-child"},
                            {"name": self.cat2.name},
                        ],
                    }
                ],
            },
        )

        for data in cases:
            with self.subTest(data=data):
                with self.assertRaises(ValidationError):
                    CategoryTreeSerializer(data=data).is_valid(raise_exception=True)
