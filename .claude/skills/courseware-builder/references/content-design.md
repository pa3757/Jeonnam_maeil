# Designing the course content

## Split of media
- **PPTX** = concepts only: why, frameworks, principles, checklists, Before/After. Short
  text, one message per slide, read-aloud script in notes.
- **Notion shared** = everything a learner needs to redo the exercises alone: steps,
  copyable prompts, sample materials, checklists, homework.
- **Notion instructor** = how to run it live: timeline, talk points, prep, failure modes.
- **HTML viewer** = public, image-only copy of the deck for sharing.

## Session skeleton (50-min session, demo style)
Interleave instead of "all concepts, then all exercises": 1-2 concept slides → a
**practice transition slide** → the matching 1-3 exercises in Notion → back to the deck.
A session has 2-4 such switches, so each concept is practiced while it's fresh.
Transition slide = the session's PRACTICE list slide duplicated per switch: current
exercises highlighted (▶, accent color), finished ones ✓ and dimmed, upcoming dimmed.
Slides stay lean: no minutes/schedules or "총 200분 · 실습 20개" stat cards on slides, the
cover shows only the course title and the closing slide only "감사합니다"; timing lives
in the speaker notes and the instructor guide. If the user wants "as much practice as
possible", keep concept slides lean and give every topic in the syllabus at least one
exercise. Each exercise: one tool or a cross-check between tools, 1-2 prompts, a visible
"aha" moment (difference between Before/After, a caught error, a hallucination).

## Follow the user's constraints exactly
If the user excludes tools (e.g. "Genspark 안 씀, ChatGPT와 Claude만"), remove every
syllabus item tied to them and replace it with the closest capability of the allowed
tools; say what you substituted in the final report. Do this for implicit cases too
(a syllabus feature that only exists in an excluded product).

## Sample materials
- Write fictional sample data (press release, transcript, memo) and label it
  "실습용 가상 자료" both on the page and inside the text. Plant deliberate checkpoints
  (vague stats, unverifiable rankings, hedged quotes, idioms, numbers easily misheard)
  and list them on the instructor page so the demo has something to find.
- Anything that must be real (a law PDF, a recent press release, a photo, a public
  figure to research) is chosen by the instructor: give selection criteria instead of
  inventing it. Never state specific real-world facts (statistics, article numbers,
  report titles) you have not verified; if an exercise needs a "nonexistent" item to
  provoke hallucination, tell the instructor to verify it doesn't exist the day before.
- Personal data in samples: obviously fake (홍길동, 010-0000-0000).

## Pair every exercise with a real-material comparison
Fictional samples are "practice problems" with planted answers; real public material is
the "live" case where the answer is unknown. Every exercise page ends with a
**"실제 자료로 비교해 보기"** section that reruns the same prompt on real public material
and compares the two in a table. What makes a good real comparison:
- **A real "answer key" exists**: official 개정이유 / 신구법비교 for a law summary, an
  official bilingual text for translation, a published article for a draft, a photo
  whose caption states place and date, a court's already-anonymized ruling for
  de-identification, a published industry guideline for a policy draft.
- **Real data shows a failure the fictional one can't**: e.g. the same statistic ("4.8배")
  reported for different quarters and scopes → time-point errors; a real photo judged
  "AI-generated" → false positives; search OFF vs ON for a real person's career.
- **Direct links, not "go find it"**: put a clickable link to the actual article,
  law page, list page or portal in the shared page so learners can open it in class.
  Find them with web search; use only URLs that appear in search results, never
  constructed or remembered ones (exception: stable official URL patterns such as
  `https://www.law.go.kr/법령/<법령명>`). If you can't open the pages from your
  environment, say so on the instructor page and add "click every link the day before"
  to the prep checklist.
- Facts you learned from search snippets go on the **instructor** page as "사전 검색 기준,
  원문 확인 필요" with their source links; the shared page carries the links and the task,
  not the answers.
- Real material is public only: no embargoed or source material, even for comparison.
- Live time: demo one real comparison per session (★ on the instructor page, ~+4 min),
  shorten another exercise to pay for it, and leave the rest as homework. Add the ★ table
  and a one-sentence takeaway per session to the instructor guide.

## Claims about tools
Product features, menu names and plan limits change. Phrase as "수업 시점 기준",
put "전날 강사 계정에서 확인" on the instructor page, and give a fallback for each
feature-dependent exercise (text mode if voice fails, a pre-run backup for slow
deep-research or image generation).

## Speaker scripts
See pptx-workflow.md §5. Write them after slide content is final so they match the slide.
