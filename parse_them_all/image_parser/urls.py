from django.urls import path, re_path
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from image_parser.views import ImageView

app_name = 'image_parser'

urlpatterns = [
    path('create/', ImageView.as_view(authentication_classes=(SessionAuthentication,)), name='create_image'),
    re_path(r'update-content/(?P<pk>[0-9a-z-]+)/?', ImageView.as_view(authentication_classes=(TokenAuthentication,)),
            name='update_image'),
]
