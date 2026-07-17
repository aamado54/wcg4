from django.db import migrations


def seed_usd_gtq(apps, schema_editor):
    Currency = apps.get_model("core", "Currency")
    for code, name, symbol in (
        ("USD", "Dólar estadounidense", "$"),
        ("GTQ", "Quetzal guatemalteco", "Q"),
    ):
        Currency.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "symbol": symbol,
                "is_active": True,
            },
        )


def unseed_usd_gtq(apps, schema_editor):
    # No borrar en reverse: pueden estar referenciados por filas de importación.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_fix_investment_une_aliases"),
    ]

    operations = [
        migrations.RunPython(seed_usd_gtq, unseed_usd_gtq),
    ]
