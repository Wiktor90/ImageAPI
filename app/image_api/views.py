from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from image_api.models import ImageUploads
from image_api.serializers import ImageUploadsOutputSerializer
from image_api.serializers import ImageUploadsInputSerializer
from image_api.services import resize_image
from image_api.services import set_up_image_dimensions


filter_param = openapi.Parameter(
    'title', openapi.IN_QUERY, description="Provided image's title", type=openapi.TYPE_STRING
    )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Images List"],
        manual_parameters=[filter_param],
        operation_id="Images List",
        operation_description="List of images filtered by title. If title is empty or not defined, return full list",
    ),
)
class ImageUploadsView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ImageUploadsOutputSerializer
    queryset = ImageUploads.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create image in DB. Width & Height are optional request body parameters.
        If width & height are provided in the request body, then image will be resized to requested size.
        If width & height are not provided image will be saved with original dimensions.
        """

        serializer = ImageUploadsInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        width = serializer.validated_data.get('width', None)
        height = serializer.validated_data.get('height', None)
        image: ImageUploads = serializer.save()

        if all([width, height]):
            resize_image(image, width, height)
        else:
            set_up_image_dimensions(image)

        headers = self.get_success_headers(serializer.data)
        output_serializer = ImageUploadsOutputSerializer(image)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        title = self.request.query_params.get("title")

        if title:
            queryset = ImageUploads.objects.filter(title__icontains=title)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
