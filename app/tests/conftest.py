import io

import pytest
from PIL import Image
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def image_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(0, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


@pytest.fixture
def text_file():
    text = b"text file"
    file = io.BytesIO(text)
    file.name = "test.txt"
    return file
