#!/usr/bin/env python3
"""F2: five conceptual bands and readable, complete registered-category panels.

Independent entry point. Scientific loading stays in qcc.figure_data. STYLE and
AXES/DOMAINS below are presentation settings, never classification authorities.
"""
from pathlib import Path
import copy,json,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from qcc.figure_data import tree_records,taxonomy_context,TAXONOMY_INPUTS,KINDS
from qcc.figure_utils import ROOT,arguments,parameters,plotting,export

DOMAINS={'RQ1':'Quality Phenomena','RQ2':'Verification and Validation',
 'RQ3':'Software Representations','RQ4':'Validation Conditions','RQ5':'Model-Level Operationalization'}
AXES={'affected_artifact':'Affected artifact','manifestation':'Manifestation','phenomenon_family':'Phenomenon family',
 'origin':'Origin','evidence_nature':'Evidence nature','analysis_mode':'Analysis mode','technique_family':'Technique family',
 'test_level':'Test level','representation_family':'Representation family','representation_role':'Representation role',
 'constraint_content_domain':'Condition content','constraint_form_role':'Formal role','checkability_status':'Reported checkability',
 'operationalization_requirements':'Required information','candidate_provenance':'Candidate provenance',
 'operationalization_pairing_provenance':'Pairing provenance'}
AXIS_ORDER={
 'RQ1':['affected_artifact','manifestation','phenomenon_family','origin','evidence_nature'],
 'RQ2':['analysis_mode','technique_family','test_level'],
 'RQ3':['representation_family','representation_role'],
 'RQ4':['constraint_content_domain','constraint_form_role','checkability_status'],
 'RQ5':['operationalization_requirements','candidate_provenance','operationalization_pairing_provenance']}
TYPES={'taxonomy':('P','Taxonomic predicate'),'descriptor':('D','Evidence / assessment descriptor'),
 'provenance':('Q','Provenance qualifier')}
QUALIFICATION='Visual grouping organizes classification vocabulary, not empirical, semantic, or causal relationships.'
# Only token-to-readable-text aliases are used, exclusively in the compact view.
# Each effective alias is exported alongside its canonical ID, label and version.
COMPACT_ALIASES={'SYN-RQ1-C0003':'Real observed',
'SYN-RQ2-C0011':'Dynamic',
 'SYN-RQ2-C0021':'Unit testing','SYN-RQ4-C0001':'Assertion','SYN-RQ5-C0001':'Reviewer-derived'}
STYLE=dict(formats=['pdf','svg','png'],width=8.,height=None,font_family='DejaVu Sans',dpi=300,padding=.04,
 font_sizes=dict(base=10.5,title=14,subtitle=9.5,domain=11,axis=10,category=10.5,metadata=8.2,legend=9,note=9),
 colors=dict(ink='#233442',muted='#53616d',taxonomy='#176582',descriptor='#946419',provenance='#71508e',
  taxonomy_fill='#f1f7fa',descriptor_fill='#fbf6eb',provenance_fill='#f7f3fa',container='#f4f5f6',rule='#cbd1d6',white='#ffffff'),
 layout=dict(margin=.14,domain_width=1.35,gutter=.10,panel_padding=.10,band_gap=.12,facet_gap=.10,
  header_height=.78,footer_height=.62,axis_gap=.08,metadata_gap=.035,
  line_height=1.26,complete_columns=3,complete_body_height=5.28,
  border_width=.55,separator_width=1.1,legend_x=[.14,1.95,5.10]),
 labels=dict(title='Quantum Software Quality',
  compact_subtitle='Five conceptual dimensions · representative registered examples',
  complete_subtitle='Complete registered public projection · canonical category labels and IDs'),
 minimum_category_font=10.)
PROFILES={'compact':{},'complete':dict(width=10.)}
COMPLETE_LAYOUT=dict(domain_width=1.55,panel_padding=.08,band_gap=.07,line_height=1.22,
 complete_body_height=5.70,complete_axis_columns={'analysis_mode':4,'constraint_form_role':4,'checkability_status':4})
COMPACT_LAYOUT=dict(margin=.10,domain_width=1.90,panel_padding=.065,band_gap=.07,facet_gap=.055,
 header_height=.60,footer_height=.52,axis_gap=.025,line_height=1.15,outer_padding=.035)

