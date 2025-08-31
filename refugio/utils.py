from __future__ import annotations

from datetime import date, datetime


def parse_date(text: str) -> date:
    text = (text or "").strip()
    # formatos aceitos: DD/MM/AAAA ou AAAA-MM-DD
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            continue
    raise ValueError("Formato de data inválido. Use DD/MM/AAAA")


def format_date(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def overlaps(a_start: date, a_end: date, b_start: date, b_end: date) -> bool:
    return not (a_end <= b_start or b_end <= a_start)

