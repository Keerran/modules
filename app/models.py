from django.db import models


# Create your models here.
class Module(models.Model):
    code = models.TextField(primary_key=True, max_length=13)
    name = models.TextField(max_length=100)
    year = models.PositiveSmallIntegerField()
    desc = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Parent(models.Model):
    parent = models.ForeignKey(Module, related_name="parent", on_delete=models.CASCADE)
    child = models.ForeignKey(Module, related_name="child", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parent.name} -> {self.child.name}"
