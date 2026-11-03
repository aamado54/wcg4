"""Formularios capturas manuales PGO."""

from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from pgo.capturas_services import OP_REPORTES_PGO_7_ROWS, validate_operation_id
from pgo.scorecard_catalog import UNE_CODES, UNE_LABELS

UNE_CHOICES = [(c, UNE_LABELS.get(c, c)) for c in UNE_CODES if c != "INSURANCE"]

PERCENT_CHOICES = [
    ("0", "0%"),
    ("25", "25%"),
    ("50", "50%"),
    ("75", "75%"),
    ("100", "100%"),
]

QUARTER_CHOICES = [("1", "Q1 (ene–mar)"), ("2", "Q2 (abr–jun)"), ("3", "Q3 (jul–sep)"), ("4", "Q4 (oct–dic)")]


class PeriodFieldsMixin(forms.Form):
    period_year = forms.IntegerField(
        min_value=2000,
        max_value=2100,
        label="Año",
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
    )
    period_month = forms.IntegerField(
        min_value=1,
        max_value=12,
        label="Mes",
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
    )
    change_note = forms.CharField(
        required=False,
        max_length=800,
        label="Nota de cambio",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )


class LegalGarantiasRegistroForm(PeriodFieldsMixin):
    une = forms.ChoiceField(choices=UNE_CHOICES, label="UNE")
    operation_id = forms.CharField(
        max_length=20,
        label="ID operación",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm", "style": "text-transform:uppercase"}),
    )
    client_name = forms.CharField(
        max_length=200,
        label="Nombre cliente",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )
    fecha_formalizacion = forms.DateField(
        label="Fecha formalización",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    hora_formalizacion = forms.TimeField(
        required=False,
        label="Hora formalización (opc.)",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control form-control-sm"}),
    )
    fecha_registro_garantia = forms.DateField(
        label="Fecha registro garantía",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    hora_registro_garantia = forms.TimeField(
        required=False,
        label="Hora registro (opc.)",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-control form-control-sm"}),
    )
    observaciones = forms.CharField(
        required=False,
        max_length=800,
        label="Observaciones",
        widget=forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3}),
    )
    reviewed = forms.BooleanField(required=False, label="Revisado")
    attachment = forms.FileField(
        required=False,
        label="Evidencia PDF/JPG",
        widget=forms.ClearableFileInput(attrs={"class": "form-control form-control-sm", "accept": ".pdf,.jpg,.jpeg"}),
    )

    def clean_operation_id(self):
        raw = self.cleaned_data.get("operation_id", "")
        err = validate_operation_id(raw)
        if err:
            raise ValidationError(err)
        return raw.strip().upper()

    def clean_attachment(self):
        f = self.cleaned_data.get("attachment")
        if not f:
            return f
        name = (f.name or "").lower()
        if not (name.endswith(".pdf") or name.endswith(".jpg") or name.endswith(".jpeg")):
            raise ValidationError("Solo PDF o JPG.")
        if f.size > 15 * 1024 * 1024:
            raise ValidationError("Archivo máximo 15 MB.")
        return f

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        return {
            "une": cd["une"],
            "operation_id": cd["operation_id"],
            "client_name": cd["client_name"],
            "fecha_formalizacion": cd["fecha_formalizacion"].isoformat(),
            "hora_formalizacion": cd["hora_formalizacion"].isoformat() if cd.get("hora_formalizacion") else None,
            "fecha_registro_garantia": cd["fecha_registro_garantia"].isoformat(),
            "hora_registro_garantia": cd["hora_registro_garantia"].isoformat()
            if cd.get("hora_registro_garantia")
            else None,
            "observaciones": cd.get("observaciones") or "",
            "reviewed": bool(cd.get("reviewed")),
        }


