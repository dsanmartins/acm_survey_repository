"""Independent S2 marginals composed for the actual landscape supplement."""
import argparse
from pathlib import Path
import sys,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from qcc.figure_utils import ROOT,arguments,parameters,export
from qcc.acm_figure_data import level_payload,LEVEL_INPUTS
from qcc.acm_figure_support import configure,text_inside_canvas

STYLE = dict(width=6.8, height=2.35, font_family='cmr10', font_sizes=dict(base=10),formats=['pdf','svg','png'],padding=0,bbox_inches=None,
             dpi=220, left=.16, right=.66, top=.75, bottom=.25, bar_height=.48,
             color='#166781', ink='#182c38', x_max=20)


def render(data,style,output_dir):
    assert style['width']*72.27 <= 722.7
    plt,fonts=configure(style)
    fig, ax = plt.subplots(figsize=(style['width'], style['height']))
    fig.subplots_adjust(left=style['left'], right=style['right'], top=style['top'], bottom=style['bottom'])
    ax.barh(range(3), [r['items'] for r in data['levels']], color=style['color'], height=style['bar_height'])
    for i, r in enumerate(data['levels']):
        ax.text(r['items']+.45, i, str(r['items']), va='center')
        ax.text(1.10, i, str(r['publications'])+' / 182', transform=ax.get_yaxis_transform(), va='center')
    ax.text(1.10, 1.15, 'Distinct publications', transform=ax.transAxes)
    ax.set_yticks(range(3), [r['label'] for r in data['levels']])
    ax.set(xlim=(0, 20), ylim=(2.6,-.6), xlabel='Positive items / full inventory of 451')
    ax.set_xticks([0,4,8,12,16,20]); ax.tick_params(axis='y', length=0, pad=8)
    ax.spines[['top','right','left']].set_visible(False)
    text_inside_canvas(fig)
    stats = dict(levels=data['levels'], positive_items=30, publication_union=21,
                 full_items=451, full_publications=182, scoped_nonpositive=421, family_level='NOT_MAPPED')
    hashes=export(fig,'rq2_test_levels',output_dir,style,LEVEL_INPUTS,'paper/figures/rq2_test_levels.py',
        dict(scientific_statistics=stats,font_provenance=fonts,additional_code_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['src/qcc/acm_figure_data.py','src/qcc/acm_figure_support.py']}))
    plt.close(fig)
    return stats


def main():
    args=arguments(__doc__);style=parameters(STYLE,args);style['bbox_inches']=None
    render(level_payload(),style,args.output_dir)


if __name__=='__main__':main()
