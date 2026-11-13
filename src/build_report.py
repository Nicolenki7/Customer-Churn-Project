"""Construye docs/report.html de churn (Telco) a partir del CSV por cliente.

Uso: python src/build_report.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report import escribir, num

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "telco_churn.csv")
d["baja"] = d.Churn.astype(str).str.strip().str.lower().isin(["yes", "1", "true"]).astype(int)
d["tramo"] = pd.cut(d.tenure, [-1, 12, 24, 48, 100], labels=["0-12 m", "13-24 m", "25-48 m", "más de 48"])

filas = []
for g, s in (("contrato", "Contract"), ("tramo", "tramo"), ("pago", "PaymentMethod")):
    for k, sub in d.groupby(s):
        filas.append({"a": "todos", "g": g, "k": str(k), "v": round(100 * sub.baja.mean(), 1), "u": "%"})
for k, sub in d.groupby("Contract"):
    filas.append({"a": "todos", "g": "cuota", "k": str(k), "v": round(float(sub.MonthlyCharges.mean()), 2), "u": "$"})

tabla = [[str(k), num(len(s)), f"{num(100 * s.baja.mean(), 1)} %",
          f"{num(s.MonthlyCharges.mean(), 2)} $", num(s.tenure.mean(), 0)]
         for k, s in d.groupby("PaymentMethod")]
tabla.sort(key=lambda r: float(r[2].replace(" %", "").replace(",", ".")), reverse=True)

escribir(
    ROOT / "docs" / "report.html",
    eyebrow="Retención · Telco churn",
    titulo="Churn: quién se va y cuánto cuesta que se vaya",
    pregunta=("Una operadora pierde clientes todos los meses y no todos se van por el mismo motivo. "
              "La pregunta útil no es cuánta gente se va, sino qué contratos y qué tramos de antigüedad "
              "concentran las bajas, porque ahí es donde se puede intervenir."),
    kpis=[("Clientes", num(len(d)), "una fila por cliente"),
          ("Bajas", f"{num(100 * d.baja.mean(), 1)} %", "tasa global"),
          ("Cuota media", f"{num(d.MonthlyCharges.mean(), 2)} $", "por mes"),
          ("Antigüedad media", f"{num(d.tenure.mean(), 0)} m", "meses como cliente")],
    filtros=None,
    graficos=[
        {"id": "c", "grupo": "contrato", "titulo": "Tasa de baja por tipo de contrato",
         "subtitulo": "% de clientes que se van, en cada grupo", "unidad": "%"},
        {"id": "t", "grupo": "tramo", "titulo": "Tasa de baja por antigüedad",
         "subtitulo": "el primer año es el que decide la relación", "unidad": "%"},
        {"id": "p", "grupo": "pago", "titulo": "Tasa de baja por método de pago",
         "subtitulo": "el domiciliado retiene; el manual no", "unidad": "%"},
        {"id": "m", "grupo": "cuota", "titulo": "Cuota mensual media por contrato",
         "subtitulo": "lo que paga de media cada grupo", "unidad": "$"},
    ],
    filas=filas,
    tabla={"titulo": "El detalle por método de pago",
           "subtitulo": "ordenado de más a menos bajas",
           "cabeceras": ["Método", "Clientes", "Bajas", "Cuota media", "Antigüedad (m)"],
           "filas": tabla},
    metodo=["Cada fila es un cliente; la tasa es la media de Churn convertida a 0/1.",
            "Los tramos de antigüedad se cortan en 12, 24 y 48 meses, que son los saltos de contrato del dataset.",
            "No se cruzan dos dimensiones a la vez: cada gráfico responde una pregunta distinta.",
            "La cuota es MonthlyCharges, no el gasto histórico total."],
    limitaciones=["El CSV no trae fecha de baja ni motivo: no se puede saber cuándo se fue ni por qué.",
                  "Sin coste de adquisición no se puede calcular el valor de vida del cliente.",
                  "Es una foto de una operadora ficticia congelada en el tiempo, no una serie mensual.",
                  "Los grupos pequeños (dos meses de contrato) tienen tasas inestables."],
    fuente="telco_churn.csv",
    metodo_sub="Una fila por cliente; cada corte agrupa por una sola dimensión.",
    lim_sub="Lo que este dataset no permite afirmar.")
print("docs/report.html:", (ROOT / "docs" / "report.html").stat().st_size, "bytes")
