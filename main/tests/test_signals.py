import logging
from decimal import Decimal

from django.core.files.images import ImageFile

from main.models import Product, ProductImage


def test_thumbnails_are_generated_on_save(caplog) -> None:
    product = Product.objects.create(
        name='The cathedral and the bazaar', price=Decimal('10.00')
    )

    with open('main/fixtures/capital.png', 'rb') as f:
        image = ProductImage(
            product=product,
            image=ImageFile(f, name='tctb.png'),
        )

        with caplog.at_level(logging.INFO, logger='main.signals'):
            image.save()

    assert len(caplog.records) >= 1

    # check if the generated thumbnail is what expected
    image.refresh_from_db()

    with open('main/fixtures/capital-thumb.png', 'rb') as f:
        expected_content: bytes = f.read()
        assert image.thumbnail.read() == expected_content

    # delete generated files
    image.thumbnail.delete(save=False)
    image.image.delete(save=False)
