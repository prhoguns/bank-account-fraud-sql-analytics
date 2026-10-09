"""Write a small synthetic data/raw/Base.csv for CI.

Same 32 columns, types, value ranges and -1 sentinels as the BAF Base variant, with fraud made a
little more likely where the real data shows it (weak name/email match, foreign requests, reused
devices) so every rule query has something to find. It checks that every query runs; it says
nothing about the real data.
"""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/raw/Base.csv'
N = 20_000

random.seed(3)


def sentinel(p, lo, hi):
    return -1 if random.random() < p else random.randint(lo, hi)


rows = []
for _ in range(N):
    sim = random.random()
    foreign = int(random.random() < 0.03)
    device_emails = random.choice([-1, 0, 1, 1, 1, 2])
    risk = 0.005 + 0.03 * (sim < 0.1) + 0.04 * foreign + 0.03 * (device_emails >= 2)
    rows.append({
        'fraud_bool': int(random.random() < risk),
        'income': random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
        'name_email_similarity': sim,
        'prev_address_months_count': sentinel(0.7, 0, 383),
        'current_address_months_count': sentinel(0.01, 0, 428),
        'customer_age': random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90]),
        'days_since_request': random.expovariate(1.0),
        'intended_balcon_amount': random.uniform(-15, 113),
        'payment_type': random.choice(['AA', 'AB', 'AC', 'AD', 'AE']),
        'zip_count_4w': random.randint(1, 6700),
        'velocity_6h': random.uniform(-170, 16715),
        'velocity_24h': random.uniform(1300, 9506),
        'velocity_4w': random.uniform(2825, 6994),
        'bank_branch_count_8w': random.randint(0, 2385),
        'date_of_birth_distinct_emails_4w': random.randint(0, 39),
        'employment_status': random.choice(['CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG']),
        'credit_risk_score': random.randint(-170, 389),
        'email_is_free': random.randint(0, 1),
        'housing_status': random.choice(['BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG']),
        'phone_home_valid': random.randint(0, 1),
        'phone_mobile_valid': random.randint(0, 1),
        'bank_months_count': sentinel(0.25, 0, 32),
        'has_other_cards': random.randint(0, 1),
        'proposed_credit_limit': random.choice([190.0, 200.0, 500.0, 1000.0, 1500.0, 2000.0, 2100.0]),
        'foreign_request': foreign,
        'source': random.choice(['INTERNET'] * 9 + ['TELEAPP']),
        'session_length_in_minutes': -1.0 if random.random() < 0.002 else random.uniform(0, 85),
        'device_os': random.choice(['linux', 'macintosh', 'other', 'windows', 'x11']),
        'keep_alive_session': random.randint(0, 1),
        'device_distinct_emails_8w': device_emails,
        'device_fraud_count': 0,
        'month': random.randint(0, 7),
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f'fixture: {N:,} rows in {OUT}')
