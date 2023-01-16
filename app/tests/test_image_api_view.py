import os

import pytest
from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status

from app import settings
from image_api.models import ImageUploads


# helper
def delete_img_after_test(file_url):
    path = f"{settings.MEDIA_ROOT}{file_url}"
    os.remove(path)


@pytest.mark.django_db
def test_should_create_image_with_default_size(client, image_file):
    url = reverse("images")
    payload = {"title": "photo1", "image_obj": image_file}
    response = client.post(url, payload, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    # base size of image_file implemented in fixture is 100x100
    assert data["width"], data["height"] == (100, 100)

    delete_img_after_test(data["url"])


@pytest.mark.django_db
def test_should_create_resized_image(client, image_file):
    url = reverse("images")
    payload = {
        "title": "photo2", "image_obj": image_file, "width": 200, "height": 200
    }

    response = client.post(url, payload, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["width"], data["height"] == (200, 200)
    img_from_db = ImageUploads.objects.last()
    assert img_from_db.image_obj.width == data["width"]
    assert img_from_db.image_obj.height == data["height"]

    delete_img_after_test(data["url"])


@pytest.mark.django_db
def test_should_throw_400_when_upload_not_supported_file(client, text_file):
    url = reverse("images")
    payload = {"title": "photo2", "image_obj": text_file}

    response = client.post(url, payload, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Upload a valid image" in response.json()["image_obj"][0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "query_params, expected_count",
    [
        ({"title": "log"}, 2),
        ({"title": "logo"}, 1),
    ]
)
def test_should_filter_images_by_title(client, query_params, expected_count):
    # feed_db
    ImageUploads.objects.create(title="log", image_obj="photo.png")
    ImageUploads.objects.create(title="logo", image_obj="photo.jpg")

    url = reverse("images")
    qs = urlencode(query_params)
    url = f"{url}?{qs}"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == expected_count
