from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registration", "0003_hennahuesregistration_participant_2_department_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="estrellaregistration",
            old_name="participated_in_technical_event",
            new_name="participated_in_technical_or_non_technical_event",
        ),
        migrations.RenameField(
            model_name="estrellaregistration",
            old_name="technical_events",
            new_name="technical_or_non_technical_events",
        ),
        migrations.AlterField(
            model_name="estrellaregistration",
            name="participated_in_technical_or_non_technical_event",
            field=models.BooleanField(
                verbose_name=(
                    "Have you participated in at least one technical or non-technical event?"
                )
            ),
        ),
        migrations.AlterField(
            model_name="estrellaregistration",
            name="technical_or_non_technical_events",
            field=models.CharField(
                blank=True,
                max_length=300,
                verbose_name="Technical or non-technical event(s)",
            ),
        ),
    ]
