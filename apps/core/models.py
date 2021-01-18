from typing import Optional, Tuple

from django.db import models, transaction
from django.db.models.expressions import F
from django.db.models.query import QuerySet


class MPTTModel(models.Model):
    """ Base class for MPTT models """

    name = models.CharField(unique=True, max_length=125)
    lft = models.PositiveIntegerField()
    rgt = models.PositiveIntegerField()
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        ordering = ["name"]

    def get_parents(self) -> "QuerySet[MPTTModel]":
        """ Get parent nodes """
        return self.__class__.objects.filter(
            lft__lt=self.lft, rgt__gt=self.rgt
        ).order_by("rgt")

    def get_all_children(self) -> "QuerySet[MPTTModel]":
        """ Get all children nodes"""
        return self.__class__.objects.filter(
            lft__gt=self.lft, rgt__lt=self.rgt
        ).order_by("lft")

    def get_children(self) -> "QuerySet[MPTTModel]":
        """ Get children nodes"""
        return self.__class__.objects.filter(parent=self).order_by("name")

    def get_siblings(self, include_self=False) -> "QuerySet[MPTTModel]":
        """ Get siblings nodes """
        qs = self.__class__.objects.filter(parent=self.parent)

        if not include_self:
            qs = qs.exclude(pk=self.pk)

        return qs

    @classmethod
    @transaction.atomic
    def add_node(cls, name: str, parent: Optional["MPTTModel"] = None) -> "MPTTModel":
        """
        Adds new child node. Let's assume that there is only one root node.

        :param str name: An unique name of node.
        :param Optional[MPTTModel] parent: A parent node if exists. Otherwise, create a root node.
        :return New node in tree.
        """
        if not parent:
            # add a root node if not exists yet
            root, created = cls.objects.get_or_create(
                parent=None, defaults={"name": name, "lft": 1, "rgt": 2}
            )  # type: Tuple[MPTTModel, bool]
            if created:
                return root
            parent = root

        cls.objects.filter(rgt__gt=parent.lft).update(rgt=F("rgt") + 2)
        cls.objects.filter(lft__gt=parent.lft).update(lft=F("lft") + 2)

        return cls.objects.create(
            name=name, lft=parent.lft + 1, rgt=parent.lft + 2, parent=parent
        )

    objects = models.Manager()
