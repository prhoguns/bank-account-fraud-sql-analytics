from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / 'data/raw/Base.csv'
if not raw.exists():
    raise SystemExit('Run python scripts/download.py first.')
db = ROOT / 'data/analytics.duckdb'
con = duckdb.connect(str(db))
con.execute('CREATE OR REPLACE TABLE applications AS SELECT * FROM read_csv_auto(?)', [str(raw)])
count, fraud = con.execute('SELECT COUNT(*), SUM(fraud_bool) FROM applications').fetchone()
assert count == 1_000_000 and 0 < fraud < count, (count, fraud)
print(f'{count:,} applications; {fraud:,} labeled fraud; database: {db}')
con.close()
