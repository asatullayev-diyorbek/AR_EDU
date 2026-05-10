"""
Education app admin — configured with django-unfold.
"""
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Course, Topic, Resource, ResourceNode, Quiz


class TopicInline(TabularInline):
    model = Topic
    extra = 0
    fields = ["title", "order", "summary"]
    show_change_link = True


class ResourceNodeInline(TabularInline):
    model = ResourceNode
    extra = 0
    fields = ["name", "order", "description"]
    show_change_link = True


class ResourceInline(TabularInline):
    model = Resource
    extra = 0
    fields = ["title", "resource_type"]
    show_change_link = True


class QuizInline(TabularInline):
    model = Quiz
    extra = 0
    fields = ["question", "correct"]
    show_change_link = True


class CourseAdminForm(forms.ModelForm):
    full_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 20, "style": "font-family: monospace;"}),
        help_text="Markdown formatida yozing. **qalin**, *kursiv*, ## sarlavha, - ro'yxat, `kod`",
    )

    class Meta:
        model = Course
        fields = "__all__"


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    form = CourseAdminForm
    list_display = ["id", "title", "short_description", "published", "created_at", "updated_at"]
    search_fields = ["title", "short_description", "description"]
    ordering = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [TopicInline]
    fieldsets = [
        (
            "Asosiy ma'lumotlar",
            {
                "fields": ["title", "slug", "image", "published"],
            },
        ),
        (
            "Tavsif",
            {
                "fields": ["short_description", "description", "full_description"],
                "description": (
                    "short_description — kartochkalarda ko'rinadigan qisqa matn (max 300 belgi). "
                    "description — oddiy matn (qisqacha). "
                    "full_description — kurs sahifasida Markdown formatida to'liq tavsif."
                ),
            },
        ),
        (
            "Vaqtlar",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ["id", "title", "course", "order", "created_at"]
    search_fields = ["title", "summary", "course__title"]
    list_filter = ["course__title"]
    ordering = ["course", "order", "title"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ResourceInline, QuizInline]
    fieldsets = [
        (
            "Topic Details",
            {
                "fields": ["course", "title", "summary", "order"],
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


@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    list_display = ["id", "title", "topic", "resource_type", "created_at"]
    search_fields = ["title", "description", "topic__title"]
    list_filter = ["resource_type"]
    ordering = ["topic", "title"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ResourceNodeInline]
    fieldsets = [
        (
            "Resource Details",
            {
                "fields": [
                    "topic",
                    "title",
                    "description",
                    "resource_type",
                    "content",
                    "image",
                    "video_url",
                    "url",
                    "file",
                ],
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


@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    list_display = ["id", "question_preview", "topic", "correct", "created_at"]
    search_fields = ["question", "option_a", "option_b", "option_c", "option_d"]
    list_filter = ["correct", "topic__course"]
    ordering = ["topic", "id"]
    readonly_fields = ["created_at"]
    fieldsets = [
        (
            "Question",
            {
                "fields": ["topic", "question", "explanation"],
            },
        ),
        (
            "Options",
            {
                "fields": [
                    "option_a",
                    "option_b",
                    "option_c",
                    "option_d",
                    "correct",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    @admin.display(description="Question")
    def question_preview(self, obj):
        return obj.question[:60] + ("..." if len(obj.question) > 60 else "")
