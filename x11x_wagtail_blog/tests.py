from django.utils import timezone
from django.test import override_settings
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page
from faker import Faker
from wagtail.images import get_image_model

from x11x_wagtail_blog.models import ArticlePage
from x11x_wagtail_blog.fakers import X11XWagtailBlogProvider

fake = Faker()
fake.add_provider(X11XWagtailBlogProvider)

Image = get_image_model()


@override_settings(
    X11X_WAGTAIL_BLOG_ARTICLE_TEMPLATE="x11x_wagtail_blog_testing/article_page.html"
)
class TestBlogPages(WagtailPageTestCase):
    def setUp(self):
        self.home = Page.objects.get(slug="home")

    def test_blog_has_title_image(self):
        author = self.create_user("username")

        image_base_name = "test-image"
        image_extension = "png"

        header_image = Image.objects.create(
            title=fake.word(),
            file=fake.title_image_file(
                name=f"{image_base_name}.{image_extension}",
            )
        )
        page = fake.article_page(owner=author)
        page.title_image = header_image
        self.home.add_child(instance=page)

        response = self.client.get(page.full_url)
        self.assertContains(response, page.title_image.title)
        self.assertContains(response, image_base_name)
        self.assertContains(response, image_extension)

    def test_blog_articles_have_the_basic_fields(self):
        content = fake.paragraph()
        title = fake.sentence().title()
        username = fake.user_name()
        publishing_date = timezone.make_aware(fake.date_time())
        summary_text = fake.sentence()

        author = self.create_user(
            username,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        page = ArticlePage(
            title=title,
            body=[("markdown", content)],
            owner=author,
            summary=summary_text,
            date=publishing_date
        )
        self.home.add_child(instance=page)

        response = self.client.get(page.full_url)
        self.assertContains(response, f"<p>{content}</p>")
        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)
        self.assertContains(response, str(publishing_date.year))
        self.assertContains(response, str(publishing_date.month))
        self.assertContains(response, str(publishing_date.day))
        self.assertTemplateUsed(
            response,
            "x11x_wagtail_blog_testing/article_page.html",
        )

    def test_related_articles_are_rendered_properly(self):
        owner = self.create_user("username")

        related_page_a = fake.article_page(owner=owner)
        related_page_b = fake.article_page(owner=owner)

        self.home.add_child(instance=related_page_a)
        self.home.add_child(instance=related_page_b)

        page = ArticlePage(
            title="Page",
            body=[("markdown", "Content")],
            owner=owner,
        )
        page.related_articles = [related_page_a, related_page_b]
        self.home.add_child(instance=page)

        response = self.client.get(page.full_url)
        for related_page in [related_page_a, related_page_b]:
            self.assertContains(response, f"<a href=\"{related_page.url}\">{related_page.title}</a>")
