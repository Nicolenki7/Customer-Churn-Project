#!/usr/bin/env python3
"""Descarga el dataset Telco Customer Churn de IBM y verifica su checksum.

El CSV no se versiona: pesa ~1 MB y se puede reconstruir byte a byte
desde la fuente original. Este script garantiza que todo el mundo
analiza exactamente los mismos datos.

Uso:
    python src/download_data.py
    python src/download_data.py --force    # vuelve a bajar aunque exista
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

URL = (
    "https://raw.githubusercontent.com/IBM/"
    "telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
)
SHA256 = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
DESTINO = Path(__file__).resolve().parents[1] / "data" / "raw" / "Telco-Customer-Churn.csv"


def sha256(ruta: Path) -> str:
    """Checksum del archivo, leído por bloques para no cargarlo entero."""
    h = hashlib.sha256()
    with ruta.open("rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Descarga el dataset Telco de IBM.")
    parser.add_argument("--force", action="store_true", help="descarga otra vez")
    args = parser.parse_args()

    if DESTINO.exists() and not args.force:
        print(f"Ya existe: {DESTINO.name}")
    else:
        DESTINO.parent.mkdir(parents=True, exist_ok=True)
        print(f"Descargando {URL}")
        urllib.request.urlretrieve(URL, DESTINO)

    obtenido = sha256(DESTINO)
    if obtenido != SHA256:
        print(f"Checksum distinto.\n  esperado: {SHA256}\n  obtenido: {obtenido}", file=sys.stderr)
        return 1

    kb = DESTINO.stat().st_size / 1024
    print(f"OK  {kb:.0f} KB  sha256 {obtenido[:16]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
