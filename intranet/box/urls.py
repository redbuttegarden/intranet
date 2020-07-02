# URLconf
from django.urls import path

from . import views

app_name = 'box'
urlpatterns = [
    path('folders/', views.folder_sizes, name='folders'),
]
