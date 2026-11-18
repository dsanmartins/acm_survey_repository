#!/usr/bin/env python3
"""Reproduce approved consolidated aggregates; Python standard library only."""
import argparse,collections,csv,io,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def csvbytes(rows):
    s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return s.getvalue().encode()
def produce():
    ref=json.loads((ROOT/'data/provenance/reference_totals.json').read_text());expected=ref['summary']
    publications=load('data/selected_publications.csv');items=load('data/items.csv');scopes=load('data/scopes.csv');members=load('data/memberships.csv');cats=load('data/taxonomies/categories.csv')
    groups=load('data/evidence_groups.csv');bibmap=load('data/bibliographic_to_evidence.csv');aliases=load('data/item_correspondence.csv')
    pubs={r['paper_id']:r for r in publications};byitem={r['item_id']:r for r in items};byscope={r['scope_id']:r for r in scopes};bycat={(r['category_id'],r['category_version']):r for r in cats};bygroup={r['representative_paper_id']:r for r in groups}
    assert len(pubs)==len(publications)==expected['bibliographic_selected']
    assert len(byitem)==len(items)==expected['items'] and len(byscope)==len(scopes)==expected['scopes']
    assert len(bycat)==len(cats)==expected['categories'] and len(members)==expected['memberships']
    assert len(bygroup)==len(groups)==expected['selected_evidence_groups']
    assert sum(r['analytical_publication']=='YES' for r in publications)==expected['bibliographic_analytical']
    assert sum(r['has_normalized_rq_items']=='YES' for r in publications)==expected['bibliographic_item_bearing']
    assert all(r['selected_publication']=='YES' for r in publications)
    assert sum(r['analytical']=='YES' for r in groups)==expected['analytical_evidence_groups']
    assert sum(r['has_items']=='YES' for r in groups)==expected['item_bearing_evidence_groups']
    assert all(r['independent_study_asserted']=='False' for r in groups)
    mapping={r['paper_id']:r for r in bibmap};assert len(mapping)==len(bibmap)==len(pubs) and set(mapping)==set(pubs)
    assert [json.loads(r['manifestations_json']) for r in groups if len(json.loads(r['manifestations_json']))>1]==[['LC0173','LC0174']]
    for group in groups:
        rep=group['representative_paper_id'];manifestations=json.loads(group['manifestations_json'])
        assert rep in manifestations
        for pid in manifestations:
            assert mapping[pid]['representative_paper_id']==rep and mapping[pid]['doi']==pubs[pid]['doi']
            assert mapping[pid]['selected']=='YES'
    assert mapping['LC0174']['representative_paper_id']=='LC0173'
    assert pubs['LC0173']['doi']=='10.1145/3691621.3694959' and pubs['LC0174']['doi']=='10.1145/3695750.3695823'
    assert len({r['original_item_id'] for r in aliases})==len(aliases)
    assert {r['representative_item_id'] for r in aliases}==set(byitem)
    for a in aliases:
        i=byitem[a['representative_item_id']]
        assert a['evidence_group_representative']==i['paper_id']==mapping[a['original_paper_id']]['representative_paper_id']
        assert (a['counted_as_representative']=='True')==(a['original_item_id']==a['representative_item_id'])
        if a['counted_as_representative']=='True':assert a['original_source_row_sha256']==i['source_row_sha256']
        else:assert a['original_paper_id']=='LC0174' and a['representative_item_id']=='LC0173'+a['original_item_id'][6:]
    assert sorted(a['original_item_id'][7:] for a in aliases if a['counted_as_representative']=='False')==['RQ1-001','RQ2-001','RQ2-002','RQ4-001']
    assert all(i['paper_id'] in bygroup and i['paper_id']!='LC0174' and i['item_id'].startswith(i['paper_id']+'-'+i['rq']+'-') and i['evidence_locator'] for i in items)
    assert {i['paper_id'] for i in items}=={r['representative_paper_id'] for r in groups if r['has_items']=='YES'}
    positive=collections.defaultdict(dict);membership_keys=set()
    for m in members:
        key=(m['scope_id'],m['category_id'],m['category_version']);assert key not in membership_keys;membership_keys.add(key)
        s=byscope[m['scope_id']];c=bycat[m['category_id'],m['category_version']]
        assert (s['rq'],s['paper_id'],s['item_id'],s['axis'])==(m['rq'],m['paper_id'],m['item_id'],m['axis'])
        assert (c['rq'],c['axis'])==(m['rq'],m['axis'])
        assert s['scientific_state']=='APPROVED_POSITIVE'
        positive[m['scope_id']][m['category_id']]=m['category_version']
    for s in scopes:
        i=byitem[s['item_id']];assert (s['paper_id'],s['rq'])==(i['paper_id'],i['rq'])
        assert s['scope_id']==s['item_id']+'::'+s['axis']
        if s['scientific_state'] in ['APPROVED_POSITIVE','APPROVED_SCOPED_NONPOSITIVE']:
            assert json.loads(s['approved_set_json'])==positive[s['scope_id']]
            assert bool(positive[s['scope_id']])==(s['scientific_state']=='APPROVED_POSITIVE')
        else:assert s['scientific_state'] in ['INCOMPLETE','CONTEXT_PROPOSAL_UNAPPLIED'] and s['approved_set_json']=='' and not positive[s['scope_id']]
    coverage=[];support=[];axes=[]
    for rq in ['RQ1','RQ2','RQ3','RQ4','RQ5']:
        ii=[i for i in items if i['rq']==rq];ss=[s for s in scopes if s['rq']==rq];mm=[m for m in members if m['rq']==rq];counts=collections.Counter(s['scientific_state'] for s in ss)
        coverage.append(dict(rq=rq,evidence_groups=len({i['paper_id'] for i in ii}),items=len(ii),scopes=len(ss),resolved=counts['APPROVED_POSITIVE']+counts['APPROVED_SCOPED_NONPOSITIVE'],positive_scopes=counts['APPROVED_POSITIVE'],scoped_nonpositive=counts['APPROVED_SCOPED_NONPOSITIVE'],incomplete=counts['INCOMPLETE'],context=counts['CONTEXT_PROPOSAL_UNAPPLIED'],memberships=len(mm)))
        assert {k:v for k,v in coverage[-1].items() if k!='rq'}==ref['RQ'][rq]
        for axis in sorted({s['axis'] for s in ss}):
            aa=[s for s in ss if s['axis']==axis];state=collections.Counter(s['scientific_state'] for s in aa)
            axes.append(dict(rq=rq,axis=axis,scopes=len(aa),resolved=state['APPROVED_POSITIVE']+state['APPROVED_SCOPED_NONPOSITIVE'],positive=state['APPROVED_POSITIVE'],nonpositive=state['APPROVED_SCOPED_NONPOSITIVE'],incomplete=state['INCOMPLETE'],context=state['CONTEXT_PROPOSAL_UNAPPLIED']))
        for c in [c for c in cats if c['rq']==rq]:
            cc=[m for m in mm if m['category_id']==c['category_id']]
            support.append(dict(**c,memberships=len(cc),unique_items=len({m['item_id'] for m in cc}),evidence_groups=len({m['paper_id'] for m in cc}),item_denominator=len(ii),group_denominator=coverage[-1]['evidence_groups']))
    peritem=collections.defaultdict(dict)
    for m in members:
        if m['rq']=='RQ2':assert m['axis'] not in peritem[m['item_id']];peritem[m['item_id']][m['axis']]=m['category_id']
    cells=collections.defaultdict(list)
    for item,d in peritem.items():
        if 'technique_family' in d and 'analysis_mode' in d:cells[d['technique_family'],d['analysis_mode']].append(item)
    catids={c['category_id']:c for c in cats};bubble=[]
    for (family,mode),ids in sorted(cells.items(),key=lambda pair:(pair[0][1],pair[0][0])):
        groups_in_cell=sorted({byitem[i]['paper_id'] for i in ids})
        bubble.append(dict(analysis_mode=mode,analysis_mode_label=catids[mode]['category_name'],technique_family=family,technique_family_label=catids[family]['category_name'],distinct_evidence_groups=len(groups_in_cell),source_items=len(ids),item_ids_json=json.dumps(sorted(ids)),evidence_group_ids_json=json.dumps(groups_in_cell)))
    assert len(bubble)==expected['figure4_cells'] and sum(r['source_items'] for r in bubble)==expected['figure4_items']
    assert len({g for cell in bubble for g in json.loads(cell['evidence_group_ids_json'])})==expected['figure4_evidence_group_union']
    proposals=load('data/rq5_pairing_proposals.csv');assert len(proposals)==ref['pending_rq5_pairings']
    assert all(p['item_id'] in byitem and byitem[p['item_id']]['rq']=='RQ5' and p['scope_id'] in byscope and p['researcher_decision']=='UNDECIDED' and p['instance_applied']=='False' for p in proposals)
    grid=load('data/rq2_family_level_not_mapped.csv');assert len(grid)*3==ref['family_level_not_mapped_cells']
    assert all(r['cell_status']=='NOT_MAPPED' and all(r[k]=='' for k in ['Unit','Integration','System']) for r in grid)
    return {'coverage.csv':coverage,'category_support.csv':support,'rq2_bubble.csv':bubble,'axis_coverage.csv':axes}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');a=ap.parse_args()
    outputs=produce()
    for name,records in outputs.items():
        payload=csvbytes(records)
        if payload!=(ROOT/'results/reference'/name).read_bytes():raise SystemExit('FAIL: generated '+name+' differs from approved reference')
        if not a.check:
            dest=ROOT/'results/reproduced'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload)
        print('PASS:',name,len(records),'rows; byte-identical to approved reference')
    print('PASS: consolidated identities, memberships, MorphQ++ aliases, unresolved proposals and unmapped cells. No classifications changed.')
if __name__=='__main__':main()
