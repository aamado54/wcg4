"""Lectura y consolidación de plantillas Excel por cliente → workbook evaluación."""

from .pipeline import build_evaluacion_workbook, consolidate_templates

__all__ = ["consolidate_templates", "build_evaluacion_workbook"]
