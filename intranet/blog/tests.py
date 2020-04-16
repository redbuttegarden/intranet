import pytest
from wagtail.core.models import Page, Site
from wagtail.tests.utils import WagtailPageTests
from wagtail.tests.utils.form_data import streamfield

from .apps import BlogConfig
from .models import BlogCategory, BlogIndexPage, BlogPage


@pytest.fixture()
def user_model(django_user_model):
    user = django_user_model.objects.create(username='user', password='pass')
    yield user


@pytest.fixture()
def blog_category_model(db):
    blog_cat = BlogCategory.objects.create(name='Projects',
                                           slug='projects')
    yield blog_cat


@pytest.fixture()
def make_blog_page(db):
    def _make_blog_page(user, title, slug):
        return BlogPage(author=user,
                        title=title,
                        slug=slug,
                        summary='summary text',
                        body=[
                            ('heading', 'Lorem ipsum dolor sit amet.')
                        ])

    return _make_blog_page


def test_blog_installed(settings):
    assert BlogConfig.name in settings.INSTALLED_APPS


def test_blog_category_string(blog_category_model):
    blog_cat = blog_category_model
    assert str(blog_cat) == 'Projects'


def test_blog_index_page_context(make_blog_page, user_model, client):
    site = Site.objects.first()
    index = BlogIndexPage(title='Blog Index Page', slug='blog-index')
    site.root_page.add_child(instance=index)
    blog_page_1 = make_blog_page(user_model, title='One', slug='one')
    blog_page_2 = make_blog_page(user_model, title='Two', slug='two')
    index.add_child(instance=blog_page_1)
    index.add_child(instance=blog_page_2)

    response = client.get(index.full_url)
    assert len(response.context['posts']) == 2
    assert response.context['index_page'] == index
