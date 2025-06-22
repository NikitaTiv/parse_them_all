import logging
import mimetypes
from urllib.parse import urljoin
import requests
from requests.exceptions import HTTPError, ConnectionError

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.db import transaction

from config import settings
from image_parser.models import Image


logger = logging.getLogger(__name__)


@transaction.atomic
@shared_task(bind=True, acks_late=True, ignore_result=True)
def send_image_to_tessaract(self, instance_id: str) -> None:
    image_instance = Image.objects.select_for_update().get(pk=instance_id)
    image_obj = image_instance.image_object
    mimetype, _ = mimetypes.guess_type(image_obj.path)
    if not mimetype:
        error_msg = f'Wrong mimetype for {instance_id}'
        logger.info(f'Task send_image_to_tesseract failed. {error_msg}')
        image_instance.mark_image_as_failed(error_msg)
        return
    try:
        url = urljoin(settings.TESSERACT_URL, 'image_api/')
        with open(image_obj.path, 'rb') as file:
            files = (('image_object', (image_obj.name, file, mimetype)),)
            response = requests.post(url, data=(('request_id', instance_id),), files=files, timeout=10)
        response.raise_for_status()
    except FileNotFoundError as e:
        image_instance.mark_image_as_failed(e)
        logger.exception(f'Task send_image_to_tesseract failed. {e}')
    except (HTTPError, requests.Timeout, ConnectionError) as e:
        logger.info(f'Retrying send_image_to_tessaract for {instance_id}: {e}')
        try:
            raise self.retry(countdown=15, max_retries=5)
        except MaxRetriesExceededError as e:
            image_instance.mark_image_as_failed(e)
            logger.exception(f'Task send_image_to_tesseract failed. {e}')
    else:
        image_instance.mark_image_as_processing()
        logger.info('Task send_image_to_tesseract. Sending success')
