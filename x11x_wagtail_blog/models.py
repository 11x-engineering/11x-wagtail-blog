from django.conf import settings
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtailmarkdown.blocks import MarkdownBlock

_RICH_TEXT_SUMMARY_FEATURES = getattr(settings, "X11X_WAGTAIL_BLOG_SUMMARY_FEATURES", ["bold", "italic", "code", "superscript", "subscript", "strikethrough"])


class RelatedArticles(models.Model):
    related_to = ParentalKey("ArticlePage", verbose_name="Article", related_name="related_article_to")
    related_from = ParentalKey("ArticlePage", verbose_name="Article", related_name="related_article_from")


class ArticlePage(Page):
    date = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=True)
    summary = RichTextField(features=_RICH_TEXT_SUMMARY_FEATURES, default="", blank=True, null=False)
    title_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.RESTRICT,
        related_name="+",
        null=True,
        blank=True,
    )

    body = StreamField(
        [
            ("markdown", MarkdownBlock()),
        ],
        use_json_field=True,
    )

    settings_panels = Page.settings_panels + [
        FieldPanel("date"),
        FieldPanel("owner"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel("title_image"),
        FieldPanel("summary"),
        FieldPanel("body"),
        InlinePanel(
            "related_article_from",
            label="Related Articles",
            panels=[FieldPanel("related_to")]
        )
    ]

    def get_template(self, request, *args, **kwargs):
        return getattr(settings, "X11X_WAGTAIL_BLOG_ARTICLE_TEMPLATE", "x11x_wagtail_blog/article_page.html")

    @property
    def related_articles(self):
        return [to.related_to for to in self.related_article_from.all()]

    @related_articles.setter
    def related_articles(self, value):
        """
        An iterable of all articles related to this one.
        """
        self.related_article_from = [
            RelatedArticles(
                related_from=self,
                related_to=v
            ) for v in value
        ]
