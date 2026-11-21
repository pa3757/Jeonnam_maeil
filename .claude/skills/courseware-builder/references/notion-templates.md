# Notion: shared (수강생용) and instructor (강사용) lesson databases

The user usually creates two empty inline databases under a course page (e.g.
"수업교안(공유용)" and "수업교안(강사용)"). Find them with notion-search, fetch each to get
the `collection://` data source id, then add columns. Load the Notion tools via ToolSearch
(`notion-search, notion-fetch, notion-create-pages, notion-update-data-source,
notion-update-view, notion-update-page`) and read `notion://docs/notion-flavored-markdown-spec`
once before writing content.

## 1. Columns

Shared DB:
```
ADD COLUMN "순서" NUMBER; ADD COLUMN "교시" SELECT('공통':gray, '1교시 · <주제>':red, '2교시 · <주제>':yellow, '3교시 · <주제>':green, '4교시 · <주제>':blue);
ADD COLUMN "유형" SELECT('안내':gray, '실습':orange, '사후 과제':purple);
ADD COLUMN "사용 도구" MULTI_SELECT('<도구1>':green, '<도구2>':orange);
ADD COLUMN "소요 시간(분)" NUMBER; ADD COLUMN "한 줄 요약" RICH_TEXT
```
Instructor DB: same 교시/사용 도구/순서/소요 시간, 유형 = '운영'/'실습'/'사후 과제', plus
`"관련 슬라이드" RICH_TEXT; "사전 준비" RICH_TEXT; "리허설 완료" CHECKBOX; "돌아갈 슬라이드" NUMBER (deck slide to resume after the exercise);
"공유용 페이지" RELATION('<shared data source UUID>')`.

Gotcha: RELATION takes the bare UUID, not the `collection://` URL.
Adapt the session list to the course (2 sessions, 6 modules ...).

Afterwards update each DB's default view: `SORT BY "순서" ASC; SHOW <columns>; HIDE "순서"`.

## 2. Pages

Numbering via 순서: 0 = 안내/운영 guide, 11-15 = session 1 exercises, 21-25 ..., 99 = 사후 과제.
Titles: shared "실습 1-1. <제목>", instructor "[강사] 실습 1-1. <제목>".

Create pages in batches of ~5-6 per `notion-create-pages` call with `allow_async: false`
so you get URLs back (you need shared URLs for the instructor relation and links).
Mentions must point at real URLs: `<mention url="https://www.notion.so/<32hex id>">label</mention>`.
A mention whose url is a page title fails the whole batch.

Match the user's existing lesson-page style if they have one (fetch a recent lesson page
under the same parent). The defaults below follow a style that worked: H1/H2 numbered
sections, comparison tables, prompts in ```bash blocks preceded by
`> 📎 사용 텍스트 (… 그대로 복사)`, tips/warnings in ```py blocks or callouts.

### Shared page "00. 수업 안내 · 공통 실습 자료"
1. 과정 한눈에: callout (course title, duration, tools, "시연 중심, 프롬프트 복사해 따라 하기") + session table
2. 준비 사항 (accounts, free vs paid, files to bring)
3. 기본 루프 (지시 → 생성 → 검증 → 기록)
4. 공통 실습 자료: callout "가상 자료" warning, then each fictional sample text in a ```bash block

### Shared exercise page
```
# 1. 실습의 핵심          callout (one-sentence point) + optional 기존 방식 vs AI 방식 table
## 2. 준비물
## 3. 진행 순서           numbered steps
## 4. 프롬프트            ### 프롬프트 ① … ② … (each in ```bash, with role / context / format / constraints)
## 5. 확인 포인트          - [ ] checklist (+ result-recording table if the exercise compares outputs)
## 6. 실제 자료로 비교해 보기  callout (why compare) + "실제 자료 바로가기" links + method
                           + 비교 table (가상 vs 실제) + 관전 포인트 (see content-design.md)
```
Add a "실제 자료 비교 실습 안내" section to the shared guide: table of material type →
direct link → exercises that use it.

### Shared "99. 사후 실습 과제 · 점검 체크리스트"
Core principles callout, 2-3 homework tasks (target, steps referencing exercise numbers,
deliverable), field checklists.

### Instructor "00. 강의 운영 가이드"
Overview callout linking the shared guide; minute-by-minute timeline table per session
(concept slides → 전환 N → return slide, with exercise minutes); "전날 세팅 체크리스트" (accounts/features,
files to prepare, equipment); 운영 원칙; 예상 질문 → 답변 방향 table; which exercises to
cut first if late.

### Instructor exercise page
Properties: 관련 슬라이드, 사전 준비, 공유용 페이지 (relation to the shared page URL).
```
# 1. 시연 흐름 (N분)      table | 시간 | 행동 | 멘트 포인트 |
> 📋 프롬프트는 <mention url=shared page>공유용 실습 X-Y</mention>에서 복사합니다.
## 2. 예상 결과 / 관전 포인트 (what the sample data is designed to surface)
## 3. 트러블슈팅          table | 상황 | 대응 | + 축약 버전 (N분)
## 4. 예상 질문
## 5. (★) 실제 자료 비교    prep (what to download), candidate material with links and
                           "사전 검색 기준, 원문 확인 필요" facts, +N min, 멘트, which exercise to shorten
```
Keep prompts only on the shared page (single source of truth); the instructor page links to it.

**Prompts must be paste-ready.** The instructor and learners copy a block and press enter,
so never leave a placeholder for something the course already fixes: embed the sample
material (press release, transcript, memo) and the claim to verify directly inside the
prompt block, labeled "실습용 가상 자료". Keep placeholders only for what truly varies
per person or comes from an earlier step (their own article, the previous answer, a
research result), and write them as `[← 앞 단계 결과 붙여넣기]` so it's obvious.

### Instructor "99. 마무리 · 사후 과제 해설"
Wrap-up flow, rubric table (good result vs common mistakes per task), post-class checklist.
