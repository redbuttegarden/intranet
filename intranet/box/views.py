from django.shortcuts import render

from django_tables2 import RequestConfig

from .models import FolderStats
from .tables import FolderStatTable


def folder_sizes(request):
    table = FolderStatTable(FolderStats.objects.all().prefetch_related('folder'))
    RequestConfig(request).configure(table)

    return render(request, "box/box_stats.html", {
        "table": table
    })
