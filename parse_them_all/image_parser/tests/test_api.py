from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from image_parser.models import Image
from image_parser.tests.factories import UserFactory
from image_parser.tests.mixins import CleanStorageMixin, GenerateImageMixin


class CreateImageApiTestCase(GenerateImageMixin, CleanStorageMixin, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('image_handlers:create_image')
        cls.user = UserFactory()

    def test__create__ok(self):
        data = {'user': self.user.pk, 'image_object': self.generate_test_file()}

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.data, {'id': Image.objects.last().pk, 'user': self.user.id})

    def test__create__user_is_blank(self):
        data = {'user': '', 'image_object': self.generate_test_file()}

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test__create__user_not_exists(self):
        last_existing_user_id = User.objects.order_by('id').last().pk
        data = {'user': last_existing_user_id + 1, 'image_object': self.generate_test_file()}

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test__create__file_wrong_format(self):
        data = {'user': self.user.pk, 'image_object': self.generate_test_file('renamed_image.txt')}

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test__create__file_is_blank(self):
        data = {'user': self.user.pk, 'image_object': ''}

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
