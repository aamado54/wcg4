from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")
    tipo = forms.ChoiceField(
        choices=[
            ("leasing_database", "Base de datos Leasing (CSV/XLSX)"),
            ("leasing_rentas", "Rentas / cuotas leasing"),
            ("estados_financieros", "Estados financieros"),
            ("programacion_pagos", "Programación de pagos"),
            ("pagos_realizados", "Pagos realizados"),
            ("snapshots", "Snapshots operativos"),
        ],
        label="Tipo de importación",
    )
