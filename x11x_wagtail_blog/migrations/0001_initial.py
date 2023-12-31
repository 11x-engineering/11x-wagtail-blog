# Generated by Django 4.2.3 on 2023-07-11 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import wagtail.fields
import wagtail.snippets.blocks
import x11x_wagtail_blog.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtensibleArticlePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("summary", wagtail.fields.RichTextField(blank=True, default="")),
                (
                    "authors",
                    wagtail.fields.StreamField(
                        [
                            (
                                "about_the_authors",
                                wagtail.snippets.blocks.SnippetChooserBlock(x11x_wagtail_blog.models.AboutTheAuthor),
                            )
                        ],
                        blank=True,
                        default=list,
                        use_json_field=True,
                    ),
                ),
                (
                    "title_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="RelatedArticles",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "related_from",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_article_from",
                        to="x11x_wagtail_blog.extensiblearticlepage",
                        verbose_name="Article",
                    ),
                ),
                (
                    "related_to",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_article_to",
                        to="x11x_wagtail_blog.extensiblearticlepage",
                        verbose_name="Article",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AboutTheAuthor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", wagtail.fields.RichTextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="about_the_author_snippets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
