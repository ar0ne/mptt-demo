from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=125)
    lft = models.PositiveIntegerField()
    rgt = models.PositiveIntegerField()
    parent = models.ForeignKey(
        "self", null=True, related_name="category", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    def get_parent(self):
        return Category.objects.filter(lft__lt=self.lft, rgt__gt=self.rgt).order_by(
            "rgt"
        )

    def get_children(self):
        return Category.objects.filter(lft__gt=self.lft, rgt__lt=self.rgt).order_by(
            "lft"
        )

    def get_siblings(self, include_self=False):
        qs = Category.objects.filter(parent=self.parent)

        if not include_self:
            qs = qs.exclude(pk=self.pk)

        return qs

    class Meta:
        ordering = ["name"]
