from django.dispatch import receiver
from django.db.models.signals import post_save

from image_parser.models import Image
from image_parser.tasks import send_image_to_tessaract


@receiver(post_save, sender=Image, dispatch_uid='post_save_image_signal')
def post_save_image(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created'] is False:
        return
    send_image_to_tessaract.delay_on_commit(instance.request_id)
