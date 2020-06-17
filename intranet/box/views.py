from django.http import HttpResponse
from django.shortcuts import render

from .models import FolderStats


def folder_sizes(request):
    stats = FolderStats.objects.all().prefetch_related('folder')
    return render(request, 'box/box_stats.html', {'stats': stats})
