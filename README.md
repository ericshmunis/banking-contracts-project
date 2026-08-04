# Banking Data Contract Enforcement (Learning Project)

A simplified data contract enforcement pipeline for a banking scenario, built
to learn the core ideas behind data contracts before running the real
validation logic on **Databricks Free Edition**.

## What's here

This repo holds the code and config that *feed into* the pipeline — the
actual contract validation/enforcement runs on Databricks, not locally.

- **`contracts/accounts_daily.yml`** — a data contract describing the
  expected schema and quality rules for a daily `accounts` extract: field
  types/nullability, uniqueness constraints on `account_id` and
  `customer_ssn`, and a non-negative `balance` rule.
- **`generate_data.py`** — generates synthetic banking account records
  (via [Faker](https://faker.readthedocs.io/)) that match the contract's
  schema, as CSV or JSON. Supports an `--inject-errors` flag to deliberately
  produce a couple of contract-violating records (null SSN, duplicate SSN)
  for testing that validation actually catches them.
- **`requirements.txt`** — Python dependencies (just `Faker` for now).

## Status

Scaffolding only. Nothing has been installed or run yet — dependencies and
the Databricks-side validation logic come next.

## Planned next steps

1. Install dependencies (`pip install -r requirements.txt`) and generate a
   sample dataset, including an error-injected version.
2. Upload the generated data to Databricks Free Edition.
3. Implement contract validation logic (e.g. via PySpark or a data quality
   library) that checks data against `contracts/accounts_daily.yml` and
   reports violations.

## Note on data

`customer_ssn` is flagged as PII in the contract. All data produced by
`generate_data.py` is synthetic (Faker-generated), not real customer data.
