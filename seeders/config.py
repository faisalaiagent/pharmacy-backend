from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXPORT_DIR = BASE_DIR / "exports"

EXPORT_DIR.mkdir(exist_ok=True)

# =========================
# RECORD COUNTS
# =========================

CATEGORY_COUNT = 25

SUBCATEGORY_COUNT = 120

BRAND_COUNT = 50

MANUFACTURER_COUNT = 50

PRODUCT_COUNT = 2500

REVIEW_COUNT = 10000

IMAGE_PER_PRODUCT = 3

# =========================
# EXPORTS
# =========================

EXPORT_CSV = True

EXPORT_JSON = True

EXPORT_SQL = True

EXPORT_EXCEL = True

# =========================
# RANDOM SEED
# =========================

RANDOM_SEED = 42

# =========================
# CURRENCY
# =========================

DEFAULT_CURRENCY = "PKR"

DEFAULT_TAX = 0.00