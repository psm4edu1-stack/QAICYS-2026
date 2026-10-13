from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import (
    BattleZoneRegistration,
    BidByteRegistration,
    EstrellaRegistration,
    PitchPerfectRegistration,
)
from .utils import get_valid_registration_numbers


class RegistrationApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.numbers = sorted(get_valid_registration_numbers())[:8]

    def setUp(self):
        self.client = APIClient()

    def individual_payload(self, number=None):
        return {
            "name": "Test Student",
            "year_of_study": "II Year",
            "department": "BBA",
            "registration_number": number or self.numbers[0],
            "whatsapp_number": "+91 98765 43210",
            "email": "student@example.com",
        }

    def bid_byte_payload(self):
        return {
            "team_name": "Byte Team",
            "team_lead_name": "Lead Student",
            "team_lead": "Lead Student",
            "team_lead_registration_number": self.numbers[0],
            "team_lead_phone_number": "9876543210",
            "team_lead_email": "lead@example.com",
            "member_1_name": "Member One",
            "member_1_registration_number": self.numbers[1],
            "member_1_phone_number": "9876543211",
            "member_1_email": "one@example.com",
            "member_1_year_department": "II Year BBA",
            "member_2_name": "Member Two",
            "member_2_registration_number": self.numbers[2],
            "member_2_phone_number": "9876543212",
            "member_2_email": "two@example.com",
            "member_2_year_department": "II Year BBA",
        }

    def two_participant_payload(self):
        payload = self.individual_payload()
        payload.update({
            "team_name": "Two Person Team",
            "participant_2_name": "Second Student",
            "participant_2_year_of_study": "II Year",
            "participant_2_department": "BBA",
            "participant_2_registration_number": self.numbers[1],
            "participant_2_whatsapp_number": "9876543211",
            "participant_2_email": "second@example.com",
        })
        return payload

    def unscripted_payload(self, team_size=5):
        payload = self.individual_payload()
        payload["team_name"] = "Performance Team"
        payload["team_size"] = team_size
        for number in range(2, team_size + 1):
            payload.update({
                f"participant_{number}_name": f"Performer {number}",
                f"participant_{number}_year_of_study": "II Year",
                f"participant_{number}_department": "BBA",
                f"participant_{number}_registration_number": self.numbers[number - 1],
                f"participant_{number}_whatsapp_number": f"98765432{number:02d}",
                f"participant_{number}_email": f"performer{number}@example.com",
            })
        return payload

    def battle_zone_payload(self):
        payload = {"team_name": "Battle Team"}
        for index, prefix in enumerate(("team_lead", "member_1", "member_2", "member_3")):
            payload.update({
                f"{prefix}_name": f"Player {index + 1}",
                f"{prefix}_registration_number": self.numbers[index],
                f"{prefix}_contact_number": f"98765432{index:02d}",
                f"{prefix}_email": f"player{index + 1}@example.com",
                f"{prefix}_department_year": "III Year BBA",
            })
        return payload

    def test_valid_individual_registration(self):
        response = self.client.post(reverse("registration:pitch-perfect"), self.two_participant_payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(PitchPerfectRegistration.objects.count(), 1)

    def test_all_other_standard_individual_event_endpoints(self):
        for index, route in enumerate((
            "promptoopia", "pixel-cipher", "click-craft",
        )):
            with self.subTest(route=route):
                response = self.client.post(
                    reverse(f"registration:{route}"),
                    self.individual_payload(self.numbers[index]),
                    format="json",
                )
                self.assertEqual(response.status_code, 201)

    def test_registration_number_cannot_register_same_event_twice(self):
        payload = self.individual_payload(self.numbers[0])
        first = self.client.post(reverse("registration:promptoopia"), payload, format="json")
        second = self.client.post(reverse("registration:promptoopia"), payload, format="json")
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)
        self.assertIn("already registered for this event", second.data["errors"]["registration_number"][0])

    def test_registration_number_can_join_only_two_regular_events(self):
        number = self.numbers[0]
        first = self.client.post(reverse("registration:promptoopia"), self.individual_payload(number), format="json")
        second = self.client.post(reverse("registration:pixel-cipher"), self.individual_payload(number), format="json")
        third = self.client.post(reverse("registration:click-craft"), self.individual_payload(number), format="json")
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(third.status_code, 400)
        self.assertIn("maximum of two", third.data["errors"]["registration_number"][0])

    def test_team_member_cannot_register_same_event_again_in_another_role(self):
        first_payload = self.bid_byte_payload()
        first = self.client.post(reverse("registration:bid-byte"), first_payload, format="json")

        second_payload = self.bid_byte_payload()
        second_payload.update({
            "team_name": "Second Byte Team",
            "team_lead_registration_number": self.numbers[3],
            "member_1_registration_number": self.numbers[4],
            "member_2_registration_number": self.numbers[1],
        })
        second = self.client.post(reverse("registration:bid-byte"), second_payload, format="json")

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)
        self.assertIn("already registered for this event", second.data["errors"]["member_2_registration_number"][0])

    def test_battle_zone_rejects_twenty_fifth_team(self):
        for team_number in range(24):
            payload = self.battle_zone_payload()
            payload["team_name"] = f"Existing Team {team_number + 1}"
            for member_number, prefix in enumerate(("team_lead", "member_1", "member_2", "member_3")):
                payload[f"{prefix}_registration_number"] = f"LEGACY-{team_number}-{member_number}"
            BattleZoneRegistration.objects.create(**payload)

        response = self.client.post(
            reverse("registration:battle-zone"),
            self.battle_zone_payload(),
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("24 teams", response.data["errors"]["non_field_errors"][0])

    def test_synapse_accepts_two_valid_participants(self):
        response = self.client.post(reverse("registration:synapse"), self.two_participant_payload(), format="json")
        self.assertEqual(response.status_code, 201)

    def test_henna_hues_accepts_artist_and_model(self):
        response = self.client.post(reverse("registration:henna-hues"), self.two_participant_payload(), format="json")
        self.assertEqual(response.status_code, 201)

    def test_palette_pop_requires_model_details(self):
        payload = self.two_participant_payload()
        payload["participant_2_name"] = ""
        response = self.client.post(reverse("registration:palette-pop"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("participant_2_name", response.data["errors"])

    def test_two_participant_event_requires_team_name(self):
        payload = self.two_participant_payload()
        payload["team_name"] = ""
        response = self.client.post(reverse("registration:synapse"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("team_name", response.data["errors"])

    def test_two_participant_event_rejects_invalid_second_number(self):
        payload = self.two_participant_payload()
        payload["participant_2_registration_number"] = "INVALID"
        response = self.client.post(reverse("registration:pitch-perfect"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("participant_2_registration_number", response.data["errors"])

    def test_unscripted_accepts_five_valid_participants(self):
        response = self.client.post(reverse("registration:unscripted"), self.unscripted_payload(), format="json")
        self.assertEqual(response.status_code, 201)

    def test_unscripted_rejects_invalid_fifth_participant(self):
        payload = self.unscripted_payload()
        payload["participant_5_registration_number"] = "INVALID"
        response = self.client.post(reverse("registration:unscripted"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("participant_5_registration_number", response.data["errors"])

    def test_unscripted_rejects_duplicate_participant(self):
        payload = self.unscripted_payload()
        payload["participant_5_registration_number"] = payload["participant_2_registration_number"]
        response = self.client.post(reverse("registration:unscripted"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("participant_2_registration_number", response.data["errors"])
        self.assertIn("participant_5_registration_number", response.data["errors"])

    def test_the_verdict_accepts_supported_language(self):
        payload = self.individual_payload()
        payload["language"] = "Tamil"
        response = self.client.post(reverse("registration:the-verdict"), payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_invalid_individual_registration_number(self):
        payload = self.individual_payload()
        payload["registration_number"] = "NOT-A-STUDENT"
        response = self.client.post(reverse("registration:promptoopia"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("registration_number", response.data["errors"])

    def test_valid_bid_byte_team(self):
        response = self.client.post(reverse("registration:bid-byte"), self.bid_byte_payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BidByteRegistration.objects.count(), 1)

    def test_bid_byte_rejects_one_invalid_member(self):
        payload = self.bid_byte_payload()
        payload["member_1_registration_number"] = "INVALID"
        response = self.client.post(reverse("registration:bid-byte"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("member_1_registration_number", response.data["errors"])

    def test_bid_byte_rejects_duplicate_member(self):
        payload = self.bid_byte_payload()
        payload["member_1_registration_number"] = payload["team_lead_registration_number"]
        response = self.client.post(reverse("registration:bid-byte"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("team_lead_registration_number", response.data["errors"])
        self.assertIn("member_1_registration_number", response.data["errors"])

    def test_valid_battle_zone_team(self):
        response = self.client.post(reverse("registration:battle-zone"), self.battle_zone_payload(), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BattleZoneRegistration.objects.count(), 1)

    def test_battle_zone_rejects_one_invalid_member(self):
        payload = self.battle_zone_payload()
        payload["member_3_registration_number"] = "INVALID"
        response = self.client.post(reverse("registration:battle-zone"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("member_3_registration_number", response.data["errors"])

    def test_battle_zone_rejects_duplicate_member(self):
        payload = self.battle_zone_payload()
        payload["member_3_registration_number"] = payload["member_1_registration_number"]
        response = self.client.post(reverse("registration:battle-zone"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("member_1_registration_number", response.data["errors"])
        self.assertIn("member_3_registration_number", response.data["errors"])

    def test_estrella_yes_requires_participated_events(self):
        number = self.numbers[0]
        prerequisite = self.client.post(
            reverse("registration:promptoopia"),
            self.individual_payload(number),
            format="json",
        )
        payload = self.individual_payload()
        payload.update({
            "participated_in_technical_or_non_technical_event": True,
            "technical_or_non_technical_events": "",
        })
        response = self.client.post(reverse("registration:estrella"), payload, format="json")
        self.assertEqual(prerequisite.status_code, 201)
        self.assertEqual(response.status_code, 400)
        self.assertIn("technical_or_non_technical_events", response.data["errors"])

    def test_estrella_accepts_non_technical_event_participation(self):
        number = self.numbers[0]
        prerequisite = self.client.post(
            reverse("registration:click-craft"),
            self.individual_payload(number),
            format="json",
        )
        payload = self.individual_payload()
        payload.update({
            "participated_in_technical_or_non_technical_event": True,
            "technical_or_non_technical_events": "Click Craft",
        })
        response = self.client.post(reverse("registration:estrella"), payload, format="json")
        self.assertEqual(prerequisite.status_code, 201)
        self.assertEqual(response.status_code, 201)
        registration = EstrellaRegistration.objects.get()
        self.assertTrue(registration.participated_in_technical_or_non_technical_event)
        self.assertEqual(registration.technical_or_non_technical_events, "Click Craft")

    def test_estrella_rejects_participant_without_another_qaicys_event(self):
        payload = self.individual_payload()
        payload.update({
            "participated_in_technical_or_non_technical_event": True,
            "technical_or_non_technical_events": "External college event",
        })
        response = self.client.post(reverse("registration:estrella"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("at least one other", response.data["errors"]["registration_number"][0])
        self.assertEqual(EstrellaRegistration.objects.count(), 0)

    def test_estrella_requires_participation_confirmation(self):
        number = self.numbers[0]
        prerequisite = self.client.post(
            reverse("registration:promptoopia"),
            self.individual_payload(number),
            format="json",
        )
        payload = self.individual_payload(number)
        payload.update({
            "participated_in_technical_or_non_technical_event": False,
            "technical_or_non_technical_events": "",
        })
        response = self.client.post(reverse("registration:estrella"), payload, format="json")
        self.assertEqual(prerequisite.status_code, 201)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "participated_in_technical_or_non_technical_event",
            response.data["errors"],
        )

    def test_registration_number_can_join_two_regular_events_plus_estrella(self):
        number = self.numbers[0]
        first = self.client.post(
            reverse("registration:promptoopia"),
            self.individual_payload(number),
            format="json",
        )
        second = self.client.post(
            reverse("registration:pixel-cipher"),
            self.individual_payload(number),
            format="json",
        )
        estrella_payload = self.individual_payload(number)
        estrella_payload.update({
            "participated_in_technical_or_non_technical_event": True,
            "technical_or_non_technical_events": "Promptoopia, Pixel Cipher",
        })
        estrella = self.client.post(
            reverse("registration:estrella"),
            estrella_payload,
            format="json",
        )
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(estrella.status_code, 201)

    def test_estrella_does_not_consume_a_regular_event_slot(self):
        number = self.numbers[0]
        first = self.client.post(
            reverse("registration:promptoopia"),
            self.individual_payload(number),
            format="json",
        )
        estrella_payload = self.individual_payload(number)
        estrella_payload.update({
            "participated_in_technical_or_non_technical_event": True,
            "technical_or_non_technical_events": "Promptoopia",
        })
        estrella = self.client.post(
            reverse("registration:estrella"),
            estrella_payload,
            format="json",
        )
        second = self.client.post(
            reverse("registration:pixel-cipher"),
            self.individual_payload(number),
            format="json",
        )
        third = self.client.post(
            reverse("registration:click-craft"),
            self.individual_payload(number),
            format="json",
        )
        self.assertEqual(first.status_code, 201)
        self.assertEqual(estrella.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(third.status_code, 400)

    def test_estrella_accepts_legacy_participation_field_names(self):
        number = self.numbers[0]
        prerequisite = self.client.post(
            reverse("registration:promptoopia"),
            self.individual_payload(number),
            format="json",
        )
        payload = self.individual_payload()
        payload.update({
            "participated_in_technical_event": True,
            "technical_events": "Promptoopia",
        })
        response = self.client.post(reverse("registration:estrella"), payload, format="json")
        self.assertEqual(prerequisite.status_code, 201)
        self.assertEqual(response.status_code, 201)
        registration = EstrellaRegistration.objects.get()
        self.assertEqual(registration.technical_or_non_technical_events, "Promptoopia")

    def test_invalid_email(self):
        payload = self.individual_payload()
        payload["email"] = "invalid-email"
        response = self.client.post(reverse("registration:promptoopia"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data["errors"])

    def test_missing_required_field(self):
        payload = self.individual_payload()
        payload.pop("name")
        response = self.client.post(reverse("registration:promptoopia"), payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data["errors"])

    def test_get_is_not_allowed_on_public_registration_endpoint(self):
        response = self.client.get(reverse("registration:pitch-perfect"))
        self.assertEqual(response.status_code, 405)
