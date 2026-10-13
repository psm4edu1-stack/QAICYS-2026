from rest_framework import serializers

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
from .utils import is_valid_registration_number, normalize_registration_number
from .constraints import validate_participation_constraints


class RegistrationNumberValidationMixin:
    registration_number_fields = ("registration_number",)

    def get_registration_number_fields(self, attrs):
        return self.registration_number_fields

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}
        normalized_numbers = []

        registration_fields = self.get_registration_number_fields(attrs)
        for field in registration_fields:
            number = normalize_registration_number(attrs.get(field, ""))
            attrs[field] = number
            normalized_numbers.append(number)
            if not is_valid_registration_number(number):
                errors[field] = ["Invalid registration number."]

        duplicates = {number for number in normalized_numbers if normalized_numbers.count(number) > 1}
        if duplicates:
            for field in registration_fields:
                if attrs[field] in duplicates:
                    errors[field] = ["A registration number cannot be used twice in the same team."]

        if not errors:
            errors.update(
                validate_participation_constraints(
                    self.Meta.model,
                    attrs,
                    registration_fields,
                )
            )

        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class IndividualRegistrationSerializer(RegistrationNumberValidationMixin, serializers.ModelSerializer):
    class Meta:
        fields = (
            "id", "name", "year_of_study", "department", "registration_number",
            "whatsapp_number", "email", "created_at",
        )
        read_only_fields = ("id", "created_at")


class TwoParticipantRegistrationSerializer(IndividualRegistrationSerializer):
    registration_number_fields = (
        "registration_number",
        "participant_2_registration_number",
    )

    class Meta(IndividualRegistrationSerializer.Meta):
        fields = IndividualRegistrationSerializer.Meta.fields + (
            "team_name",
            "participant_2_name",
            "participant_2_year_of_study",
            "participant_2_department",
            "participant_2_registration_number",
            "participant_2_whatsapp_number",
            "participant_2_email",
        )

    def validate(self, attrs):
        errors = {}
        for field in (
            "team_name", "participant_2_name", "participant_2_year_of_study", "participant_2_department",
            "participant_2_registration_number", "participant_2_whatsapp_number", "participant_2_email",
        ):
            if not str(attrs.get(field, "")).strip():
                errors[field] = ["This field is required for the second participant."]
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)


class PitchPerfectSerializer(TwoParticipantRegistrationSerializer):
    class Meta(TwoParticipantRegistrationSerializer.Meta):
        model = PitchPerfectRegistration


class PromptoopiaSerializer(IndividualRegistrationSerializer):
    class Meta(IndividualRegistrationSerializer.Meta):
        model = PromptoopiaRegistration


class PixelCipherSerializer(IndividualRegistrationSerializer):
    class Meta(IndividualRegistrationSerializer.Meta):
        model = PixelCipherRegistration


class SynapseSerializer(TwoParticipantRegistrationSerializer):
    class Meta(TwoParticipantRegistrationSerializer.Meta):
        model = SynapseRegistration


class HennaHuesSerializer(TwoParticipantRegistrationSerializer):
    class Meta(TwoParticipantRegistrationSerializer.Meta):
        model = HennaHuesRegistration


class PalettePopSerializer(TwoParticipantRegistrationSerializer):
    class Meta(TwoParticipantRegistrationSerializer.Meta):
        model = PalettePopRegistration


class ClickCraftSerializer(IndividualRegistrationSerializer):
    class Meta(IndividualRegistrationSerializer.Meta):
        model = ClickCraftRegistration


class TheVerdictSerializer(IndividualRegistrationSerializer):
    class Meta(IndividualRegistrationSerializer.Meta):
        model = TheVerdictRegistration
        fields = IndividualRegistrationSerializer.Meta.fields + ("language",)


