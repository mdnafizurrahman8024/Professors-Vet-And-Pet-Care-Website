from django.db import migrations, models


CLINIC_LATITUDE = 24.367926395092578
CLINIC_LONGITUDE = 88.62464757770542
CLINIC_MAP_URL = (
    "https://maps.google.com/maps?q=24.367926395092578,88.62464757770542"
    "&t=k&z=18&ie=UTF8&iwloc=&output=embed"
)


def set_clinic_coordinates(apps, schema_editor):
    clinic_model = apps.get_model("core", "ClinicInfo")
    clinic_model.objects.all().update(
        map_latitude=CLINIC_LATITUDE,
        map_longitude=CLINIC_LONGITUDE,
        map_satellite_embed_url=CLINIC_MAP_URL,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="clinicinfo",
            name="map_latitude",
            field=models.DecimalField(decimal_places=15, default=CLINIC_LATITUDE, max_digits=18),
        ),
        migrations.AddField(
            model_name="clinicinfo",
            name="map_longitude",
            field=models.DecimalField(decimal_places=15, default=CLINIC_LONGITUDE, max_digits=18),
        ),
        migrations.AlterField(
            model_name="clinicinfo",
            name="map_satellite_embed_url",
            field=models.TextField(default=CLINIC_MAP_URL),
        ),
        migrations.RunPython(set_clinic_coordinates, migrations.RunPython.noop),
    ]
