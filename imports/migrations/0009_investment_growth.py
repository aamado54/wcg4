# Generated manually for investment growth imports

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0008_backfill_client_rate_basis"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvestmentGrowthRow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveIntegerField()),
                ("instrument", models.CharField(max_length=4)),
                ("company", models.CharField(blank=True, max_length=255)),
                ("operation_code", models.CharField(max_length=100)),
                ("currency_code", models.CharField(blank=True, max_length=10)),
                ("amount_original", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("maturity_date", models.DateField(blank=True, null=True)),
                ("exchange_rate", models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True)),
                ("amount_gtq", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("amount_usd", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("source_row_number", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "file_upload",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="investment_growth_rows",
                        to="imports.fileupload",
                    ),
                ),
            ],
            options={
                "verbose_name": "Saldo inversión AP/PG",
                "verbose_name_plural": "Saldos inversión AP/PG",
                "ordering": ["year", "month", "instrument", "operation_code"],
            },
        ),
        migrations.CreateModel(
            name="BankLoanMonthSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveIntegerField()),
                ("exchange_rate", models.DecimalField(decimal_places=6, max_digits=12)),
                ("total_gtq", models.DecimalField(decimal_places=2, max_digits=18)),
                ("total_usd", models.DecimalField(decimal_places=2, max_digits=18)),
                ("bank_amounts_json", models.JSONField(blank=True, default=dict)),
                (
                    "file_upload",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bank_loan_snapshots",
                        to="imports.fileupload",
                    ),
                ),
            ],
            options={
                "verbose_name": "Préstamos bancarios (cierre)",
                "verbose_name_plural": "Préstamos bancarios (cierre)",
                "ordering": ["year", "month"],
                "unique_together": {("year", "month")},
            },
        ),
        migrations.AddIndex(
            model_name="investmentgrowthrow",
            index=models.Index(fields=["year", "month"], name="imports_inv_year_mo_idx"),
        ),
        migrations.AddIndex(
            model_name="investmentgrowthrow",
            index=models.Index(fields=["year", "month", "instrument"], name="imports_inv_yr_mo_inst_idx"),
        ),
        migrations.AddIndex(
            model_name="investmentgrowthrow",
            index=models.Index(fields=["operation_code", "year", "month"], name="imports_inv_op_yr_mo_idx"),
        ),
    ]