class CreditorLineForm(forms.Form):
    creditor_name = forms.CharField(max_length=200, label="Acreedor / línea")
    due_date = forms.DateField(label="Vencimiento", widget=forms.DateInput(attrs={"type": "date"}))
    formalized = forms.ChoiceField(
        choices=(("yes", "Sí"), ("no", "No")),
        label="¿Formalizado?",
    )
    date_done = forms.DateField(
        required=False,
        label="Fecha hecho",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    notes = forms.CharField(required=False, max_length=500, label="Notas", widget=forms.Textarea(attrs={"rows": 2}))


class LegalContratosAcreedoresForm(PeriodFieldsMixin):
    creditor_name = forms.CharField(max_length=200, label="Acreedor / línea")
    due_date = forms.DateField(
        label="Fecha vencimiento",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    formalized = forms.ChoiceField(
        choices=(("yes", "Sí"), ("no", "No")),
        label="¿Formalizado?",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    date_done = forms.DateField(
        required=False,
        label="Fecha realizado",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    notes = forms.CharField(
        required=False,
        max_length=500,
        label="Notas",
        widget=forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 2}),
    )

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        return {
            "lines": [
                {
                    "creditor_name": cd["creditor_name"],
                    "due_date": cd["due_date"].isoformat(),
                    "formalized": cd["formalized"],
                    "date_done": cd["date_done"].isoformat() if cd.get("date_done") else None,
                    "notes": cd.get("notes") or "",
                }
            ]
        }


class OpCronogramaProyectosForm(PeriodFieldsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for code in UNE_CODES:
            self.fields[f"cumple_{code}"] = forms.ChoiceField(
                choices=(("", "—"), ("yes", "Sí cumple"), ("no", "No cumple")),
                required=True,
                label=f"{UNE_LABELS.get(code, code)}",
                widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
            )

    def to_payload(self) -> dict:
        entries = {}
        for code in UNE_CODES:
            val = self.cleaned_data.get(f"cumple_{code}")
            entries[code] = val
        return {"entries": entries}


class TiCronogramaProyectosForm(PeriodFieldsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for code in UNE_CODES:
            self.fields[f"pct_{code}"] = forms.ChoiceField(
                choices=PERCENT_CHOICES,
                required=True,
                label=f"{UNE_LABELS.get(code, code)}",
                widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
            )

    def to_payload(self) -> dict:
        return {f"pct_{code}": self.cleaned_data.get(f"pct_{code}") for code in UNE_CODES}


class TiBackupNasForm(PeriodFieldsMixin):
    quarter = forms.ChoiceField(choices=QUARTER_CHOICES, label="Trimestre")
    areas_implemented = forms.ChoiceField(
        choices=(("yes", "Sí"), ("no", "No")),
        label="Implementación áreas",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    backup_nas_done = forms.ChoiceField(
        choices=(("yes", "Sí"), ("no", "No")),
        label="Backup NAS realizado",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    notes = forms.CharField(
        required=False,
        max_length=500,
        label="Notas",
        widget=forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 2}),
    )

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        return {
            "quarter": cd["quarter"],
            "areas_implemented": cd["areas_implemented"],
            "backup_nas_done": cd["backup_nas_done"],
            "notes": cd.get("notes") or "",
        }


class OpReportesPgcPgo7Form(PeriodFieldsMixin):
    """Campos dinámicos completion_* y notes_* por reporte."""

    def __init__(self, suggested: dict[str, str | None], initial_rows: dict | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keys = [k for k, _ in OP_REPORTES_PGO_7_ROWS]
        initial_rows = initial_rows or {}
        for key, label in OP_REPORTES_PGO_7_ROWS:
            sug = suggested.get(key)
            self.fields[f"completion_{key}"] = forms.DateField(
                required=False,
                label=f"Fecha cumplimiento — {label}",
                widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
            )
            self.fields[f"notes_{key}"] = forms.CharField(
                required=False,
                max_length=300,
                label="Notas",
                widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            )
            if initial_rows.get(key):
                row = initial_rows[key]
                if row.get("completion_date"):
                    self.fields[f"completion_{key}"].initial = row["completion_date"]
                if row.get("notes"):
                    self.fields[f"notes_{key}"].initial = row["notes"]
            elif sug:
                self.fields[f"completion_{key}"].help_text = f"Sugerido import: {sug}"

    def to_payload(self, suggested: dict[str, str | None]) -> dict:
        reports = []
        for key, label in OP_REPORTES_PGO_7_ROWS:
            comp = self.cleaned_data.get(f"completion_{key}")
            reports.append(
                {
                    "key": key,
                    "label": label,
                    "suggested_date": suggested.get(key),
                    "completion_date": comp.isoformat() if comp else None,
                    "notes": self.cleaned_data.get(f"notes_{key}") or "",
                }
            )
        return {"reports": reports}

    @property
    def report_rows(self):
        return OP_REPORTES_PGO_7_ROWS
