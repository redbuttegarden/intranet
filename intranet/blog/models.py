from django import forms
from django.conf import settings
from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from home.models import Heading

LANGUAGES = (
    # Code names need to match up with those expected by highlight.js to be colored correctly
    ('python', 'Python'),
    ('django', 'Django'),
    ('bash', 'Bash'),
    ('css', 'CSS'),
    ('dockerfile', 'Dockerfile'),
    ('javascript', 'Javascript'),
    ('ini', 'Ini'),
    ('sql', 'SQL'),
    ('json', 'JSON'),
    ('markdown', 'Markdown'),
    ('html', 'HTML'),
    ('nginx', 'Nginx'),
)


class CodeBlock(blocks.StructBlock):
    code = blocks.TextBlock(max_length=20000)
    language = blocks.ChoiceBlock(choices=LANGUAGES, required=False, default='bash')

    class Meta:
        template = 'blocks/code.html'
        icon = 'spinner'
        label = 'Code chunk'


BLOCK_TYPES = [
    ('heading', Heading()),
    ('paragraph', blocks.RichTextBlock(required=True, classname='paragraph')),
    ('image', ImageChooserBlock()),
    ('html', blocks.RawHTMLBlock(required=False)),
    ('code', CodeBlock()),
    ('table', TableBlock()),
]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self',
        blank=True, null=True,
        related_name="children",
        help_text=_("Unlike tags, categories can have a hierarchy so they can be more specifically organized."),
        on_delete=models.CASCADE
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('parent'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='blog_tags')


class BlogIndexPage(RoutablePageMixin, Page):
    subpage_types = ['blog.BlogPage']

    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context['index_page'] = self
        context['posts'] = self.posts
        return context

    def get_posts(self):
        return BlogPage.objects.descendant_of(self).live().order_by('-last_published_at')

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)


class BlogPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Split available categories between RBG Staff / IT
        parent_page = kwargs.get('parent_page')
        if parent_page.title == "Staff Info":
            self.fields['categories'].queryset = BlogCategory.objects.filter(parent__slug__contains='rbg')
        else:
            self.fields['categories'].queryset = BlogCategory.objects.filter(parent__slug__contains='it')


class BlogPage(Page):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )
    date = models.DateTimeField(verbose_name="Post date", default=timezone.now)
    # Determine if this blog page is a child of IT Documentation or RBG Staff Index Page
    categories = ParentalManyToManyField(BlogCategory, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    summary = CharField(max_length=500, help_text=_("Brief summary of the post"))
    body = StreamField(BLOCK_TYPES)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading=_("Tags and Categories")),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField('summary'),
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    parent_page_types = ['blog.BlogIndexPage']

    base_form_class = BlogPageForm

    @property
    def blog_index_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['blog_index_page'] = self.blog_index_page
        context['post'] = self
        return context

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        if not self.search_description:
            self.search_description = self.summary
        return super().save_revision(*args, **kwargs)


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, blank=True, null=True, on_delete=models.SET_NULL, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
