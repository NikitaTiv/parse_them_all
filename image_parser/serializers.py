from PIL import Image, UnidentifiedImageError
from rest_framework import serializers

from image_parser.models import Image as ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'user', 'image_object')
        extra_kwargs = {
            'image_object': {'write_only': True}
        }

    def validate_image_object(self, file):
        try:
            img = Image.open(file)
            img.verify()
        except (UnidentifiedImageError, IOError):
            raise serializers.ValidationError("Uploaded file is not a valid image.")
        return file
