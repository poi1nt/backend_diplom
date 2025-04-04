from django.contrib import admin
from files.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file_name', 'comment', 'size',
                    'uploaded', 'downloaded', 'special_link']
    readonly_fields = ['size', 'uploaded', 'downloaded', 'special_link']
    list_filter = ['user']
    search_fields = ['user__username', 'file_name']
