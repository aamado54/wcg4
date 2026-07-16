from django.db import migrations
from django.db.models import Q


def _mentions_investment(raw: str) -> bool:
    text = (raw or "").lower()
    return any(
        token in text
        for token in (
            "investment",
            "investments",
            "invest",
            "inversiones",
            "inversion",
            "inversión",
        )
    )


def fix_investment_mappings(apps, schema_editor):
    UNE = apps.get_model("core", "UNE")
    UNEAlias = apps.get_model("core", "UNEAlias")
    NewClientImportRow = apps.get_model("imports", "NewClientImportRow")
    CrossSaleImportRow = apps.get_model("imports", "CrossSaleImportRow")

    investment = UNE.objects.filter(code="INVESTMENT").first()
    if not investment:
        return

    for alias in UNEAlias.objects.all():
        if _mentions_investment(alias.raw_value) and alias.une_id != investment.id:
            alias.une_id = investment.id
            alias.save(update_fields=["une_id"])

    invest_q = (
        Q(raw_une_value__icontains="invest")
        | Q(raw_une_value__icontains="invers")
    )
    NewClientImportRow.objects.filter(invest_q).exclude(une_id=investment.id).update(
        une_id=investment.id
    )

    for row in CrossSaleImportRow.objects.all().iterator():
        changed = False
        if _mentions_investment(row.raw_une_destination) and row.une_destination_id != investment.id:
            row.une_destination_id = investment.id
            changed = True
        if _mentions_investment(row.raw_une_origin) and row.une_origin_id != investment.id:
            row.une_origin_id = investment.id
            changed = True
        if changed:
            row.save(update_fields=["une_destination_id", "une_origin_id"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_entidad_datadictionary_dataimportbatch_contacto_and_more"),
        ("imports", "0004_alter_fileupload_status_crosssaleimportrow"),
    ]

    operations = [
        migrations.RunPython(fix_investment_mappings, noop_reverse),
    ]
