from django.contrib import admin
from django.urls import include, path

from .views import health_check


urlpatterns = [
    path("health/", health_check, name="health"),
    path("admin/", admin.site.urls),
    path("api/registration/", include("registration.urls")),
    path("api/dashboard/", include("dashboard.api_urls")),
    path("manager/", include("dashboard.urls")),
]
