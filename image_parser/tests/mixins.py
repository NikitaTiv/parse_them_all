import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
from PIL import Image


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


class GenerateImageMixin:
    @staticmethod
    def generate_test_file(filename='test.png'):
        image = Image.new('RGB', (100, 100), color='red')
        byte_io = io.BytesIO()
        image.save(byte_io, format='PNG')
        byte_io.seek(0)
        return SimpleUploadedFile(name=filename, content=byte_io.read(), content_type='image/png')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CleanStorageMixin(SimpleTestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
