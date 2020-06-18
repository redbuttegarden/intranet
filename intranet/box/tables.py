import django_tables2 as tables

from .models import FolderStats


class FolderStatTable(tables.Table):
    class Meta:
        model = FolderStats
        attrs = {"class": "table"}
