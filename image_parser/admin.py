from django.contrib import admin

from image_parser.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
