from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_object = models.ImageField()
    content = models.TextField(default='', blank=True)
    is_handled = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)
