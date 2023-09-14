import logging
from io import BytesIO

from django.contrib.auth import user_logged_in
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image

from .models import Basket, ProductImage

THUMBNAIL_SIZE = (300, 300)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductImage)
def generate_thumbnail(sender, instance, **kwargs) -> None:
    logger.info(f'Generating thumbnail for product {instance.product.id}')

    image = Image.open(instance.image)
    image = image.convert("RGB")
    image.thumbnail(THUMBNAIL_SIZE, Image.BICUBIC)

    temp_thumb = BytesIO()
    image.save(temp_thumb, 'JPEG')
    temp_thumb.seek(0)

    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,  # to prevent it to run in an infinite loop
    )

    temp_thumb.close()


@receiver(user_logged_in)
def merge_baskets_if_found(sender, request, user, **kwargs):
    anonymous_basket = getattr(
        request,
        'basket',
        None,
    )

    if anonymous_basket:
        try:
            logged_in_basket: Basket = Basket.objects.get(
                user=user,
                status=Basket.OPEN,
            )

            for line in anonymous_basket.basketlines.all():
                line.basket = logged_in_basket
                line.save()

            anonymous_basket.delete()
            request.basket = logged_in_basket
            logger.info(f'Merge basket to {logged_in_basket.id}')
        except Basket.DoesNotExist:
            anonymous_basket.user = user
            anonymous_basket.save()
            logger.info(f'Assigned user to basket {id}')
