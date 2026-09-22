"""Telco customer churn — exploratory charts for portfolio storytelling."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "telco_churn_feature_engineered_for_tableau.csv"
FI = ROOT / "churn_feature_importance.csv"
FIG = ROOT / "outputs" / "figures"
INSIGHTS = ROOT / "outputs" / "insights.md"
FIG.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.bbox"] = "tight"


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["ChurnLabel"] = df["Churn"].map({0: "Stayed", 1: "Churned"})
    return df


def chart_overall(df: pd.DataFrame) -> None:
    rate = df["Churn"].mean()
    counts = df["ChurnLabel"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(counts.index, counts.values, color=["#2A9D8F", "#E76F51"])
    ax.set_title(f"Overall churn rate: {rate:.1%}")
    ax.set_ylabel("Customers")
    for i, v in enumerate(counts.values):
        ax.text(i, v, f"{v:,}\n({v/len(df):.1%})", ha="center", va="bottom")
    fig.savefig(FIG / "01_overall_churn.png")
    plt.close(fig)


def chart_by_category(df: pd.DataFrame, col: str, title: str, fname: str, order=None) -> None:
    g = df.groupby(col)["Churn"].agg(["mean", "count"]).reset_index()
    if order:
        g[col] = pd.Categorical(g[col], categories=order, ordered=True)
        g = g.sort_values(col)
    else:
        g = g.sort_values("mean", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=g, x=col, y="mean", ax=ax, color="#1B4965")
    ax.set_title(title)
    ax.set_ylabel("Churn rate")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.tick_params(axis="x", rotation=25)
    for i, r in enumerate(g.itertuples()):
        ax.text(i, r.mean, f"n={r.count}", ha="center", va="bottom", fontsize=9)
    fig.savefig(FIG / fname)
    plt.close(fig)


def chart_tenure(df: pd.DataFrame) -> None:
    bins = [0, 6, 12, 24, 48, 72]
    labels = ["0-6m", "6-12m", "1-2y", "2-4y", "4y+"]
    d = df.copy()
    d["tenure_bin"] = pd.cut(d["tenure"], bins=bins, labels=labels, right=True, include_lowest=True)
    chart_by_category(d, "tenure_bin", "Churn rate by tenure", "04_churn_by_tenure.png", order=labels)


def chart_charges_box(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="ChurnLabel", y="MonthlyCharges", palette={"Stayed": "#2A9D8F", "Churned": "#E76F51"}, ax=ax)
    ax.set_title("Monthly charges by churn outcome")
    ax.set_xlabel("")
    ax.set_ylabel("Monthly charges ($)")
    fig.savefig(FIG / "05_monthly_charges_by_churn.png")
    plt.close(fig)


def chart_feature_importance() -> None:
    fi = pd.read_csv(FI).sort_values("Absolute_Coefficient", ascending=True).tail(12)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = np.where(fi["Coefficient"] >= 0, "#E76F51", "#2A9D8F")
    ax.barh(fi["Feature"], fi["Coefficient"], color=colors)
    ax.axvline(0, color="#333", lw=1)
    ax.set_title("Logistic regression coefficients (top |impact|)")
    ax.set_xlabel("Coefficient (→ raises churn risk)")
    fig.savefig(FIG / "06_feature_coefficients.png")
    plt.close(fig)


def chart_heatmap(df: pd.DataFrame) -> None:
    # Contract x InternetService churn rates
    pivot = df.pivot_table(index="Contract", columns="InternetService", values="Churn", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".0%", cmap="YlOrRd", ax=ax)
    ax.set_title("Churn rate: Contract × Internet service")
    fig.savefig(FIG / "07_contract_internet_heatmap.png")
    plt.close(fig)


def write_insights(df: pd.DataFrame) -> None:
    rate = df["Churn"].mean()
    by_contract = df.groupby("Contract")["Churn"].mean().sort_values(ascending=False)
    by_pay = df.groupby("PaymentMethod")["Churn"].mean().sort_values(ascending=False)
    early = df.loc[df["tenure"] <= 12, "Churn"].mean()
    late = df.loc[df["tenure"] > 48, "Churn"].mean()
    fi = pd.read_csv(FI).sort_values("Absolute_Coefficient", ascending=False).head(5)
    lines = [
        "# Telco Churn — Key insights",
        "",
        f"_Dataset: `{DATA.name}` · **{len(df):,}** customers._",
        "",
        "## Headline",
        f"- Overall churn rate: **{rate:.1%}** ({df['Churn'].sum():,} churned).",
        f"- Early tenure (≤12 months) churn: **{early:.1%}** vs long tenure (>48m): **{late:.1%}**.",
        "",
        "## Highest-risk segments",
        f"- Contract: **{by_contract.index[0]}** ({by_contract.iloc[0]:.1%})",
        f"- Payment: **{by_pay.index[0]}** ({by_pay.iloc[0]:.1%})",
        "",
        "## Model drivers (logistic coefficients)",
    ]
    for _, r in fi.iterrows():
        direction = "↑ risk" if r["Coefficient"] > 0 else "↓ risk"
        lines.append(f"- `{r['Feature']}`: {r['Coefficient']:+.3f} ({direction})")
    lines += [
        "",
        "## Business takeaway",
        "- Focus retention on **month-to-month + electronic check + fiber** customers in the first year.",
        "- Longer contracts, tech support, and online security associate with lower churn.",
        "",
        "## Figures",
        "- `outputs/figures/01_overall_churn.png`",
        "- `outputs/figures/02_churn_by_contract.png`",
        "- `outputs/figures/03_churn_by_payment.png`",
        "- `outputs/figures/04_churn_by_tenure.png`",
        "- `outputs/figures/05_monthly_charges_by_churn.png`",
        "- `outputs/figures/06_feature_coefficients.png`",
        "- `outputs/figures/07_contract_internet_heatmap.png`",
    ]
    INSIGHTS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    df = load()
    chart_overall(df)
    chart_by_category(df, "Contract", "Churn rate by contract type", "02_churn_by_contract.png")
    chart_by_category(df, "PaymentMethod", "Churn rate by payment method", "03_churn_by_payment.png")
    chart_tenure(df)
    chart_charges_box(df)
    chart_feature_importance()
    chart_heatmap(df)
    write_insights(df)
    print(f"Done · {len(df):,} customers · figures → {FIG}")


if __name__ == "__main__":
    main()
