from django.db import migrations


def forwards(apps, schema_editor):
    NewClientImportRow = apps.get_model("imports", "NewClientImportRow")
    from imports.client_rates import clean_cell, rate_basis_for

    for row in NewClientImportRow.objects.select_related("une").iterator():
        changed = False
        name = clean_cell(row.client_name)
        nit = clean_cell(row.nit)
        op = clean_cell(row.operation_code)
        if name != (row.client_name or ""):
            row.client_name = name
            changed = True
        if nit != (row.nit or ""):
            row.nit = nit
            changed = True
        if op != (row.operation_code or ""):
            row.operation_code = op
            changed = True
        basis = rate_basis_for(row.une, row.raw_une_value or "")
        if row.rate_basis != basis:
            row.rate_basis = basis
            changed = True
        if changed:
            row.save(update_fields=["client_name", "nit", "operation_code", "rate_basis"])


def backwards(apps, schema_editor):
    NewClientImportRow = apps.get_model("imports", "NewClientImportRow")
    NewClientImportRow.objects.update(rate_basis="")


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0007_newclientimportrow_interest_rate"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
