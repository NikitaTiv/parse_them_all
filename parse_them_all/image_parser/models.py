import uuid
from django.db import models
from django.contrib.auth.models import User

from image_parser.consts import STATUS_CREATED, STATUS_PROCESSING, STATUS_SUCCESS, STATUS_FAILED


class Image(models.Model):
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Created'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_object = models.ImageField()
    content = models.TextField(default='', blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    create_date = models.DateTimeField(auto_now=True)
    errors = models.CharField(max_length=255, blank=True, default='')

    def mark_image_as_successful(self, content=''):
        self.errors = ''
        self.content = content
        self.status = STATUS_SUCCESS
        self.save(update_fields=('status', 'errors', 'content'))

    def mark_image_as_failed(self, error=''):
        self.errors = error
        self.status = STATUS_FAILED
        self.save(update_fields=('status', 'errors'))

    def mark_image_as_processing(self):
        self.status = STATUS_FAILED
        self.save(update_fields=('status',))