def measure_factory(style):
    """Measure actual selected-font widths in points, independently of rendering."""
    from matplotlib.font_manager import FontProperties,findfont
    from matplotlib.backends.backend_agg import RendererAgg
    findfont(style['font_family'],fallback_to_default=False)
    renderer=RendererAgg(1,1,72)
    def measure(text,size,bold=False):
        font=FontProperties(family=style['font_family'],size=size,weight='bold' if bold else 'normal')
        return renderer.get_text_width_height_descent(text,font,False)[0]/72
    return measure

def wrapped(text,width,size,measure,bold=False,break_long_words=True):
    """Width-aware wrapping; no ellipses, omission, or semantic abbreviation."""
    lines=[]
    for paragraph in text.split('\n'):
        current=''
        for word in paragraph.split(' '):
            candidate=(current+' '+word).strip()
            if measure(candidate,size,bold)<=width:
                current=candidate;continue
            if current:lines.append(current);current=''
            assert break_long_words or measure(word,size,bold)<=width, ('AXIS_WORD_TOO_WIDE',word,width)
            # Category labels preserve all characters; axis headings never split words.
            for char in word:
                if current and measure(current+char,size,bold)>width:
                    lines.append(current);current=''
                current+=char
        lines.append(current)
    return '\n'.join(lines)

def text_height(text,size,style):
    return len(text.split('\n'))*size/72*style['layout']['line_height']+.025

def canonical_map(records,compact):
    return [dict(category_id=c['category_id'],category_version=c['category_version'],axis=c['axis'],rq=c['rq'],
        canonical_label=c['category_name'],definition=c['definition'],presentation_label=COMPACT_ALIASES.get(c['category_id'],c['category_name']) if compact else c['category_name'],
        display_kind=c['display_kind']) for c in records]

def version_key(version):
    match=re.fullmatch('SA01-staging-definition-([12])',version)
    assert match,('UNKNOWN_VERSION_REQUIRES_EXPLICIT_PRESENTATION_KEY',version)
    return 'v'+match[1]

def category_card(c,width,style,measure,compact):
    f=style['font_sizes'];l=style['layout'];inner=width-2*l['panel_padding']
    label=COMPACT_ALIASES.get(c['category_id'],c['category_name']) if compact else c['category_name']
    label=wrapped(label,inner,f['category'],measure)
    meta='' if compact else c['category_id']+' · '+version_key(c['category_version'])
    return dict(record=c,label=label,metadata=meta,width=width,
        height=text_height(label,f['category'],style)+(text_height(meta,f['metadata'],style)+l['metadata_gap'] if meta else 0))

def compact_band(rq,records,style,measure):
    l=style['layout'];f=style['font_sizes'];w=style['width']-2*l['margin']-l['domain_width']-l['gutter']
    axes=AXIS_ORDER[rq];domain_axes=[a for a in axes if KINDS.get(a,'taxonomy')=='taxonomy' and a!='origin']
    evidence_axes=[a for a in axes if a not in domain_axes]
    sections=[]
    for axis_group,role in [(domain_axes,'domain'),(evidence_axes,'characterization')]:
        if not axis_group:continue
        cw=(w-l['facet_gap']*(len(axis_group)-1))/len(axis_group)
        panels=[]
        for axis in axis_group:
            c=next(c for c in records if c['rq']==rq and c['axis']==axis)
            kind=c['display_kind'];badge=TYPES[kind][0]
            heading=wrapped(badge+'  '+AXES[axis],cw-2*l['panel_padding'],f['axis'],measure,True)
            card=category_card(c,cw,style,measure,True)
            # Origin remains a predicate, despite its position beside descriptors.
            note=''
            height=2*l['panel_padding']+text_height(heading,f['axis'],style)+l['axis_gap']+card['height']
            if note:height+=text_height(note,f['note'],style)+.02
            panels.append(dict(axis=axis,kind=kind,heading=heading,card=card,note=note,width=cw,height=height))
        sections.append(dict(role=role,panels=panels,height=max(p['height'] for p in panels)))
    return dict(rq=rq,sections=sections,height=sum(s['height'] for s in sections)+l['facet_gap']*(len(sections)-1)+2*l.get('outer_padding',l['panel_padding']))

