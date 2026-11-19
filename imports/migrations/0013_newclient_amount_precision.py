from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0012_investment_amount_original_precision"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newclientimportrow",
            name="amount",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=18, null=True
            ),
        ),
    ]