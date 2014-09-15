from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.management import call_command
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import indexed

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from south.signals import post_migrate


COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
)


# A couple of abstract classes that contain commonly used fields

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True

# Carousel items

class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    image_title = models.CharField(max_length=255, blank=True)
    image_caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('image_title'),
        FieldPanel('image_caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

# Home Page


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('flowpatrolcore.HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('flowpatrolcore.HomePage', related_name='related_links')


class HomePage(Page):
    body = RichTextField(blank=True)
    headline = models.CharField(max_length=255, blank=True)
    features = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = "Homepage"

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('headline'),
    FieldPanel('features'),
    FieldPanel('body', classname="full"),
    InlinePanel(HomePage, 'carousel_items', label="Carousel items"),
    InlinePanel(HomePage, 'related_links', label="Related links"),
]

HomePage.promote_panels     = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('flowpatrolcore.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('flowpatrolcore.StandardPage', related_name='related_links')


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro', 'body', )
    search_name = None

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(StandardPage, 'carousel_items', label="Carousel items"),
    FieldPanel('body', classname="full"),
    InlinePanel(StandardPage, 'related_links', label="Related links"),
]

StandardPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]