def complete_rows(rq,records,style,measure):
    """One axis band at a time; category grid creates no new scientific parents."""
    l=style['layout'];f=style['font_sizes'];w=style['width']-2*l['margin']-l['domain_width']-l['gutter']
    rows=[]
    for axis in AXIS_ORDER[rq]:
        cc=[c for c in records if c['rq']==rq and c['axis']==axis]
        if not cc:continue
        columns=l.get('complete_axis_columns',{}).get(axis,l['complete_columns'])
        cw=(w-(columns-1)*l['facet_gap'])/columns
        cards=[category_card(c,cw,style,measure,False) for c in cc]
        for i in range(0,len(cards),columns):
            group=cards[i:i+columns]
            heading=AXES[axis]+(' (continued)' if i else '')
            rows.append(dict(rq=rq,axis=axis,heading=heading,kind=cc[0]['display_kind'],cards=group,
                height=max(max(c['height'] for c in group)+2*l['panel_padding'],.65),continuation=bool(i)))
    return rows

def paginate(rows,maximum):
    """Keep contiguous axis groups together whenever the whole group fits."""
    groups=[]
    for row in rows:
        if not groups or groups[-1][-1]['axis']!=row['axis']:groups.append([])
        groups[-1].append(row)
    units=[]
    for group in groups:
        if sum(r['height'] for r in group)<=maximum:units.append(group)
        else:units.extend([row] for row in group)  # Retain order and continuation labels.
    pages=[];current=[];height=0
    for unit in units:
        unit_height=sum(r['height'] for r in unit)
        assert unit_height<=maximum,'CATEGORY_ROW_EXCEEDS_PAGE: increase width or page height'
        if current and height+unit_height>maximum:
            pages.append(current);current=[];height=0
        current.extend(unit);height+=unit_height
    if current:pages.append(current)
    return pages

