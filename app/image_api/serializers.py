from rest_framework import serializers

from image_api.models import ImageUploads


class ImageUploadsInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUploads
        fields = ["title", "image_obj", "width", "height"]


class ImageUploadsOutputSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageUploads
        fields = ["id", "title", "url", "width", "height"]

    @staticmethod
    def get_url(obj):
        return obj.image_obj.url
