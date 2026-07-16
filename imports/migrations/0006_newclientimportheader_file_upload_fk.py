# Generated manually for multi-month client imports

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0005_alter_fileimportlog_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newclientimportheader",
            name="file_upload",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="new_clients_headers",
                to="imports.fileupload",
            ),
        ),
    ]