def render_scene(scene,records,context,style,name,output_dir,compact,rq_filter=None,page=None):
    plt,_=plotting(style)
    from matplotlib.patches import Rectangle
    l=style['layout'];f=style['font_sizes'];colors=style['colors'];measure=measure_factory(style)
    body=sum(b['height'] for b in scene)+l['band_gap']*(len(scene)-1)
    natural=l['header_height']+body+l['footer_height']+2*l['margin']
    height=style['height'] if style['height'] is not None else natural
    assert height>=natural-.001,'CANVAS_TOO_SHORT: use automatic height or increase --height'
    fig=plt.figure(figsize=(style['width'],height));ax=fig.add_axes([0,0,1,1])
    ax.set(xlim=(0,style['width']),ylim=(height,0));ax.axis('off');bounds=[];texts=[]
    def box(x,y,w,h,fill,border=None,lw=None):
        ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor=border or colors['rule'],lw=l['border_width'] if lw is None else lw))
    def text(x,y,label,size,color='ink',bold=False,region=None):
        t=ax.text(x,y,label,fontsize=size,color=colors.get(color,color),fontweight='bold' if bold else 'normal',
            va='top',ha='left',linespacing=l['line_height'])
        texts.append(t)
        if region:bounds.append((t,region,label))
        return t
    margin=l['margin'];x_content=margin+l['domain_width']+l['gutter'];content_w=style['width']-margin-x_content
    title=style['labels']['title'] if compact or not rq_filter else DOMAINS[rq_filter]
    text(margin,margin,title,f['title'],bold=True)
    subtitle=style['labels']['compact_subtitle'] if compact else style['labels']['complete_subtitle']
    if page:subtitle+=f' · part {page[0]} of {page[1]}'
    text(margin,margin+.28,subtitle,f['subtitle'],'muted')
    y=margin+l['header_height']
    for block in scene:
        h=block['height'];box(margin,y,style['width']-2*margin,h,colors['container'],lw=l['separator_width'])
        if block.get('domain_header'):
            text(margin+l['panel_padding'],y+l['panel_padding'],block['heading'],f['domain'],bold=True)
        elif compact:
            domain=wrapped(DOMAINS[block['rq']],l['domain_width']-2*l['panel_padding'],f['domain'],measure,True)
            text(margin+l['panel_padding'],y+l['panel_padding'],domain,f['domain'],bold=True,
                region=(margin,y,l['domain_width'],h))
            sy=y+l.get('outer_padding',l['panel_padding'])
            for section in block['sections']:
                x=x_content
                for panel in section['panels']:
                    pw=panel['width'];kind=panel['kind'];ph=section['height']
                    box(x,sy,pw,ph,colors[kind+'_fill'],colors[kind])
                    ty=sy+l['panel_padding'];region=(x,sy,pw,ph)
                    text(x+l['panel_padding'],ty,panel['heading'],f['axis'],kind,True,region)
                    ty+=text_height(panel['heading'],f['axis'],style)+l['axis_gap']
                    text(x+l['panel_padding'],ty,panel['card']['label'],f['category'],region=region)
                    if panel['note']:
                        ty+=panel['card']['height']+.02
                        text(x+l['panel_padding'],ty,panel['note'],f['note'],'muted',region=region)
                    x+=pw+l['facet_gap']
                sy+=section['height']+l['facet_gap']
        else:
            kind=block['kind'];badge=TYPES[kind][0]
            heading=wrapped(badge+'  '+block['heading'],l['domain_width']-2*l['panel_padding'],f['axis'],measure,True,break_long_words=False)
            text(margin+l['panel_padding'],y+l['panel_padding'],heading,f['axis'],kind,True,
                region=(margin,y,l['domain_width'],h))
            x=x_content
            for card in block['cards']:
                pw=card['width'];region=(x,y,pw,h)
                box(x,y,pw,h,colors[kind+'_fill'],colors[kind])
                ty=y+l['panel_padding'];text(x+l['panel_padding'],ty,card['label'],f['category'],region=region)
                ty+=text_height(card['label'],f['category'],style)+l['metadata_gap']
                text(x+l['panel_padding'],ty,card['metadata'],f['metadata'],'muted',region=region)
                x+=pw+l['facet_gap']
        y+=h+l['band_gap']
    footer=height-l['footer_height']
    for x,kind in zip(l['legend_x'],TYPES):
        badge,label=TYPES[kind];text(x,footer,badge+'  '+label,f['legend'],kind,True)
    text(margin,footer+.22,QUALIFICATION,f['note'],'muted')
    if not compact:
        text(margin,footer+.42,'v1 = SA01-staging-definition-1; v2 = SA01-staging-definition-2. IDs and versions retain registered authority.',f['metadata'],'muted')
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    # Validate physical text extents against their allocated panels, with 1 pt tolerance.
    failures=[]
    for t,(x,yy,w,h),label in bounds:
        extent=t.get_window_extent(renderer);corners=ax.transData.inverted().transform(extent.get_points())
        left,right=sorted(corners[:,0]);top,bottom=sorted(corners[:,1]);tol=1/72
        if left<x-tol or right>x+w+tol or top<yy-tol or bottom>yy+h+tol:failures.append(label)
    assert not failures,('TEXT_OVERFLOW',name,failures)
    extents=[t.get_window_extent(renderer) for t in texts]
    overlaps=[(texts[i].get_text(),texts[j].get_text()) for i in range(len(texts)) for j in range(i+1,len(texts))
        if extents[i].overlaps(extents[j])]
    assert not overlaps,('TEXT_OVERLAP',name,overlaps)
    extra=dict(view='compact' if compact else rq_filter or 'complete',registered_nodes=len(records),
        scientific_context=context,domain_to_rq={v:k for k,v in DOMAINS.items()},display_records=canonical_map(records,compact),
        layout_validation=dict(text_overflow=0,text_overlap=0,minimum_category_font_points=f['category']),
        qualification=QUALIFICATION,part=page,
        origin_note='Registered taxonomic predicate for deliberately constructed faults only; not a comprehensive causal taxonomy.')
    export(fig,name,output_dir,style,TAXONOMY_INPUTS,'paper/figures/fig02_taxonomy_tree.py',extra)
    plt.close(fig)
    return dict(stem=name,category_ids=[c['category_id'] for c in records],canvas_inches=[style['width'],height])

