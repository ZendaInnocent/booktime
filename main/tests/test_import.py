import tempfile
from io import StringIO

from django.test import TestCase, override_settings
from django.core.management import call_command

from main.models import Product, ProductTag, ProductImage


class TestImport(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        out = StringIO()
        args = ['main/fixtures/sample-data.csv',
                'main/fixtures/sample-images/']

        call_command('importdata', *args, stdout=out)

        expected_output = ("Importing Products...\n"
                           "Products processed=3 (created=0)\n"
                           "Tags processed=6 (created=6)\n"
                           "Images processed=3\n")

        self.assertIn(expected_output, out.getvalue())
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(ProductTag.objects.count(), 6)
        self.assertEqual(ProductImage.objects.count(), 3)
