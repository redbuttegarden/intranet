import django

from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class FolderStats(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    size = models.IntegerField(verbose_name="Size (KB)")
    date = models.DateField(default=django.utils.timezone.now)
