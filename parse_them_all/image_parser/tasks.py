import mimetypes
from urllib.parse import urljoin
import requests
from requests.exceptions import HTTPError

from celery import shared_task
from django.db import transaction

from config import settings
from image_parser.consts import STATUS_PROCESSING, STATUS_FAILED
from image_parser.models import Image


@shared_task
def send_image_to_tessaract(instance_id: str) -> None:
    with transaction.atomic():
        image_instance = Image.objects.select_for_update().get(pk=instance_id)
        image_obj = image_instance.image_object
        mimetype, _ = mimetypes.guess_type(image_obj.path)
        if not mimetype:
            return
        try:
            image_obj.open('rb')
            url = urljoin(settings.TESSERACT_URL, 'image_api/')
            files = (('image_object', (image_obj.name, image_obj.file, mimetype)),)
            response = requests.post(url, data=(('request_id', instance_id),), files=files)
            response.raise_for_status()
            image_instance.status = STATUS_PROCESSING
            print('Sending success')
        except HTTPError:
            image_instance.status = STATUS_FAILED
            print('Sending failed')
        finally:
            image_obj.close()
            image_instance.save(update_fields=('status',))
