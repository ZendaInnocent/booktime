from decimal import Decimal

from django.test import TestCase
from django.core.files.images import ImageFile

from main.models import Product, ProductImage


class TestMainAppSignals(TestCase):

    def test_thumbnails_are_generated_on_save(self):
        product = Product.objects.create(
            name='The cathedral and the bazaar',
            price=Decimal('10.00')
        )

        with open('main/fixtures/db.png', 'rb') as f:
            image = ProductImage(
                product=product,
                image=ImageFile(f, name='tctb.png'),
            )

            with self.assertLogs('main.signals', level='INFO') as cm:
                image.save()

        self.assertGreaterEqual(len(cm.output), 1)

        # check if the generated thumbnail is what expected
        image.refresh_from_db()

        with open('main/fixtures/db-thumb.png', 'rb') as f:
            expected_content = f.read()
            assert image.thumbnail.read() == expected_content

        # delete generated files
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
