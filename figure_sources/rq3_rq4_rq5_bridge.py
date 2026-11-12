"""Create a compact, editable evidence-path map for RQ3--RQ5.

This is an interpretive comparison of SOURCE-SPECIFIC cases, not newly validated
item-level links, a checker implementation, or an empirical result. Existing
scientific figures are never overwritten. Requires matplotlib only.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'figures/rq3_rq4_rq5_bridge.pdf'
C={'ink':'#263E52','blue':'#23537A','teal':'#2B7776','gold':'#9E711E',
   'line':'#AABFCB','pale':'#F4F8FA','warm':'#FBF7EC','lav':'#F4F2F8'}

fig,ax=plt.subplots(figsize=(9.0,4.4))
ax.set_xlim(0,9);ax.set_ylim(0,4.4);ax.axis('off')
xs=[.22,3.29,6.36];w=2.43
heads=[('RQ3  REPRESENTATION','Information available'),('RQ4  CONDITION','Property to assess'),('RQ5  ASSESSMENT PATH','What a check requires')]
for j,(title,desc) in enumerate(heads):
 x=xs[j]
 ax.add_patch(FancyBboxPatch((x,3.74),w,.55,boxstyle='round,pad=.02,rounding_size=.07',facecolor=C['blue'],edgecolor=C['blue']))
 ax.text(x+w/2,4.09,title,ha='center',va='center',color='white',fontweight='bold',fontsize=9)
 ax.text(x+w/2,3.87,desc,ha='center',va='center',color='white',fontsize=8.1)

rows=[
 ('STRUCTURAL', C['pale'],[
    'Graph model\noperand and control links',
    'Control--target\ndisjointness',
    'Structural predicate\nover model relations']),
 ('SEMANTIC', C['lav'],[
    'Twist purity annotations\nand state semantics',
    'Purity / factorization\nunder stated semantics',
    'Static reasoning and\nruntime assertions']),
 ('OBSERVATIONAL', C['warm'],[
    'Exact reference distribution\nand sampled outcomes',
    'Distributional agreement\nfor sampled outcomes',
    'Statistical oracle; requires\nsampled observations'])
]
ys=[2.63,1.55,.47]
for i,(label,fill,items) in enumerate(rows):
 y=ys[i]
 ax.text(.03,y+.82,label,fontsize=7.8,weight='bold',ha='left',va='center',color=C['teal'] if i<2 else C['gold'])
 for j,content in enumerate(items):
  x=xs[j]
  ax.add_patch(FancyBboxPatch((x,y),w,.79,boxstyle='round,pad=.02,rounding_size=.055',edgecolor=C['line'],linewidth=.92,facecolor=fill))
  ax.text(x+w/2,y+.40,content,ha='center',va='center',fontsize=8.7,linespacing=1.25,color=C['ink'])
 for j in (0,1):
  a=xs[j]+w+.04;b=xs[j+1]-.04
  ax.add_patch(FancyArrowPatch((a,y+.39),(b,y+.39),arrowstyle='-|>',lw=1.05,color=C['teal'],mutation_scale=12))
fig.text(.03,.018,'Examples: graph models, Twist, QASMInfer. These are not a validated common pipeline.',color=C['ink'],fontsize=8.1)
fig.savefig(OUT,format='pdf',bbox_inches='tight',pad_inches=.04,metadata={'Creator':'QCC author-editable Python source'})
plt.close(fig)
print(OUT)
