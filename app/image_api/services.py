import os

from PIL import Image

from app import settings
from image_api.models import ImageUploads


def resize_image(image: ImageUploads, width: int, height: int):
    # resize image to requested width and height
    path = os.path.join(settings.MEDIA_ROOT, image.image_obj.name)
    size = width, height
    img = Image.open(path)
    img = img.resize(size)
    img.save(path)

    # update model dimensions
    image.width, image.height = size
    image.save()


def set_up_image_dimensions(image: ImageUploads):
    # set original uploaded image size if not other dimensions requested
    image.width = image.image_obj.width
    image.height = image.image_obj.height
    image.save()
