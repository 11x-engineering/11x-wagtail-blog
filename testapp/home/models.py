from wagtail.admin.panels import FieldPanel
from wagtail.blocks import TextBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from x11x_wagtail_blog.models import ExtensibleArticlePage


class BlogArticlePage(ExtensibleArticlePage):
    body = StreamField([
        ("text", TextBlock()),
    ], use_json_field=True)

    content_panels = ExtensibleArticlePage.with_body_panels([
        FieldPanel("body"),
    ])


class HomePage(Page):
    pass
