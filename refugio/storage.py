from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Cliente, Quarto, Reserva, TipoQuarto


class StorageJSON:
    """Persistência simples em JSON em uma pasta `data/` no projeto."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.fp_clientes = self.data_dir / "clientes.json"
        self.fp_quartos = self.data_dir / "quartos.json"
        self.fp_reservas = self.data_dir / "reservas.json"

    # ----- Clientes -----
    def save_clientes(self, clientes: Iterable[Cliente]) -> None:
        data = [c.to_dict() for c in clientes]
        self.fp_clientes.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_clientes(self) -> list[Cliente]:
        if not self.fp_clientes.exists():
            return []
        data = json.loads(self.fp_clientes.read_text(encoding="utf-8") or "[]")
        return [Cliente.from_dict(d) for d in data]

    # ----- Quartos -----
    def save_quartos(self, quartos: Iterable[Quarto]) -> None:
        data = [q.to_dict() for q in quartos]
        self.fp_quartos.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_quartos(self) -> list[Quarto]:
        if not self.fp_quartos.exists():
            return self._seed_quartos()
        data = json.loads(self.fp_quartos.read_text(encoding="utf-8") or "[]")
        return [Quarto.from_dict(d) for d in data]

    def _seed_quartos(self) -> list[Quarto]:
        # Inicializa com um pequeno conjunto de quartos
        seed = []
        preco = {TipoQuarto.SINGLE: 200.0, TipoQuarto.DOUBLE: 320.0, TipoQuarto.SUITE: 520.0}
        n = 1
        for _ in range(4):
            seed.append(Quarto(numero=n, tipo=TipoQuarto.SINGLE, preco_diaria=preco[TipoQuarto.SINGLE])); n += 1
        for _ in range(3):
            seed.append(Quarto(numero=n, tipo=TipoQuarto.DOUBLE, preco_diaria=preco[TipoQuarto.DOUBLE])); n += 1
        for _ in range(3):
            seed.append(Quarto(numero=n, tipo=TipoQuarto.SUITE, preco_diaria=preco[TipoQuarto.SUITE])); n += 1
        self.save_quartos(seed)
        return seed

    # ----- Reservas -----
    def save_reservas(self, reservas: Iterable[Reserva]) -> None:
        data = [r.to_dict() for r in reservas]
        self.fp_reservas.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_reservas(self) -> list[Reserva]:
        if not self.fp_reservas.exists():
            return []
        data = json.loads(self.fp_reservas.read_text(encoding="utf-8") or "[]")
        return [Reserva.from_dict(d) for d in data]

