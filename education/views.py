"""
Education app views.
"""
import logging

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from core.utils.response import success_response, error_response
from .models import Course, Topic, Resource, ResourceNode, Quiz, SavedCourse
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    TopicSerializer,
    TopicDetailSerializer,
    ResourceSerializer,
    ResourceNodeSerializer,
    QuizSerializer,
)

logger = logging.getLogger(__name__)


class BaseReadOnlyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message=f"{self.basename.title()} list fetched successfully",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message=f"{self.basename.title()} fetched successfully",
        )


class CourseViewSet(BaseReadOnlyViewSet):
    queryset = Course.objects.prefetch_related("topics").all()
    filterset_fields = ["published"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    ordering = ["title"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer


class TopicViewSet(BaseReadOnlyViewSet):
    queryset = Topic.objects.select_related("course").prefetch_related("resources", "quizzes").all()
    filterset_fields = ["course"]
    search_fields = ["title", "summary"]
    ordering_fields = ["order", "created_at"]
    ordering = ["order", "title"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TopicDetailSerializer
        return TopicSerializer


class ResourceViewSet(BaseReadOnlyViewSet):
    queryset = Resource.objects.select_related("topic", "topic__course").prefetch_related("nodes").all()
    filterset_fields = ["topic", "resource_type"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    ordering = ["title"]

    serializer_class = ResourceSerializer


class ResourceNodeViewSet(BaseReadOnlyViewSet):
    queryset = ResourceNode.objects.select_related(
        "resource",
        "resource__topic",
        "resource__topic__course",
    ).all()
    filterset_fields = ["resource", "resource__topic"]
    search_fields = ["name", "description"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]

    serializer_class = ResourceNodeSerializer


class QuizViewSet(BaseReadOnlyViewSet):
    queryset = Quiz.objects.select_related("topic", "topic__course").all()
    filterset_fields = ["topic"]
    search_fields = ["question"]
    ordering_fields = ["id", "created_at"]
    ordering = ["id"]

    serializer_class = QuizSerializer


class SavedCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved = (
            SavedCourse.objects
            .filter(user=request.user)
            .select_related("course")
            .prefetch_related("course__topics")
        )
        courses = [s.course for s in saved]
        serializer = CourseListSerializer(courses, many=True, context={"request": request})
        return success_response(data=serializer.data, message="Saved courses fetched successfully")

    def post(self, request):
        course_id = request.data.get("course_id")
        course = Course.objects.filter(id=course_id, published=True).first()
        if not course:
            return error_response(message="Course not found", code=404)
        SavedCourse.objects.get_or_create(user=request.user, course=course)
        return success_response(data={"course_id": course.id}, message="Course saved", code=201)

    def delete(self, request):
        course_id = request.data.get("course_id")
        deleted, _ = SavedCourse.objects.filter(user=request.user, course_id=course_id).delete()
        if deleted:
            return success_response(data={}, message="Course unsaved")
        return error_response(message="Not found in saved list", code=404)
