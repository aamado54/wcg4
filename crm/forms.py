from django import forms

from .models import Interaccion, Tarea


class InteraccionForm(forms.ModelForm):
    class Meta:
        model = Interaccion
        fields = ["tipo", "asunto", "descripcion", "fecha"]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "fecha_vencimiento", "estado", "asignado_a"]
        widgets = {
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")
