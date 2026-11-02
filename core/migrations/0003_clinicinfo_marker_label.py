from django.db import migrations, models


CLINIC_MAP_URL = (
    "https://maps.google.com/maps?q=Professor%27s%20Vet%20%26%20Pet%20Care"
    "%4024.367926395092578,88.62464757770542&t=k&z=18&ie=UTF8&iwloc=&output=embed"
)


def set_marker_label(apps, schema_editor):
    clinic_model = apps.get_model("core", "ClinicInfo")
    clinic_model.objects.all().update(map_satellite_embed_url=CLINIC_MAP_URL)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_clinicinfo_coordinates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinicinfo",
            name="map_satellite_embed_url",
            field=models.TextField(default=CLINIC_MAP_URL),
        ),
        migrations.RunPython(set_marker_label, migrations.RunPython.noop),
    ]
