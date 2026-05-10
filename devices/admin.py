"""
Devices app admin — configured with django-unfold.
"""
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Device, Node


class NodeInline(TabularInline):
    model = Node
    extra = 0
    fields = ["name", "description", "icon"]
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["id", "name", "device_count"]
    search_fields = ["name"]
    ordering = ["name"]

    @admin.display(description="Devices")
    def device_count(self, obj):
        return obj.devices.count()


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    list_display = ["id", "name", "category", "topic", "short_desc", "created_at", "updated_at"]
    list_filter = ["category", "topic", "created_at"]
    search_fields = ["name", "short_desc", "description", "topic__title"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [NodeInline]
    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["category", "topic", "name", "short_desc", "description", "image", "model_file"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(Node)
class NodeAdmin(ModelAdmin):
    list_display = ["id", "name", "device", "created_at"]
    list_filter = ["device__category", "created_at"]
    search_fields = ["name", "description", "device__name"]
    ordering = ["name"]
    readonly_fields = ["created_at"]
    autocomplete_fields = ["device"]
