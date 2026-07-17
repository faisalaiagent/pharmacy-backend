import pandas as pd
from pathlib import Path

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

def export_csv(name, rows):
    if not rows:
        return

    df = pd.DataFrame(rows)
    df.to_csv(EXPORT_DIR / f"{name}.csv", index=False)