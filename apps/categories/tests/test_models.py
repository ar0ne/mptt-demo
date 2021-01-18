""" Unit tests for Models """

from apps.categories.models import Category
from apps.categories.tests.conftest import BaseTestCase


class TestCategoryModel(BaseTestCase):
    def test_get_parents(self):
        self.assertEqual([], list(self.main.get_parents()))
        self.assertEqual([self.main], list(self.cat1.get_parents()))
        self.assertEqual([self.cat1, self.main], list(self.cat11.get_parents()))
        self.assertEqual([self.main], list(self.cat2.get_parents()))

    def test_get_children(self):
        self.assertEqual([self.cat1, self.cat2], list(self.main.get_children()))
        self.assertEqual([], list(self.cat2.get_children()))
        self.assertEqual([self.cat11, self.cat12], list(self.cat1.get_children()))

    def test_get_all_children(self):
        self.assertEqual(
            [self.cat1, self.cat11, self.cat12, self.cat2],
            list(self.main.get_all_children()),
        )

    def test_get_siblings(self):
        self.assertEqual([], list(self.main.get_siblings()))
        self.assertEqual([self.cat2], list(self.cat1.get_siblings()))
        self.assertEqual([self.cat1], list(self.cat2.get_siblings()))

        self.assertEqual([self.cat1, self.cat2], list(self.cat1.get_siblings(True)))
        self.assertEqual([self.cat1, self.cat2], list(self.cat2.get_siblings(True)))

    def test_add_node(self):
        cat3 = Category.add_node("cat3", self.main)

        self.main.refresh_from_db()

        self.assertTrue(cat3.parent.lft < cat3.lft < cat3.parent.rgt)
        self.assertTrue(cat3.parent.lft < cat3.rgt < cat3.parent.rgt)

        cat31 = Category.add_node("cat31", cat3)

        cat3.refresh_from_db()
        self.assertTrue(cat31.parent.parent.lft < cat31.parent.lft < cat31.lft)
        self.assertTrue(cat31.lft < cat31.parent.rgt < cat31.parent.parent.rgt)
        self.assertTrue(cat31.parent.parent.lft < cat31.parent.lft < cat31.rgt)
        self.assertTrue(cat31.rgt < cat31.parent.rgt < cat31.parent.parent.rgt)

    def test_add_root_node(self):
        Category.objects.all().delete()

        new_main = Category.add_node("new_main", None)
        self.assertEqual(1, new_main.lft)
        self.assertEqual(2, new_main.rgt)
        self.assertEqual("new_main", new_main.name)
