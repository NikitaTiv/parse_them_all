from django.urls import path, re_path

from image_parser.views import ImageCreateView, UpdateContentView


app_name = 'image_parser'

urlpatterns = [
    path('create/', ImageCreateView.as_view(), name='create_image'),
    re_path(r'update-content/(?P<pk>[0-9a-z-]+)/?', UpdateContentView.as_view(), name='update_image'),
]
