"""
Root URL configuration.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from core.auth import LoginView, RegisterView, MeView, ChangePasswordView
from core.ai import AIChatView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/me/", MeView.as_view(), name="me"),
    path("api/auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("api/ai/chat/", AIChatView.as_view(), name="ai-chat"),
    path("api/", include("devices.urls")),
    path("api/", include("education.urls")),
    # Serve media through Django so CorsMiddleware adds Access-Control-Allow-Origin headers.
    # model_viewer_plus WebView (localhost origin) requires CORS on .glb files.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
