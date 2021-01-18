""" Tests for views """
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.categories.tests.conftest import BaseTestCase


class TestCategoryViewSet(BaseTestCase):
    """ Tests for CategoryViewSet """

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_get_category_by_id(self):
        """ Tests getting category by id """
        response = self.client.get(f"/categories/{self.root.id}/", format="json")

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "id": self.root.id,
                "name": self.root.name,
                "parents": [],
                "children": [
                    {"id": self.cat1.id, "name": self.cat1.name},
                    {"id": self.cat2.id, "name": self.cat2.name},
                ],
                "siblings": [],
            },
            response.json(),
        )

    def test_add_category(self):
        """ Tests adding new category """
        count = Category.objects.all().count()

        response = self.client.post(
            "/categories/",
            {
                "name": "cat3",
                "children": [
                    {"name": "cat31"},
                    {"name": "cat32", "children": [{"name": "cat321"}]},
                ],
            },
            format="json",
        )
        self.assertEqual(204, response.status_code)
        self.assertEqual(count + 4, Category.objects.all().count())

        cat3 = Category.objects.get(name="cat3")
        self.assertEqual(self.root, cat3.parent)

        cat31 = Category.objects.get(name="cat31")
        self.assertEqual(cat3, cat31.parent)

        cat32 = Category.objects.get(name="cat32")
        self.assertEqual(cat3, cat32.parent)

        cat321 = Category.objects.get(name="cat321")
        self.assertEqual(cat32, cat321.parent)
