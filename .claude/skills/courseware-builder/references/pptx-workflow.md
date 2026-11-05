# PPTX: template-derived concept deck

The goal is a deck that looks like the user's reference template (same frame, fonts,
colors, decorations) with new content. Edit the template rather than recreating it:
the reference decks this skill is for usually carry their design in pictures (window
frames, cards, shadows) and embedded fonts that a from-scratch generator cannot match.

Load the pptx skill first; its `scripts/` (add_slide.py, clean.py, thumbnail.py,
slide_text.py, office/validate.py, office/soffice.py) are used below. `$P` = pptx skill
dir, `$K` = this skill dir, work in the scratchpad.

## 1. Understand the template

```bash
cp <template>.pptx ref.pptx
python3 $K/scripts/extract_fonts.py ref.pptx          # embedded fonts -> ~/.fonts (QA accuracy)
python3 $P/scripts/thumbnail.py ref.pptx refthumb      # layout grid; view the jpg(s)
python3 $K/scripts/inspect_template.py ref.pptx > shapes.txt
```

- Render the reference once (soffice.py -> pdftoppm) and look at 3-4 slides at full size:
  note the palette (sample pixels for icon colors), which pictures are decoration vs.
  content (stock photos, chart images, icons).
- From `shapes.txt` build a layout map: for each template slide, which shape id is the
  title, the body, card 1..n titles/descriptions, which picture ids are icons/photos,
  and how many paragraphs/runs each box has. Multi-run paragraphs are reusable highlight
  styles (e.g. run 2 colored).
- Plain text boxes in these templates are pre-broken into one paragraph per line. Write
  content with similar line counts and lengths as the placeholder text. A good rule:
  stay within ~110% of the placeholder's character count per line.

## 2. Choose a layout per slide

Map each planned slide to a template slide. Typical mapping:

| Content | Template slide type |
| --- | --- |
| Cover / closing "감사합니다" | cover |
| Agenda, and per-session "PRACTICE" list of exercises | index / TOC |
| Session divider (01, 02 ...) | section title |
| 3 concepts + one-line takeaway | three-column cards + summary bar |
| 4-step process | steps / chevrons (swap icons per topic) |
| Principle + two checklists | objective / goal infographic |
| Tool A vs Tool B | versus |
| Schedule, 6-row framework | table (+ stat cards) |
| 4 items with visuals | grid with photos (replace photos with icon tiles) |
| Before/After prompt | transformation (replace photos with prompt cards) |
| 4 big numbers / rules | big-number cards |
| Wrap-up paragraph | long text |

Vary layouts; don't put consecutive slides on the same frame unless they are a series.
Skip template slides whose pictures encode fixed data you can't change (e.g. a line graph
whose dots are images).

## 3. Build

```bash
python3 $K/scripts/build_structure.py ref.pptx struct.pptx --order 1,2,8,9,14,3,6,... --pptx-skill $P
```

Then write a project fill script using `pptx_fill.Deck` (see the docstring). Keep content
in a separate file (one function call per slide) so text edits don't touch logic. Per
slide also call `d.notes(slide, script=..., memo=...)`.

Pictures:
- Icons: `render_icons.js` (Lucide). White icons on colored circles; colored icons on light
  chevrons; uniform `size=` when swapping so mixed original sizes don't show.
- Stock photos that don't fit the topic: replace with icon tiles (`tile` mode, sized to the
  photo's pixel size) or `render_cards.js` prompt cards. Never leave unrelated stock photos.
- Charts drawn as images (donuts, dot graphs): delete them (and widen the table) rather than
  leaving fake numbers.

## 4. QA (required, expect 1-2 fix rounds)

```bash
python3 $P/scripts/office/validate.py deck.pptx --original ref.pptx
python3 $P/scripts/office/soffice.py --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 50 deck.pdf j        # then tile 6 per image with PIL and view all
```

Issues seen in practice, check each:
- Text wrapping onto an extra line and colliding with the box below (card descriptions,
  subtitles, section-divider body, stat descriptions). Fix by shortening, not shrinking.
- Table rows whose first cell has 1 run instead of 2 lose their text if you write two
  texts; `_set_para` merges the tail into the last run to avoid this, but re-check.
- Header URL-bar labels wrapping (keep them short, ASCII).
- Prompt-card images too small to read once scaled onto the slide: big fonts (48-68px at
  1648px width) and few lines.
- Grep for leftover placeholder text: `slide_text.py deck.pptx | grep -E "키워드|입력해|presentation_"`.

Name scratch Python files so they don't shadow stdlib modules (a file called
`struct.py` breaks lxml/pptx imports).

## 5. Speaker notes = read-aloud script

Every slide gets two blocks (`Deck.notes` formats them):

- **【발표 스크립트】** what the instructor literally says. Spoken Korean, 합니다체, short
  sentences, one idea per line. Concept slides ~150-400 chars (1-2 min); dividers and
  practice-list slides 2-4 sentences ending with a hand-off ("노션에서 '실습 1-1'을 열어 주세요").
  Explain the "why", give the concrete example, end with the bridge to the next slide/exercise.
- **【진행 메모】** timing ([3분]), what to emphasize, which exercise it sets up, cautions
  (feature names change; check the day before).
