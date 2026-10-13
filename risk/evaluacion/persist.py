"""Persistencia en BD del dataset consolidado de evaluación (Task 3B)."""

from __future__ import annotations

from typing import Any

from risk.evaluacion.reader import (
    AltmanModel,
    CompanyEval,
    EvaluacionDataset,
    PeriodPoint,
)


def dataset_to_dict(dataset: EvaluacionDataset) -> dict[str, Any]:
    return dataset.to_dict()


def dataset_from_dict(data: dict[str, Any]) -> EvaluacionDataset:
    companies: list[CompanyEval] = []
    for raw in data.get("companies") or []:
        periods: list[PeriodPoint] = []
        for period in raw.get("periods") or []:
            periods.append(
                PeriodPoint(
                    year=int(period["year"]),
                    status=period.get("status"),
                    metrics=dict(period.get("metrics") or {}),
                    z_scores=dict(period.get("z_scores") or {}),
                    z_label=period.get("z_label"),
                )
            )
        companies.append(
            CompanyEval(
                code=str(raw.get("code") or ""),
                name=str(raw.get("name") or ""),
                currency_unit=raw.get("currency_unit"),
                giro=raw.get("giro"),
                auditor=raw.get("auditor"),
                periods=periods,
            )
        )

    models: list[AltmanModel] = []
    for raw in data.get("altman_models") or []:
        models.append(
            AltmanModel(
                id=int(raw["id"]),
                name=str(raw.get("name") or ""),
                low_cut=raw.get("low_cut"),
                high_cut=raw.get("high_cut"),
                bajo_riesgo=raw.get("bajo_riesgo"),
                riesgo_moderado=raw.get("riesgo_moderado"),
                alto_riesgo=raw.get("alto_riesgo"),
            )
        )

    return EvaluacionDataset(
        source=str(data.get("source") or ""),
        sheets_read=list(data.get("sheets_read") or []),
        sheets_missing=list(data.get("sheets_missing") or []),
        companies=companies,
        altman_models=models,
        primary_z_key=str(data.get("primary_z_key") or "z_emergentes"),
        errors=list(data.get("errors") or []),
    )


def save_import_run(dataset: EvaluacionDataset, *, user=None, plantillas_count: int = 0):
    from risk.models import EvaluacionImportRun

    return EvaluacionImportRun.objects.create(
        uploaded_by=user if getattr(user, "is_authenticated", False) else None,
        source_label=dataset.source,
        companies_count=len(dataset.companies),
        plantillas_count=plantillas_count,
        status=dataset.status,
        dataset_json=dataset_to_dict(dataset),
        alerts=list(dataset.errors or [])[:50],
    )


def load_latest_dataset() -> EvaluacionDataset | None:
    from risk.models import EvaluacionImportRun

    run = EvaluacionImportRun.objects.order_by("-created_at").first()
    if not run or not run.dataset_json:
        return None
    dataset = dataset_from_dict(run.dataset_json)
    dataset.source = f"BD ({run.created_at:%Y-%m-%d %H:%M}) — {dataset.source}"
    return dataset
