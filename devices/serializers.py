"""
Devices app serializers.
"""
from rest_framework import serializers
from .models import Category, Device, Node
from education.models import Topic


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "name", "description", "icon", "created_at"]


class TopicRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title"]


class DeviceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — no nested nodes."""

    category = CategorySerializer(read_only=True)
    topic = TopicRefSerializer(read_only=True)

    class Meta:
        model = Device
        fields = ["id", "category", "topic", "name", "short_desc", "image", "created_at"]


class DeviceDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view — includes nested nodes."""

    category = CategorySerializer(read_only=True)
    topic = TopicRefSerializer(read_only=True)
    nodes = NodeSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "category",
            "topic",
            "name",
            "short_desc",
            "description",
            "image",
            "model_file",
            "nodes",
            "created_at",
            "updated_at",
        ]
