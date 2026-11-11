"""Create the reader-facing study-selection figure by editing only textual labels.

The original, scientifically validated vector layout stays byte-for-byte intact in
figures/study_selection.pdf. This script uses that PDF as the design source and
removes operational IDs and wording, while retaining all stage counts and arrows.

Run: python figure_sources/study_selection_clean.py
Requires PyMuPDF; the output is a vector PDF.
"""
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'figures' / 'study_selection.pdf'
DEST = ROOT / 'figures' / 'study_selection_clean.pdf'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# Each replacement is anchored by its exact old text in the preserved vector diagram.
# Coordinates are in original PDF points; only the text line is redacted.
REPL = [
    ('Primary searches S1–S3', 'Primary database searches'),
    ('Supplementary search S4', 'Supplementary search'),
    ('15 within-S4 duplicates', '15 duplicate occurrences'),
    ('After reconciliation: 255 included;', '256 proceeded to full-text review;'),
    ('1 uncertain advances', '87 excluded at title/abstract screening'),
    ('12 pilot + 241 main-assessment records', '253 records with assessable full texts'),
    ('Includes LC0297: E8', 'Full-text criteria applied'),
    ('LC0193: source-provenance hold; outside analytical inventory.',
     'One selected publication lacks an analytical record.'),
    ('LC0234 and LC0299: inventoried without normalized RQ items.',
     'Two analytical publications lack normalized RQ items.'),
    ('Not additional eligibility exclusions.',
     'These are not additional eligibility exclusions.'),
]

# Matched background color of the original light-blue and light-ochre boxes.
BLUE = (241/255, 247/255, 250/255)
OCHRE = (251/255, 246/255, 235/255)
INK = (35/255, 52/255, 66/255)


def main():
    doc = fitz.open(SOURCE)
    p = doc[0]
    spans = {}
    for block in p.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for sp in line['spans']:
                spans[sp['text']] = sp
    substitutions = []
    for old, new in REPL:
        matches = p.search_for(old)
        if len(matches) != 1:
            raise RuntimeError(f'Expected one instance of {old!r}; found {len(matches)}')
        box = matches[0]
        # Obtain exact line's baseline; anchor the new writing to its former position.
        same = spans.get(old)
        if same is None:
            raise RuntimeError(f'Missing underlying text span for {old!r}')
        origin = same['origin']
        size = same['size']
        # Redact in the interior of the container, so no border or connector is touched.
        area = fitz.Rect(box.x0 - 0.4, box.y0 + 2.0, box.x1 + 0.4, box.y1 - 2.0)
        is_ochre = 'Includes LC0297' in old
        p.add_redact_annot(area, fill=OCHRE if is_ochre else BLUE, cross_out=False)
        substitutions.append((old, new, origin, size, same['color']))
    # Preserve line-art and all other graphics from the approved original diagram.
    p.apply_redactions(images=0, graphics=0, text=0)
    # Replacements are embedded DejaVu text, making the resulting PDF searchable.
    p.insert_font(fontname='DejaVuClean', fontfile=FONT)
    p.insert_font(fontname='DejaVuCleanBold', fontfile=BOLD_FONT)
    regular_metrics = fitz.Font(fontfile=FONT)
    bold_metrics = fitz.Font(fontfile=BOLD_FONT)
    for old, new, origin, size, original_color in substitutions:
        title = old in ('Primary searches S1–S3', 'Supplementary search S4')
        font_metrics = bold_metrics if title else regular_metrics
        new_font = 'DejaVuCleanBold' if title else 'DejaVuClean'
        color = ((original_color >> 16 & 255) / 255, (original_color >> 8 & 255) / 255, (original_color & 255) / 255)
        # Optimize width to stay within the same box; cap small body text at 10.4pt.
        max_x = 595 if old == 'Includes LC0297: E8' else (481 if old.startswith(('LC0193','LC0234','Not additional')) else 610)
        if old.startswith(('After reconciliation', '1 uncertain')): max_x = 430
        if old.startswith('12 pilot'): max_x = 430
        # Font size <= source; preserve the original visual hierarchy.
        fs = size
        while font_metrics.text_length(new, fontsize=fs) > (max_x - origin[0]) and fs > 8.3:
            fs -= 0.1
        p.insert_text(fitz.Point(*origin), new, fontsize=fs, fontname=new_font, color=color, overlay=True)
    if hasattr(doc, "subset_fonts"):
        doc.subset_fonts()
    doc.save(DEST, garbage=4, deflate=True, clean=True)
    doc.close()
    check = fitz.open(DEST)[0].get_text()
    if any(x in check for x in ('LC0193','LC0234','LC0299','LC0297', 'S1–S3','S4')):
        raise AssertionError('Operational identifiers unexpectedly present in clean selection diagram')
    print('Wrote', DEST)

if __name__ == '__main__':
    main()