class EstrellaSerializer(IndividualRegistrationSerializer):
    class Meta(IndividualRegistrationSerializer.Meta):
        model = EstrellaRegistration
        fields = IndividualRegistrationSerializer.Meta.fields + (
            "participated_in_technical_or_non_technical_event",
            "technical_or_non_technical_events",
        )

    def to_internal_value(self, data):
        data = data.copy()
        if (
            "participated_in_technical_or_non_technical_event" not in data
            and "participated_in_technical_event" in data
        ):
            data["participated_in_technical_or_non_technical_event"] = data.get(
                "participated_in_technical_event"
            )
        if "technical_or_non_technical_events" not in data and "technical_events" in data:
            data["technical_or_non_technical_events"] = data.get("technical_events")
        return super().to_internal_value(data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        participated = attrs.get("participated_in_technical_or_non_technical_event")
        events = attrs.get("technical_or_non_technical_events", "").strip()
        if not participated:
            raise serializers.ValidationError(
                {
                    "participated_in_technical_or_non_technical_event": [
                        "Estrella is available only after participating in another "
                        "QAICYS 2026 event."
                    ]
                }
            )
        if participated and not events:
            raise serializers.ValidationError(
                {
                    "technical_or_non_technical_events": [
                        "Mention at least one technical or non-technical event."
                    ]
                }
            )
        return attrs


class UnscriptedSerializer(IndividualRegistrationSerializer):
    participant_fields = ("name", "year_of_study", "department", "registration_number", "whatsapp_number", "email")

    class Meta(IndividualRegistrationSerializer.Meta):
        model = UnscriptedRegistration
        fields = IndividualRegistrationSerializer.Meta.fields + (
            "team_name",
            "team_size",
            "participant_2_name", "participant_2_year_of_study", "participant_2_department",
            "participant_2_registration_number", "participant_2_whatsapp_number", "participant_2_email",
            "participant_3_name", "participant_3_year_of_study", "participant_3_department",
            "participant_3_registration_number", "participant_3_whatsapp_number", "participant_3_email",
            "participant_4_name", "participant_4_year_of_study", "participant_4_department",
            "participant_4_registration_number", "participant_4_whatsapp_number", "participant_4_email",
            "participant_5_name", "participant_5_year_of_study", "participant_5_department",
            "participant_5_registration_number", "participant_5_whatsapp_number", "participant_5_email",
        )

    def get_registration_number_fields(self, attrs):
        team_size = int(attrs.get("team_size", 1))
        return ("registration_number",) + tuple(
            f"participant_{number}_registration_number"
            for number in range(2, team_size + 1)
        )

    def validate(self, attrs):
        team_size = int(attrs.get("team_size", 1))
        errors = {}
        suffixes = ("name", "year_of_study", "department", "registration_number", "whatsapp_number", "email")

        for number in range(2, team_size + 1):
            for suffix in suffixes:
                field = f"participant_{number}_{suffix}"
                if not str(attrs.get(field, "")).strip():
                    errors[field] = ["This field is required for the selected team size."]

        if not str(attrs.get("team_name", "")).strip():
            errors["team_name"] = ["Team name is required."]

        if errors:
            raise serializers.ValidationError(errors)

        attrs = super().validate(attrs)

        for number in range(team_size + 1, 6):
            for suffix in suffixes:
                attrs[f"participant_{number}_{suffix}"] = ""
        return attrs


class BidByteSerializer(RegistrationNumberValidationMixin, serializers.ModelSerializer):
    registration_number_fields = (
        "team_lead_registration_number",
        "member_1_registration_number",
        "member_2_registration_number",
    )

    class Meta:
        model = BidByteRegistration
        fields = "__all__"
        read_only_fields = ("id", "created_at")


class BattleZoneSerializer(RegistrationNumberValidationMixin, serializers.ModelSerializer):
    registration_number_fields = (
        "team_lead_registration_number",
        "member_1_registration_number",
        "member_2_registration_number",
        "member_3_registration_number",
    )

    class Meta:
        model = BattleZoneRegistration
        fields = "__all__"
        read_only_fields = ("id", "created_at")
