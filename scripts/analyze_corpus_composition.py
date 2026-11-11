#!/usr/bin/env python3
"""Reproduce descriptive composition of the 243 *publication records*.

This is not a primary/secondary study design classifier, a risk-of-bias
appraisal, or a publication-family de-duplication procedure. The page span is
calculated only when inclusive start and end page numbers exist.
"""
from pathlib import Path
from collections import Counter
import csv,re,json,argparse
R=Path(__file__).resolve().parents[1]

def read(name):
    with (R/name).open(newline='', encoding='utf-8-sig') as h:
        return list(csv.DictReader(h))

def write(name,fields,rows):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)

def run(check=False):
    p=read('data/selected_publications.csv')
    pg=read('data/publication_page_ranges.csv')
    if len(p)!=243 or len(pg)!=243 or len({r['paper_id'] for r in p})!=243 or {r['paper_id'] for r in pg}!={r['paper_id'] for r in p}:
        raise SystemExit('FAIL: publication metadata / page-range ID reconciliation')
    pages={r['paper_id']:r['bibliographic_page_range'] for r in pg}
    counts=Counter(r['publication_type'] for r in p)
    typs=['Conference paper','Article','Book chapter','Review','Note']
    if set(counts)!=set(typs):raise SystemExit('FAIL: unexpected bibliographic type')
    types=[{'source_document_type':k,'selected_publication_records':counts[k]} for k in typs]
    states=Counter()
    selected_short=[]
    for r in p:
        s=pages[r['paper_id']].strip().replace('–','-').replace('—','-')
        m=re.fullmatch(r'(\d+)\s*-\s*(\d+)',s)
        if m:
            a,b=map(int,m.groups());n=b-a+1
            if not 1<=n<=300:
                raise SystemExit('FAIL: impossible page range for '+r['paper_id'])
            states['page_span_recorded']+=1
            if n<=6:
                states['page_span_6_or_fewer']+=1
                selected_short.append({'paper_id':r['paper_id'],'page_range':pages[r['paper_id']],'inclusive_page_span':n,'title':r['title']})
            else:states['page_span_over_6']+=1
        elif not s:
            states['page_span_unavailable']+=1
        else:
            raise SystemExit('FAIL: unparsed page range for '+r['paper_id']+': '+s)
    summary=[
        ('selected_publication_records',len(p)),
        ('analytical_publication_records',sum(r['analytical_publication']=='YES' for r in p)),
        ('item_bearing_publication_records',sum(r['has_normalized_rq_items']=='YES' for r in p)),
        *[(k,states[k]) for k in ['page_span_recorded','page_span_6_or_fewer','page_span_over_6','page_span_unavailable']],
    ]
    assert dict(summary)=={'selected_publication_records':243,'analytical_publication_records':242,'item_bearing_publication_records':240,'page_span_recorded':189,'page_span_6_or_fewer':59,'page_span_over_6':130,'page_span_unavailable':54}
    outputs={
      'results/composition/document_types.csv':(['source_document_type','selected_publication_records'],types),
      'results/composition/composition_summary.csv':(['metric','value'],[{'metric':k,'value':v} for k,v in summary]),
    }
    for name,(fields,rows) in outputs.items():
        if check:
            with (R/name).open(newline='',encoding='utf-8') as fh:old=list(csv.DictReader(fh))
            if old!=[{k:str(r[k]) for k in fields} for r in rows]:raise SystemExit('FAIL: '+name+' mismatch')
        else: write(name,fields,rows)
    print('PASS: composition of 243 records; 159/71/9/3/1 document types; 189 page spans, 59 <=6, 54 unavailable')
    print('WARNING: metadata cannot establish secondary-study counts, empirical quality, or study independence')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();run(args.check)
