from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")
