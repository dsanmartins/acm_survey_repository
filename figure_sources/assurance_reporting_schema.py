"""Compact, editable illustration of the seven-field assurance-claim schema.

Usage (from any working directory):
    python figure_sources/assurance_reporting_schema.py

No numerical results are computed. The illustrative QASMInfer labels summarize
its *reported procedure* (LC0110), not an observed simulator verdict.
Edit the `groups`, `example_lines`, colors, and dimensions below as needed.
"""
from pathlib import Path
from datetime import datetime, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'figures' / 'assurance_reporting_schema.pdf'

# Editable editorial parameters
INK = '#172B40'
ACCENT = '#184F77'
BORDER = '#A8BECC'
PALE = '#F3F7FA'
EXAMPLE = '#EAF2F6'

# Exactly seven fields, organized in three interpretive questions.
groups = [
    ('WHAT IS CHECKED?', ['1  Target artifact and property',
                         '2  Available representation',
                         '3  Required information / observations']),
    ('HOW IS IT ASSESSED?', ['4  Checking mechanism',
                            '5  Assumptions and premises']),
    ('WHAT FOLLOWS?', ['6  Supported verdict',
                      '7  Limits of the conclusion']),
]
# A concrete illustrative application, not a result from a new experiment.
example_lines = [
    ['Software-stack simulator;',
     'exact reference distribution',
     'and 1,024 sampled outcomes'],
    ['One-sample chi-square',
     'goodness-of-fit test;',
     'rejection threshold p < 0.01'],
    ['Possible: reject or fail to reject.',
     'Failure to reject is not proof',
     'of overall simulator correctness'],
]

fig, ax = plt.subplots(figsize=(8.7, 3.12))
ax.set_xlim(0, 8.7)
ax.set_ylim(0, 3.12)
ax.axis('off')

start_x, card_w, gap = 0.15, 2.62, 0.27
xs = [start_x + i * (card_w + gap) for i in range(3)]
for i, ((heading, fields), lines) in enumerate(zip(groups, example_lines)):
    x = xs[i]
    # Upper area: what each part of the schema reports.
    card = FancyBboxPatch((x, 1.53), card_w, 1.43,
        boxstyle='round,pad=0.035,rounding_size=0.075',
        linewidth=0.85, edgecolor=BORDER, facecolor=PALE)
    ax.add_patch(card)
    ax.text(x + card_w / 2, 2.77, heading, fontsize=10.2,
            color=ACCENT, weight='bold', ha='center', va='center')
    for j, line in enumerate(fields):
        y = 2.47 - j*0.275
        if i == 0 and j == 2:  # Preserve full wording without overflow.
            ax.text(x + .13, y, '3  Required information /', fontsize=9.8,
                    color=INK, ha='left', va='center')
            ax.text(x + .31, y - .20, 'observations', fontsize=9.8,
                    color=INK, ha='left', va='center')
        else:
            ax.text(x + .13, y, line, fontsize=9.8, color=INK,
                    ha='left', va='center')
    # Lower area: show what a named mechanism actually supplies.
    ex = FancyBboxPatch((x, .12), card_w, 1.12,
        boxstyle='round,pad=0.035,rounding_size=0.075',
        linewidth=.8, edgecolor=BORDER, facecolor=EXAMPLE)
    ax.add_patch(ex)
    for j, line in enumerate(lines):
        ax.text(x + .13, 0.99 - j*.30, line, fontsize=9.7,
                color=INK, ha='left', va='center')

# Arrows indicate inferential connections, not an executable workflow.
for i in (0, 1):
    x0 = xs[i] + card_w + .038
    x1 = xs[i+1] - .038
    ax.add_patch(FancyArrowPatch((x0, 2.12), (x1, 2.12),
        arrowstyle='-|>', mutation_scale=10, lw=1.1, color=ACCENT))

ax.text(.18, 1.38, 'ILLUSTRATIVE CASE  |  QASMInfer simulator assessment',
    fontsize=9.6, weight='bold', color=ACCENT, ha='left', va='center')
# Explicitly avoid presenting a hypothetical decision as an observed finding.
# The caption makes clear that the example describes a possible verdict, not an observed result.

fig.subplots_adjust(left=.009, right=.991, bottom=.015, top=.99)
PDF.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(PDF, format='pdf', metadata={
    'Title': 'From Assessment Properties to Justified Assurance Claims: An Illustrative Framework',
    'Creator': 'Editable Matplotlib scientific illustration',
    'CreationDate': datetime(2026, 11, 11, tzinfo=timezone.utc),
})
fig.savefig(PDF.with_suffix('.png'), dpi=220)
plt.close(fig)
print(PDF)
