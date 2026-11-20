# Statistical analysis plan: WALK-G pilot (synthetic data)

Written before the visit 2 data were seen. Version 1.0.

## Design

Randomized pilot trial, 1:1, two arms: **walking** (10 minutes of walking after each main
meal) and **usual** care. 60 adults with type 2 diabetes. Two clinic visits: visit 1
(baseline) and visit 2 (week 12). At each visit the participant's meter exports 8 readings:
4 fasting, 4 post-meal.

## Data handling

- Glucose in mmol/L is converted to mg/dL (× 18.016).
- 999 is a meter error: that reading is missing. Other readings of the visit still count.
- A participant's **visit mean** is the mean of their non-missing readings of one kind
  (post-meal or fasting) at one visit.

## Primary outcome and analysis

- **Outcome:** visit 2 mean post-meal glucose (mg/dL).
- **Analysis sample:** randomized participants with a post-meal mean at both visits.
- **Model:** linear regression (ANCOVA) of the visit 2 mean post-meal glucose on arm,
  adjusted for the visit 1 mean post-meal glucose. One row per participant.
- **Estimate:** walking minus usual, with its 95% confidence interval.

## Secondary analyses

1. The same model for **fasting** glucose.
2. A linear mixed model on the individual visit 2 post-meal readings, with arm and the
   visit 1 post-meal mean as fixed effects and a random intercept for participant
   (`lme4::lmer`). The estimate should be close to the primary one.

## Report

- Number randomized per arm, number analysed per arm, number with no visit 2.
- For the primary and secondary analyses: estimate, 95% CI, and p-value, to 1 decimal
  place (p to 3).
- No other models, subgroups, or covariates without a written amendment to this plan.

## Output

`output/results.json`, one flat object with these keys (numbers, not strings):

```
n_randomized_walking, n_randomized_usual,
n_analysed_walking, n_analysed_usual, n_no_visit2,
primary_estimate, primary_ci_low, primary_ci_high, primary_p,
fasting_estimate, fasting_ci_low, fasting_ci_high,
mixed_estimate, mixed_ci_low, mixed_ci_high
```

Estimates are walking minus usual, in mg/dL.
