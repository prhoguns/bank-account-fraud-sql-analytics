from pathlib import Path
import duckdb
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Bank account fraud analytics', layout='wide')
st.title('Bank account fraud analytics')
st.caption('Feedzai BAF Base variant · synthetic account applications · descriptive SQL analytics')
db = ROOT / 'data/analytics.duckdb'
if not db.exists():
    st.error('Run scripts/download.py and scripts/build_db.py first.')
    st.stop()
con = duckdb.connect(str(db), read_only=True)
months = [r[0] for r in con.execute('SELECT DISTINCT month FROM applications ORDER BY 1').fetchall()]
month_range = st.sidebar.select_slider('Months', options=months, value=(months[0], months[-1]))
sources = [r[0] for r in con.execute('SELECT DISTINCT source FROM applications ORDER BY 1').fetchall()]
selected = st.sidebar.multiselect('Application sources', sources, default=sources)
if not selected:
    st.warning('Select at least one application source.')
    st.stop()
where = f"month BETWEEN {int(month_range[0])} AND {int(month_range[1])} AND source IN ({','.join(repr(x) for x in selected)})"
overview = con.execute(f'''SELECT COUNT(*) n, SUM(fraud_bool) frauds,
 100.0*AVG(fraud_bool) rate FROM applications WHERE {where}''').fetchone()
a,b,c = st.columns(3)
a.metric('Applications', f'{overview[0]:,}')
b.metric('Labeled fraud', f'{overview[1]:,}')
c.metric('Fraud rate', f'{overview[2]:.2f}%')
monthly = con.execute(f'''SELECT month, source, COUNT(*) applications,
 100.0*AVG(fraud_bool) fraud_rate_pct FROM applications WHERE {where}
 GROUP BY 1,2 ORDER BY 1,2''').df()
left,right = st.columns(2)
left.plotly_chart(px.line(monthly, x='month', y='fraud_rate_pct', color='source', markers=True,
 title='Fraud rate over dataset months'), use_container_width=True)
right.plotly_chart(px.bar(monthly, x='month', y='applications', color='source', barmode='group',
 title='Application volume'), use_container_width=True)
segments = con.execute(f'''SELECT device_os, COUNT(*) applications,
 100.0*AVG(fraud_bool) fraud_rate_pct FROM applications WHERE {where}
 GROUP BY 1 ORDER BY applications DESC''').df()
left,right = st.columns(2)
left.plotly_chart(px.bar(segments, x='device_os', y='fraud_rate_pct', hover_data=['applications'],
 title='Fraud rate by device OS'), use_container_width=True)
rules = con.execute((ROOT/'sql/14_simple_rules.sql').read_text()).df()
right.plotly_chart(px.scatter(rules, x='precision_pct', y='recall_pct', size='reviews', text='rule_name',
 title='Transparent review rules (all months)'), use_container_width=True)
st.subheader('Review capacity')
budget = con.execute((ROOT/'sql/15_review_budget.sql').read_text()).df()
st.plotly_chart(px.line(budget, x='review_pct', y='fraud_recall_pct', markers=True,
 title='Fraud found at a fixed review budget (all months)'), use_container_width=True)
st.caption('This dashboard describes labeled outcomes in synthetic data. Segment differences are associations, not causal effects. Review-rule charts use the full Base variant.')
con.close()
