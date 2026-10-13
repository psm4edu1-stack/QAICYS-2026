from django.contrib import admin

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


class IndividualRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "registration_number", "department", "year_of_study", "created_at")
    search_fields = ("name", "registration_number", "email", "whatsapp_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


class TwoParticipantRegistrationAdmin(IndividualRegistrationAdmin):
    list_display = (
        "team_name", "name", "registration_number", "participant_2_name",
        "participant_2_registration_number", "created_at",
    )
    search_fields = IndividualRegistrationAdmin.search_fields + (
        "team_name", "participant_2_name", "participant_2_registration_number", "participant_2_email",
    )


for model in (
    PromptoopiaRegistration,
    PixelCipherRegistration,
    ClickCraftRegistration,
    TheVerdictRegistration,
    EstrellaRegistration,
):
    admin.site.register(model, IndividualRegistrationAdmin)

for model in (
    PitchPerfectRegistration,
    SynapseRegistration,
    HennaHuesRegistration,
    PalettePopRegistration,
):
    admin.site.register(model, TwoParticipantRegistrationAdmin)


@admin.register(UnscriptedRegistration)
class UnscriptedRegistrationAdmin(IndividualRegistrationAdmin):
    list_display = ("team_name", "name", "registration_number", "team_size", "created_at")
    search_fields = IndividualRegistrationAdmin.search_fields + ("team_name",) + tuple(
        field
        for number in range(2, 6)
        for field in (f"participant_{number}_name", f"participant_{number}_registration_number")
    )


@admin.register(BidByteRegistration)
class BidByteRegistrationAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_lead_name", "team_lead_registration_number", "created_at")
    search_fields = (
        "team_name", "team_lead_name", "team_lead_registration_number",
        "member_1_registration_number", "member_2_registration_number",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(BattleZoneRegistration)
class BattleZoneRegistrationAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_lead_name", "team_lead_registration_number", "created_at")
    search_fields = (
        "team_name", "team_lead_name", "team_lead_registration_number",
        "member_1_registration_number", "member_2_registration_number",
        "member_3_registration_number",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
