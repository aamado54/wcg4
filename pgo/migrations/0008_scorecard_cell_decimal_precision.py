from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pgo", "0007_remove_pgo_manual_capture_attachment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pgoscorecardcell",
            name="max_points",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="pgoscorecardcell",
            name="points",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=12, null=True
            ),
        ),
    ]