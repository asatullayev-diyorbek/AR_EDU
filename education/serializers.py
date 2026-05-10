"""
Education app serializers.
"""
from rest_framework import serializers
from .models import Course, Topic, Resource, ResourceNode, Quiz


class ResourceNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceNode
        fields = [
            "id",
            "name",
            "description",
            "order",
            "created_at",
        ]


class ResourceSerializer(serializers.ModelSerializer):
    nodes = ResourceNodeSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "description",
            "resource_type",
            "content",
            "image",
            "video_url",
            "url",
            "file",
            "nodes",
            "created_at",
            "updated_at",
        ]


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "topic",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct",
            "explanation",
            "created_at",
        ]


class TopicReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title", "summary", "order"]


class TopicDetailSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "summary",
            "order",
            "resources",
            "quizzes",
            "created_at",
            "updated_at",
        ]


class CourseListSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()

    def get_topic_count(self, obj):
        return obj.topics.count()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "full_description",
            "image",
            "published",
            "topic_count",
            "created_at",
            "updated_at",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    topics = TopicDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "full_description",
            "image",
            "published",
            "topics",
            "created_at",
            "updated_at",
        ]


class TopicSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "course",
            "title",
            "summary",
            "order",
            "created_at",
            "updated_at",
        ]
