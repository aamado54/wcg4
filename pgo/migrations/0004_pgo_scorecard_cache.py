from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pgo", "0003_pgo_archivo_registro"),
    ]

    operations = [
        migrations.CreateModel(
            name="PgoScorecardCacheMeta",
            fields=[
                ("id", models.PositiveSmallIntegerField(default=1, primary_key=True, serialize=False)),
                ("fingerprint", models.CharField(max_length=64)),
                ("computed_at", models.DateTimeField()),
                ("years", models.JSONField(default=list)),
                ("processed_months", models.JSONField(default=dict)),
            ],
            options={
                "verbose_name": "Caché tablero PGO (meta)",
                "verbose_name_plural": "Caché tablero PGO (meta)",
            },
        ),
        migrations.CreateModel(
            name="PgoScorecardCell",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("year", models.PositiveSmallIntegerField(db_index=True)),
                ("month", models.PositiveSmallIntegerField(db_index=True)),
                ("une", models.CharField(db_index=True, max_length=20)),
                ("concept_id", models.CharField(db_index=True, max_length=80)),
                ("points", models.FloatField(blank=True, null=True)),
                ("max_points", models.FloatField(default=0)),
                ("confidence", models.CharField(default="none", max_length=10)),
                ("note", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Celda tablero PGO",
                "verbose_name_plural": "Celdas tablero PGO",
            },
        ),
        migrations.AddIndex(
            model_name="pgoscorecardcell",
            index=models.Index(fields=["year", "month"], name="pgo_scorecard_year_month_idx"),
        ),
        migrations.AddConstraint(
            model_name="pgoscorecardcell",
            constraint=models.UniqueConstraint(
                fields=("year", "month", "une", "concept_id"),
                name="pgo_scorecard_cell_uniq",
            ),
        ),
    ]
