from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class Heading(blocks.CharBlock):
    class Meta:
        template = 'blocks/heading.html'
        icon = 'grip'
        label = 'Heading'


class GeneralPage(Page):
    body = StreamField(block_types=[
        ('heading', Heading(classname='full title')),
        ('paragraph', blocks.RichTextBlock(required=True, classname='paragraph')),
        ('image', ImageChooserBlock()),
        ('html', blocks.RawHTMLBlock()),
    ], blank=False)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class TwoColumnGeneralPage(Page):
    body = StreamField(block_types=([
        ('heading', Heading(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
        ('html', blocks.RawHTMLBlock()),
    ]), null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]


class HomePage(Page):
    pass
