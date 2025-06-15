import logging

from rest_framework import views, status
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class GetImageView(views.APIView):
    def post(self, request, **kwargs):
        logger.info('Received request.')
        return Response(status=status.HTTP_202_ACCEPTED)
