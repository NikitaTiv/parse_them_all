from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from image_parser.serializers import ImageSerializer, UpdateContentSerializer
from image_parser.models import Image


class ImageView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Image.objects
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ImageSerializer
        return UpdateContentSerializer
