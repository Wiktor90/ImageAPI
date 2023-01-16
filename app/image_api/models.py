import os
from uuid import uuid4

from django.db import models


def get_image_path(instance, filename=None):
    file_ext = filename.split(".")[-1]
    filename = f"{instance.uuid}.{file_ext}"
    target_location = os.path.join("images", filename)
    return target_location


class ImageUploads(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    title = models.CharField(
        max_length=32,
        help_text="Title of uploaded image. Field is using as a search parameter",
        verbose_name="Image title",
    )
    image_obj = models.ImageField(upload_to=get_image_path)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
