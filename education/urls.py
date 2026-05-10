"""
Education app URL routing.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, TopicViewSet, ResourceViewSet, ResourceNodeViewSet, QuizViewSet, SavedCourseView

router = DefaultRouter()
router.register(r"courses",        CourseViewSet,       basename="course")
router.register(r"topics",         TopicViewSet,        basename="topic")
router.register(r"resources",      ResourceViewSet,     basename="resource")
router.register(r"resource-nodes", ResourceNodeViewSet, basename="resource-node")
router.register(r"quiz",           QuizViewSet,         basename="quiz")

urlpatterns = router.urls + [
    path("saved/", SavedCourseView.as_view(), name="saved-courses"),
]
