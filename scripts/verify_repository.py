#!/usr/bin/env python3
"""Verify integrity of the repository-only research/data package."""
import csv
import hashlib
from pathlib import Path

R = Path(__file__).resolve().parents[1]

def rows(path):
    with (R/path).open(newline="",encoding="utf-8-sig") as fp:
        return list(csv.DictReader(fp))

def check(test, message):
    if not test:
        raise SystemExit("FAIL: "+message)

def main():
    publications = rows("data/selected_publications.csv")
    check(len(publications)==243, "expected 243 selected publication records")
    check({x["paper_id"] for x in publications}=={x["paper_id"] for x in rows("data/bibliography/publications.csv")}, "bibliographic inventory IDs differ")
    counts = [(col,sum(p[col]=="YES" for p in publications)) for col in ("selected_publication","analytical_publication","has_normalized_rq_items")]
    check(counts==[("selected_publication",243),("analytical_publication",242),("has_normalized_rq_items",240)], "unexpected publication cohorts")
    for entry in rows("MANIFEST_SHA256.csv"):
        p=R/entry["path"]
        check(p.is_file(), f"missing {entry['path']}")
        check(hashlib.sha256(p.read_bytes()).hexdigest()==entry["sha256"], f"hash mismatch: {entry['path']}")
        check(p.stat().st_size==int(entry["size_bytes"]), f"size mismatch: {entry['path']}")
    check(not (R/"manuscript").exists(), "unexpected manuscript directory in repository-only package")
    print("PASS: repository-only file integrity and selected-publication cohorts (243/242/240)")
    print("The 11 original PDF figures and the compiled manuscript are in separately supplied manuscript ZIP; not tested here.")
    print("Rights status: private reviewer candidate; release authorization requires separate review.")

if __name__=="__main__":
    main()
