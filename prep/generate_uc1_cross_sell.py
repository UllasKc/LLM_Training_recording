"""
Generate synthetic input data for UC1 - Cross-sell / Up-sell model.

Outputs (written to recording_workspace/UC1_Cross_Sell/Deliverables/1_Input/):
    input 1 - customers.csv          20,000 synthetic retail-bank customers (+ CRM-merge duplicates)
    input 2 - data dictionary.xlsx   column definitions and source systems

Fully synthetic and deterministic (fixed seed). Data-quality issues are planted on purpose
so they can be found and fixed on camera - see use_cases/UC1_Cross_Sell_Use_Case.md
(section "Planted data issues") for the answer key. Do NOT open this script on camera.

Usage:  python prep/generate_uc1_cross_sell.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_CUSTOMERS = 20_000
SNAPSHOT_DATE = pd.Timestamp("2026-06-30")

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "recording_workspace" / "UC1_Cross_Sell" / "Deliverables" / "1_Input"


def build_clean(rng: np.random.Generator) -> pd.DataFrame:
    n = N_CUSTOMERS
    df = pd.DataFrame({"customer_id": [f"CUST{100000 + i}" for i in rng.permutation(n)]})
    df["snapshot_date"] = SNAPSHOT_DATE.strftime("%Y-%m-%d")

    df["age"] = np.clip(rng.normal(42, 13, n), 18, 85).round().astype(int)
    df["gender"] = rng.choice(["Female", "Male", "Other"], n, p=[0.49, 0.50, 0.01])
    df["region"] = rng.choice(["North", "South", "East", "West", "Central"], n,
                              p=[0.22, 0.24, 0.18, 0.20, 0.16])

    income = rng.lognormal(np.log(4200), 0.45, n)
    df["monthly_income"] = income.round(0)
    df["customer_segment"] = np.select(
        [income > 9000, income > 5500], ["Premier", "Affluent"], default="Mass")

    tenure = np.clip(rng.gamma(2.0, 30, n), 1, 300).round().astype(int)
    df["tenure_months"] = tenure
    df["customer_since"] = [
        (SNAPSHOT_DATE - pd.DateOffset(months=int(t))).strftime("%Y-%m-%d") for t in tenure]

    df["primary_product"] = rng.choice(
        ["Current Account", "Savings Account", "Credit Card", "Personal Loan", "Mortgage"], n,
        p=[0.42, 0.25, 0.18, 0.09, 0.06])
    num_products = rng.choice([1, 2, 3, 4], n, p=[0.55, 0.30, 0.11, 0.04])
    df["num_products"] = num_products
    # months since the most recent product was opened (cannot exceed tenure)
    last_open = np.where(num_products == 1, tenure,
                         np.minimum(tenure, rng.integers(0, 60, n)))
    df["months_since_last_product_open"] = last_open

    df["avg_monthly_balance"] = (income * rng.lognormal(0.2, 0.7, n)).round(2)
    df["credit_score"] = np.clip(rng.normal(680, 70, n), 300, 850).round().astype(int)

    app_p = np.clip(0.95 - 0.012 * (df["age"] - 25), 0.25, 0.95)
    has_app = (rng.random(n) < app_p).astype(int)
    df["has_mobile_app"] = has_app
    df["digital_logins_30d"] = rng.poisson(np.where(has_app == 1, 9, 1.5))
    df["num_transactions_90d"] = rng.poisson(25 + 2.0 * df["digital_logins_30d"])
    df["branch_visits_90d"] = rng.poisson(np.where(has_app == 1, 0.6, 2.2))

    opt_in = (rng.random(n) < 0.76).astype(int)
    df["marketing_opt_in"] = opt_in
    df["email_open_rate"] = np.where(opt_in == 1, rng.beta(2.2, 6, n), np.nan).round(3)
    df["complaints_12m"] = rng.poisson(0.22, n)
    df["last_contact_channel"] = rng.choice(["Email", "SMS", "Phone", "Branch", "None"], n,
                                            p=[0.38, 0.22, 0.14, 0.10, 0.16])
    df["days_since_last_contact"] = np.where(
        df["last_contact_channel"] == "None", np.nan, rng.integers(1, 365, n))

    # ---- outcome: bought another product within 90 days after the snapshot ----
    tenure_eff = np.select([tenure < 6, (tenure >= 12) & (tenure <= 60)], [-0.45, 0.55], 0.0)
    prod_eff = pd.Series(num_products).map({1: 0.0, 2: 0.55, 3: 0.75, 4: 0.15}).to_numpy()
    recency_eff = np.select([last_open < 6, (last_open >= 6) & (last_open <= 24)], [-0.55, 0.35], 0.0)
    open_rate = np.nan_to_num(df["email_open_rate"].to_numpy(), nan=0.0)
    logins = np.minimum(df["digital_logins_30d"], 20)
    z = (
        -4.15
        + 1.6 * prod_eff
        + 1.6 * tenure_eff
        + 1.6 * recency_eff
        + 0.11 * logins * has_app                                   # engagement only counts via the app
        + 4.0 * np.maximum(open_rate - 0.20, 0) * opt_in              # threshold effect on email engagement
        - 0.6 * (1 - opt_in)
        + 0.9 * ((income > 6000) & (tenure >= 12) & (tenure <= 60))   # affluent & established
        + 0.50 * np.clip((df["credit_score"] - 680) / 70, -2, 1)       # capped upside
        - 0.9 * np.minimum(df["complaints_12m"], 2)
        - 0.0022 * (df["age"] - 36) ** 2
        + 0.9 * ((df["primary_product"] == "Credit Card") & (df["avg_monthly_balance"] > 6000))
        + 0.6 * ((df["primary_product"] == "Mortgage") & (num_products <= 2))
        + rng.normal(0, 0.30, n)
    )
    p = 1 / (1 + np.exp(-z))
    y = (rng.random(n) < p).astype(int)
    df["next_product_purchased_90d"] = y

    # ---- leakage columns (populated by downstream systems AFTER the purchase) ----
    df["cross_sell_product_type"] = np.where(
        y == 1, rng.choice(["Credit Card", "Savings Account", "Personal Loan", "Insurance"], n,
                           p=[0.38, 0.27, 0.15, 0.20]), "")
    df["welcome_pack_sent"] = np.where(y == 1, rng.random(n) < 0.94, rng.random(n) < 0.02).astype(int)
    return df


def inject_issues(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    df = df.copy()

    def pick(frac, mask=None):
        idx = df.index if mask is None else df.index[mask]
        return rng.choice(idx, int(round(frac * len(idx))), replace=False)

    # inconsistent category labels
    reg_map = {"North": ["north", "NORTH ", "N."], "South": ["south", "SOUTH", " South"],
               "East": ["east", "EAST "], "West": ["west", "W."], "Central": ["central", "CENTRAL"]}
    for i in pick(0.04):
        df.at[i, "region"] = rng.choice(reg_map[df.at[i, "region"]])
    prod_map = {"Current Account": ["current acct", "CURRENT ACCOUNT"],
                "Savings Account": ["Savings", "savings account"],
                "Credit Card": ["CREDIT CARD", "credit card", "CC"],
                "Personal Loan": ["personal loan", "P. Loan"], "Mortgage": ["mortgage", "MORTGAGE "]}
    for i in pick(0.03):
        df.at[i, "primary_product"] = rng.choice(prod_map[df.at[i, "primary_product"]])

    # missing values (income missing more often for Mass segment)
    mass = (df["customer_segment"] == "Mass").to_numpy()
    df.loc[pick(0.10, mass), "monthly_income"] = np.nan
    df.loc[pick(0.04, ~mass), "monthly_income"] = np.nan
    df.loc[pick(0.03), "credit_score"] = np.nan

    # sentinel / impossible values
    df.loc[pick(0.002), "age"] = 999
    df.loc[pick(0.001), "age"] = 0
    df.loc[pick(0.003), "avg_monthly_balance"] = -99999
    df.loc[pick(0.002), "tenure_months"] = -1

    # mixed date formats in customer_since (DD/MM/YYYY)
    for i in pick(0.02):
        d = pd.Timestamp(df.at[i, "customer_since"])
        df.at[i, "customer_since"] = d.strftime("%d/%m/%Y")

    # CRM-merge duplicates: exact copies + same customer with a refreshed balance
    exact = df.loc[pick(0.010)]
    near = df.loc[pick(0.003)].copy()
    near["avg_monthly_balance"] = (near["avg_monthly_balance"] * rng.uniform(0.9, 1.1, len(near))).round(2)
    near["last_contact_channel"] = "Email"
    df = pd.concat([df, exact, near], ignore_index=True)
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


COLUMN_ORDER = [
    "customer_id", "snapshot_date", "customer_since", "tenure_months", "age", "gender", "region",
    "customer_segment", "monthly_income", "primary_product", "num_products",
    "months_since_last_product_open", "avg_monthly_balance", "credit_score", "has_mobile_app",
    "digital_logins_30d", "num_transactions_90d", "branch_visits_90d", "marketing_opt_in",
    "email_open_rate", "complaints_12m", "last_contact_channel", "days_since_last_contact",
    "welcome_pack_sent", "cross_sell_product_type", "next_product_purchased_90d",
]

DICTIONARY = [
    ("customer_id", "Unique customer identifier", "string", "Core Banking", "Primary key"),
    ("snapshot_date", "Date the feature snapshot was taken", "date (YYYY-MM-DD)", "Data Warehouse", "All features are as of this date"),
    ("customer_since", "Date the customer relationship started", "date", "Core Banking", ""),
    ("tenure_months", "Months since customer_since, as of snapshot", "integer", "Data Warehouse", "Derived"),
    ("age", "Customer age in years at snapshot", "integer", "Core Banking", ""),
    ("gender", "Customer self-reported gender", "category", "Core Banking", "Protected attribute"),
    ("region", "Home region of the customer", "category", "CRM", "North, South, East, West, Central"),
    ("customer_segment", "Value segment assigned by Marketing", "category", "CRM", "Mass, Affluent, Premier"),
    ("monthly_income", "Declared monthly income (USD)", "float", "Onboarding / KYC", "Not mandatory at onboarding"),
    ("primary_product", "Customer's main product with the bank", "category", "Core Banking", ""),
    ("num_products", "Number of active products held at snapshot", "integer", "Core Banking", ""),
    ("months_since_last_product_open", "Months since the most recent product was opened", "integer", "Core Banking", ""),
    ("avg_monthly_balance", "Average monthly balance across accounts, last 6 months (USD)", "float", "Data Warehouse", ""),
    ("credit_score", "Bureau credit score at snapshot", "integer", "Credit Bureau feed", "Range 300-850"),
    ("has_mobile_app", "1 if the customer has activated the mobile app", "binary", "Digital Platform", ""),
    ("digital_logins_30d", "Number of app / web logins in the 30 days before snapshot", "integer", "Digital Platform", ""),
    ("num_transactions_90d", "Number of card and account transactions, 90 days before snapshot", "integer", "Data Warehouse", ""),
    ("branch_visits_90d", "Branch visits in the 90 days before snapshot", "integer", "Branch System", ""),
    ("marketing_opt_in", "1 if the customer consented to marketing communications", "binary", "CRM / Consent", "Compliance: only opted-in customers may be contacted"),
    ("email_open_rate", "Share of marketing emails opened, last 12 months", "float (0-1)", "Marketing Automation", "Only tracked when emails were sent"),
    ("complaints_12m", "Number of complaints logged in the last 12 months", "integer", "Complaints System", ""),
    ("last_contact_channel", "Channel of the most recent outbound marketing contact", "category", "Marketing Automation", "None = never contacted"),
    ("days_since_last_contact", "Days since the most recent outbound marketing contact", "integer", "Marketing Automation", ""),
    ("welcome_pack_sent", "1 if a welcome pack has been dispatched to the customer", "binary", "Fulfilment System", "Refreshed daily"),
    ("cross_sell_product_type", "Category of the most recent cross-sell product", "category", "Sales Ledger", "Refreshed daily"),
    ("next_product_purchased_90d", "TARGET: 1 if the customer opened an additional product within 90 days after snapshot_date", "binary", "Sales Ledger", "Label"),
]


def write_dictionary(path: Path) -> None:
    dd = pd.DataFrame(DICTIONARY, columns=["Column", "Description", "Type", "Source System", "Notes"])
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        dd.to_excel(xw, sheet_name="Data Dictionary", index=False)
        ws = xw.sheets["Data Dictionary"]
        for col, width in zip("ABCDE", [32, 80, 18, 22, 48]):
            ws.column_dimensions[col].width = width
        ws.freeze_panes = "A2"


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = inject_issues(build_clean(rng), rng)[COLUMN_ORDER]
    df.to_csv(OUT_DIR / "input 1 - customers.csv", index=False, lineterminator="\n")
    write_dictionary(OUT_DIR / "input 2 - data dictionary.xlsx")
    print(f"UC1: {len(df):,} rows, {df['customer_id'].nunique():,} unique customers, "
          f"target rate {df['next_product_purchased_90d'].mean():.1%} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
