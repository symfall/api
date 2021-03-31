from django.contrib import admin

from .models import Chat, Message, File


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'updated_at',
        'id',
        'title',
        'creator',
        'is_closed',
    )
    list_filter = ('created_at', 'updated_at', 'creator', 'is_closed')
    raw_id_fields = ('invited',)
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'updated_at',
        'id',
        'sender',
        'chat',
        'message',
        'status',
    )
    list_filter = ('created_at', 'updated_at', 'sender', 'chat')
    date_hierarchy = 'created_at'


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'id', 'document', 'message')
    list_filter = ('created_at', 'updated_at', 'message')
    date_hierarchy = 'created_at'
