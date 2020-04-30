from django.core.management.base import BaseCommand
from wagtail.core.models import Page


class Command(BaseCommand):
    help = 'Deletes the default Wagtail welcome page if it still exists'

    def handle(self, *args, **options):
        try:
            Page.objects.get(title="Welcome to your new Wagtail site!").delete()
        except Page.DoesNotExist:
            pass
