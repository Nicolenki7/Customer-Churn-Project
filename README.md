# 📉 Customer Churn Prediction — Telco Analytics

**Predictive Analytics | Logistic Regression | Customer Risk Profiling | Tableau Dashboard**

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn)](https://scikit-learn.org/)
[![Tableau](https://img.shields.io/badge/Tableau-E97627?logo=tableau)](https://www.tableau.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Overview

End-to-end churn analysis combining demographic and usage data to identify at-risk customers for a telecommunications company. Demonstrates predictive analytics workflow from data cleaning (Python) through feature transformation (SQL) to risk segment visualization (Tableau).

This project showcases production-ready patterns for customer retention analytics with actionable risk profiling.

---

## 💼 Business Impact

- **Proactive Retention**: Identify at-risk customers before they churn
- **Targeted Interventions**: Enable marketing teams to focus retention efforts
- **Revenue Protection**: Reduce customer acquisition costs through retention
- **Risk Segmentation**: Visual dashboards for executive decision-making

---

## 🛠️ Technical Stack

| Category | Technologies |
| :--- | :--- |
| **Data Cleaning** | Python, Pandas |
| **Feature Engineering** | SQL (PostgreSQL/MySQL) |
| **Machine Learning** | scikit-learn (Logistic Regression) |
| **Visualization** | Tableau |
| **Data Storage** | CSV, SQL Database |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  CHURN PREDICTION PIPELINE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DATA INGESTION                                             │
│  └─→ Telco Customer Churn dataset (CSV)                     │
│      - Demographics, usage, contract, billing data          │
│                                                              │
│  DATA CLEANING (Python)                                     │
│  └─→ Null handling, type correction, outlier detection      │
│                                                              │
│  FEATURE TRANSFORMATION (SQL)                               │
│  └─→ Feature engineering, aggregations, encoding            │
│                                                              │
│  MODELING (Logistic Regression)                             │
│  └─→ Churn probability prediction, coefficient analysis     │
│                                                              │
│  VISUALIZATION (Tableau)                                    │
│  └─→ Risk segment dashboard, driver analysis                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

### Data Cleaning (Python)
- **Null Handling**: Missing value imputation
- **Type Correction**: Consistent data types
- **Outlier Detection**: Statistical anomaly identification

### Feature Engineering (SQL)
- **Usage Aggregations**: Monthly usage patterns
- **Tenure Calculations**: Customer lifetime metrics
- **Contract Features**: Contract type, payment method encoding

### Logistic Regression Model
- **Algorithm**: Logistic Regression (scikit-learn)
- **Output**: Churn probability (0-1)
- **Interpretability**: Coefficient-based driver analysis

### Tableau Dashboard
- **Risk Segments**: High/Medium/Low churn risk
- **Driver Analysis**: Feature importance visualization
- **Demographic Breakdown**: Age, tenure, contract type analysis

---

## 📊 Results & Metrics

| Metric | Value |
| :--- | :--- |
| **Model Type** | Logistic Regression |
| **Key Drivers** | Contract type, tenure, monthly charges |
| **Risk Segments** | 3 tiers (High/Medium/Low) |
| **Visualization** | Interactive Tableau dashboard |

---

## 📁 Project Structure

```
Customer-Churn-Project/
├── data/                              # Raw and processed data
├── notebooks/                         # Python cleaning notebooks
├── sql/                               # Feature engineering scripts
├── models/                            # Trained model files
├── tableau/                           # Tableau workbook (.twbx)
└── README.md                          # Project documentation
```

---

## 🔧 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Nicolenki7/Customer-Churn-Project.git
cd Customer-Churn-Project

# Install Python dependencies
pip install -r requirements.txt

# Run data cleaning
python src/clean_data.py

# Execute feature engineering (SQL)
psql -f sql/feature_engineering.sql

# Train model
python src/train_model.py

# Open Tableau dashboard
open tableau/Churn_Analysis.twbx
```

---

## 📈 Usage

### Dashboard Features

| Visualization | Purpose |
| :--- | :--- |
| **Risk Distribution** | Customer count by risk tier |
| **Driver Analysis** | Feature importance (coefficients) |
| **Demographic Breakdown** | Churn rate by age, gender, tenure |
| **Contract Analysis** | Churn by contract type, payment method |
| **Geographic View** | Regional churn patterns |

### Key Insights
- **Month-to-month contracts** have highest churn rates
- **Tenure < 12 months** correlates with higher churn
- **Fiber optic** service has higher churn than DSL
- **Electronic check** payment method shows elevated risk

---

## 🎯 Key Learnings

- **Logistic Regression** provides interpretable coefficients for business stakeholders
- **Feature engineering** in SQL enables scalable transformations
- **Risk segmentation** makes predictions actionable for marketing teams
- **Tableau** excels at executive-level churn dashboards

---

## 🔮 Future Enhancements

- [ ] Advanced models (Random Forest, XGBoost, Neural Networks)
- [ ] SHAP values for local interpretability
- [ ] Real-time churn scoring API
- [ ] A/B testing framework for retention campaigns
- [ ] Customer lifetime value (CLV) integration

---

## 🔗 Links

| Resource | URL |
| :--- | :--- |
| **Repository** | https://github.com/Nicolenki7/Customer-Churn-Project |
| **Dataset** | [Telco Churn on Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |

---

## 📝 Resumen en Español

Análisis completo de churn combinando datos demográficos y de uso para identificar clientes en riesgo de abandono en una empresa de telecomunicaciones.

El flujo incluye limpieza de datos (Python), transformación de features (SQL), modelado predictivo (Regresión Logística), y visualización de segmentos de riesgo (Tableau). Los drivers principales son tipo de contrato, tenure, y cargos mensuales.

---

## 📄 License

MIT License — Feel free to fork, modify, and use for personal or commercial projects.

---

## 👤 Author

**Nicolás Zalazar** | Senior Data Engineer & Microsoft Fabric Specialist

- GitHub: [@Nicolenki7](https://github.com/Nicolenki7)
- LinkedIn: [nicolas-zalazar-63340923a](https://www.linkedin.com/in/nicolas-zalazar-63340923a)
- Portfolio: [nicolenki7.github.io/Portfolio](https://nicolenki7.github.io/Portfolio/)
- Email: zalazarn046@gmail.com

---

*Last Updated: March 2026*
