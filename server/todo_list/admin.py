from django.contrib import admin
from .models import Task



# !Code For Task Model Admin Interface
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'title',
        'status',
        'created_at',
        'updated_at',
    )
    list_editable = (
        'title',
        'status',
    )
    list_per_page = 10
    search_fields = (
        'title__icontains',
        'user__username__icontains', 
    )
    list_filter = (
        'status',
        'user',
        'created_at',
    )

    date_hierarchy = 'created_at'


    def get_queryset(self, request):
        """
        Over riding the base queryset
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('user')
