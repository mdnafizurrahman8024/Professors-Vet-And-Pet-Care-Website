from django.db import migrations


CLINIC_MAP_URL = (
    "https://maps.google.com/maps?q=138+Debishing+Para,+Madrashar+More,"
    "+Rajshahi&t=k&z=18&ie=UTF8&iwloc=&output=embed"
)


def update_searchable_map_url(apps, schema_editor):
    clinic_model = apps.get_model("core", "ClinicInfo")
    clinic_model.objects.all().update(map_satellite_embed_url=CLINIC_MAP_URL)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_clinicinfo_searchable_map"),
    ]

    operations = [
        migrations.RunPython(update_searchable_map_url, migrations.RunPython.noop),
    ]
