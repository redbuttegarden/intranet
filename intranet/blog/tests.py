import pytest

from .apps import BlogConfig
from .models import BlogCategory


@pytest.fixture()
def blog_category_model(db):
    blog_cat = BlogCategory.objects.create(name="Projects",
                                           slug='projects')
    yield blog_cat


def test_blog_installed(settings):
    assert BlogConfig.name in settings.INSTALLED_APPS


def test_blog_category_string(blog_category_model):
    blog_cat = blog_category_model
    assert str(blog_cat) == "Projects"
