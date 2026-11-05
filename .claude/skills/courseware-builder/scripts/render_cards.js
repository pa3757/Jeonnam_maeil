// Render "prompt example" cards (chat-bubble style) as PNGs, e.g. to replace stock photos
// on a Before/After template slide.
//
// Usage: node render_cards.js spec.json out_dir
// spec.json: [
//   {"file":"c_before.png","kind":"before","w":1648,"h":906,
//    "user":"이 보도자료 기사로 써줘","ai":"○○군이 지역 발전의 ...","tag":"결과: 홍보 문구가 그대로"},
//   {"file":"c_after.png","kind":"after","w":1648,"h":906,
//    "user":"역할: ...\n맥락: ...\n형식: ...\n검증: ...","tag":"결과: 데스크에 올릴 초안"}
// ]
// Size w/h to the picture being replaced (inches x 192 keeps text crisp). Keep text short:
// the card is shrunk onto the slide, so 4-6 lines of prompt is the readable maximum.
// The font is whatever the system has under "Pretendard" (install with extract_fonts.py) or a fallback.
const fs = require('fs'), path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const html = c => {
  const before = c.kind === 'before';
  const big = before ? 68 : 48;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;background:transparent}
.c{width:${c.w}px;height:${c.h}px;box-sizing:border-box;border-radius:28px;padding:110px 64px 56px;position:relative;
 font-family:'Pretendard Regular','Pretendard','Noto Sans CJK KR',sans-serif;background:${before ? '#EEEEEE' : '#3F4044'};
 display:flex;flex-direction:column;justify-content:center;gap:30px;overflow:hidden}
.lbl{position:absolute;top:50px;left:64px;font-family:'Pretendard Bold','Pretendard';font-weight:700;font-size:38px;color:${before ? '#8A8A8E' : '#FFCD4A'}}
.u{align-self:flex-end;max-width:${Math.round(c.w * 0.85)}px;background:#fff;color:#2B2B2E;border-radius:28px 28px 6px 28px;padding:30px 38px;font-size:${big}px;line-height:1.5;white-space:pre-wrap;box-shadow:0 4px 14px rgba(0,0,0,.08)}
.a{max-width:${Math.round(c.w * 0.75)}px;background:${before ? '#DADADC' : '#55565B'};color:${before ? '#55565B' : '#F2F2F2'};border-radius:28px 28px 28px 6px;padding:32px 44px;font-size:54px;line-height:1.5;white-space:pre-wrap}
.tag{align-self:flex-start;background:${before ? '#FF4E33' : '#75A05B'};color:#fff;font-family:'Pretendard Bold','Pretendard';font-weight:700;font-size:44px;border-radius:50px;padding:14px 36px}
</style></head><body><div class="c"><div class="lbl">${before ? 'BEFORE' : 'AFTER'} · ${esc(c.label || '프롬프트 예시')}</div>
<div class="u">${esc(c.user)}</div>${c.ai ? `<div class="a">${esc(c.ai)}</div>` : ''}${c.tag ? `<div class="tag">${esc(c.tag)}</div>` : ''}</div></body></html>`;
};

(async () => {
  const [specPath, out] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const c of spec) {
    c.w = c.w || 1648; c.h = c.h || 906;
    const p = await b.newPage({ viewport: { width: c.w, height: c.h } });
    await p.setContent(html(c)); await p.waitForTimeout(150);
    await p.locator('.c').screenshot({ path: path.join(out, c.file), omitBackground: true });
    await p.close(); console.log('wrote', c.file);
  }
  await b.close();
})();
