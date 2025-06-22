import logging
from PIL import Image, UnidentifiedImageError
from rest_framework import serializers

from image_parser.models import Image as ImageModel
from image_parser.consts import STATUS_SUCCESS, STATUS_FAILED


logger = logging.getLogger(__name__)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('request_id', 'user', 'image_object')
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


class UpdateContentSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=('Success', 'Failed'))
    content = serializers.CharField(allow_blank=True)

    def update(self, instance: ImageModel, validated_data):
        if validated_data['status'] == 'Success':
            instance.mark_image_as_successful(content=validated_data['content'])
        else:
            instance.mark_image_as_failed(error='Failed to handle the image by Tesseract.')
        return instance
