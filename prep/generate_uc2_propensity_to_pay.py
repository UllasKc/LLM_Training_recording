"""
Generate the input data for UC2 - Propensity-to-Pay (collections) model.

Outputs (written to recording_workspace/UC2_Propensity_To_Pay/Deliverables/):
    input 1 - collections accounts.csv   20,000 delinquent accounts, Jan-Jun 2026 (+ duplicates)
    input 2 - data dictionary.xlsx       column definitions and source systems

Deterministic (fixed seed). Data-quality issues, leakage and a gradual
drift across months are planted on purpose - see use_cases/UC2_Propensity_To_Pay_Use_Case.md
(section "Planted data issues") for the answer key. Do NOT open this script on camera.

Usage:  python prep/generate_uc2_propensity_to_pay.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 7
N_ACCOUNTS = 20_000
START, END = pd.Timestamp("2026-01-01"), pd.Timestamp("2026-06-30")
EXTRACT_DATE = pd.Timestamp("2026-08-15")

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "recording_workspace" / "UC2_Propensity_To_Pay" / "Deliverables"


def build_clean(rng: np.random.Generator) -> pd.DataFrame:
    n = N_ACCOUNTS
    df = pd.DataFrame({"account_id": [f"ACC{3000000 + i}" for i in rng.permutation(n)]})

    days = (END - START).days
    # slightly more accounts entering collections in later months (rising stress)
    offsets = np.sort(np.floor(days * rng.beta(1.15, 1.0, n)).astype(int))
    rng.shuffle(offsets)
    dates = START + pd.to_timedelta(offsets, unit="D")
    df["delinquency_date"] = dates.strftime("%Y-%m-%d")
    month_idx = (dates.month - 1).to_numpy()  # 0 = Jan ... 5 = Jun
    df["extract_date"] = EXTRACT_DATE.strftime("%Y-%m-%d")

    # product mix shifts toward BNPL over time
    bnpl_p = 0.14 + 0.025 * month_idx
    u = rng.random(n)
    df["product_type"] = np.where(u < bnpl_p, "BNPL",
                                  np.where(u < bnpl_p + 0.30, "Personal Loan", "Credit Card"))
    df["region"] = rng.choice(["North", "South", "East", "West", "Central"], n,
                              p=[0.22, 0.24, 0.18, 0.20, 0.16])
    df["customer_age"] = np.clip(rng.normal(39, 12, n), 18, 80).round().astype(int)
    df["tenure_months"] = np.clip(rng.gamma(2.0, 22, n), 1, 240).round().astype(int)

    emp = rng.choice(["Salaried", "Self-employed", "Unemployed", "Retired", "Student"], n,
                     p=[0.58, 0.17, 0.10, 0.08, 0.07])
    df["employment_status"] = emp
    inc_mult = pd.Series(emp).map({"Salaried": 1.0, "Self-employed": 1.05, "Unemployed": 0.35,
                                   "Retired": 0.6, "Student": 0.3}).to_numpy()
    income = rng.lognormal(np.log(3600), 0.40, n) * inc_mult
    df["monthly_income"] = income.round(0)

    prod = df["product_type"].to_numpy()
    limit = np.where(prod == "Credit Card", rng.choice([2000, 3000, 5000, 7500, 10000], n),
                     np.where(prod == "BNPL", rng.choice([500, 1000, 1500, 2500], n),
                              rng.choice([5000, 10000, 15000, 25000], n)))
    df["credit_limit_or_loan_amount"] = limit
    util = np.clip(rng.beta(5, 2, n) * 1.05, 0.05, 1.10)
    balance = np.where(prod == "Personal Loan", limit * rng.uniform(0.2, 0.95, n), limit * util)
    df["outstanding_balance"] = balance.round(2)
    df["utilization_ratio"] = np.where(prod == "Personal Loan", np.nan, util.round(3))
    amount_due = np.where(prod == "Personal Loan", limit / rng.choice([24, 36, 48, 60], n),
                          np.maximum(35, balance * rng.uniform(0.03, 0.08, n)))
    df["amount_due"] = amount_due.round(2)

    dpd = np.clip(rng.gamma(1.6, 14, n), 1, 90).round().astype(int)
    df["days_past_due"] = dpd
    df["num_prior_delinquencies_12m"] = rng.poisson(0.9, n)
    df["on_time_payment_ratio_12m"] = np.clip(
        rng.beta(6, 2, n) - 0.06 * df["num_prior_delinquencies_12m"], 0, 1).round(3)
    df["days_since_last_payment"] = (dpd + rng.integers(0, 30, n)).astype(int)
    df["last_payment_amount"] = (amount_due * rng.uniform(0.3, 1.6, n)).round(2)
    df["autopay_enrolled"] = (rng.random(n) < 0.27).astype(int)
    df["preferred_channel"] = rng.choice(["Phone", "SMS", "Email", "App"], n, p=[0.35, 0.25, 0.20, 0.20])
    df["contact_attempts_7d"] = rng.poisson(2.5, n)
    rpc = (rng.random(n) < np.clip(0.15 + 0.10 * df["contact_attempts_7d"], 0, 0.85)).astype(int)
    df["right_party_contact_7d"] = rpc
    df["broken_promises_12m"] = rng.poisson(0.5, n)
    df["promise_to_pay_7d"] = (rpc * (rng.random(n) < 0.45)).astype(int)
    df["has_open_dispute"] = (rng.random(n) < 0.04).astype(int)
    df["hardship_flag"] = (rng.random(n) < np.where(emp == "Unemployed", 0.25, 0.05)).astype(int)

    # ---- outcome: paid amount_due in full within 30 days of delinquency_date ----
    burden = np.minimum(amount_due / np.maximum(income, 1), 1.5)
    emp_eff = pd.Series(emp).map({"Salaried": 0.0, "Self-employed": -0.15, "Unemployed": -0.9,
                                  "Retired": 0.1, "Student": -0.3}).to_numpy()
    prod_eff = pd.Series(prod).map({"Credit Card": 0.0, "Personal Loan": 0.2, "BNPL": -0.25}).to_numpy()
    ptp = df["promise_to_pay_7d"].to_numpy()
    otr = df["on_time_payment_ratio_12m"].to_numpy()
    z = (
        0.90
        - 0.025 * dpd - 0.045 * np.maximum(dpd - 30, 0)              # cure rate collapses after 30 DPD
        + 4.0 * (otr - 0.7) * (otr > 0.5) - 1.2 * (otr <= 0.5)
        - 0.45 * np.minimum(df["num_prior_delinquencies_12m"], 3)
        + 0.50 * df["autopay_enrolled"] * (burden < 0.15)             # autopay helps only if affordable
        + 1.00 * rpc
        + ptp * (1.5 - 0.9 * np.minimum(df["broken_promises_12m"], 2))
        - 2.0 * burden - 2.5 * (burden > 0.35)                        # affordability cliff
        + 1.6 * emp_eff
        + prod_eff
        - 0.015 * np.minimum(df["days_since_last_payment"] - dpd, 30)
        - 1.10 * df["hardship_flag"]
        - 1.00 * df["has_open_dispute"]
        - 1.00 * (util > 0.95) * (prod != "Personal Loan")
        + 0.20 * np.log1p(df["tenure_months"]) - 0.8
        - 0.08 * month_idx                                            # macro stress -> lower cure rate
        - 0.20 * month_idx * (prod == "BNPL")                         # BNPL deteriorates fastest (concept drift)
        - 0.12 * month_idx * (burden > 0.2)
        + rng.normal(0, 0.30, n)
    )
    p = 1 / (1 + np.exp(-z))
    y = (rng.random(n) < p).astype(int)
    df["paid_within_30d"] = y

    # ---- leakage columns (captured AFTER the 30-day outcome window) ----
    df["account_status_at_extract"] = np.where(
        y == 1, rng.choice(["Current", "Settled"], n, p=[0.85, 0.15]),
        rng.choice(["Delinquent", "Charged-Off", "Payment Plan"], n, p=[0.70, 0.12, 0.18]))
    df["amount_recovered_30d"] = np.where(
        y == 1, amount_due * rng.uniform(1.0, 1.3, n), amount_due * rng.uniform(0, 0.6, n) * (rng.random(n) < 0.4)
    ).round(2)
    # total over the whole 30-day window: payers stop receiving calls once they pay
    df["total_contact_attempts_30d"] = df["contact_attempts_7d"] + rng.poisson(np.where(y == 1, 2.5, 5.0))
    return df


def inject_issues(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    df = df.copy()

    def pick(frac, mask=None):
        idx = df.index if mask is None else df.index[mask]
        return rng.choice(idx, int(round(frac * len(idx))), replace=False)

    prod_map = {"Credit Card": ["credit_card", "CC", "CREDIT CARD"],
                "Personal Loan": ["personal loan", "PL", "Personal-Loan"], "BNPL": ["bnpl", "Buy Now Pay Later"]}
    for i in pick(0.035):
        df.at[i, "product_type"] = rng.choice(prod_map[df.at[i, "product_type"]])

    emp_missing = pick(0.06)
    df.loc[emp_missing, "employment_status"] = rng.choice(["", "Unknown", "N/A"], len(emp_missing))
    df.loc[pick(0.10), "monthly_income"] = np.nan
    df.loc[pick(0.005), "monthly_income"] = 0

    df.loc[pick(0.002), "days_past_due"] = -5
    df.loc[pick(0.002), "days_past_due"] = 999
    # business-rule violation: amount_due larger than the outstanding balance
    bad = pick(0.005)
    df.loc[bad, "amount_due"] = (df.loc[bad, "outstanding_balance"] * rng.uniform(1.5, 3, len(bad))).round(2)
    df.loc[pick(0.003, df["utilization_ratio"].notna().to_numpy()), "utilization_ratio"] = 9.99

    for i in pick(0.02):
        d = pd.Timestamp(df.at[i, "delinquency_date"])
        df.at[i, "delinquency_date"] = d.strftime("%d/%m/%Y")

    exact = df.loc[pick(0.012)]
    df = pd.concat([df, exact], ignore_index=True)
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


COLUMN_ORDER = [
    "account_id", "delinquency_date", "extract_date", "product_type", "region", "customer_age",
    "tenure_months", "employment_status", "monthly_income", "credit_limit_or_loan_amount",
    "outstanding_balance", "amount_due", "utilization_ratio", "days_past_due",
    "num_prior_delinquencies_12m", "on_time_payment_ratio_12m", "days_since_last_payment",
    "last_payment_amount", "autopay_enrolled", "preferred_channel", "contact_attempts_7d",
    "right_party_contact_7d", "promise_to_pay_7d", "broken_promises_12m", "has_open_dispute",
    "hardship_flag", "total_contact_attempts_30d", "account_status_at_extract",
    "amount_recovered_30d", "paid_within_30d",
]

DICTIONARY = [
    ("account_id", "Unique account identifier", "string", "Collections System", "Primary key"),
    ("delinquency_date", "Date the account entered collections (missed a due payment)", "date (YYYY-MM-DD)", "Collections System", "Observation point; Jan-Jun 2026"),
    ("extract_date", "Date this dataset was extracted", "date", "Data Warehouse", ""),
    ("product_type", "Credit product that is past due", "category", "Core Lending", "Credit Card, Personal Loan, BNPL"),
    ("region", "Customer home region", "category", "CRM", ""),
    ("customer_age", "Customer age in years at delinquency_date", "integer", "Core Lending", ""),
    ("tenure_months", "Months the customer has held credit with us", "integer", "Core Lending", ""),
    ("employment_status", "Latest known employment status", "category", "Onboarding / KYC", "Updated at onboarding or review"),
    ("monthly_income", "Declared monthly income (USD)", "float", "Onboarding / KYC", ""),
    ("credit_limit_or_loan_amount", "Credit limit (cards / BNPL) or original loan amount", "float", "Core Lending", ""),
    ("outstanding_balance", "Total balance owed at delinquency_date (USD)", "float", "Core Lending", ""),
    ("amount_due", "Past-due amount required to cure the account (USD)", "float", "Core Lending", "Must not exceed outstanding_balance"),
    ("utilization_ratio", "outstanding_balance / credit limit at delinquency_date", "float", "Core Lending", "Revolving products only"),
    ("days_past_due", "Days past due at delinquency_date", "integer", "Collections System", "Valid range 1-90"),
    ("num_prior_delinquencies_12m", "Number of previous delinquency episodes in the last 12 months", "integer", "Collections System", ""),
    ("on_time_payment_ratio_12m", "Share of payments made on time in the last 12 months", "float (0-1)", "Core Lending", ""),
    ("days_since_last_payment", "Days since the last payment, as of delinquency_date", "integer", "Core Lending", ""),
    ("last_payment_amount", "Amount of the last payment before delinquency_date (USD)", "float", "Core Lending", ""),
    ("autopay_enrolled", "1 if the customer has autopay set up", "binary", "Core Lending", ""),
    ("preferred_channel", "Customer's preferred contact channel", "category", "CRM", ""),
    ("contact_attempts_7d", "Collection contact attempts in the first 7 days after delinquency_date", "integer", "Dialler", ""),
    ("right_party_contact_7d", "1 if an agent reached the account holder within the first 7 days", "binary", "Dialler", ""),
    ("promise_to_pay_7d", "1 if the customer made a promise to pay within the first 7 days", "binary", "Collections System", ""),
    ("broken_promises_12m", "Promises to pay not kept in the last 12 months", "integer", "Collections System", ""),
    ("has_open_dispute", "1 if the customer has an open billing dispute", "binary", "Disputes System", ""),
    ("hardship_flag", "1 if the customer is registered for financial hardship support", "binary", "Collections System", ""),
    ("total_contact_attempts_30d", "Total collection contact attempts for this episode", "integer", "Dialler", "Refreshed at extract"),
    ("account_status_at_extract", "Account status at extract_date", "category", "Collections System", "Refreshed at extract"),
    ("amount_recovered_30d", "Amount collected on this episode", "float", "Payments Ledger", "Refreshed at extract"),
    ("paid_within_30d", "TARGET: 1 if amount_due was paid in full within 30 days of delinquency_date", "binary", "Payments Ledger", "Label"),
]


def write_dictionary(path: Path) -> None:
    dd = pd.DataFrame(DICTIONARY, columns=["Column", "Description", "Type", "Source System", "Notes"])
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        dd.to_excel(xw, sheet_name="Data Dictionary", index=False)
        ws = xw.sheets["Data Dictionary"]
        for col, width in zip("ABCDE", [30, 80, 18, 22, 40]):
            ws.column_dimensions[col].width = width
        ws.freeze_panes = "A2"


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = inject_issues(build_clean(rng), rng)[COLUMN_ORDER]
    df.to_csv(OUT_DIR / "input 1 - collections accounts.csv", index=False, lineterminator="\n")
    write_dictionary(OUT_DIR / "input 2 - data dictionary.xlsx")
    print(f"UC2: {len(df):,} rows, {df['account_id'].nunique():,} unique accounts, "
          f"target rate {df['paid_within_30d'].mean():.1%} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
