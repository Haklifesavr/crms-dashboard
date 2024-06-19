from django.contrib import admin
from .models import Board, Item

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'comments', 'badge_text', 'badge_color', 'due_date', 'attachments')
    list_filter = ('board', 'badge_text', 'badge_color')
    search_fields = ('title',)
    raw_id_fields = ('board',)  # This will display board as a raw ID field instead of a dropdown
