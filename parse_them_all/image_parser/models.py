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
