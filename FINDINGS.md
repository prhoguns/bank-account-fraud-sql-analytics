# Findings

The Base variant has **1,000,000 applications and 11,029 labeled fraud cases**, an overall rate of **1.10%**. All values below come from the committed SQL result files.

1. **The fraud rate rises in later dataset months.** It is 1.13% in month 0, dips to 0.88% in month 2, and reaches 1.48% in month 7. [Monthly result](results/01_monthly_fraud.md)
2. **Foreign requests are a higher-rate segment, but a small one.** They account for 25,242 applications at 2.20% labeled fraud, versus 1.08% for domestic requests. A foreign-request-only review rule finds just 5.03% of all fraud. [Segment result](results/05_foreign_request.md) · [Rule result](results/14_simple_rules.md)
3. **Review capacity is the key operational constraint.** Reviewing the highest-ranked 5% of applications under the transparent score ordering finds 20.23% of labeled fraud; reviewing 10% finds 30.48%. This is a descriptive ranking, not a held-out model evaluation. [Review budget](results/15_review_budget.md)
4. **Simple single-feature rules are blunt.** The weak name/email match rule finds 38.21% of fraud but queues 221,045 applications. The reused-device rule queues 25,302 and finds 9.38%. [Rule comparison](results/14_simple_rules.md)

## Limits

The data is synthetic, and the full feature set may encode relationships that differ from a real bank. A segment's fraud rate is an association, not evidence that the segment causes fraud. Any operational threshold should be evaluated on a later, separate period with fairness and false-positive costs considered.
