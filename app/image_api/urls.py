from django.urls import path

from image_api.views import ImageUploadsView

urlpatterns = [
    path(
        "images",
        ImageUploadsView.as_view({"get": "list", "post": "create"}),
        name="images",
    ),
    path(
        "images/<int:pk>",
        ImageUploadsView.as_view({"get": "retrieve"}),
        name="image-details",
    )
]
