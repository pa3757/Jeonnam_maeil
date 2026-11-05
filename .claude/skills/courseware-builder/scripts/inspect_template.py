#!/usr/bin/env python3
"""Dump every slide's shapes so a content spec can target them by shape id.

For each slide: text boxes (id, name, position/size in inches, and per-paragraph run
counts + text), pictures (id, position/size, pixel size) and tables (rows x cols,
runs in each first-column cell). Run counts matter: a paragraph with 3 runs usually
means a highlighted middle run (different color/weight) you can reuse.

Usage: python3 inspect_template.py template.pptx [--slides 3,6,9]
"""
import argparse
from pptx import Presentation

EMU = 914400


def pos(s):
    return f'x={s.left/EMU:.2f} y={s.top/EMU:.2f} w={s.width/EMU:.2f} h={s.height/EMU:.2f}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx')
    ap.add_argument('--slides', help='comma-separated 1-based slide numbers')
    a = ap.parse_args()
    p = Presentation(a.pptx)
    print(f'slide size: {p.slide_width/EMU:.2f} x {p.slide_height/EMU:.2f} in')
    want = {int(x) for x in a.slides.split(',')} if a.slides else None
    for i, s in enumerate(p.slides, 1):
        if want and i not in want:
            continue
        print(f'\n=== slide {i}')
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                print(f'  TEXT [{sh.shape_id}] {pos(sh)}')
                for j, para in enumerate(sh.text_frame.paragraphs):
                    print(f'      p{j} runs={len(para.runs)}: {para.text[:60]!r}')
            elif getattr(sh, 'has_table', False) and sh.has_table:
                t = sh.table
                print(f'  TABLE [{sh.shape_id}] {len(t.rows)}x{len(t.columns)} {pos(sh)} '
                      f'col_w={[round(c.width/EMU,2) for c in t.columns]}')
                for r, row in enumerate(t.rows):
                    print(f'      r{r} first-cell runs={len(row.cells[0].text_frame.paragraphs[0].runs)}: '
                          f'{[c.text[:14] for c in row.cells]}')
            elif sh.shape_type == 13:
                print(f'  PIC  [{sh.shape_id}] {pos(sh)} px={sh.image.size}')
            elif sh.shape_type == 6:
                print(f'  GROUP [{sh.shape_id}] {pos(sh)}')


if __name__ == '__main__':
    main()
