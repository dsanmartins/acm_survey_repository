"""Official ACM Figure 3: editable native-width, approved same-item family-mode support."""
import argparse
import json
import textwrap
from pathlib import Path
import sys,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from qcc.figure_utils import ROOT,arguments,parameters,export
from qcc.figure_data import bubble_payload,BUBBLE_INPUTS
from qcc.acm_figure_support import configure,text_inside_canvas

STYLE = dict(formats=['pdf','svg','png'],width=430.00462/72.27,height=5.65,font_family='QCC Libertine',
             font_sizes=dict(base=9,category=9,count=9,legend=8),font_units='TeX pt',dpi=220,padding=0,bbox_inches=None,
             left=.555,right=.965,top=.88,bottom=.085,family_wrap=47,
             color='#166781',band='#f0f4f6',grid='#d4dce1',ink='#182c38',
             area_per_publication=9.0,outline_width=0,label_inside_min=8,small_label_offset_pt=6,
             legend_counts=[1,10,25,50],mode_order=['STATIC','DYNAMIC','HYBRID','FORMAL'],
             mode_labels=['Static','Dynamic','Hybrid','Formal'])


def render(data, style, output_dir):
    plt,fonts = configure(style)
    assert style['area_per_publication']>0
    fig, ax = plt.subplots(figsize=(style['width'], style['height']))
    fig.subplots_adjust(left=style['left'], right=style['right'], top=style['top'], bottom=style['bottom'])
    cells = data['cells']
    families = sorted({c['technique_family'] for c in cells})
    names = {c['technique_family']: c['technique_family_label'] for c in cells}
    assert len(families) == 15
    for i in range(15):
        if i % 2 == 0:
            ax.axhspan(i-.5, i+.5, color=style['band'], zorder=0)
    for x in range(4):
        ax.axvline(x, color=style['grid'], linewidth=.45, zorder=1)
    support = []
    for c in cells:
        n = len(set(json.loads(c['paper_ids_json'])))
        x = style['mode_order'].index(c['analysis_mode_label']); y = families.index(c['technique_family'])
        marker = ax.scatter(x, y, s=n*style['area_per_publication'], color=style['color'], linewidths=0, zorder=2)
        marker.set_gid('cell-'+c['technique_family']+'-'+c['analysis_mode_label'])
        if n >= style['label_inside_min']:
            txt = ax.text(x, y, str(n), ha='center', va='center', fontsize=style['font_sizes']['count']*72/72.27,
                          color='white', fontweight='bold', zorder=3)
        else:
            txt = ax.annotate(str(n), (x, y), xytext=(style['small_label_offset_pt'], 0), textcoords='offset points',
                              ha='left', va='center', fontsize=style['font_sizes']['count']*72/72.27, color=style['ink'])
        txt.set_gid('count-'+c['technique_family']+'-'+c['analysis_mode_label'])
        support.append(dict(family_id=c['technique_family'], mode=c['analysis_mode_label'], publications=n,
                            item_ids=json.loads(c['item_ids_json']), paper_ids=json.loads(c['paper_ids_json'])))
    ax.set_xticks(range(4), style['mode_labels'])
    ax.set_yticks(range(15), [textwrap.fill(names[k], style['family_wrap'], break_long_words=False) for k in families],
                  fontsize=style['font_sizes']['category']*72/72.27)
    ax.tick_params(length=0, pad=6)
    ax.set(xlim=(-.43, 3.48), ylim=(14.5, -.5))
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.text(.025, .973, 'Distinct publication records per cell', va='top', color=style['ink'])
    legend = fig.add_axes([.56, .943, .41, .035]); legend.axis('off')
    legend.set(xlim=(-.4, 3.6), ylim=(-1, 1))
    for x, n in enumerate(style['legend_counts']):
        legend.scatter(x, 0, s=n*style['area_per_publication'], color=style['color'], linewidths=0, clip_on=False)
        legend.annotate(str(n), (x, 0), xytext=(0, -17), textcoords='offset points', ha='center', va='top', fontsize=style['font_sizes']['legend']*72/72.27)
    text_inside_canvas(fig)
    item_union=set().union(*(set(c['item_ids']) for c in support))
    publication_union=set().union(*(set(c['paper_ids']) for c in support))
    assert (len(item_union),len(publication_union),len(support))==(383,161,28)
    stats = dict(matrix=[15,4], items=len(item_union), publication_union=len(publication_union), positive_cells=len(support), labels=len(support),
                 full_items=451, full_publications=182, excluded_family_scoped_nonpositive=68,
                 cells=support, minimum_font_tex_pt=8, reading_size_not_scaled=True)
    hashes=export(fig,'rq2_bubble',output_dir,style,BUBBLE_INPUTS,'paper/figures/fig03_rq2_bubble.py',
        dict(scientific_statistics={k:v for k,v in data.items() if k!='cells'},approved_support=stats,
             font_provenance=fonts,additional_code_sha256={'src/qcc/acm_figure_support.py':hashlib.sha256((ROOT/'src/qcc/acm_figure_support.py').read_bytes()).hexdigest()}))
    import matplotlib
    plt.close(fig)
    return hashes,matplotlib.__version__


def main():
    args=arguments(__doc__);data=bubble_payload();style=parameters(STYLE,args);style['bbox_inches']=None
    hashes,version=render(data,style,args.output_dir)
    if args.output_dir.resolve()==(ROOT/'paper/figures').resolve():
        from qcc.pipeline import write,jsonbytes
        write('results/figure_statistics.json',jsonbytes(dict(x='analysis mode',y='technique family',bubble_area='distinct publications',
            area_scale_points_squared_per_publication=style['area_per_publication'],joint_source_items=data['joint_items'],
            observed_cells=data['observed_cells'],all_RQ2_items=data['total_items'],excluded_items=data['excluded_items'],
            unique_publications=161,matplotlib_version=version,source_data='results/rq2_bubble.csv',
            source_data_sha256=hashlib.sha256((ROOT/'results/rq2_bubble.csv').read_bytes()).hexdigest(),
            files={'paper/figures/'+k:v for k,v in hashes.items()})))


if __name__=='__main__':main()
