import base64
import binascii
import io
import logging
from urllib.parse import urljoin
import requests
from requests import exceptions

from celery import shared_task
from PIL import Image, UnidentifiedImageError
import pytesseract

from config import settings


logger = logging.getLogger(__name__)


@shared_task
def parse_image_task(request_id, image_str: str):
    try:
        image_bytes = base64.b64decode(image_str)
        with Image.open(io.BytesIO(image_bytes)) as image:
            text = pytesseract.image_to_string(image)
        status_payload = {'status': 'Success', 'content': text}
        logger.info(f'Task parse_image_task: Request_id={request_id} have parsed successfully.')
    except (FileNotFoundError, UnidentifiedImageError, ValueError, TypeError, binascii.Error) as e:
        status_payload = {'status': 'Failed', 'content': ''}
        logger.exception(f'Task parse_image_task: Failed to open image for request_id={request_id}). {str(e)}')

    try:
        url = urljoin(settings.PARSE_THEM_ALL_URL, f'parse-image/update-content/{request_id}/')
        headers = {'Authorization': f'Token {settings.PARSE_THEM_ALL_TOKEN}'}
        response = requests.patch(url, headers=headers, json=status_payload)
        response.raise_for_status()
        logger.info(f'Task parse_image_task: Callback sent successfully for request_id={request_id}')
    except exceptions.HTTPError as e:
        logger.error(f'parse_image_task: Callback failed for request_id={request_id}: {e}')
