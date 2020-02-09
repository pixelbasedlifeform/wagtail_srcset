import os
import io
import pytest

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from wagtail.images.models import Image as WagtailImage


def create_small_rgb():
    # this is a small test jpeg
    img = Image.new("RGB", (200, 200), (255, 0, 0, 0))
    return img


@pytest.fixture()
def small_jpeg_io():
    rgb = create_small_rgb()
    im_io = io.BytesIO()
    rgb.save(im_io, format="JPEG", quality=60, optimize=True, progressive=True)
    im_io.seek(0)
    im_io.name = "testimage.jpg"
    return im_io


@pytest.fixture()
def small_uploaded_file(small_jpeg_io):
    simple_png = SimpleUploadedFile(
        name="test.png", content=small_jpeg_io.read(), content_type="image/png"
    )
    small_jpeg_io.seek(0)
    return simple_png


@pytest.fixture
def image(small_uploaded_file):
    image = WagtailImage(file=small_uploaded_file)
    image.save()
    yield image
    # teardown
    os.unlink(image.file.path)
