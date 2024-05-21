from django.contrib import admin
from .models import JournalImage,Journal




class JournalImageInline(admin.StackedInline):
    model=JournalImage
    extra=3


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'title',
        'content',
        'date',
        'user'
        ]
    inlines=[JournalImageInline]
    