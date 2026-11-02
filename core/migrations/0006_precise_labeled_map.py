from django.db import migrations, models


CLINIC_MAP_URL = (
    "https://maps.google.com/maps?q="
    "24.367926395092578,88.62464757770542+"
    "(Professor's+Vet+%26+Pet+Care)&t=k&z=18&ie=UTF8&iwloc=&output=embed"
)


def set_precise_labeled_map(apps, schema_editor):
    clinic_model = apps.get_model("core", "ClinicInfo")
    clinic_model.objects.all().update(map_satellite_embed_url=CLINIC_MAP_URL)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_update_searchable_map_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinicinfo",
            name="map_satellite_embed_url",
            field=models.TextField(default=CLINIC_MAP_URL),
        ),
        migrations.RunPython(set_precise_labeled_map, migrations.RunPython.noop),
    ]
