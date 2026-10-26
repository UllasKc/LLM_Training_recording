"""
Shared configuration for the collections propensity-to-pay pipeline.

Used by all four notebooks so that paths, business rules, time windows and the model
definitions are defined in exactly one place:

    01_data_preprocessing.ipynb    input 1 -> artifact 2 (cleaned accounts), artifact 3 (data quality log)
    02_model_training.ipynb        out-of-time split -> artifact 4 (time split), artifact 5 (trained models)
    03_model_testing.ipynb         June evaluation, calibration, prioritisation -> artifact 6, artifact 7
    04_worklist_and_package.ipynb  June agent work list -> artifact 8, final output 3 (model package)
"""
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------- paths
# Deliverables/ is the first parent folder that contains 1_Input
BASE = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "1_Input").exists())
INPUT = BASE / "1_Input"
INTERMEDIATE = BASE / "3_Intermediate"
OUTPUT = BASE / "4_Output"
INTERMEDIATE.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

RAW_FILE = INPUT / "input 1 - collections accounts.csv"
CLEAN_FILE = INTERMEDIATE / "artifact 2 - cleaned accounts.csv"
DQ_LOG_FILE = INTERMEDIATE / "artifact 3 - data quality log.csv"
SPLIT_FILE = INTERMEDIATE / "artifact 4 - time split.csv"
MODEL_DIR = INTERMEDIATE / "artifact 5 - trained models"
COMPARISON_FILE = INTERMEDIATE / "artifact 6 - model comparison.csv"
CHART_DIR = INTERMEDIATE / "artifact 7 - evaluation charts"
WORKLIST_FILE = INTERMEDIATE / "artifact 8 - june agent work list.csv"
PACKAGE_DIR = OUTPUT / "final output 3 - model package"

# ---------------------------------------------------------------- business rules (input 3 - strategy brief)
SCORING_DAY = 7                     # accounts are re-prioritised 7 days after entering collections
AGENT_CAPACITY_SHARE = 0.37         # 25 agents can work ~37% of a monthly cohort in depth
TRAIN_MONTHS = [1, 2, 3, 4]         # Jan-Apr 2026
CALIBRATION_MONTH = 5               # May 2026: validation and probability calibration
TEST_MONTH = 6                      # June 2026: untouched out-of-time test, and the cohort for the work list

ACCEPTANCE = {"roc_auc": 0.78}
RANDOM_STATE = 42

# ---------------------------------------------------------------- columns
TARGET = "paid_within_30d"
ID_COLUMNS = ["account_id", "delinquency_date", "extract_date", "cohort_month"]
LEAKY_COLUMNS = ["account_status_at_extract", "amount_recovered_30d"]   # captured after the day-7 decision point
SPECIALIST_FLAGS = ["has_open_dispute", "hardship_flag"]                # model inputs, but routed to a specialist team
CATEGORICAL = ["product_type", "region", "employment_status", "preferred_channel"]

EXCLUDED = ID_COLUMNS + LEAKY_COLUMNS + [TARGET]


def feature_columns(df):
    """All model inputs: every column that is not an ID / time index, leaky or the target."""
    return [c for c in df.columns if c not in EXCLUDED]


def numeric_columns(df):
    return [c for c in feature_columns(df) if c not in CATEGORICAL]


# ---------------------------------------------------------------- models
def build_baseline(df):
    """Logistic regression: median-imputed, scaled numerics + one-hot categoricals."""
    preprocess = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_columns(df)),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return make_pipeline(preprocess, LogisticRegression(max_iter=2000))


def build_gradient_boosting(df):
    """Histogram gradient boosting: handles missing numerics natively."""
    preprocess = ColumnTransformer([
        ("num", "passthrough", numeric_columns(df)),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
    ], verbose_feature_names_out=False)
    model = HistGradientBoostingClassifier(
        learning_rate=0.05, max_iter=300, max_leaf_nodes=31, min_samples_leaf=40,
        l2_regularization=1.0, early_stopping=False, random_state=RANDOM_STATE)
    return make_pipeline(preprocess, model)
