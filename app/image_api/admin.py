from django.contrib import admin

from image_api.models import ImageUploads


@admin.register(ImageUploads)
class ImageUploadAdmin(admin.ModelAdmin):

    list_display = ("uuid", "title", "image_obj")
    readonly_fields = ("uuid",)
    search_fields = ("title",)
