# Precision for investment aggregates: store full Decimal on save, round only in UI.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0009_investment_growth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmentgrowthrow",
            name="amount_gtq",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name="investmentgrowthrow",
            name="amount_usd",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name="bankloanmonthsnapshot",
            name="total_gtq",
            field=models.DecimalField(decimal_places=6, max_digits=18),
        ),
        migrations.AlterField(
            model_name="bankloanmonthsnapshot",
            name="total_usd",
            field=models.DecimalField(decimal_places=6, max_digits=18),
        ),
    ]