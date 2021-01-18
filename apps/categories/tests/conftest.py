from django.test.testcases import TestCase

from apps.categories.models import Category


class BaseTestCase(TestCase):
    def setUp(self):
        self.main = Category.objects.create(name="main", lft=1, rgt=10, parent=None)
        self.cat1 = Category.objects.create(name="cat1", lft=2, rgt=7, parent=self.main)
        self.cat11 = Category.objects.create(
            name="cat11", lft=3, rgt=4, parent=self.cat1
        )
        self.cat12 = Category.objects.create(
            name="cat12", lft=5, rgt=6, parent=self.cat1
        )
        self.cat2 = Category.objects.create(name="cat2", lft=8, rgt=9, parent=self.main)
