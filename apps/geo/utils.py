from datetime import datetime
from text_unidecode import unidecode
from django.utils.text import slugify


def create_name_slug(instance):
    slug = instance.slug
    if not slug:
        slug = slugify(unidecode(instance.name.get("name_uz")))
    model = instance.__class__
    qs_exists = model.objects.filter(slug=slug).exists()
    if qs_exists:
        if model.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.name.get("name_uz")), datetime.now().timestamp()))
    return slug
