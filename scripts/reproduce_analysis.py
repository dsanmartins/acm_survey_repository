#!/usr/bin/env python3
"""Reproduce selected scientific aggregates from approved public classification tables.

Only standard-library modules are required. This never changes approved source data,
scientific decisions, figure PDFs, or the manuscript. It does not repeat source screening.
"""
import argparse, collections, csv, io, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]

def load(path):
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write_csv(rows):
    stream=io.StringIO(newline=''); writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows);return stream.getvalue().encode('utf-8')
def produce():
    pubs=load('data/selected_publications.csv')
    items=load('data/items.csv'); scopes=load('data/scopes.csv'); memberships=load('data/memberships.csv'); cats=load('data/taxonomies/categories.csv')
    assert len(pubs)==len({r['paper_id'] for r in pubs})==243
    assert [sum(r[k]=='YES' for r in pubs) for k in ['selected_publication','analytical_publication','has_normalized_rq_items']]==[243,242,240]
    assert len(items)==1558 and len(scopes)==5506 and len(memberships)==3707 and len(cats)==86
    by_item={r['item_id']:r for r in items}; by_cat={(c['category_id'],c['category_version']):c for c in cats}
    by_scope={s['scope_id']:s for s in scopes}
    assert len(by_item)==len(items) and len(by_scope)==len(scopes)
    for m in memberships:
        s=by_scope[m['scope_id']];c=by_cat[m['category_id'],m['category_version']]
        assert s['scientific_state']=='APPROVED_POSITIVE' and (s['rq'],s['axis'],s['paper_id'],s['item_id'])==(m['rq'],m['axis'],m['paper_id'],m['item_id'])
        assert (c['rq'],c['axis'])==(m['rq'],m['axis'])
    coverage=[]
    for rq in ['RQ1','RQ2','RQ3','RQ4','RQ5']:
        si=[s for s in scopes if s['rq']==rq]; ii=[i for i in items if i['rq']==rq]
        state=collections.Counter(s['scientific_state'] for s in si)
        coverage.append(dict(rq=rq,source_publications=len({i['paper_id'] for i in ii}),
            source_items=len(ii),original_scopes=len(si),
            approved_or_resolved_sets=state['APPROVED_POSITIVE']+state['APPROVED_SCOPED_NONPOSITIVE'],
            positive_sets=state['APPROVED_POSITIVE'],scoped_nonpositive_sets=state['APPROVED_SCOPED_NONPOSITIVE'],
            positive_memberships=sum(m['rq']==rq for m in memberships),
            unapproved_or_incomplete=state['INCOMPLETE']+state['CONTEXT_PROPOSAL_UNAPPLIED'],
            context_application_proposals=state['CONTEXT_PROPOSAL_UNAPPLIED']))
    category_support=[]
    for (id,version),c in sorted(by_cat.items()):
        matches=[m for m in memberships if m['category_id']==id and m['category_version']==version]
        category_support.append(dict(rq=c['rq'],axis=c['axis'],category_id=id,category_version=version,
            category_name=c['category_name'],memberships=len(matches),unique_items=len({m['item_id'] for m in matches}),
            unique_publications=len({m['paper_id'] for m in matches})))
    by_rq2=collections.defaultdict(dict)
    for m in memberships:
        if m['rq']=='RQ2':by_rq2[m['item_id']][m['axis']]=m['category_id']
    cells=collections.defaultdict(list)
    for item,info in by_rq2.items():
        if 'technique_family' in info and 'analysis_mode' in info:cells[(info['technique_family'],info['analysis_mode'])].append(item)
    labels={c['category_id']:c['category_name'] for c in cats}
    rq2=[]
    for (family,mode),ids in sorted(cells.items()):
        supports=sorted({by_item[i]['paper_id'] for i in ids})
        rq2.append(dict(analysis_mode=mode,analysis_mode_label=labels[mode],technique_family=family,
            technique_family_label=labels[family],distinct_publications=len(supports),source_items=len(ids),
            item_ids_json=json.dumps(sorted(ids)),paper_ids_json=json.dumps(supports)))
    assert len(rq2)==28 and sum(x['source_items'] for x in rq2)==383
    pairing=load('data/rq5_pairing_proposals.csv')
    assert len(pairing)==58 and all(p['researcher_decision']=='UNDECIDED' and p['instance_applied']=='False' for p in pairing)
    return {'coverage.csv':coverage,'category_support.csv':category_support,'rq2_bubble.csv':rq2}

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--check',action='store_true',help='Compare generated CSV byte-for-byte with reference data')
    a=pa.parse_args();outputs=produce();out_dir=ROOT/'results/reproduced'
    if not a.check:out_dir.mkdir(parents=True,exist_ok=True)
    for name,rows in outputs.items():
        payload=write_csv(rows);reference=(ROOT/'results/reference'/name).read_bytes()
        if payload!=reference:
            print('FAIL:',name,'differs from the reference.',file=sys.stderr);return 2
        if not a.check:(out_dir/name).write_bytes(payload)
        print('PASS:',name,'matches reference; records:',len(rows))
    print('PASS: 243 selected publications; 242 analytical; 240 item-bearing; 58 undecided proposals')
    print('Scope: reproduction of approved aggregates, not source screening or full scientific re-extraction.')
    return 0
if __name__=='__main__':raise SystemExit(main())
