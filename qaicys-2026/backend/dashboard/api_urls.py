from django.urls import path

from . import api_views


app_name = "dashboard-api"

urlpatterns = [
    path("events/", api_views.EventSummaryView.as_view(), name="events"),
    path("events/<slug:event_slug>/export/", api_views.EventRegistrationExportView.as_view(), name="event-export"),
    path("events/<slug:event_slug>/", api_views.EventRegistrationListView.as_view(), name="event-list"),
    path("events/<slug:event_slug>/<int:pk>/", api_views.EventRegistrationDeleteView.as_view(), name="event-delete"),
]
