from django.db import models, transaction
from django.db.models.expressions import F


class Category(models.Model):
    """ Model for Category"""

    name = models.CharField(unique=True, max_length=125)
    lft = models.PositiveIntegerField()
    rgt = models.PositiveIntegerField()
    parent = models.ForeignKey(
        "self", null=True, related_name="category", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    def get_parent(self):
        """ Get parent nodes """
        return Category.objects.filter(lft__lt=self.lft, rgt__gt=self.rgt).order_by(
            "rgt"
        )

    def get_all_children(self):
        """ Get all children nodes """
        return Category.objects.filter(lft__gt=self.lft, rgt__lt=self.rgt).order_by(
            "lft"
        )

    def get_children(self):
        """ Get children """
        return Category.objects.filter(parent=self).order_by("name")

    def get_siblings(self, include_self=False):
        """
        Get siblings nodes.

        :param include_self: By default excludes self node from result.
        :return:
        """
        qs = Category.objects.filter(parent=self.parent)

        if not include_self:
            qs = qs.exclude(pk=self.pk)

        return qs

    def has_children(self) -> bool:
        return Category.objects.filter(parent=self).exists()

    @classmethod
    def is_exists(cls, name) -> bool:
        return cls.objects.filter(name=name).exists()

    @classmethod
    @transaction.atomic
    def add_node(cls, name, parent):
        """ Add a child node """
        if not parent:
            # add root node
            return cls.objects.create(name=name, lft=1, rgt=2, parent=None)

        # add a node as a child of a node that has no existing children
        cls.objects.filter(rgt__gt=parent.lft).update(rgt=F("rgt") + 2)
        cls.objects.filter(lft__gt=parent.lft).update(lft=F("lft") + 2)

        return cls.objects.create(
            name=name, lft=parent.lft + 1, rgt=parent.lft + 2, parent=parent
        )

    class Meta:
        ordering = ["name"]
