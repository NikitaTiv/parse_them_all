from rest_framework import generics

from image_parser.serializers import ImageSerializer, UpdateContentSerializer
from image_parser.models import Image


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects
    serializer_class = ImageSerializer


class UpdateContentView(generics.UpdateAPIView):
    queryset = Image.objects
    serializer_class = UpdateContentSerializer
