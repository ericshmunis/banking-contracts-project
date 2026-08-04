#!/usr/bin/env python3
"""
Generate synthetic banking account records matching the accounts_daily
data contract (contracts/accounts_daily.yml).

Usage:
    python generate_data.py --count 750 --format csv --output data/accounts.csv
    python generate_data.py --count 500 --format json --inject-errors

Requires: faker (see requirements.txt). Not installed/run automatically —
review the code first, then `pip install -r requirements.txt`.
"""

import argparse
import csv
import json
import random
import sys
import uuid
from pathlib import Path

from faker import Faker

ACCOUNT_TYPES = ["checking", "savings", "loan"]

DEFAULT_MIN_RECORDS = 500
DEFAULT_MAX_RECORDS = 1000


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate synthetic banking account records for the "
        "accounts_daily data contract."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help=(
            "Number of records to generate. Defaults to a random value "
            f"between {DEFAULT_MIN_RECORDS} and {DEFAULT_MAX_RECORDS}."
        ),
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path. Defaults to accounts_daily.<format>.",
    )
    parser.add_argument(
        "--inject-errors",
        action="store_true",
        help=(
            "Deliberately insert a couple of contract-violating records "
            "(a null customer_ssn and a duplicate customer_ssn) so contract "
            "validation can be tested against known-bad data."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible output.",
    )
    return parser.parse_args()


def make_account_id() -> str:
    return f"ACC-{uuid.uuid4().hex[:12].upper()}"


def make_record(fake: Faker) -> dict:
    return {
        "account_id": make_account_id(),
        "customer_ssn": fake.ssn(),
        "customer_name": fake.name(),
        "balance": round(random.uniform(0, 250_000), 2),
        "account_type": random.choice(ACCOUNT_TYPES),
    }


def inject_errors(records: list) -> list:
    """Mutate a couple of records in place to violate the contract:
    one null customer_ssn, one duplicate customer_ssn."""
    if len(records) < 2:
        return records

    # Record with a null SSN.
    records[0]["customer_ssn"] = None

    # Record with a duplicate SSN (copy an existing valid SSN onto another record).
    source_ssn = records[2 % len(records)]["customer_ssn"] if len(records) > 2 else records[1]["customer_ssn"]
    records[1]["customer_ssn"] = source_ssn

    return records


def write_csv(records: list, path: Path):
    fieldnames = ["account_id", "customer_ssn", "customer_name", "balance", "account_type"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def write_json(records: list, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        Faker.seed(args.seed)

    count = args.count if args.count is not None else random.randint(
        DEFAULT_MIN_RECORDS, DEFAULT_MAX_RECORDS
    )
    if count <= 0:
        print("--count must be a positive integer", file=sys.stderr)
        sys.exit(1)

    fake = Faker()
    records = [make_record(fake) for _ in range(count)]

    if args.inject_errors:
        records = inject_errors(records)

    output_path = Path(args.output) if args.output else Path(f"accounts_daily.{args.format}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "csv":
        write_csv(records, output_path)
    else:
        write_json(records, output_path)

    print(f"Wrote {len(records)} records to {output_path}")
    if args.inject_errors:
        print("Injected errors: 1 null customer_ssn, 1 duplicate customer_ssn")


if __name__ == "__main__":
    main()
