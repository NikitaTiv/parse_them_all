from django.urls import path

from image_app.views import GetImageView

app_name = 'image_app'

urlpatterns = [
    path('', GetImageView.as_view(), name='get_image')
]
