import base64
import logging

from rest_framework import views, status
from rest_framework.response import Response

from image_app.tasks import parse_image_task


logger = logging.getLogger(__name__)


class GetImageView(views.APIView):
    def post(self, request, **kwargs):
        request_id = request.data.get('request_id')
        logger.info(f'Received request for {request_id} processing.')
        if not (image := request.FILES.get('image_object')):
            logger.info(f'File hasnt been provided for {request_id}')
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        image_bytes = image.read()
        parse_image_task.delay(request_id, base64.b64encode(image_bytes))
        return Response(status=status.HTTP_202_ACCEPTED)
