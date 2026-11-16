#!/usr/bin/env python3
"""Verify the historical 12-record full-text pilot agreement (aggregate counts only).

Rows: original automated initial assessment; columns: original researcher
assessment. Labels: INCLUDE, EXCLUDE, UNCERTAIN. Reconciled decisions are
not used for inter-assessor agreement. No external dependencies.
"""
from csv import DictReader
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/methodology/fulltext_pilot_contingency.csv"
LABELS = ("INCLUDE", "EXCLUDE", "UNCERTAIN")
with PATH.open(newline="", encoding="utf-8") as stream:
    rows = list(DictReader(stream))
assert [r["automated_initial_assessment"] for r in rows] == list(LABELS)
matrix = [[int(row[f"researcher_{label}"]) for label in LABELS] for row in rows]
assert all(value >= 0 for row in matrix for value in row)
n = sum(map(sum, matrix))
agreement = sum(matrix[i][i] for i in range(3))
expected_numerator = sum(sum(matrix[i]) * sum(row[i] for row in matrix) for i in range(3))
po = Fraction(agreement, n)
pe = Fraction(expected_numerator, n*n)
kappa = (po - pe) / (1 - pe)
assert n == 12 and agreement == 11
assert po == Fraction(11, 12) and pe == Fraction(85, 144)
assert kappa == Fraction(47, 59)
print(f"PASS: n={n}; agreements={agreement}; po={po}; pe={pe}; Cohen kappa={kappa} ({float(kappa):.6f})")
print("Scope: original researcher-versus-automated 12-record pilot; not two independent human reviewers or corpus-wide reliability.")
