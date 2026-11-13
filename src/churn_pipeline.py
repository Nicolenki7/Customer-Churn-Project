"""Telco churn: limpieza, feature engineering en SQL y drivers de la baja.

Es la versión ejecutable de `Customer_Churn_Python+SQlite.ipynb`: mismo
código, pensado para correr de punta a punta con `python src/churn_pipeline.py`.
Datos: IBM Telco Customer Churn (ver src/download_data.py).
"""
import pathlib
import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
IMG = ROOT / "docs" / "img"
OUT = ROOT / "outputs"
IMG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})
AZUL, ROJO, GRIS = "#0f62fe", "#da1e28", "#8d8d8d"


def guardar(fig, nombre):
    ruta = IMG / nombre
    fig.tight_layout()
    fig.savefig(ruta, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"  gráfico -> docs/img/{nombre} ({ruta.stat().st_size} B)")


# ---------- 1. carga ----------
df = pd.read_csv(RAW)
print(f"1. cargado: {df.shape[0]} filas x {df.shape[1]} columnas")

# ---------- 2. limpieza ----------
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
nulos = int(df["TotalCharges"].isna().sum())
nuevos = int((df.loc[df["TotalCharges"].isna(), "tenure"] == 0).sum())
print(f"2. TotalCharges: {nulos} no numéricos, {nuevos} con tenure=0 (altas del mes)")

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
for col in ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]:
    df[col] = df[col].map({"Yes": 1, "No": 0})

for col in ["OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies"]:
    df[col] = df[col].replace("No internet service", "No")

df["TotalCharges"] = df["TotalCharges"].fillna(0.0)
df = df.drop(columns=["customerID"])

tasa = df["Churn"].mean()
print(f"   tasa de churn global: {tasa:.1%}  ({int(df['Churn'].sum())} de {len(df)})")
df.to_csv(OUT / "telco_churn_limpio.csv", index=False)

# ---------- 3. feature engineering en SQL ----------
conn = sqlite3.connect(":memory:")
df.to_sql("churn_data", conn, if_exists="replace", index=False)
sql = """
SELECT *,
  CASE WHEN tenure <= 12 THEN '0-1 año'
       WHEN tenure <= 36 THEN '1-3 años'
       WHEN tenure <= 60 THEN '3-5 años'
       ELSE '5+ años' END AS Seniority_Category,
  CASE WHEN MonthlyCharges < 30 THEN 'Bajo'
       WHEN MonthlyCharges < 80 THEN 'Medio'
       ELSE 'Alto' END AS Monthly_Charges_Level
FROM churn_data;
"""
df_fe = pd.read_sql_query(sql, conn)
conn.close()
df_fe.to_csv(OUT / "telco_churn_feature_engineered_for_tableau.csv", index=False)
print(f"3. SQL: +2 columnas -> {df_fe.shape[1]} columnas")

# ---------- 4. diagnóstico visual ----------
fig, ax = plt.subplots(figsize=(7, 1.5))
ax.barh([0], [1 - tasa], color=GRIS, height=.5)
ax.barh([0], [tasa], left=[1 - tasa], color=ROJO, height=.5)
ax.set_xlim(0, 1)
ax.set_ylim(-.6, .6)
ax.axis("off")
ax.text((1 - tasa) / 2, 0, f"se queda {1 - tasa:.1%}", ha="center", va="center",
        color="white", fontweight="bold")
ax.text(1 - tasa / 2, 0, f"churn {tasa:.1%}", ha="center", va="center",
        color="white", fontweight="bold")
ax.set_title(f"7.043 clientes: {int(df['Churn'].sum())} se dieron de baja", loc="left")
guardar(fig, "churn-tasa.svg")


def tasa_por(col, orden=None):
    s = df_fe.groupby(col)["Churn"].agg(["mean", "size"])
    return s.loc[orden] if orden else s.sort_values("mean", ascending=False)


