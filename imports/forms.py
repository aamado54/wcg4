from django import forms

class FileUploadForm(forms.Form):
    stored_file = forms.FileField(label="Archivo a importar")