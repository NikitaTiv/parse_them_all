from rest_framework import generics

from image_parser.serializers import ImageSerializer
from image_parser.models import Image


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects
    serializer_class = ImageSerializer
