# Plan de ejecucion

## Estado actual
- Dataset Telco versionado (7.043 filas, 22 columnas) validado por CI.
- Notebook de analisis, features para Tableau e importancias de regresion logistica.

## Proximos pasos
1. Extraer el notebook a `src/train.py` con CLI.
2. `tests/test_schema.py`: columnas esperadas y rangos validos.
3. Versionar `metrics.json` (AUC, recall, matriz de confusion) con semilla fija.
4. Comparar contra una linea base (churn = contrato month-to-month).

## Criterio de aceptacion
- CI verde y metricas reproducibles con la misma semilla.

## Riesgos
- Desbalance de clases: reportar recall y no solo accuracy.
