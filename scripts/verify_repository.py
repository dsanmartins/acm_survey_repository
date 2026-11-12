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
    trace = rows("data/selection/candidates_343.csv")
    check(len(trace)==343 and len({r["paper_id"] for r in trace})==343, "candidate selection trace must contain exactly 343 unique IDs")
    stages={label:sum(r["final_selection_stage"]==label for r in trace) for label in ("SELECTED","EXCLUDED_TITLE_ABSTRACT","EXCLUDED_FULL_TEXT","NO_SCIENTIFIC_FT_DECISION")}
    check(stages=={"SELECTED":243,"EXCLUDED_TITLE_ABSTRACT":87,"EXCLUDED_FULL_TEXT":10,"NO_SCIENTIFIC_FT_DECISION":3}, "inconsistent selection-stage counts")
    check({r["paper_id"] for r in trace if r["final_selection_stage"]=="SELECTED"}=={r["paper_id"] for r in publications}, "selected IDs do not match publication index")
    check(sum(r["full_text_input"]=="YES" for r in trace)==256, "expected 256 full-text stage inputs")
    check(sum(r["full_text_access_status"]=="AVAILABLE" for r in trace)==253, "expected 253 assessable full texts")
    check(sum(bool(r["title"]) for r in trace)==243, "metadata for nonselected candidates must remain uninferred")
    run_rows=rows("data/selection/search_runs_8.csv")
    check(len(run_rows)==8 and sum(int(r["raw_occurrences"]) for r in run_rows)==549, "search occurrence totals mismatch")
    check(len(rows("data/selection/primary_duplicate_occurrences_188.csv"))==188, "primary duplicate counts mismatch")
    check(len(rows("data/selection/supplementary_s4_occurrences_41.csv"))==41, "S4 occurrence counts mismatch")
    check(len(rows("docs/PRISMA_2020_CROSSWALK.csv"))==27,"PRISMA 2020 mapping must include 27 items")
    for entry in rows("MANIFEST_SHA256.csv"):
        p=R/entry["path"]
        check(p.is_file(), f"missing {entry['path']}")
        check(hashlib.sha256(p.read_bytes()).hexdigest()==entry["sha256"], f"hash mismatch: {entry['path']}")
        check(p.stat().st_size==int(entry["size_bytes"]), f"size mismatch: {entry['path']}")
    check(not (R/"manuscript").exists(), "unexpected manuscript directory in repository-only package")
    print("PASS: repository-only file integrity, selected-publication cohorts (243/242/240), candidate-screening trace (343/256/243), and retrospective PRISMA mapping")
    print("The 11 original PDF figures and the compiled manuscript are in separately supplied manuscript ZIP; not tested here.")
    print("Rights status: private reviewer candidate; release authorization requires separate review.")

if __name__=="__main__":
    main()
