from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        if request.user.is_staff:
            search_results = Page.objects.live().search(search_query)
        else:
            search_results = Page.objects.public().live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    return render(request, 'home/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
