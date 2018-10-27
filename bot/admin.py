from django.contrib import admin

from bot.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'frequency']
    list_filter = ['frequency','blacklist']
    search_fields = ['text']
    date_hierarchy = 'created_at'

