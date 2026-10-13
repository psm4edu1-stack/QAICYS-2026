from contextlib import contextmanager

from django.db import connection, transaction
from django.db.models import Q

from .models import (
    BattleZoneRegistration,
    BidByteRegistration,
    ClickCraftRegistration,
    EstrellaRegistration,
    HennaHuesRegistration,
    PalettePopRegistration,
    PitchPerfectRegistration,
    PixelCipherRegistration,
    PromptoopiaRegistration,
    SynapseRegistration,
    TheVerdictRegistration,
    UnscriptedRegistration,
)


MAX_REGULAR_EVENTS_PER_REGISTRATION_NUMBER = 2
BATTLE_ZONE_TEAM_LIMIT = 24

# Every place a participant registration number can be stored for each event.
EVENT_REGISTRATION_FIELDS = {
    PitchPerfectRegistration: (
        "registration_number",
        "participant_2_registration_number",
    ),
    BidByteRegistration: (
        "team_lead_registration_number",
        "member_1_registration_number",
        "member_2_registration_number",
    ),
    PromptoopiaRegistration: ("registration_number",),
    PixelCipherRegistration: ("registration_number",),
    SynapseRegistration: (
        "registration_number",
        "participant_2_registration_number",
    ),
    HennaHuesRegistration: (
        "registration_number",
        "participant_2_registration_number",
    ),
    PalettePopRegistration: (
        "registration_number",
        "participant_2_registration_number",
    ),
    ClickCraftRegistration: ("registration_number",),
    TheVerdictRegistration: ("registration_number",),
    EstrellaRegistration: ("registration_number",),
    UnscriptedRegistration: (
        "registration_number",
        "participant_2_registration_number",
        "participant_3_registration_number",
        "participant_4_registration_number",
        "participant_5_registration_number",
    ),
    BattleZoneRegistration: (
        "team_lead_registration_number",
        "member_1_registration_number",
        "member_2_registration_number",
        "member_3_registration_number",
    ),
}

# Estrella is an additional "Star of the Event" entry. It does not consume one
# of the two regular event slots, but it requires at least one regular entry.
REGULAR_EVENT_REGISTRATION_FIELDS = {
    model: fields
    for model, fields in EVENT_REGISTRATION_FIELDS.items()
    if model is not EstrellaRegistration
}


def registration_number_exists_in_event(model, registration_number):
    query = Q()
    for field in EVENT_REGISTRATION_FIELDS[model]:
        query |= Q(**{field: registration_number})
    return model.objects.filter(query).exists()


def registered_regular_event_count(registration_number):
    return sum(
        registration_number_exists_in_event(model, registration_number)
        for model in REGULAR_EVENT_REGISTRATION_FIELDS
    )


def validate_participation_constraints(model, attrs, submitted_fields):
    errors = {}

    for field in submitted_fields:
        registration_number = attrs[field]
        if registration_number_exists_in_event(model, registration_number):
            errors[field] = [
                "This registration number is already registered for this event."
            ]
        elif model is EstrellaRegistration and registered_regular_event_count(registration_number) == 0:
            errors[field] = [
                "Estrella is available only to participants registered in at least one other "
                "QAICYS 2026 Technical or Non-Technical event."
            ]
        elif (
            model is not EstrellaRegistration
            and registered_regular_event_count(registration_number)
            >= MAX_REGULAR_EVENTS_PER_REGISTRATION_NUMBER
        ):
            errors[field] = [
                "This registration number has already registered for the maximum of two "
                "Technical / Non-Technical events. Estrella is available as one additional event."
            ]

    if model is BattleZoneRegistration and BattleZoneRegistration.objects.count() >= BATTLE_ZONE_TEAM_LIMIT:
        errors["non_field_errors"] = [
            "Battle Zone registration is full. The limit is 24 teams (96 participants)."
        ]

    return errors


@contextmanager
def registration_submission_guard():
    """Serialize submissions so concurrent requests cannot bypass capacity limits."""
    with transaction.atomic():
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(%s)", [2026081301])
        yield
