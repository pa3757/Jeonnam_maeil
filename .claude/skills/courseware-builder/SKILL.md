---
name: courseware-builder
description: 슬라이드 레퍼런스(.pptx 템플릿)와 강의 내용(강의계획서·커리큘럼 PDF/문서)을 받아 강의 교안 세트를 만든다 — ① 템플릿 디자인을 유지한 개념 설명 PPTX(발표자 노트에 읽는 스크립트 포함), ② 노션 수업교안 공유용/강사용 DB 페이지(실습 프롬프트·시연 스크립트), ③ GitHub Pages로 배포할 공유용 HTML 슬라이드 뷰어(노트·다운로드 없음). 강의안, 교안, 수업 자료, 특강 자료, 워크숍 실습 자료, "이 템플릿으로 강의 PPT + 노션 실습 페이지 만들어줘", "강의계획서 보고 교안 만들어줘"처럼 강의·교육 자료를 PPT와 노션으로 함께 만들어 달라는 요청이면 파일 형식을 명시하지 않아도 이 스킬을 사용한다. 단순히 PPT 한 장만 고치거나 노션 페이지 하나만 쓰는 요청에는 쓰지 않는다.
---

# Courseware builder

Turns a slide template + a syllabus into a complete, demo-ready course kit:

| Output | Audience | What it contains |
| --- | --- | --- |
| Concept deck `.pptx` | instructor (presents it) | template design, one message per slide, notes = read-aloud script + run memo |
| Notion **shared** DB pages | learners | guide, every exercise with copyable prompts, sample materials, homework |
| Notion **instructor** DB pages | instructor | minute timeline, demo script per exercise, prep, troubleshooting, Q&A |
| HTML viewer (`docs/`) | anyone with the link | slide images only — no notes, no PPTX download |

The pieces reference each other (slide → exercise number → Notion page), so plan once and
build all of them from the same plan.

## Inputs to collect

Usually already attached; ask only for what's missing and can't be defaulted:
- **Slide reference** `.pptx` (the design to keep). Required.
- **Lecture content**: syllabus/curriculum (sessions, minutes, topics, audience). Required.
- **Constraints**: tools to use/exclude, delivery style (demo vs hands-on), "practice-heavy".
- **Notion destination**: page holding the shared/instructor databases. If the user named
  it, search for it; if the databases don't exist, create two inline databases under the
  named page with those titles.
- **Repo** for the HTML viewer (the current git repo by default).

## Workflow

Track these as tasks; each phase depends on the plan from phase 1.

### 1. Read and plan
1. Read the syllabus fully. Read the template (see `references/pptx-workflow.md` §1):
   extract fonts, thumbnails, `inspect_template.py`, one full-size render.
2. Write a plan in the scratchpad: per session → concept slides (each mapped to a template
   layout, `references/pptx-workflow.md` §2) and 4-6 exercises (title, tool(s), minutes,
   sample material needed). Apply `references/content-design.md`: exclusions, fictional
   vs. instructor-provided materials, practice-heavy pacing, and a **real-material
   comparison** for every exercise (search for real public sources now and keep their
   links for the Notion pages).
3. Fix the global numbering now: slide order, exercise ids (1-1 … 4-5), Notion 순서.
   Give the user a 3-4 line status (layouts found, deck size, exercise count) and continue;
   don't wait for approval unless an input is ambiguous.

### 2. Concept deck (PPTX)
Follow `references/pptx-workflow.md` §3-§5: `build_structure.py` → project fill script
using `scripts/pptx_fill.py` → icons/cards (`render_icons.js`, `render_cards.js`) →
validate → render every slide and fix overflow/overlap → speaker notes with
【발표 스크립트】 and 【진행 메모】. Commit the `.pptx` (e.g. `slides/<강의명>.pptx`).

### 3. Notion
Follow `references/notion-templates.md`: add columns to both DBs → create shared pages
(guide, exercises, homework) in batches of 5-6 synchronously → create instructor pages
with the relation to the matching shared page and links instead of duplicated prompts →
set both views sorted by 순서.

### 4. HTML viewer for GitHub Pages
```bash
python3 <skill>/scripts/build_viewer.py <deck>.pptx --out docs --title "<덱 제목>" \
  --subtitle "<강의명>" --titles titles.json --sections sections.json
```
`titles.json` = one short title per slide; `sections.json` = first slide number of each
session. The viewer has keyboard/swipe navigation, a table of contents (G) and fullscreen
(F), and deliberately no notes or download — speaker notes live only in the PPTX.
Check it in Playwright at desktop and 390px width (no horizontal scroll, buttons =
목차/전체 화면 only). Commit `docs/` and tell the user: Settings → Pages → branch, folder
**`/docs`** (choosing `/ (root)` would also publish the PPTX).

### 5. Report
Short summary per output with links/paths, what was substituted for excluded tools, what
the instructor must prepare (real materials you didn't invent), and caveats: tool features
to recheck the day before; if the repo is public, the PPTX in the repo is downloadable
from GitHub itself even though the Pages site doesn't serve it; cached old Pages versions
can take ~10 minutes to clear.

## Bundled files
- `scripts/extract_fonts.py` — embedded EOT fonts → installed TTF named as the slides reference them
- `scripts/inspect_template.py` — shape ids, positions, paragraph/run counts, tables, pictures
- `scripts/build_structure.py` — reorder/duplicate template slides into the planned sequence
- `scripts/pptx_fill.py` — `Deck` helper: style-preserving text, tables, picture swaps, notes
- `scripts/render_icons.js` — Lucide icons / icon tiles to PNG
- `scripts/render_cards.js` — Before/After prompt cards to PNG
- `scripts/build_viewer.py` + `assets/viewer_template.html` — public slide viewer
- `references/pptx-workflow.md`, `references/notion-templates.md`, `references/content-design.md`
