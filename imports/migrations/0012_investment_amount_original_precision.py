from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0011_importauditevent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmentgrowthrow",
            name="amount_original",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
    ]