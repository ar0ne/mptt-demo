from typing import Optional

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
        return self.__class__.objects.filter(
            lft__lt=self.lft, rgt__gt=self.rgt
        ).order_by("rgt")

    def get_all_children(self) -> "QuerySet[MPTTModel]":
        return self.__class__.objects.filter(
            lft__gt=self.lft, rgt__lt=self.rgt
        ).order_by("lft")

    def get_children(self) -> "QuerySet[MPTTModel]":
        return self.__class__.objects.filter(parent=self).order_by("name")

    def get_siblings(self, include_self=False):
        qs = self.__class__.objects.filter(parent=self.parent)

        if not include_self:
            qs = qs.exclude(pk=self.pk)

        return qs

    def has_children(self) -> bool:
        return self.__class__.objects.filter(parent=self).exists()

    @classmethod
    @transaction.atomic
    def add_node(cls, name: str, parent: Optional["MPTTModel"] = None) -> "MPTTModel":
        if not parent:
            # add a root node
            return cls.objects.create(name=name, lft=1, rgt=2, parent=None)

        cls.objects.filter(rgt__gt=parent.lft).update(rgt=F("rgt") + 2)
        cls.objects.filter(lft__gt=parent.lft).update(lft=F("lft") + 2)

        return cls.objects.create(
            name=name, lft=parent.lft + 1, rgt=parent.lft + 2, parent=parent
        )

    objects = models.Manager()

    def __str__(self):
        return f"{self.id} - {self.name}"
