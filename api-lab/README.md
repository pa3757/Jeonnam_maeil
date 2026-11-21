# 검색 OFF 비교 실험실 (api-lab)

ChatGPT API와 Claude API에 같은 프롬프트를 보내 **웹 검색 없이** 답하는 모습을 나란히 비교하는 실습 페이지입니다 (전남매일 AI 특강 실습 1-3, 3-1).

- `public/index.html` — 화면 (프리셋: 1-3 환각 유도·안전장치·실제 통계, 3-1 인물 브리핑)
- `api/claude.js` — Anthropic SDK, Messages API (도구 없음 = 검색 없음)
- `api/openai.js` — OpenAI SDK, Responses API (도구 없음 = 검색 없음)
- `api/models.js` — 모델 목록 (Claude 고정 목록, ChatGPT는 계정 조회 결과 + 기본 목록 + 직접 입력)

## Vercel 환경 변수 (필수)

| 이름 | 내용 |
| --- | --- |
| `ANTHROPIC_API_KEY` | Claude API 키 |
| `OPENAI_API_KEY` | OpenAI API 키 |
| `ACCESS_CODE` | 수업용 접속 코드 (링크를 아는 사람이 크레딧을 쓰지 못하게) |
| `OPENAI_MODEL` | (선택) ChatGPT 기본 모델 id |

키는 서버 함수에서만 읽고 브라우저로 보내지 않습니다.
