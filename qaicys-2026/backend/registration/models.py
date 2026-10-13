from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^\+?[0-9][0-9\s-]{6,17}$",
    message="Enter a valid phone number.",
)


class IndividualRegistration(models.Model):
    name = models.CharField(max_length=150)
    year_of_study = models.CharField(max_length=30)
    department = models.CharField(max_length=120)
    registration_number = models.CharField(max_length=50, db_index=True)
    whatsapp_number = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.registration_number})"


class TwoParticipantRegistration(IndividualRegistration):
    team_name = models.CharField(max_length=150, blank=True, default="")
    participant_2_name = models.CharField(max_length=150, blank=True, default="")
    participant_2_year_of_study = models.CharField(max_length=30, blank=True, default="")
    participant_2_department = models.CharField(max_length=120, blank=True, default="")
    participant_2_registration_number = models.CharField(max_length=50, blank=True, default="", db_index=True)
    participant_2_whatsapp_number = models.CharField(max_length=20, blank=True, default="", validators=[phone_validator])
    participant_2_email = models.EmailField(blank=True, default="")

    class Meta(IndividualRegistration.Meta):
        abstract = True


class PitchPerfectRegistration(TwoParticipantRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Pitch Perfect registration"
        verbose_name_plural = "Pitch Perfect registrations"


class PromptoopiaRegistration(IndividualRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Promptoopia registration"
        verbose_name_plural = "Promptoopia registrations"


class PixelCipherRegistration(IndividualRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Pixel Cipher registration"
        verbose_name_plural = "Pixel Cipher registrations"


class SynapseRegistration(TwoParticipantRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Synapse registration"
        verbose_name_plural = "Synapse registrations"


class HennaHuesRegistration(TwoParticipantRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Henna Hues registration"
        verbose_name_plural = "Henna Hues registrations"


class PalettePopRegistration(TwoParticipantRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Palette Pop registration"
        verbose_name_plural = "Palette Pop registrations"


class ClickCraftRegistration(IndividualRegistration):
    class Meta(IndividualRegistration.Meta):
        verbose_name = "Click Craft registration"
        verbose_name_plural = "Click Craft registrations"


class TheVerdictRegistration(IndividualRegistration):
    LANGUAGE_CHOICES = [("English", "English"), ("Tamil", "Tamil")]
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

    class Meta(IndividualRegistration.Meta):
        verbose_name = "The Verdict registration"
        verbose_name_plural = "The Verdict registrations"


class EstrellaRegistration(IndividualRegistration):
    participated_in_technical_or_non_technical_event = models.BooleanField(
        verbose_name="Have you participated in at least one technical or non-technical event?"
    )
    technical_or_non_technical_events = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Technical or non-technical event(s)",
    )

    class Meta(IndividualRegistration.Meta):
        verbose_name = "Estrella registration"
        verbose_name_plural = "Estrella registrations"


class UnscriptedRegistration(IndividualRegistration):
    TEAM_SIZE_CHOICES = [(size, str(size)) for size in range(1, 6)]
    team_name = models.CharField(max_length=150, blank=True, default="")
    team_size = models.PositiveSmallIntegerField(choices=TEAM_SIZE_CHOICES, default=1)

    participant_2_name = models.CharField(max_length=150, blank=True, default="")
    participant_2_year_of_study = models.CharField(max_length=30, blank=True, default="")
    participant_2_department = models.CharField(max_length=120, blank=True, default="")
    participant_2_registration_number = models.CharField(max_length=50, blank=True, default="", db_index=True)
    participant_2_whatsapp_number = models.CharField(max_length=20, blank=True, default="", validators=[phone_validator])
    participant_2_email = models.EmailField(blank=True, default="")

    participant_3_name = models.CharField(max_length=150, blank=True, default="")
    participant_3_year_of_study = models.CharField(max_length=30, blank=True, default="")
    participant_3_department = models.CharField(max_length=120, blank=True, default="")
    participant_3_registration_number = models.CharField(max_length=50, blank=True, default="", db_index=True)
    participant_3_whatsapp_number = models.CharField(max_length=20, blank=True, default="", validators=[phone_validator])
    participant_3_email = models.EmailField(blank=True, default="")

    participant_4_name = models.CharField(max_length=150, blank=True, default="")
    participant_4_year_of_study = models.CharField(max_length=30, blank=True, default="")
    participant_4_department = models.CharField(max_length=120, blank=True, default="")
    participant_4_registration_number = models.CharField(max_length=50, blank=True, default="", db_index=True)
    participant_4_whatsapp_number = models.CharField(max_length=20, blank=True, default="", validators=[phone_validator])
    participant_4_email = models.EmailField(blank=True, default="")

    participant_5_name = models.CharField(max_length=150, blank=True, default="")
    participant_5_year_of_study = models.CharField(max_length=30, blank=True, default="")
    participant_5_department = models.CharField(max_length=120, blank=True, default="")
    participant_5_registration_number = models.CharField(max_length=50, blank=True, default="", db_index=True)
    participant_5_whatsapp_number = models.CharField(max_length=20, blank=True, default="", validators=[phone_validator])
    participant_5_email = models.EmailField(blank=True, default="")

    class Meta(IndividualRegistration.Meta):
        verbose_name = "Unscripted registration"
        verbose_name_plural = "Unscripted registrations"


class BidByteRegistration(models.Model):
    team_name = models.CharField(max_length=150)
    team_lead_name = models.CharField(max_length=150)
    team_lead = models.CharField(
        max_length=150,
        help_text="The additional Team Lead field required by the event form.",
    )
    team_lead_registration_number = models.CharField(max_length=50, db_index=True)
    team_lead_phone_number = models.CharField(max_length=20, validators=[phone_validator])
    team_lead_email = models.EmailField()
    member_1_name = models.CharField(max_length=150)
    member_1_registration_number = models.CharField(max_length=50, db_index=True)
    member_1_phone_number = models.CharField(max_length=20, validators=[phone_validator])
    member_1_email = models.EmailField()
    member_1_year_department = models.CharField(max_length=180)
    member_2_name = models.CharField(max_length=150)
    member_2_registration_number = models.CharField(max_length=50, db_index=True)
    member_2_phone_number = models.CharField(max_length=20, validators=[phone_validator])
    member_2_email = models.EmailField()
    member_2_year_department = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bid Byte registration"
        verbose_name_plural = "Bid Byte registrations"

    def __str__(self):
        return f"{self.team_name} — {self.team_lead_name}"


class BattleZoneRegistration(models.Model):
    team_name = models.CharField(max_length=150)

    team_lead_name = models.CharField(max_length=150)
    team_lead_registration_number = models.CharField(max_length=50, db_index=True)
    team_lead_contact_number = models.CharField(max_length=20, validators=[phone_validator])
    team_lead_email = models.EmailField()
    team_lead_department_year = models.CharField(max_length=180)

    member_1_name = models.CharField(max_length=150)
    member_1_registration_number = models.CharField(max_length=50, db_index=True)
    member_1_contact_number = models.CharField(max_length=20, validators=[phone_validator])
    member_1_email = models.EmailField()
    member_1_department_year = models.CharField(max_length=180)

    member_2_name = models.CharField(max_length=150)
    member_2_registration_number = models.CharField(max_length=50, db_index=True)
    member_2_contact_number = models.CharField(max_length=20, validators=[phone_validator])
    member_2_email = models.EmailField()
    member_2_department_year = models.CharField(max_length=180)

    member_3_name = models.CharField(max_length=150)
    member_3_registration_number = models.CharField(max_length=50, db_index=True)
    member_3_contact_number = models.CharField(max_length=20, validators=[phone_validator])
    member_3_email = models.EmailField()
    member_3_department_year = models.CharField(max_length=180)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Battle Zone registration"
        verbose_name_plural = "Battle Zone registrations"

    def __str__(self):
        return f"{self.team_name} — {self.team_lead_name}"
