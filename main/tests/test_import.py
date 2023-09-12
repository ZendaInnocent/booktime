import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import override_settings

from main.models import Product, ProductImage, ProductTag


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
def test_import_data() -> None:
    out = StringIO()
    args = ['main/fixtures/sample-data.csv', 'main/fixtures/sample-images/']

    call_command('importdata', *args, stdout=out)

    expected_output = (
        "Importing Products...\n"
        "Products processed=3 (created=0)\n"
        "Tags processed=6 (created=6)\n"
        "Images processed=3\n"
    )

    assert expected_output in out.getvalue()
    assert Product.objects.count() == 3
    assert ProductTag.objects.count() == 6
    assert ProductImage.objects.count() == 3
