import pytest

from django.core.management import call_command
from wagtail.core.models import Page


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('delete_wagtail_welcome')
        call_command('loaddata', 'blog/fixtures/blog_test_fixtures.json')