def generate(view,output_dir,style,context):
    compact=view=='compact';rq_filter=view.upper() if view.startswith('rq') else None
    records=tree_records(compact,rq_filter);measure=measure_factory(style)
    if compact:
        scene=[compact_band(rq,records,style,measure) for rq in DOMAINS]
        return [render_scene(scene,records,context,style,'integrated_taxonomy',output_dir,True)]
    rows=[]
    for rq in DOMAINS:
        if rq_filter and rq!=rq_filter:continue
        rr=complete_rows(rq,records,style,measure)
        if not rq_filter:
            # Domain names replace the left axis labels only on a separate, neutral header row.
            # This is the registered domain-to-RQ organization, never a new category parent.
            rows.append(dict(rq=rq,axis=None,heading=DOMAINS[rq],kind='taxonomy',cards=[],height=.65,domain_header=True))
        rows.extend(rr)
    if not rq_filter:
        return [render_scene(rows,records,context,style,'taxonomy_complete',output_dir,False)]
    # Account for row gaps before pagination, never shrink fonts to fit a page.
    expanded=[dict(r,height=r['height']+style['layout']['band_gap']) for r in rows]
    pages=paginate(expanded,style['layout']['complete_body_height'])
    result=[]
    for i,page_rows in enumerate(pages,1):
        page_rows=[dict(r,height=r['height']-style['layout']['band_gap']) for r in page_rows]
        page_records=[c['record'] for r in page_rows for c in r['cards']]
        name='taxonomy_'+view+(f'_page{i}' if i>1 else '')
        result.append(render_scene(page_rows,page_records,context,style,name,output_dir,False,rq_filter,(i,len(pages))))
    assert [c for r in result for c in r['category_ids']]==[card['record']['category_id'] for row in rows for card in row['cards']]
    return result

def main():
    args=arguments(__doc__,['all','compact','complete','rq1','rq2','rq3','rq4','rq5']);context=taxonomy_context()
    views=['compact','complete','rq1','rq2','rq3','rq4','rq5'] if args.view=='all' else [args.view]
    index=[]
    for view in views:
        defaults=copy.deepcopy(STYLE);defaults.update(PROFILES['compact' if view=='compact' else 'complete'])
        defaults['layout'].update(COMPACT_LAYOUT if view=='compact' else COMPLETE_LAYOUT)
        style=parameters(defaults,args)
        assert style['font_sizes']['category']>=style['minimum_category_font'],'CATEGORY_FONT_TOO_SMALL'
        index.extend(generate(view,args.output_dir,style,context))
    if args.view=='all':
        payload=dict(generator='paper/figures/fig02_taxonomy_tree.py',views=index,domain_to_rq={v:k for k,v in DOMAINS.items()},scientific_context=context)
        (args.output_dir/'taxonomy_views.json').write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    if args.output_dir.resolve()==(ROOT/'paper/figures').resolve() and args.view=='all':
        # Existing scientific node/axis exports remain byte-identical, verified rather than rewritten.
        from qcc.pipeline import csvbytes
        expected={'results/taxonomy_figure_nodes.csv':csvbytes(tree_records(True)),
                  'results/taxonomy_tree_complete_nodes.csv':csvbytes(tree_records())}
        axes=[]
        for rq,axis in dict.fromkeys((c['rq'],c['axis']) for c in tree_records()):
            axes.append(dict(rq=rq,axis=axis,display_class=KINDS.get(axis,'taxonomy'),registered_definitions=sum(c['rq']==rq and c['axis']==axis for c in tree_records())))
        expected['results/taxonomy_figure_axes.csv']=csvbytes(axes)
        for path,content in expected.items():assert (ROOT/path).read_bytes()==content,('SCIENTIFIC_EXPORT_DRIFT',path)
        snippets=['% Generated by fig02_taxonomy_tree.py; complete public projection, with readable continuation panels.']
        first=True
        for entry in index:
            if not entry['stem'].startswith('taxonomy_rq'):continue
            snippets.extend([r'\begin{center}',r'\includegraphics[width=\linewidth,height='+('.73' if first else '.93')+r'\textheight,keepaspectratio]{figures/'+entry['stem']+'.pdf}',r'\end{center}',r'\clearpage'])
            first=False
        (ROOT/'paper/supplements/taxonomy_views.tex').write_text('\n'.join(snippets)+'\n')
if __name__=='__main__':main()
