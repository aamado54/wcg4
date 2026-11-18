"""Formularios capturas manuales PGO."""

from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from pgo.capturas_services import OP_REPORTES_PGO_7_ROWS, validate_operation_id
from pgo.scorecard_catalog import UNE_CODES, UNE_LABELS

UNE_CHOICES = [(c, UNE_LABELS.get(c, c)) for c in UNE_CODES if c != "INSURANCE"]

LEGAL_GARANTIAS_UNE_CHOICES = [(c, UNE_LABELS.get(c, c)) for c in ("FACTORING", "LEASING")]

PERCENT_CHOICES = [
    ("0", "0%"),
    ("25", "25%"),
    ("50", "50%"),
    ("75", "75%"),
    ("100", "100%"),
]

QUARTER_CHOICES = [("1", "Q1 (ene–mar)"), ("2", "Q2 (abr–jun)"), ("3", "Q3 (jul–sep)"), ("4", "Q4 (oct–dic)")]

OPTIONAL_YES_NO_CHOICES = (("", "—"), ("yes", "Sí"), ("no", "No"))

_SM_SELECT = {"class": "form-select form-select-sm"}
_SM_INPUT = {"class": "form-control form-control-sm"}


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


class LegalGarantiasRegistroForm(PeriodFieldsMixin):
    une = forms.ChoiceField(choices=LEGAL_GARANTIAS_UNE_CHOICES, label="UNE")
    operation_id = forms.CharField(
        max_length=20,
        label="ID operación",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm", "style": "text-transform:uppercase"}),
    )
    fecha_formalizacion = forms.DateField(
        label="Fecha formalización",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    fecha_registro_garantia = forms.DateField(
        label="Fecha registro garantía",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    planner_ref = forms.CharField(
        required=False,
        max_length=80,
        label="Opcional — sustituto: referencia planner / ID alterno",
        help_text="No sustituye el ID operación. Solo ayuda si el caso también vive en WCG Créditos.",
        widget=forms.TextInput(attrs={**_SM_INPUT, "style": "text-transform:uppercase"}),
    )
    registro_mismo_dia_firma = forms.ChoiceField(
        required=False,
        choices=OPTIONAL_YES_NO_CHOICES,
        label="Opcional — sustituto: ¿registro el mismo día de firma?",
        help_text="Referencia PGO Legal; el dato primario siguen siendo las dos fechas.",
        widget=forms.Select(attrs=_SM_SELECT),
    )
    caso_en_planner_wcg = forms.ChoiceField(
        required=False,
        choices=OPTIONAL_YES_NO_CHOICES,
        label="Opcional — sustituto: ¿caso registrado en planner WCG Créditos?",
        help_text="Para la regla de 3 días hábiles solo cuentan casos en planner; campo opcional.",
        widget=forms.Select(attrs=_SM_SELECT),
    )

    def clean_operation_id(self):
        raw = self.cleaned_data.get("operation_id", "")
        err = validate_operation_id(raw)
        if err:
            raise ValidationError(err)
        return raw.strip().upper()

    def clean_planner_ref(self):
        raw = (self.cleaned_data.get("planner_ref") or "").strip()
        return raw.upper() if raw else ""

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        payload = {
            "une": cd["une"],
            "operation_id": cd["operation_id"],
            "fecha_formalizacion": cd["fecha_formalizacion"].isoformat(),
            "fecha_registro_garantia": cd["fecha_registro_garantia"].isoformat(),
        }
        if cd.get("planner_ref"):
            payload["planner_ref"] = cd["planner_ref"]
        for key in ("registro_mismo_dia_firma", "caso_en_planner_wcg"):
            val = cd.get(key)
            if val:
                payload[key] = val
        return payload


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
        label="Fecha formalización (realizado)",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control form-control-sm"}),
    )
    dias_anticipacion_calendario = forms.IntegerField(
        required=False,
        min_value=0,
        label="Opcional — referencia derivada: días anticipación (calendario)",
        help_text="Ayuda opcional. Si la deja vacía y hay fechas, el sistema puede guardar un cálculo auxiliar.",
        widget=forms.NumberInput(attrs=_SM_INPUT),
    )

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        line = {
            "creditor_name": cd["creditor_name"],
            "due_date": cd["due_date"].isoformat(),
            "formalized": cd["formalized"],
            "date_done": cd["date_done"].isoformat() if cd.get("date_done") else None,
        }
        dias_manual = cd.get("dias_anticipacion_calendario")
        if dias_manual is not None:
            line["dias_anticipacion_calendario"] = dias_manual
        elif cd.get("date_done") and cd.get("due_date"):
            line["dias_anticipacion_calendario_calculado"] = (cd["due_date"] - cd["date_done"]).days
        return {"lines": [line]}


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

    def to_payload(self) -> dict:
        cd = self.cleaned_data
        return {
            "quarter": cd["quarter"],
            "areas_implemented": cd["areas_implemented"],
            "backup_nas_done": cd["backup_nas_done"],
        }


class OpReportesPgcPgo7Form(PeriodFieldsMixin):
    """Campos dinámicos completion_* por reporte (día 7 PGC/PGO)."""

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
            if initial_rows.get(key):
                row = initial_rows[key]
                if row.get("completion_date"):
                    self.fields[f"completion_{key}"].initial = row["completion_date"]
            elif sug:
                self.fields[f"completion_{key}"].help_text = (
                    f"Opcional — referencia derivada (import ArchivosPGO): {sug}"
                )

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
                }
            )
        return {"reports": reports}

    @property
    def report_rows(self):
        return OP_REPORTES_PGO_7_ROWS
