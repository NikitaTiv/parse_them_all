from django.urls import path

from image_parser.views import ImageCreateView


app_name = 'image_parser'

urlpatterns = [
    path('create/', ImageCreateView.as_view(), name='create_image')
]