por_contrato = tasa_por("Contract", ["Month-to-month", "One year", "Two year"])
fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(por_contrato.index, por_contrato["mean"] * 100, color=[ROJO, AZUL, AZUL])
for i, (m, n) in enumerate(zip(por_contrato["mean"], por_contrato["size"])):
    ax.text(i, m * 100 + 1, f"{m:.1%}", ha="center", fontweight="bold")
    ax.text(i, -3.2, f"n={n}", ha="center", fontsize=9, color=GRIS)
ax.set_ylabel("churn (%)")
ax.set_ylim(0, 48)
ax.set_title("El contrato mensual concentra el riesgo", loc="left")
ax.tick_params(axis="x", length=0, pad=14)
guardar(fig, "churn-contrato.svg")

antig = tasa_por("Seniority_Category", ["0-1 año", "1-3 años", "3-5 años", "5+ años"])
fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(antig.index, antig["mean"] * 100, color=[ROJO, ROJO, AZUL, AZUL])
for i, m in enumerate(antig["mean"]):
    ax.text(i, m * 100 + 1, f"{m:.1%}", ha="center", fontweight="bold")
ax.set_ylabel("churn (%)")
ax.set_ylim(0, 58)
ax.set_title("El primer año es la ventana crítica", loc="left")
ax.tick_params(axis="x", length=0)
guardar(fig, "churn-antiguedad.svg")

# ---------- 5. modelo y drivers ----------
X = df_fe.drop(columns=["Churn", "Seniority_Category", "Monthly_Charges_Level"])
y = df_fe["Churn"]
cat = X.select_dtypes(exclude="number").columns.tolist()
num = [c for c in X.columns if c not in cat]

pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), cat),
    ("num", StandardScaler(), num),
])
modelo = Pipeline([
    ("pre", pre),
    ("lr", LogisticRegression(max_iter=2000, class_weight="balanced")),
])
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=.25, random_state=42, stratify=y
)
modelo.fit(X_tr, y_tr)
prob = modelo.predict_proba(X_te)[:, 1]
auc = roc_auc_score(y_te, prob)
acc = accuracy_score(y_te, prob > .5)
print(f"5. modelo: AUC {auc:.3f} · accuracy {acc:.3f} · train {len(X_tr)} / test {len(X_te)}")

coefs = pd.DataFrame({
    "feature": modelo.named_steps["pre"].get_feature_names_out(),
    "coef": modelo.named_steps["lr"].coef_[0],
})
coefs["odds_ratio"] = np.exp(coefs["coef"])
coefs = coefs.reindex(coefs["coef"].abs().sort_values(ascending=False).index)
coefs.to_csv(OUT / "churn_feature_importance.csv", index=False)

top = coefs.head(8)[::-1]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.barh(range(len(top)), top["coef"],
        color=[ROJO if c > 0 else AZUL for c in top["coef"]])
ax.set_yticks(range(len(top)))
ax.set_yticklabels(
    [f.replace("cat__", "").replace("num__", "").replace("_", " ")
     for f in top["feature"]],
    fontsize=9.5,
)
ax.axvline(0, color="#333", linewidth=.8)
ax.set_xlabel("coeficiente logístico (positivo = más churn)")
ax.set_title("Qué empuja la baja", loc="left")
guardar(fig, "churn-drivers.svg")

print("\nTOP 8 drivers:")
print(top.iloc[::-1][["feature", "coef", "odds_ratio"]].to_string(index=False))
print("\nchurn por contrato:\n", (por_contrato["mean"] * 100).round(1).to_string())
print("\nchurn por antigüedad:\n", (antig["mean"] * 100).round(1).to_string())
print("\nARPU mensual medio:", round(df.loc[df.Churn == 1, "MonthlyCharges"].mean(), 2),
      "churn vs", round(df.loc[df.Churn == 0, "MonthlyCharges"].mean(), 2), "retenido")
print("tenure medio:", round(df.loc[df.Churn == 1, "tenure"].mean(), 1), "vs",
      round(df.loc[df.Churn == 0, "tenure"].mean(), 1))
