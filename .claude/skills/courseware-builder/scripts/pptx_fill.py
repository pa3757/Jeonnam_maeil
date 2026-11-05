"""Helpers for filling a template-derived deck while keeping the template's formatting.

Import from a per-project fill script:

    import sys; sys.path.insert(0, '<skill>/scripts')
    from pptx_fill import Deck
    d = Deck('struct.pptx', assets='assets/')
    s = d.slides[0]
    d.txt(s, 15, '부제')                                  # single paragraph
    d.txt(s, 17, ['첫 줄', (1, '두 번째 줄')])             # copy paragraph 1's style for line 2
    d.txt(s, 12, [(5, ['앞 ', '강조', ' 뒤'])])            # reuse a 3-run paragraph (highlight)
    d.pic(s, 16, 'icon.png', size=1.15)                    # swap a picture, keep center/z-order
    d.delete(s, 12, 14)                                    # remove shapes
    d.table(s, 13, header, rows, widths=[...], row_h=0.62, font_pt=22)
    d.notes(s, script='읽을 스크립트', memo='진행 메모')
    d.save('deck.pptx')

Why paragraph cloning: the template's text boxes carry font, size, color and spacing on
each paragraph/run. Cloning an existing paragraph and replacing only run text keeps the
design intact; python-pptx's `text_frame.text = ...` would flatten it.
"""
import copy
from pptx import Presentation
from pptx.util import Inches, Pt

A_NS = '{http://schemas.openxmlformats.org/drawingml/2006/main}'


def _set_para(p, texts):
    runs = p.findall(A_NS + 'r')
    if isinstance(texts, str):
        texts = [texts]
    if runs and len(runs) < len(texts):  # fewer runs than texts: merge the tail into the last run
        texts = texts[:len(runs) - 1] + [''.join(texts[len(runs) - 1:])]
    for i, r in enumerate(runs):
        if i < len(texts):
            r.find(A_NS + 't').text = texts[i]
        else:
            p.remove(r)
    for br in p.findall(A_NS + 'br'):
        p.remove(br)


class Deck:
    def __init__(self, path, assets=''):
        self.prs = Presentation(path)
        self.slides = list(self.prs.slides)
        self.assets = assets

    def sh(self, slide, sid):
        for s in slide.shapes:
            if s.shape_id == sid:
                return s
        raise KeyError(f'shape id {sid} not on slide {self.slides.index(slide)+1}')

    def txt(self, slide, sid, lines):
        """lines: str | list of (str | list[str] | (src_para_idx, str|list[str]))"""
        if isinstance(lines, str):
            lines = [lines]
        body = self.sh(slide, sid).text_frame._txBody
        paras = body.findall(A_NS + 'p')
        new = []
        for spec in lines:
            src, texts = spec if isinstance(spec, tuple) else (0, spec)
            p = copy.deepcopy(paras[min(src, len(paras) - 1)])
            _set_para(p, texts)
            new.append(p)
        for p in paras:
            body.remove(p)
        for p in new:
            body.append(p)

    def cell(self, c, texts):
        ps = c.text_frame._txBody.findall(A_NS + 'p')
        for extra in ps[1:]:
            c.text_frame._txBody.remove(extra)
        _set_para(ps[0], texts)

    def delete(self, slide, *sids):
        for sid in sids:
            e = self.sh(slide, sid)._element
            e.getparent().remove(e)

    def pic(self, slide, sid, png, size=None):
        """Replace a picture in place. size (inches) makes a square centered on the old one."""
        old = self.sh(slide, sid)
        l, t, w, h = old.left, old.top, old.width, old.height
        if size:
            cx, cy = l + w // 2, t + h // 2
            w = h = Inches(size)
            l, t = cx - w // 2, cy - h // 2
        new = slide.shapes.add_picture(self.assets + png, l, t, w, h)
        oe = old._element
        oe.addprevious(new._element)
        oe.getparent().remove(oe)

    def table(self, slide, sid, header, rows, widths=None, row_h=None, font_pt=None, bullet=None):
        """Rebuild a template table: header + any number of body rows.

        Body rows cycle through the template's body-row styles. If bullet is given
        (e.g. '●︎'), the first column is written as [bullet, ' ' + text] so a colored
        bullet run in the template keeps its color.
        """
        gf = self.sh(slide, sid)
        t = gf.table
        tpl = [copy.deepcopy(r._tr) for r in t.rows]
        for r in list(t.rows):
            t._tbl.remove(r._tr)
        t._tbl.append(copy.deepcopy(tpl[0]))
        body_tpl = tpl[1:] or tpl[:1]
        for i in range(len(rows)):
            t._tbl.append(copy.deepcopy(body_tpl[i % len(body_tpl)]))
        for j, h in enumerate(header):
            self.cell(t.cell(0, j), h)
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                val = [bullet, ' ' + v] if (bullet and j == 0) else v
                self.cell(t.cell(i + 1, j), val)
        if widths:
            for j, w in enumerate(widths):
                t.columns[j].width = Inches(w)
            gf.width = Inches(sum(widths))
        for r in t.rows:
            if row_h:
                r.height = Inches(row_h)
            if font_pt:
                for c in r.cells:
                    for p in c.text_frame.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(font_pt)

    def notes(self, slide, script, memo=''):
        text = '【발표 스크립트】\n' + script.strip()
        if memo:
            text += '\n\n【진행 메모】\n' + memo.strip()
        slide.notes_slide.notes_text_frame.text = text

    def save(self, path):
        self.prs.save(path)
