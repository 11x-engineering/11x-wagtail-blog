from faker.providers import BaseProvider
from django.utils.timezone import make_aware
from django.core.files import File
from io import BytesIO

from x11x_wagtail_blog.models import ArticlePage


class X11XWagtailBlogProvider(BaseProvider):
    def article_page(self, *, owner=None):
        return ArticlePage(
            title=self.generator.sentence().title(),
            summary=self.generator.sentence(),
            body=[("markdown", self.generator.paragraph())],
            date=make_aware(self.generator.date_time()),
            owner=owner,
        )

    def title_image_content(self, *, size=(2, 2)):
        return self.generator.image(
            size=size,
            image_format="png",
        )

    def title_image_file(self, *, name=None):
        name = name or self.generator.file_name(extension="png")
        return File(
            BytesIO(self.title_image_content()),
            name,
        )
