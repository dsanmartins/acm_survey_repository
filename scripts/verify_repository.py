#!/usr/bin/env python3
"""Verify the updated existing distribution; standard library only, no private roots."""
import csv,hashlib,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    publications=rows('data/selected_publications.csv');byid={p['paper_id']:p for p in publications}
    assert publications==rows('data/bibliography/publications.csv')
    trace=rows('data/selection/candidates_343.csv');assert len(trace)==len({r['paper_id'] for r in trace})==343
    assert {r['paper_id'] for r in trace if r['final_selection_stage']=='SELECTED'}==set(byid)
    assert {s:sum(r['final_selection_stage']==s for r in trace) for s in ['SELECTED','EXCLUDED_TITLE_ABSTRACT','EXCLUDED_FULL_TEXT','NO_SCIENTIFIC_FT_DECISION']}=={'SELECTED':243,'EXCLUDED_TITLE_ABSTRACT':87,'EXCLUDED_FULL_TEXT':10,'NO_SCIENTIFIC_FT_DECISION':3}
    assert sum(r['full_text_input']=='YES' for r in trace)==256 and sum(r['full_text_access_status']=='AVAILABLE' for r in trace)==253
    assert all((bool(r['title']) and r['title']==byid[r['paper_id']]['title']) if r['selected_publication']=='YES' else not any(r[k] for k in ['title','authors','year','doi']) for r in trace)
    assert len(rows('data/selection/search_runs_8.csv'))==8 and sum(int(r['raw_occurrences']) for r in rows('data/selection/search_runs_8.csv'))==549
    assert len(rows('data/selection/primary_duplicate_occurrences_188.csv'))==188 and len(rows('data/selection/supplementary_s4_occurrences_41.csv'))==41
    assert len(rows('docs/PRISMA_2020_CROSSWALK.csv'))==27
    defs=rows('data/taxonomies/operational_definitions_22.csv');cats={c['category_id'] for c in rows('data/taxonomies/categories.csv')}
    assert len(defs)==len({r['category_id'] for r in defs})==22 and all(r['category_id'] in cats and all(r[k] for k in ['category','definition','inclusion','exclusion_and_limits']) for r in defs)
    entries=rows('MANIFEST_SHA256.csv');declared={r['path'] for r in entries};assert len(declared)==len(entries)
    def included(p):
        rel=p.relative_to(ROOT);return not any(k in ['.git','.cache','__pycache__','.venv'] for k in rel.parts) and not str(rel).startswith('results/generated_figures/') and str(rel)!='MANIFEST_SHA256.csv'
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and included(p)}
    assert declared==actual,('MANIFEST_COVERAGE_DIFFERENCE',sorted(actual-declared),sorted(declared-actual))
    for r in entries:
        p=ROOT/r['path'];assert not p.is_symlink() and p.resolve().is_relative_to(ROOT)
        assert p.stat().st_size==int(r['size_bytes']) and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],('MANIFEST_MISMATCH',r['path'])
    assert not (ROOT/'manuscript').exists()
    print('PASS: complete SHA-256 manifest, 343-candidate selection, unchanged bibliographic inventory and 22 explanatory definitions.')
    print('Historical DOI 10.5281/zenodo.24168011 is not an identifier for this candidate. No publication performed.')
if __name__=='__main__':main()
