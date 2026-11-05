# Designing the course content

## Split of media
- **PPTX** = concepts only: why, frameworks, principles, checklists, Before/After. Short
  text, one message per slide, read-aloud script in notes.
- **Notion shared** = everything a learner needs to redo the exercises alone: steps,
  copyable prompts, sample materials, checklists, homework.
- **Notion instructor** = how to run it live: timeline, talk points, prep, failure modes.
- **HTML viewer** = public, image-only copy of the deck for sharing.

## Session skeleton (50-min session, demo style)
~10 min concepts (4-6 slides) → 1 "PRACTICE" slide listing the session's exercises →
~35 min exercises (5 × 6-8 min) → ~5 min Q&A. If the user wants "as much practice as
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

## Claims about tools
Product features, menu names and plan limits change. Phrase as "수업 시점 기준",
put "전날 강사 계정에서 확인" on the instructor page, and give a fallback for each
feature-dependent exercise (text mode if voice fails, a pre-run backup for slow
deep-research or image generation).

## Speaker scripts
See pptx-workflow.md §5. Write them after slide content is final so they match the slide.
