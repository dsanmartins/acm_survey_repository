"""Editable design proposals for QCC-CSUR conceptual maps.

These diagrams illustrate source-grounded categories, not new empirical pairings.
Only matplotlib is required. Source terminology: current QCC manuscript
sections 4, 5.1, 5.3--5.5 and 7.2.
"""
from pathlib import Path
from datetime import datetime, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import rcParams

OUT = Path(__file__).resolve().parent.parent / 'figures'
OUT.mkdir(exist_ok=True)
rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.family': 'DejaVu Sans'})
C = {'ink':'#203646','muted':'#576B79','blue':'#116986','blue_pale':'#EDF6FA',
     'teal':'#157C75','teal_pale':'#EDF8F5','gold':'#9A661D',
     'gold_pale':'#FBF5E9','violet':'#73558F','violet_pale':'#F4F1F8',
     'rule':'#BCD0D8','white':'#FFFFFF'}

def rect(ax, x,y,w,h,fc,ec=None,rounding=.09,lw=1.0):
    obj=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.008,rounding_size={rounding}',
                       facecolor=fc,edgecolor=ec or fc,linewidth=lw)
    ax.add_patch(obj)
    return obj

def label(ax,x,y,s,fs=12,weight='normal',color='ink',ha='left'):
    ax.text(x,y,s,ha=ha,va='center',fontsize=fs,fontweight=weight,color=C.get(color,color),linespacing=1.15)

def prep(w,h):
    fig,ax=plt.subplots(figsize=(w,h))
    fig.patch.set_facecolor(C['white'])
    ax.set(xlim=(0,w),ylim=(0,h)); ax.set_axis_off()
    fig.subplots_adjust(0,0,1,1)
    return fig,ax

def export(fig,root):
    path=OUT/root
    fig.savefig(path.with_suffix('.pdf'), metadata={'Creator':'Editable QCC-CSUR matplotlib design', 'CreationDate':datetime(2026,11,11,tzinfo=timezone.utc)})
    fig.savefig(path.with_suffix('.png'),dpi=225)
    plt.close(fig)
    print(path.with_suffix('.pdf'))

# Figure A: RQ1 facets, not asserted one-to-one or causal chains.
fig,ax=prep(10.6,4.15)
label(ax,.35,3.88,'RQ1  |  Reported quality phenomena',fs=17,weight='bold')
label(ax,.35,3.52,'Three complementary facets of a reported quality problem',fs=10.8,color='muted')
columns=[
    ('AFFECTED ARTIFACT', 'Where?', C['blue'], C['blue_pale'],
     ['Program, source,\nor circuit instance', 'Tool or platform\ncomponent', 'Generated or\ntransformed artifact']),
    ('PHENOMENON', 'What condition?', C['teal'], C['teal_pale'],
     ['Program, state, or\ndependency inconsistency', 'Structural, design, or\nintegration inadequacy', 'Analysis or test-\nassessment inadequacy']),
    ('MANIFESTATION', 'How does it appear?', C['gold'], C['gold_pale'],
     ['Diagnostic or\nquality indicator', 'Specification-relative\noutput discrepancy', 'Operational failure\nor noncompletion'])
]
start=.35; cw=3.17; gap=.20
for i,(head,question,accent,fill,items) in enumerate(columns):
    x=start+i*(cw+gap)
    rect(ax,x,2.83,cw,.56,C['ink'],rounding=.08,lw=0)
    label(ax,x+cw/2,3.16,head,fs=11.3,weight='bold',color='white',ha='center')
    label(ax,x+cw/2,2.97,question,fs=9,color='white',ha='center')
    for j,item in enumerate(items):
        y=2.14-j*.72
        rect(ax,x,y,cw,.62,fill,ec=accent,rounding=.05,lw=.8)
        label(ax,x+cw/2,y+.31,item,fs=10.2,color='ink',ha='center')
# Bottom clear interpretative boundary
rect(ax,.36,.12,9.88,.52,'#F1F3F5',ec='#CAD4DA',rounding=.05,lw=.7)
label(ax,5.30,.38,'Distinct facets; no one-to-one mapping or causal relationship is inferred.',fs=10.2,color='muted',ha='center')
export(fig,'rq1_concept_map')

# Figure B: RQ3--5 source-scoped contrasts, not a shared implemented pipeline.
fig,ax=prep(10.6,4.28)
label(ax,.32,4.03,'RQ3–RQ5  |  Representation, condition, and model-level implications',fs=15.2,weight='bold')
label(ax,.32,3.73,'Different requirements for structural, semantic, and observational assessment',fs=10.5,color='muted')
left=1.33; xs=[left,4.46,7.59]; cw=2.70
heads=[('RQ3 · REPRESENTATION','Information available'),('RQ4 · CONDITION','Property to assess'),('RQ5 · IMPLICATION','What an assessment requires')]
for x,(head,subtitle) in zip(xs,heads):
    rect(ax,x,3.04,cw,.55,C['ink'],rounding=.055,lw=0)
    label(ax,x+cw/2,3.37,head,fs=10.3,weight='bold',color='white',ha='center')
    label(ax,x+cw/2,3.16,subtitle,fs=8.4,color='white',ha='center')
rows=[
 ('STRUCTURAL',C['blue'],C['blue_pale'],['Graph-based model:\noperand and control links','Control–target\ndisjointness','Structural predicate\nover model relations']),
 ('SEMANTIC',C['violet'],C['violet_pale'],['Twist: purity annotations\nand state semantics','Purity / factorization\nunder language semantics','Semantic reasoning\nand runtime assertions']),
 ('OBSERVATIONAL',C['gold'],C['gold_pale'],['QASMInfer: reference\ndistribution and samples','Compatibility of sampled\nand expected outcomes','Statistical oracle;\nexecution data needed'])
]
for i,(kind,accent,fill,items) in enumerate(rows):
    y=2.15-i*.92
    rect(ax,.13,y+.18,1.06,.48,fill,ec=accent,rounding=.045,lw=1.0)
    label(ax,.66,y+.42,kind,fs=8.2 if kind=='OBSERVATIONAL' else 9.5,weight='bold',color=accent,ha='center')
    for j,(x,item) in enumerate(zip(xs,items)):
        rect(ax,x,y,cw,.85,fill,ec=accent,rounding=.052,lw=.85)
        label(ax,x+cw/2,y+.425,item,fs=9.85,color='ink',ha='center')
    for j in (0,1):
        xa=xs[j]+cw+.055; xb=xs[j+1]-.055
        ax.add_patch(FancyArrowPatch((xa,y+.425),(xb,y+.425),arrowstyle='-|>',
                                    color=C['teal'],linewidth=1.3,mutation_scale=10))
# The scientific scope is stated in the manuscript caption rather than
# a strip that would overlap the final row at publication scale.
export(fig,'rq3_rq4_rq5_bridge')
