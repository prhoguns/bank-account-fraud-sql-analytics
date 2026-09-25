from pathlib import Path
import duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / 'data/analytics.duckdb'), read_only=True)
out = ROOT / 'results'
charts = ROOT / 'charts'
out.mkdir(exist_ok=True)
charts.mkdir(exist_ok=True)

def markdown(df):
    cols = [str(c) for c in df.columns]
    rows = [['' if v is None else str(round(v, 4) if isinstance(v, float) else v) for v in row]
            for row in df.itertuples(index=False, name=None)]
    return '| ' + ' | '.join(cols) + ' |\n| ' + ' | '.join(['---']*len(cols)) + ' |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)

for file in sorted((ROOT / 'sql').glob('*.sql')):
    sql = file.read_text()
    title = sql.splitlines()[0].removeprefix('-- ').strip()
    df = con.execute(sql).df()
    df.to_csv(out / f'{file.stem}.csv', index=False)
    (out / f'{file.stem}.md').write_text(f'# {title}\n\n{markdown(df.head(30))}')
    print(file.name, len(df), 'rows')

monthly = con.execute((ROOT / 'sql/01_monthly_fraud.sql').read_text()).df()
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly['month'], monthly['fraud_rate_pct'], marker='o', color='#0f766e')
ax.set(xlabel='Dataset month', ylabel='Fraud rate (%)', title='Fraud rate by month')
ax.grid(alpha=.2)
fig.tight_layout(); fig.savefig(charts / 'monthly_fraud_rate.png', dpi=160); plt.close(fig)

budget = con.execute((ROOT / 'sql/15_review_budget.sql').read_text()).df()
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(budget['review_pct'], budget['fraud_recall_pct'], marker='o', color='#b45309')
ax.set(xlabel='Applications reviewed (%)', ylabel='Labeled fraud found (%)', title='Rule-based review budget')
ax.grid(alpha=.2)
fig.tight_layout(); fig.savefig(charts / 'review_budget.png', dpi=160); plt.close(fig)
