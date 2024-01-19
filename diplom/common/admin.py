from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    list_display = ['order', 'created', 'updated', 'is_active', 'is_deleted']
    list_filter = ['is_active', 'is_deleted']
    search_fields = ['name', 'description']
    ordering = ['order', 'created']
