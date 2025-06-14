from celery import shared_task


@shared_task
def send_image_to_tessaract():
    print('Hi')
