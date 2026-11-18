from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pgo", "0006_pgo_staff_member"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pgomanualcaptureversion",
            name="attachment",
        ),
    ]
