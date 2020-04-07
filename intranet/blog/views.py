from .models import BlogIndexPage


def tag_view(request, tag):
    index = BlogIndexPage.objects.first()
    return index.serve(request, tag=tag)


def category_view(request, category):
    index = BlogIndexPage.objects.first()
    return index.serve(request, category=category)
