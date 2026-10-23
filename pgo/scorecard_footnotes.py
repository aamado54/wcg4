"""Notas globales n.1, n.2… sin duplicar explicaciones entre tablas."""

from __future__ import annotations

from dataclasses import dataclass, field


BRIEF_TEXTS: dict[str, str] = {
    "row_no_total": (
        "Sin total de fila: ningún promedio mensual con puntaje en las UNE donde aplica el concepto."
    ),
    "row_has_total": (
        "Total de fila: suma de los promedios mensuales del año (solo meses con cierre y con dato; "
        "oct–dic sin cierre no se muestran ni promedian) en cada UNE donde aplica el concepto."
    ),
    "weighted_corner": (
        "Total esquina (tabla completa): suma ponderada de cada total de columna UNE "
        "multiplicado por el peso de la fila «Pesos»."
    ),
}


@dataclass
class FootnoteRegistry:
    _order: list[str] = field(default_factory=list)
    _keys: dict[str, int] = field(default_factory=dict)

    def ref(self, key: str) -> str:
        if key not in BRIEF_TEXTS:
            key = "row_no_total"
        if key not in self._keys:
            self._keys[key] = len(self._order) + 1
            self._order.append(key)
        return f"n.{self._keys[key]}"

    def as_list(self) -> list[dict]:
        return [
            {"num": self._keys[k], "key": k, "text": BRIEF_TEXTS[k]}
            for k in self._order
        ]


def parse_weight_fraction(weight_label: str) -> float:
    if not weight_label:
        return 0.0
    text = str(weight_label).strip().replace(",", ".")
    if text.endswith("%"):
        return float(text[:-1]) / 100.0
    return float(text)


def weighted_column_total(column_totals: list[float | None], weight_labels: list[str]) -> float | None:
    total = 0.0
    any_val = False
    for val, wlabel in zip(column_totals, weight_labels):
        if val is None:
            continue
        w = parse_weight_fraction(wlabel)
        if w <= 0:
            continue
        total += val * w
        any_val = True
    return total if any_val else None
