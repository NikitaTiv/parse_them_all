from datetime import datetime, timezone

from django.test import TestCase
from freezegun import freeze_time

from image_parser.consts import STATUS_CREATED
from image_parser.serializers import ImageSerializer
from image_parser.tests.factories import UserFactory
from image_parser.tests.mixins import CleanStorageMixin, GenerateImageMixin


@freeze_time('2025-01-01')
class ImageSerializerTestCase(GenerateImageMixin, CleanStorageMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test__image_serializer__create_from_data(self):
        test_file = self.generate_test_file()
        serializer = ImageSerializer(data={'user': self.user.pk, 'image_object': test_file})

        serializer.is_valid(raise_exception=True)
        new_instanse = serializer.save()

        self.assertIsNotNone(new_instanse.request_id)
        self.assertEqual(new_instanse.user_id, self.user.id)
        self.assertEqual(new_instanse.image_object.name, test_file.name)
        self.assertEqual(new_instanse.create_date, datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(new_instanse.content, '')
        self.assertEqual(new_instanse.status, STATUS_CREATED)
        self.assertEqual(new_instanse.errors, '')
