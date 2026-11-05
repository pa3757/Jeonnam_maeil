#!/usr/bin/env python3
"""Build the slide skeleton of a new deck from template slides, in a given order.

Each template slide can be used any number of times; the first use keeps the original,
later uses are duplicated with the pptx skill's add_slide.py (which does all package
bookkeeping). Template slides not used are removed with clean.py.

Usage:
  python3 build_structure.py template.pptx out.pptx --order 1,2,8,9,14,3,6,14,... \
      [--pptx-skill /path/to/pptx/skill]

If --pptx-skill is omitted, the script searches common skill folders for
pptx/scripts/add_slide.py.
"""
import argparse, glob, os, re, shutil, subprocess, sys, tempfile, zipfile


def find_pptx_skill():
    pats = ['~/.claude/skills/**/pptx/scripts/add_slide.py', '/mnt/skills/**/pptx/scripts/add_slide.py',
            '/root/.claude/skills/**/pptx/scripts/add_slide.py']
    for p in pats:
        hits = glob.glob(os.path.expanduser(p), recursive=True)
        if hits:
            return os.path.dirname(os.path.dirname(hits[0]))
    sys.exit('pptx skill not found: pass --pptx-skill')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('template'); ap.add_argument('out')
    ap.add_argument('--order', required=True)
    ap.add_argument('--pptx-skill')
    a = ap.parse_args()
    skill = a.pptx_skill or find_pptx_skill()
    order = [int(x) for x in a.order.split(',')]
    work = tempfile.mkdtemp(prefix='struct_')
    un = os.path.join(work, 'un')
    zipfile.ZipFile(a.template).extractall(un)
    used, files = set(), []
    for src in order:
        if src not in used:
            used.add(src); files.append(f'slide{src}.xml'); continue
        r = subprocess.run([sys.executable, f'{skill}/scripts/add_slide.py', un + '/', f'slide{src}.xml'],
                           capture_output=True, text=True)
        m = re.search(r'(slide\d+\.xml) from', r.stdout + r.stderr)
        if not m:
            sys.exit(r.stdout + r.stderr)
        files.append(m.group(1))
    rels = open(f'{un}/ppt/_rels/presentation.xml.rels', encoding='utf8').read()
    rid = {}
    for t in re.findall(r'<Relationship [^>]*>', rels):
        i = re.search(r'Id="([^"]+)"', t).group(1); tg = re.search(r'Target="([^"]+)"', t).group(1)
        if 'slides/slide' in tg:
            rid[tg.split('/')[-1]] = i
    pres_p = f'{un}/ppt/presentation.xml'
    pres = open(pres_p, encoding='utf8').read()
    lst = re.search(r'<p:sldIdLst>.*?</p:sldIdLst>', pres, re.S).group(0)
    ids = {r: i for i, r in re.findall(r'<p:sldId id="(\d+)" r:id="([^"]+)"/>', lst)}
    new = '<p:sldIdLst>' + ''.join(f'<p:sldId id="{ids[rid[f]]}" r:id="{rid[f]}"/>' for f in files) + '</p:sldIdLst>'
    open(pres_p, 'w', encoding='utf8').write(pres.replace(lst, new))
    subprocess.run([sys.executable, f'{skill}/scripts/clean.py', un + '/'], check=True, capture_output=True)
    if os.path.exists(a.out):
        os.remove(a.out)
    out = os.path.abspath(a.out)
    subprocess.run(['zip', '-qXr', out, '.'], cwd=un, check=True)
    shutil.rmtree(work)
    print(f'{len(files)} slides -> {a.out}')


if __name__ == '__main__':
    main()
