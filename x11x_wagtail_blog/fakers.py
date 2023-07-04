from faker.providers import BaseProvider
from django.utils.timezone import make_aware
from django.core.files import File
from django.core.files.images import ImageFile
from io import BytesIO

from x11x_wagtail_blog.models import ArticlePage, AboutTheAuthor


class X11XWagtailBlogProvider(BaseProvider):
    def article_page(self, *, owner=None) -> ArticlePage:
        return ArticlePage(
            title=self.generator.sentence().title(),
            summary=self.generator.sentence(),
            body=[("markdown", self.generator.paragraph())],
            date=make_aware(self.generator.date_time()),
            owner=owner,
        )

    def avatar_image_content(self, *, size=(32, 32)) -> bytes:
        return self.generator.image(
            size=size,
            image_format="png",
        )

    def avatar_image_file(self) -> ImageFile:
        return ImageFile(
            BytesIO(self.avatar_image_content()),
            self.generator.file_name(extension="png"),
        )

    def about_the_author(self, author) -> AboutTheAuthor:
        return AboutTheAuthor(
            author=author,
            body=self.generator.paragraph(),
        )

    def title_image_content(self, *, size=(2, 2)) -> bytes:
        return self.generator.image(
            size=size,
            image_format="png",
        )

    def title_image_file(self, *, name=None) -> File:
        name = name or self.generator.file_name(extension="png")
        return File(
            BytesIO(self.title_image_content()),
            name,
        )
