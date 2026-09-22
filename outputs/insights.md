# Telco Churn — Key insights

_Dataset: `telco_churn_feature_engineered_for_tableau.csv` · **7,043** customers._

## Headline
- Overall churn rate: **26.5%** (1,869 churned).
- Early tenure (≤12 months) churn: **47.4%** vs long tenure (>48m): **9.5%**.

## Highest-risk segments
- Contract: **Month-to-month** (42.7%)
- Payment: **Electronic check** (45.3%)

## Model drivers (logistic coefficients)
- `tenure`: -0.096 (↓ risk)
- `PaymentMethod_Electronic check`: +0.088 (↑ risk)
- `PaymentMethod_Mailed check`: -0.088 (↓ risk)
- `InternetService_No`: -0.086 (↓ risk)
- `PhoneService`: -0.086 (↓ risk)

## Business takeaway
- Focus retention on **month-to-month + electronic check + fiber** customers in the first year.
- Longer contracts, tech support, and online security associate with lower churn.

## Figures
- `outputs/figures/01_overall_churn.png`
- `outputs/figures/02_churn_by_contract.png`
- `outputs/figures/03_churn_by_payment.png`
- `outputs/figures/04_churn_by_tenure.png`
- `outputs/figures/05_monthly_charges_by_churn.png`
- `outputs/figures/06_feature_coefficients.png`
- `outputs/figures/07_contract_internet_heatmap.png`
