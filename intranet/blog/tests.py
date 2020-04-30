import pytest

from .apps import BlogConfig
from .models import BlogCategory


@pytest.fixture()
def blog_category_model(db):
    blog_cat = BlogCategory.objects.create(name='Test Category',
                                           slug='test-category')
    yield blog_cat


def test_blog_installed(settings):
    assert BlogConfig.name in settings.INSTALLED_APPS


def test_blog_category_string(blog_category_model):
    blog_cat = blog_category_model
    assert str(blog_cat) == 'Test Category'


@pytest.mark.django_db
def test_blog_index_page_context(client):
    """
    Test that keyword 'posts' contains all post objects.
    Test fixture should contain 3 posts: One, Two, and Public Post
    """
    response = client.get('/staff-info/')
    assert len(response.context['posts']) == 3
