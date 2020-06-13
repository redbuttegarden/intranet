import django

from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=500)


class FolderStats(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    size = models.IntegerField()
    date = models.DateField(default=django.utils.timezone.now)
