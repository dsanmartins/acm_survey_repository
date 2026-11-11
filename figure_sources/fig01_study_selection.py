#!/usr/bin/env python3
"""F1: PRISMA-inspired geometry for the recorded QCC selection process.

No PRISMA 2020 compliance claim is made. Counts and source identities come only
from qcc.effective_screening.selection_payload and SELECTION_INPUTS.
The frozen historical loader remains unchanged; the active flow applies the
researcher-authorized QCC-FT-1.1-ADD-01 event, preserving original decisions. Those inputs retain
versioned search runs, screening, full-text, historical accounting and the
selection-to-analysis bridge; the method seal supplies transitive provenance.
Edit STYLE for panel positions, typography, wrapping, phases and orthogonal routes.
Outputs: study_selection.pdf/.svg/.png and study_selection.provenance.json.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from qcc.effective_screening import selection_payload,SELECTION_INPUTS,STATISTICS
from qcc.figure_utils import ROOT,arguments,parameters,plotting,export

STYLE=dict(formats=['pdf','svg','png'],width=8.5,height=7.85,font_family='DejaVu Sans',dpi=300,padding=.04,
 font_sizes=dict(base=10.5,node=11.2,detail=10.4,phase=10.2),
 colors=dict(ink='#233442',primary='#176582',warning='#946419',muted='#53616d',
  fill='#f1f7fa',warning_fill='#fbf6eb',phase_fill='#f0f2f4',rule='#cbd1d6'),
 limits=dict(x=(0,8.5),y=(0,7.85)),
 boxes=dict(primary=(1.3,.12,2.6,1.25),supplementary=(4.2,.12,2.6,1.25),
  candidates=(2.1,1.72,3.9,.65),screening=(2.1,2.62,3.9,.70),ta_excluded=(6.35,2.62,2.,.70),
  fulltext=(2.1,3.57,3.9,.62),retrieval=(6.35,3.38,2.,1.),decisions=(2.1,4.50,3.9,.75),
  ft_excluded=(6.35,4.50,2.,.75),
  selected=(2.1,5.70,3.9,.62),analysis=(1.3,6.72,5.5,.97)),
 phases=[dict(label='Identification',rect=(.05,.05,1.20,2.38)),
  dict(label='Screening',rect=(.05,2.55,1.20,.84)),
  dict(label='Full-text\neligibility',rect=(.05,3.44,1.20,2.22)),
  dict(label='Included',rect=(.05,5.70,1.20,.62)),
  dict(label='Subsequent\nanalytical\ncoverage',rect=(.05,6.65,1.20,1.10))],
 routes=[
  dict(name='primary_join',points=[(2.6,1.37),(2.6,1.53),(4.05,1.53)],arrow=False),
  dict(name='supplementary_join',points=[(5.5,1.37),(5.5,1.53),(4.05,1.53)],arrow=False),
  dict(name='join_candidates',points=[(4.05,1.53),(4.05,1.72)]),
  dict(name='candidates_screening',points=[(4.05,2.37),(4.05,2.62)]),
  dict(name='screening_excluded',points=[(6.,2.97),(6.35,2.97)]),
  dict(name='screening_fulltext',points=[(4.05,3.32),(4.05,3.57)]),
  dict(name='fulltext_retrieval',points=[(6.,3.88),(6.35,3.88)]),
  dict(name='fulltext_decisions',points=[(4.05,4.19),(4.05,4.50)]),
  dict(name='decisions_excluded',points=[(6.,4.875),(6.35,4.875)]),
  dict(name='decisions_selected',points=[(4.05,5.25),(4.05,5.70)]),
  dict(name='selected_analysis',points=[(4.05,6.32),(4.05,6.72)],linestyle=(0,(3,2)))],
 node_linewidth=1.,corner_radius=.035,panel_padding=.075,title_detail_gap=.022,linespacing=1.12,
 kind_borders=dict(retained='solid',excluded='solid',unresolved=(0,(4,2)),exception=(0,(1,2))),
 arrow=dict(linewidth=1.05,head_style='-|>',head_scale=10.,color='muted'),
 separator=dict(x=(1.2,8.35),y=6.50,linewidth=.8,linestyle=(0,(3,3))),
 wrapping=dict(max_width_fraction=1.),phase_padding=.06)


def validate_accounting(d):
    """Read-only guards for the recorded identities; no source repair or recoding."""
    checks=[
      (d['primary_occurrences']-d['primary_duplicates'],d['primary_records']),
      (d['s4_occurrences']-d['s4_duplicates'],d['s4_unique']),
      (d['s4_unique']-d['s4_overlap'],d['s4_additions']),
      (d['primary_records']+d['s4_additions'],d['candidates']),
      (d['retrieved_occurrences']-d['duplicate_occurrences'],d['candidates']),
      (d['candidates']-d['ta']['EXCLUDE'],d['fulltext_input']),
      (d['fulltext_input']-d['ft']['NO_DECISION'],d['assessed']),
      (d['assessed'],d['ft']['INCLUDE']+d['ft']['EXCLUDE']+d['ft']['UNCERTAIN']),
      (d['ta']['INCLUDE']+d['ta']['UNCERTAIN'],d['fulltext_input']),
      (d['pilot']+d['main_assessed'],d['assessed']),
      (d['retrieval']['NOT_FOUND']+d['retrieval']['BIBLIOGRAPHIC_ISSUE'],d['ft']['NO_DECISION']),
      (d['selected']-len(d['held_ids']),d['inventory']),
      (d['inventory']-len(d['no_item_ids']),d['item_publications'])]
    assert all(a==b for a,b in checks),('SELECTION_ACCOUNTING_MISMATCH',checks)
    return dict(identities_checked=len(checks),all_passed=True)


def node_content(d):
    """Presentation text only: every count is supplied by the existing loader."""
    held=', '.join(d['held_ids']);no_items=' and '.join(d['no_item_ids'])
    return dict(
      primary=dict(title='Primary searches S1–S3',detail=f"{d['primary_occurrences']} retrieved occurrences\n{d['primary_duplicates']} duplicate occurrences\n{d['primary_records']} retained unique records",kind='retained'),
      supplementary=dict(title='Supplementary search S4',detail=f"{d['s4_occurrences']} retrieved occurrences\n{d['s4_duplicates']} within-S4 duplicates\n{d['s4_unique']} unique publications\n{d['s4_overlap']} primary overlaps; {d['s4_additions']} additions",kind='retained'),
      candidates=dict(title=f"{d['candidates']} unique candidate records",detail=f"{d['retrieved_occurrences']} occurrences; {d['duplicate_occurrences']} duplicates/overlaps removed",kind='retained'),
      screening=dict(title=f"Title-and-abstract screening: {d['candidates']}",detail=f"After reconciliation: {d['ta']['INCLUDE']} included;\n{d['ta']['UNCERTAIN']} uncertain advances",kind='retained'),
      ta_excluded=dict(title=f"Excluded: {d['ta']['EXCLUDE']}",detail='Screening decisions',kind='excluded'),
      fulltext=dict(title=f"Full-text records considered: {d['fulltext_input']}",detail='Retrieval and identity checked',kind='retained'),
      retrieval=dict(title='Retrieval / identity',detail=f"{d['retrieval']['NOT_FOUND']} not found\n{d['retrieval']['BIBLIOGRAPHIC_ISSUE']} bibliographic issue\nNo eligibility decision",kind='exception'),
      decisions=dict(title=f"Scientific eligibility decisions: {d['assessed']}",detail=f"{d['pilot']} pilot + {d['main_assessed']} main-assessment records",kind='retained'),
      ft_excluded=dict(title=f"Excluded: {d['ft']['EXCLUDE']}",detail=f"Includes {d['resolution_paper_id']}: {d['resolution_exclusion_code']}",kind='excluded'),
      selected=dict(title=f"Selected publication records: {d['selected']}",detail='Included after full-text assessment',kind='retained'),
      analysis=dict(title=f"{d['inventory']} analytical publications; {d['item_publications']} with normalized RQ items",detail=f"{held}: source-provenance hold; outside analytical inventory.\n{no_items}: inventoried without normalized RQ items.\nNot additional eligibility exclusions.",kind='retained'))


def segments(route):return list(zip(route['points'],route['points'][1:]))


def validate_geometry(style):
    """Reject diagonal routes, box intersections, corner ports, and unjoined crossings."""
    boxes=style['boxes'];routes=style['routes'];eps=1e-8;all_segments=[]
    for route in routes:
        for a,b in segments(route):
            assert abs(a[0]-b[0])<eps or abs(a[1]-b[1])<eps,('DIAGONAL_CONNECTOR',route['name'])
            assert a!=b,('ZERO_LENGTH_CONNECTOR',route['name'])
            all_segments.append((route['name'],a,b))
            for key,(x,y,w,h) in boxes.items():
                for point in [a,b]:
                    assert not any(abs(point[0]-cx)<eps and abs(point[1]-cy)<eps for cx,cy in [(x,y),(x+w,y),(x,y+h),(x+w,y+h)]),('CORNER_PORT',route['name'],key)
                if abs(a[1]-b[1])<eps:
                    hit=y+eps<a[1]<y+h-eps and max(min(a[0],b[0]),x+eps)<min(max(a[0],b[0]),x+w-eps)
                else:
                    hit=x+eps<a[0]<x+w-eps and max(min(a[1],b[1]),y+eps)<min(max(a[1],b[1]),y+h-eps)
                assert not hit,('CONNECTOR_THROUGH_BOX',route['name'],key)
    for i,(r,a,b) in enumerate(all_segments):
        for s,c,d in all_segments[i+1:]:
            if r==s:continue
            # An explicitly shared endpoint is a join, not a crossing.
            shared=any(abs(p[0]-q[0])<eps and abs(p[1]-q[1])<eps for p in [a,b] for q in [c,d])
            horizontal=abs(a[1]-b[1])<eps;other_horizontal=abs(c[1]-d[1])<eps
            if horizontal==other_horizontal:
                if horizontal:
                    overlap=abs(a[1]-c[1])<eps and max(min(a[0],b[0]),min(c[0],d[0]))<min(max(a[0],b[0]),max(c[0],d[0]))-eps
                else:
                    overlap=abs(a[0]-c[0])<eps and max(min(a[1],b[1]),min(c[1],d[1]))<min(max(a[1],b[1]),max(c[1],d[1]))-eps
                assert not overlap,('OVERLAPPING_CONNECTORS',r,s)
            elif not shared:
                h1,h2,v1,v2=(a,b,c,d) if horizontal else (c,d,a,b)
                crossing=min(h1[0],h2[0])-eps<=v1[0]<=max(h1[0],h2[0])+eps and min(v1[1],v2[1])-eps<=h1[1]<=max(v1[1],v2[1])+eps
                assert not crossing,('UNJOINED_CONNECTOR_CROSSING',r,s)
    return dict(orthogonal_segments=len(all_segments),diagonal_segments=0,box_intersections=0,unjoined_crossings=0,corner_ports=0)


def render(data,style,output_dir):
    accounting=validate_accounting(data);geometry=validate_geometry(style);nodes=node_content(data)
    plt,_=plotting(style)
    from matplotlib.font_manager import FontProperties,findfont
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Rectangle
    from matplotlib.path import Path as MplPath
    findfont(style['font_family'],fallback_to_default=False)
    fig=plt.figure(figsize=(style['width'],style['height']));ax=fig.add_axes([0,0,1,1])
    ax.set(xlim=style['limits']['x'],ylim=style['limits']['y'][::-1]);ax.axis('off')
    fig.canvas.draw();renderer=fig.canvas.get_renderer();f=style['font_sizes'];colors=style['colors']
    xscale=style['width']/(style['limits']['x'][1]-style['limits']['x'][0]);yscale=style['height']/(style['limits']['y'][1]-style['limits']['y'][0])
    def wrap(text,width,size,bold=False):
        font=FontProperties(family=style['font_family'],size=size,weight='bold' if bold else 'normal')
        def fits(label):return renderer.get_text_width_height_descent(label,font,False)[0]/fig.dpi<=width*xscale*style['wrapping']['max_width_fraction']
        lines=[]
        for paragraph in text.split('\n'):
            line=''
            for word in paragraph.split():
                if line and not fits(line+' '+word):lines.append(line);line=word
                else:line=(line+' '+word).strip()
                assert fits(line),('UNWRAPPABLE_LABEL',line,'increase panel width')
            lines.append(line)
        return '\n'.join(lines)
    def height(text,size):return len(text.split('\n'))*size/72*style['linespacing']/yscale
    text_regions=[]
    def text(x,y,label,size,color,bold,region,ha='left',va='top'):
        artist=ax.text(x,y,label,fontsize=size,color=color,fontweight='bold' if bold else 'normal',
            ha=ha,va=va,linespacing=style['linespacing'])
        text_regions.append((artist,region));return artist
    for phase in style['phases']:
        x,y,w,h=phase['rect'];ax.add_patch(Rectangle((x,y),w,h,facecolor=colors['phase_fill'],edgecolor='none'))
        label=wrap(phase['label'],w-2*style['phase_padding'],f['phase'],True)
        text(x+w/2,y+h/2,label,f['phase'],colors['muted'],True,phase['rect'],'center','center')
    for key,node in nodes.items():
        x,y,w,h=style['boxes'][key];kind=node['kind'];retained=kind=='retained';accent=colors['primary' if retained else 'warning']
        patch=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={style['corner_radius']}",
            facecolor=colors['fill' if retained else 'warning_fill'],edgecolor=accent,
            linewidth=style['node_linewidth'],linestyle=style['kind_borders'][kind])
        ax.add_patch(patch);pad=style['panel_padding'];region=style['boxes'][key]
        title=wrap(node['title'],w-2*pad,f['node'],True)
        detail=wrap(node['detail'],w-2*pad,f['detail']) if node['detail'] else ''
        total=height(title,f['node'])+(style['title_detail_gap']+height(detail,f['detail']) if detail else 0)
        assert total<=h-2*pad+.015,('BOX_TOO_SHORT',key,round(total+2*pad,3),h)
        ty=y+(h-total)/2
        text(x+pad,ty,title,f['node'],accent,True,region)
        if detail:text(x+pad,ty+height(title,f['node'])+style['title_detail_gap'],detail,f['detail'],colors['ink'],False,region)
    for route in style['routes']:
        points=route['points'];line=route.get('linestyle','solid');arrow=style['arrow'];color=colors[arrow['color']]
        if route.get('arrow',True):
            path=MplPath(points,[MplPath.MOVETO]+[MplPath.LINETO]*(len(points)-1))
            ax.add_patch(FancyArrowPatch(path=path,arrowstyle=arrow['head_style'],mutation_scale=arrow['head_scale'],
                linewidth=arrow['linewidth'],edgecolor=color,facecolor=color,linestyle=line,capstyle='butt',joinstyle='miter'))
        else:ax.plot([p[0] for p in points],[p[1] for p in points],color=color,lw=arrow['linewidth'],ls=line,solid_capstyle='butt')
    sep=style['separator'];ax.plot(sep['x'],[sep['y']]*2,color=colors['rule'],lw=sep['linewidth'],ls=sep['linestyle'])
    fig.canvas.draw();renderer=fig.canvas.get_renderer();extents=[]
    for artist,(x,y,w,h) in text_regions:
        extent=artist.get_window_extent(renderer);corners=ax.transData.inverted().transform(extent.get_points())
        left,right=sorted(corners[:,0]);top,bottom=sorted(corners[:,1]);tol=.015
        assert left>=x-tol and right<=x+w+tol and top>=y-tol and bottom<=y+h+tol,('TEXT_OUTSIDE_PANEL',artist.get_text())
        extents.append(extent)
    assert not any(a.overlaps(b) for i,a in enumerate(extents) for b in extents[i+1:]),'OVERLAPPING_LABELS'
    extra=dict(scientific_statistics=data,accounting_validation=accounting,geometry_validation=geometry,
        text_validation=dict(panel_overflow=0,label_overlap=0),display_nodes=nodes,
        visual_organization='PRISMA-inspired; no independent PRISMA 2020 compliance assessment asserted',
        analytical_coverage='QCC-specific post-selection extension; not additional eligibility exclusions',
        independent_studies_consolidated=False,effective_amendment=data['amendment'],historical_decisions_preserved=True)
    export(fig,'study_selection',output_dir,style,SELECTION_INPUTS,'paper/figures/fig01_study_selection.py',extra)
    plt.close(fig)


def main():
    args=arguments(__doc__);data=selection_payload();style=parameters(STYLE,args)
    if args.output_dir.resolve()==(ROOT/'paper/figures').resolve():
        # Preservation guard: this presentation task never regenerates scientific results.
        from qcc.pipeline import jsonbytes
        assert (ROOT/STATISTICS).read_bytes()==jsonbytes(data),'SELECTION_STATISTICS_DRIFT'
    render(data,style,args.output_dir)
if __name__=='__main__':main()
