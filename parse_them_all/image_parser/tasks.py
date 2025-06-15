import mimetypes
from urllib.parse import urljoin
import requests
from requests.exceptions import HTTPError

from celery import shared_task

from config import settings
from image_parser.models import Image


@shared_task
def send_image_to_tessaract(instance_id: str) -> None:
    # TODO add logging
    print('Start sending')
    image_obj = Image.objects.get(pk=instance_id).image_object
    mimetype, _ = mimetypes.guess_type(image_obj.path)
    if not mimetype:
        return
    try:
        image_obj.open('rb')
        url = urljoin(settings.TESSERACT_URL, 'image_api/')
        files = (('image_object', (image_obj.name, image_obj.file, mimetype)),)
        response = requests.post(url, files=files)
        response.raise_for_status()
        print('Sending success')
    except HTTPError:
        print('Sending failed')
    finally:
        image_obj.close()
