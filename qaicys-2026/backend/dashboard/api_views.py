from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .events import EVENTS
from .exports import XLSX_CONTENT_TYPE, build_event_registrations_xlsx
from .permissions import IsSuperUser


def get_event_or_404(slug):
    event = EVENTS.get(slug)
    if event is None:
        from django.http import Http404
        raise Http404("Event not found.")
    return event


class EventSummaryView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        return Response({
            "success": True,
            "events": [
                {"slug": slug, "name": config["name"], "count": config["model"].objects.count()}
                for slug, config in EVENTS.items()
            ],
        })


class EventRegistrationListView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, event_slug):
        event = get_event_or_404(event_slug)
        queryset = event["model"].objects.all()
        search = request.query_params.get("search", "").strip()
        if search:
            query = Q()
            for field in event["search"]:
                query |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(query)

        serializer = event["serializer"](queryset, many=True)
        return Response({
            "success": True,
            "event": {"slug": event_slug, "name": event["name"]},
            "count": queryset.count(),
            "columns": event["columns"],
            "column_labels": event.get("column_labels", {}),
            "registrations": serializer.data,
        })


class EventRegistrationExportView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, event_slug):
        event = get_event_or_404(event_slug)
        response = HttpResponse(
            build_event_registrations_xlsx(event),
            content_type=XLSX_CONTENT_TYPE,
        )
        response["Content-Disposition"] = (
            f'attachment; filename="qaicys-2026-{event_slug}-registrations.xlsx"'
        )
        response["Cache-Control"] = "no-store"
        return response


class EventRegistrationDeleteView(APIView):
    permission_classes = [IsSuperUser]

    def delete(self, request, event_slug, pk):
        event = get_event_or_404(event_slug)
        registration = get_object_or_404(event["model"], pk=pk)
        registration.delete()
        return Response(
            {"success": True, "message": "Registration deleted successfully."},
            status=status.HTTP_200_OK,
        )
