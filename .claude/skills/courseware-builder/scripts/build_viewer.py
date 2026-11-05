#!/usr/bin/env python3
"""Build a public, GitHub Pages-ready slide viewer from a finished .pptx.

The viewer shows slide images only: no speaker notes, no PPTX download. Notes stay in
the .pptx for the instructor. Output goes in its own folder (default docs/) so Pages can
publish that folder alone and the .pptx elsewhere in the repo is never served.

Usage:
  python3 build_viewer.py deck.pptx --out docs --title "덱 제목" --subtitle "강의명" \
      --titles titles.json [--sections sections.json] [--pptx-skill /path/to/pptx]

titles.json:   ["표지", "목차", ...]  one per slide (shown in header + table of contents)
sections.json: {"1": "시작", "6": "1교시 · 검증", ...}  slide number where a group starts
Renders with LibreOffice (pptx skill's soffice.py) -> pdftoppm 96dpi (1920x1080 for a
20in-wide deck) -> JPEG + 320px thumbnails.
"""
import argparse, glob, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def find_soffice(skill):
    if skill:
        return os.path.join(skill, 'scripts/office/soffice.py')
    for p in ['~/.claude/skills/**/pptx/scripts/office/soffice.py', '/mnt/skills/**/pptx/scripts/office/soffice.py',
              '/root/.claude/skills/**/pptx/scripts/office/soffice.py']:
        hits = glob.glob(os.path.expanduser(p), recursive=True)
        if hits:
            return hits[0]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx'); ap.add_argument('--out', default='docs')
    ap.add_argument('--title', required=True); ap.add_argument('--subtitle', default='')
    ap.add_argument('--description', default='')
    ap.add_argument('--titles'); ap.add_argument('--sections'); ap.add_argument('--pptx-skill')
    a = ap.parse_args()
    from PIL import Image

    tmp = tempfile.mkdtemp(prefix='viewer_')
    shutil.copy(a.pptx, os.path.join(tmp, 'deck.pptx'))
    soffice = find_soffice(a.pptx_skill)
    cmd = [sys.executable, soffice] if soffice else ['soffice']
    subprocess.run(cmd + ['--headless', '--convert-to', 'pdf', '--outdir', tmp, os.path.join(tmp, 'deck.pptx')],
                   check=True, capture_output=True, timeout=600)
    subprocess.run(['pdftoppm', '-png', '-r', '96', os.path.join(tmp, 'deck.pdf'), os.path.join(tmp, 'p')], check=True)
    pngs = sorted(glob.glob(os.path.join(tmp, 'p-*.png')))
    sd = os.path.join(a.out, 'slides')
    os.makedirs(sd, exist_ok=True)
    for f in glob.glob(os.path.join(sd, '*.jpg')):
        os.remove(f)
    for i, f in enumerate(pngs, 1):
        im = Image.open(f).convert('RGB')
        im.save(f'{sd}/slide-{i:02d}.jpg', quality=86, optimize=True, progressive=True)
        im.resize((320, round(320 * im.height / im.width)), Image.LANCZOS).save(f'{sd}/thumb-{i:02d}.jpg', quality=80)
    n = len(pngs)
    titles = json.load(open(a.titles, encoding='utf8')) if a.titles else [f'슬라이드 {i}' for i in range(1, n + 1)]
    if len(titles) != n:
        sys.exit(f'titles has {len(titles)} entries but deck has {n} slides')
    sections = json.load(open(a.sections, encoding='utf8')) if a.sections else {}
    d = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
    t = open(os.path.join(HERE, '..', 'assets', 'viewer_template.html'), encoding='utf8').read()
    t = (t.replace('__PAGE_TITLE__', esc(f'{a.title} | {a.subtitle}' if a.subtitle else a.title))
          .replace('__DESCRIPTION__', esc(a.description or a.title))
          .replace('__DECK_TITLE__', esc(a.title)).replace('__DECK_SUBTITLE__', esc(a.subtitle))
          .replace('__TITLES__', d(titles)).replace('__SECTIONS__', d({int(k): v for k, v in sections.items()})))
    open(os.path.join(a.out, 'index.html'), 'w', encoding='utf8').write(t)
    open(os.path.join(a.out, '.nojekyll'), 'w').close()
    shutil.rmtree(tmp)
    print(f'{n} slides -> {a.out}/index.html')


if __name__ == '__main__':
    main()
