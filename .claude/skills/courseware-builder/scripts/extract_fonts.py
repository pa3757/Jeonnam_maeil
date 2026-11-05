#!/usr/bin/env python3
"""Extract fonts embedded in a .pptx and install them for LibreOffice rendering (QA only).

PowerPoint embeds fonts as EOT (.fntdata). LibreOffice ignores them, so renders of a
template that uses e.g. Pretendard fall back to another font and text-fit QA becomes
unreliable. This script unwraps uncompressed EOT, renames each font's family to the
exact typeface name the slides reference (e.g. "Pretendard Regular"), and installs it
into ~/.fonts.

Usage: python3 extract_fonts.py template.pptx [--out DIR]
Requires: fonttools (pip install fonttools) for renaming; without it fonts are installed
under their original family names.
"""
import argparse, os, re, struct, subprocess, sys, zipfile


def unwrap_eot(b):
    eot_size, data_size, version, flags = struct.unpack('<IIII', b[:16])
    data = b[-data_size:]
    if flags & 0x4:  # TTEMBED_TTCOMPRESSED (MTX) - not supported
        return None
    if flags & 0x10000000:  # XOR obfuscation
        data = bytes(x ^ 0x50 for x in data)
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx')
    ap.add_argument('--out', default=os.path.expanduser('~/.fonts'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    z = zipfile.ZipFile(a.pptx)
    pres = z.read('ppt/presentation.xml').decode('utf8')
    rels = z.read('ppt/_rels/presentation.xml.rels').decode('utf8')
    rid2target = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    rid2target.update({k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        TTFont = None
        print('fonttools not installed: fonts keep original family names (pip install fonttools)')
    n = 0
    for block in re.findall(r'<p:embeddedFont>.*?</p:embeddedFont>', pres, re.S):
        face = re.search(r'typeface="([^"]+)"', block).group(1)
        for rid in re.findall(r'r:id="([^"]+)"', block):
            target = 'ppt/' + rid2target[rid].lstrip('/').replace('ppt/', '')
            data = unwrap_eot(z.read(target))
            if data is None:
                print(f'skip {face}: MTX-compressed EOT')
                continue
            path = os.path.join(a.out, re.sub(r'\W+', '_', face) + '.ttf')
            open(path, 'wb').write(data)
            if TTFont:
                f = TTFont(path)
                for rec in f['name'].names:
                    if rec.nameID in (1, 4, 16):
                        rec.string = face
                    elif rec.nameID == 6:
                        rec.string = face.replace(' ', '-')
                    elif rec.nameID in (2, 17):
                        rec.string = 'Regular'
                f.save(path)
            n += 1
            print('installed', face, '->', path)
    subprocess.run(['fc-cache', '-f'], check=False)
    print(f'{n} font(s) installed')


if __name__ == '__main__':
    sys.exit(main())
