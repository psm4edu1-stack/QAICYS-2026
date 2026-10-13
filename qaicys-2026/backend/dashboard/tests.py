from io import BytesIO
from xml.etree import ElementTree
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from registration.models import PitchPerfectRegistration
from registration.utils import get_valid_registration_numbers

from .events import EVENTS


class DashboardAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.manager = User.objects.create_superuser("manager", "manager@example.com", "safe-test-password")
        cls.regular_user = User.objects.create_user("student", "student@example.com", "safe-test-password")
        cls.registration = PitchPerfectRegistration.objects.create(
            team_name="Dashboard Team",
            name="Dashboard Student",
            year_of_study="II Year",
            department="BBA",
            registration_number=next(iter(get_valid_registration_numbers())),
            whatsapp_number="9876543210",
            email="dashboard@example.com",
            participant_2_name="Dashboard Partner",
            participant_2_year_of_study="II Year",
            participant_2_department="BBA",
            participant_2_registration_number=sorted(get_valid_registration_numbers())[1],
            participant_2_whatsapp_number="9876543211",
            participant_2_email="partner@example.com",
        )

    def setUp(self):
        self.client = APIClient()

    def test_dashboard_api_rejects_anonymous_user(self):
        response = self.client.get(reverse("dashboard-api:events"))
        self.assertIn(response.status_code, (401, 403))

    def test_dashboard_api_rejects_non_superuser(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get(reverse("dashboard-api:events"))
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_list_selected_event_only(self):
        self.client.force_authenticate(self.manager)
        response = self.client.get(reverse("dashboard-api:event-list", args=["pitch-perfect"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event"]["slug"], "pitch-perfect")
        self.assertEqual(response.data["count"], 1)
        self.assertIn("year_of_study", response.data["columns"])
        self.assertIn("department", response.data["columns"])
        self.assertIn("participant_2_year_of_study", response.data["columns"])
        self.assertIn("participant_2_department", response.data["columns"])
        self.assertEqual(response.data["registrations"][0]["year_of_study"], "II Year")
        self.assertEqual(response.data["registrations"][0]["department"], "BBA")

    def test_superuser_can_export_every_event_model_field_as_xlsx(self):
        self.client.force_authenticate(self.manager)
        response = self.client.get(reverse("dashboard-api:event-export", args=["pitch-perfect"]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("qaicys-2026-pitch-perfect-registrations.xlsx", response["Content-Disposition"])

        with ZipFile(BytesIO(response.content)) as workbook:
            self.assertIsNone(workbook.testzip())
            for filename in (name for name in workbook.namelist() if name.endswith(".xml")):
                ElementTree.fromstring(workbook.read(filename))
            worksheet = workbook.read("xl/worksheets/sheet1.xml").decode("utf-8")

        for field in PitchPerfectRegistration._meta.concrete_fields:
            expected_label = "Registered At" if field.name == "created_at" else str(field.verbose_name).title()
            self.assertIn(expected_label, worksheet)
        self.assertIn("dashboard@example.com", worksheet)
        self.assertIn("partner@example.com", worksheet)
        self.assertIn("Dashboard Partner", worksheet)

    def test_dashboard_export_rejects_anonymous_user(self):
        response = self.client.get(reverse("dashboard-api:event-export", args=["pitch-perfect"]))
        self.assertIn(response.status_code, (401, 403))

    def test_team_event_dashboards_include_available_year_and_department_fields(self):
        expected_fields = {
            "pitch-perfect": {"year_of_study", "department", "participant_2_year_of_study", "participant_2_department"},
            "synapse": {"year_of_study", "department", "participant_2_year_of_study", "participant_2_department"},
            "henna-hues": {"year_of_study", "department", "participant_2_year_of_study", "participant_2_department"},
            "palette-pop": {"year_of_study", "department", "participant_2_year_of_study", "participant_2_department"},
            "bid-byte": {"member_1_year_department", "member_2_year_department"},
            "unscripted": {
                "year_of_study", "department",
                "participant_2_year_of_study", "participant_2_department",
                "participant_3_year_of_study", "participant_3_department",
                "participant_4_year_of_study", "participant_4_department",
                "participant_5_year_of_study", "participant_5_department",
            },
            "battle-zone": {
                "team_lead_department_year", "member_1_department_year",
                "member_2_department_year", "member_3_department_year",
            },
        }
        for slug, fields in expected_fields.items():
            with self.subTest(event=slug):
                self.assertTrue(fields.issubset(EVENTS[slug]["columns"]))

    def test_superuser_can_delete_registration(self):
        self.client.force_authenticate(self.manager)
        response = self.client.delete(reverse("dashboard-api:event-delete", args=["pitch-perfect", self.registration.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PitchPerfectRegistration.objects.filter(pk=self.registration.pk).exists())

    def test_manager_login_and_logout(self):
        response = self.client.post(reverse("dashboard:login"), {"username": "manager", "password": "safe-test-password"})
        self.assertRedirects(response, reverse("dashboard:index"))
        self.assertEqual(self.client.get(reverse("dashboard:index")).status_code, 200)
        response = self.client.post(reverse("dashboard:logout"))
        self.assertRedirects(response, reverse("dashboard:login"))
        self.assertRedirects(
            self.client.get(reverse("dashboard:index")),
            f"{reverse('dashboard:login')}?next={reverse('dashboard:index')}",
        )

    def test_non_superuser_cannot_login_to_manager_dashboard(self):
        response = self.client.post(reverse("dashboard:login"), {"username": "student", "password": "safe-test-password"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "does not have manager access")
