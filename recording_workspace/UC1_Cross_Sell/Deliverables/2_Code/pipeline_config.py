"""
Shared configuration for the cross-sell propensity pipeline.

Used by all four notebooks so that paths, the feature list and the model definitions
are defined in exactly one place:

    01_data_preprocessing.ipynb   input 1 -> artifact 2 (cleaned data), artifact 3 (data quality log)
    02_model_training.ipynb       artifact 2 -> artifact 4 (train/test split), artifact 5 (trained models)
    03_model_testing.ipynb        hold-out evaluation -> artifact 6 (comparison), artifact 7 (charts)
    04_backtest_and_package.ipynb out-of-fold back-test -> artifact 8, final output 3 (model package)
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

RAW_FILE = INPUT / "input 1 - customers.csv"
CLEAN_FILE = INTERMEDIATE / "artifact 2 - cleaned customers.csv"
DQ_LOG_FILE = INTERMEDIATE / "artifact 3 - data quality log.csv"
SPLIT_FILE = INTERMEDIATE / "artifact 4 - train test split.csv"
MODEL_DIR = INTERMEDIATE / "artifact 5 - trained models"
COMPARISON_FILE = INTERMEDIATE / "artifact 6 - model comparison.csv"
CHART_DIR = INTERMEDIATE / "artifact 7 - evaluation charts"
BACKTEST_FILE = INTERMEDIATE / "artifact 8 - backtest scored customers.csv"
PACKAGE_DIR = OUTPUT / "final output 3 - model package"

# ---------------------------------------------------------------- business rules (input 3 - campaign brief)
SNAPSHOT_DATE = "2026-06-30"
CAMPAIGN_SIZE = 4_000
COST_PER_CONTACT = 4
MARGIN_PER_CONVERSION = 150
MAX_COMPLAINTS = 1            # customers with 2+ complaints are excluded from contact

ACCEPTANCE = {"roc_auc": 0.78, "top20_lift": 2.5, "backtest_lift": 2.0}
RANDOM_STATE = 42

# ---------------------------------------------------------------- columns
TARGET = "next_product_purchased_90d"
ID_COLUMNS = ["customer_id", "snapshot_date", "customer_since"]
PROTECTED_COLUMNS = ["gender"]                      # fair-treatment policy: never a model input
LEAKY_COLUMNS = ["cross_sell_product_type"]         # populated only after the purchase
CATEGORICAL = ["region", "customer_segment", "primary_product", "last_contact_channel"]

EXCLUDED = ID_COLUMNS + PROTECTED_COLUMNS + LEAKY_COLUMNS + [TARGET]


def feature_columns(df):
    """All model inputs: every column that is not an ID, protected, leaky or the target."""
    return [c for c in df.columns if c not in EXCLUDED]


def numeric_columns(df):
    return [c for c in feature_columns(df) if c not in CATEGORICAL]


# ---------------------------------------------------------------- models
def build_baseline(df):
    """Logistic regression: scaled numerics + one-hot categoricals."""
    preprocess = ColumnTransformer([
        ("num", StandardScaler(), numeric_columns(df)),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return make_pipeline(preprocess, LogisticRegression(max_iter=2000))


def build_gradient_boosting(df):
    """Histogram gradient boosting: handles missing numerics natively, early stopping on 10% of train."""
    preprocess = ColumnTransformer([
        ("num", "passthrough", numeric_columns(df)),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
    ], verbose_feature_names_out=False)
    model = HistGradientBoostingClassifier(
        learning_rate=0.05, max_iter=500, max_leaf_nodes=31, min_samples_leaf=40,
        l2_regularization=1.0, early_stopping=True, validation_fraction=0.1,
        n_iter_no_change=30, random_state=RANDOM_STATE)
    return make_pipeline(preprocess, model)
