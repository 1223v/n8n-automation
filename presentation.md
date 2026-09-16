# 발표 구성안 — "잔말말고 n8n 오케스트레이션으로": Claude Code로 n8n 워크플로우를 안전하게 맡기는 법

## 발표 개요

| 항목 | 내용 |
|------|------|
| 청중 | 외부 밋업 / 컨퍼런스 (n8n 또는 AI 코딩 도구에 관심 있는 개발자, 사전 지식 수준 다양) |
| 시간 | 28분 기준 (아래 조절 슬롯으로 20~30분 대응) |
| 언어 | 한국어, 기술 용어만 영문 병기 |
| 데모 | 라이브 없이 녹화 영상 / 스크린샷으로 대체 |
| 근거 | 킷 내부 동작은 `readme.md` · `report.md` · `arch.md` 기술 기준. 설계 원칙은 `reference.md`(경량 도메인 특화 하네스, revfactory/harness) 기준. 외부 기술(Claude Code, n8n-mcp, context7, Playwright MCP, n8n API, harness)은 공식 문서로 확인한 내용만 사용 (부록 A) |

## 한 줄 메시지

> AI에게 n8n 워크플로우를 "그냥 고쳐줘"라고 맡기면 사고가 난다. 범용 멀티에이전트 프레임워크를 얹는 대신, **분석 → 요건 확인 → 리서치 → 계획 → 실행 → 보고** 절차를 n8n 도메인에 맞춘 작고 정밀한 하네스로 강제하면, 적게 말해도 제대로 고쳐진다.

## 목차와 시간 배분

| # | 섹션 | 시간 | 누적 | 핵심 메시지 |
|---|------|------|------|-------------|
| 0 | 타이틀 & 자기소개 | 1분 | 1분 | "잔말말고 n8n 오케스트레이션으로" |
| 1 | 문제: AI에게 워크플로우를 맡기면 생기는 사고 | 3분 | 4분 | 오해 · 구식 문법 · 무검증 · 무기록 · 셋업 삽질, 그리고 범용 프레임워크의 역설 |
| 2 | 해결 아이디어: 절차 강제 + 경량 도메인 특화 하네스 | 3분 | 7분 | 7단계 절차 + 확인 게이트 2회 + 설계 원칙 4가지 |
| 3 | 재료: Claude Code의 확장 지점 4가지 | 3분 | 10분 | 스킬 · 서브에이전트 · 커맨드 · MCP |
| 4 | 아키텍처 | 4분 | 14분 | 오케스트레이터 2 + 절차 스킬 1 + 에이전트 4 + 지식 스킬 7, 팀 패턴과 Progressive Disclosure로 읽기 |
| 5 | 동작 원리 7단계 딥다이브 | 4분 | 18분 | 단계별 담당 에이전트와 MCP 도구 매핑, 새로 만들기 전에 기존 워크플로우부터 보는 현황 감사와 크기별 질문 깊이 |
| 6 | 데모 (녹화/스크린샷) | 4분 | 22분 | "n8n 켜줘" / "Slack 노드 추가해줘" |
| 7 | 효과와 차별점 | 3분 | 25분 | 안전 · 최신성 · 재사용 + 다른 방식과의 비교 + 토큰 관점 + 이 킷의 특별한 점 5가지 |
| 8 | 첫 버전의 한계와 보완 | 2분 | 27분 | 제한 3개를 어떻게 보완했는지 + 남은 다음 단계 |
| 9 | 마무리 & Q&A | 1분 + 조절 | 28분~ | 설치 3단계, 예상 질문 |

시간 조절 슬롯 (고정 콘텐츠 28분 기준): 20분 버전은 섹션 2를 2분, 섹션 3을 2분, 섹션 5를 2분, 섹션 6을 3분, 섹션 7을 2분(슬라이드 29·30 생략)으로 줄이고 섹션 8(2분)을 마무리에 합침 → 20분. 30분 버전은 Q&A 2분 추가 → 30분.

발표의 서사 축: **"절차"**(무엇을 강제하는가, 섹션 2·5)와 **"경량 도메인 특화"**(왜 범용 프레임워크가 아닌가, 섹션 1·2·4·8)를 두 줄기로 놓고, 섹션 4에서 둘이 만나게 하며, 섹션 7에서 "그래서 무엇이 다른가"로 정리한다.

---

## 0. 타이틀 & 자기소개 (1분)

### 슬라이드
1. **타이틀** — "잔말말고 n8n 오케스트레이션으로" / 부제: Claude Code로 n8n 워크플로우를 안전하게 맡기는 법
2. **발표자** — 이름, 소속, n8n을 어디에 쓰고 있는지 한 줄

### 발표자 노트
- 제목이 도발적인 이유를 먼저 말한다. "써보니 적은 요청이라도 찰떡같이 조사하면서 제가 생각지 못한 요구까지 보완해줬다"는 실제 경험이 출발점이다.
- 오늘 가져갈 것 하나: "AI에게 절차를 강제하는 구조"가 왜 필요하고 어떻게 만드는지.

### 근거
- `readme.md` 결론 섹션

### 시각 자료
- 타이틀 한 장. 배경에 7단계 절차 화살표를 흐리게 깔아두면 이후 슬라이드와 연결됨.

---

## 1. 문제: AI에게 워크플로우를 맡기면 생기는 사고 (3분)

### 슬라이드
3. **"이렇게 고쳐줘" 한 마디의 결말** — 요구사항을 다르게 이해한 채 워크플로우가 바로 바뀜
4. **다섯 가지 반복되는 사고**
   - 요구사항 오해: 확인 없이 즉시 변경
   - 구식 문법: 기억·학습 데이터 기반이라 오래된 노드 파라미터 / `typeVersion` 사용
   - 무검증: UI에서 손으로 고치면 실수를 바로 알기 어려움
   - 무기록: 무엇을 왜 바꿨는지 남지 않음
   - 셋업 삽질: "n8n 설치 어떻게 했더라", "스크립트 어디 있지"가 매번 반복, 개인 PC 절대 경로 박힌 스크립트
5. **공통 원인** — 사람이 하던 "확인 → 조사 → 계획 → 검증"을 AI에게 맡길 때 절차가 통째로 생략됨
6. **그래서 범용 멀티에이전트 프레임워크를 얹어봤더니** — 함수 이름 하나 바꾸는 일에도 에이전트들이 회의를 열고 계획을 세움. 수십 개 범용 스킬이 매 세션 컨텍스트에 올라와 본 작업 집중도가 떨어짐. 범용 "보안 감시자"는 n8n 노드 `typeVersion` 같은 도메인 문제를 모름
7. **문제의 재정의** — 에이전트 팀이라는 개념이 문제가 아니라, **도메인을 이해하지 않은 채 범용 도구를 쌓는 접근**이 문제

### 발표자 노트
- 청중이 n8n을 몰라도 되게, "워크플로우 = 노드를 선으로 이은 자동화 흐름, JSON 한 덩어리"라고 한 문장으로 정의하고 시작.
- 다섯 사고는 모두 실제로 겪은 것들. 표의 "기존 방식" 열을 그대로 읽지 말고 하나당 한 문장짜리 상황극으로.
- 슬라이드 6은 발표자의 사용 경험으로만 말한다. reference.md에 있는 타 도구 벤치마크 수치(통과율, 토큰 오버헤드, 비용 배수)는 독립 출처를 확인하지 못했으므로 외부 발표 슬라이드에는 넣지 않는다. 특정 도구 이름을 지목해 비판하기보다 "범용 프레임워크 일반"의 구조적 한계로 말한다.
- 슬라이드 7에서 "그래서 절차를 강제하되, 그 절차를 n8n 도메인에 맞춰 작게 만든다"로 다음 섹션을 연다.

### 근거
- `readme.md` / `report.md` "기존 n8n 사용 대비 장점" 표의 "기존 방식" 열
- `reference.md` "이미 느끼고 있던 그 답답함", "기존 도구들의 문제: 과한 하네스의 역설", "공통 패턴: 오버엔지니어링의 함정"

### 시각 자료
- 슬라이드 4는 아이콘 5개 + 한 줄. 슬라이드 5는 사람의 절차(4단계)와 AI에게 맡겼을 때(1단계: "고쳐줘 → 바뀜")를 나란히.
- 슬라이드 6은 "작은 요청 → 큰 회의" 대비 그림 하나. 수치 없이.

---

## 2. 해결 아이디어: 절차 강제 + 경량 도메인 특화 하네스 (3분)

### 슬라이드
8. **7단계 절차** — 분석 → 요건 명확화 → 요건 확인 → 리서치 → 계획 수립 → 실행 → 보고 (readme "동작 원리"의 7단계 그대로). 1~2단계 안에 "새로 만들기 전에 이미 있는 걸 먼저 본다"와 "작업 크기에 따라 질문 깊이를 조절한다"가 들어 있음 (섹션 5에서 확대)
9. **사람이 개입하는 지점 2곳** — 3단계 요건 확인(이해한 내용을 요약해 매번 재확인), 5단계 계획 승인(실행 전 다시 한번). 둘 다 Claude Code의 `AskUserQuestion`으로 구현
10. **이 킷이 따른 설계 원칙 4가지** (reference.md의 경량 도메인 특화 하네스 원칙을 n8n에 적용)

| 원칙 | 킷에서의 모습 |
|------|---------------|
| 에이전트·스킬은 반드시 파일로 | `.claude/agents/*.md` 4개, `.claude/skills/*/SKILL.md` 10개. Git으로 버전 관리, 팀 공유, 롤백 가능 |
| CLAUDE.md에는 포인터만 | readme 설치 2단계의 "트리거 포인터" 4줄이 전부. 도메인 지식은 스킬 파일에 |
| 필요할 때만 로드 (Progressive Disclosure) | `description`(항상) → `SKILL.md` 본문(트리거 시) → 보조 문서(필요 시). 지식 스킬 7종이 이 3계층 |
| 하네스는 진화한다 | 첫 버전의 제한 3가지(트리거 미검증, 단일 리서처, OneDrive 의존)를 실사용 피드백으로 보완한 과정이 실례 (섹션 8). 커스터마이징 "도메인 에이전트 추가 시 자동 활용"도 진화 지점 |

11. **"40개 범용 스킬"이 아니라 "n8n 스킬 10개"** — 지금 이 도메인, 지금 이 작업에 필요한 것만

### 발표자 노트
- 핵심은 "AI가 똑똑해지길 기대"하는 게 아니라 "절차를 건너뛸 수 없게 만드는 것".
- 요건 확인은 필수 단계다. 모호한 부분만 질문하는 게 아니라, 이해한 내용을 요약해 반드시 재확인한 뒤에만 다음 단계로 간다.
- 설계 원칙 표는 왼쪽 열을 읽고 오른쪽 열은 "이 킷에서는 이렇게 생겼다"로 한 줄씩. Progressive Disclosure는 섹션 4에서 파일 트리로 다시 보여준다.
- reference.md의 원칙에는 "에이전트 팀(Agent Teams)을 기본 실행 모드로"도 있으나, 이 킷 문서는 서브에이전트 위임만 기술하고 에이전트 팀은 언급하지 않는다. 슬라이드에서는 4가지만 다루고, 에이전트 팀은 섹션 8 "다음 단계"에서 선택지로만 언급.
- 이 절차와 원칙을 Claude Code 위에 어떻게 올렸는지가 다음 섹션.

### 근거
- `readme.md` "동작 원리" 1~7단계, "설치 방법" 2단계(트리거 포인터), "알려진 제한사항", "커스터마이징"
- `reference.md` "4가지 핵심 설계 원칙", "Progressive Disclosure: 필요할 때만 로드", "결론"
- `arch.md` 스킬 폴더 구성(SKILL.md + 보조 문서)

### 시각 자료
- 슬라이드 8은 7단계 가로 화살표, 3·5단계 위에 "사람 확인" 배지.
- 슬라이드 10은 2열 표. 슬라이드 11은 "40 vs 10" 숫자 대비 한 장.

---

## 3. 재료: Claude Code의 확장 지점 4가지 (3분)

### 슬라이드
12. **스킬 (Skill) — "어떻게 하는가"** — `.claude/skills/<name>/SKILL.md`. frontmatter의 `description`을 보고 Claude가 상황에 맞게 자동 호출. 같은 폴더에 보조 문서(레퍼런스, 예제)를 번들할 수 있음. 트리거 문구를 `description`에 어떻게 쓰느냐가 스킬 품질을 가름
13. **서브에이전트 (Subagent) — "누가 하는가"** — `.claude/agents/<name>.md`. 독립된 컨텍스트 창에서 실행, `tools` 필드로 사용 도구 제한(읽기 전용 에이전트 가능), 백그라운드에서 병렬 실행 가능
14. **커스텀 커맨드** — `.claude/commands/<name>.md` → `/name`. 공식 문서상 커맨드는 스킬로 통합되었고 기존 파일은 계속 동작, 신규 작업은 스킬 권장
15. **MCP 서버 3종**
    - `n8n-mcp` (MIT): n8n 인스턴스 관리 도구 21종 + 노드 문서·검증 코어 도구 7종. 노드 2,755개 커버
    - `context7`: `resolve-library-id` → `query-docs`로 최신 공식 문서 조회
    - Playwright MCP: 브라우저 조작 (로컬 n8n UI 확인용)

### 발표자 노트
- 스킬 = "어떻게 하는가", 에이전트 = "누가 하는가"로 구분해 말하면 청중이 기억하기 쉽다(reference.md의 정리). 이 킷의 오케스트레이터와 도메인 지식 7종이 전부 스킬.
- Hooks(도구 실행 전후 셸 명령)도 Claude Code 확장 지점이지만 이 킷 문서에는 등장하지 않으므로 슬라이드에서는 다루지 않고 섹션 8 개선 방향에서 한 줄만.
- 서브에이전트 = "한 가지 일만 하는 별도 컨텍스트". 공식 문서상 `tools` 필드로 도구를 읽기 전용으로 묶을 수 있고, 백그라운드 병렬 실행도 가능. 킷 문서는 분석가를 "읽기 전용 분석", 리서처를 "백그라운드 병렬"로만 기술하므로, 이것이 그 구현 수단이라는 설명은 공식 문서 기반 추정임을 발표자는 인지 (킷의 에이전트 파일 frontmatter는 직접 확인하지 않음).
- 커맨드는 `/n8n-setup` 단축 진입점 하나. "커맨드→스킬 통합"은 섹션 8의 개선 방향에서 다시 언급.
- MCP 설정 위치는 공식 기준으로 말한다. user 범위는 `~/.claude.json`, 프로젝트 공유는 `.mcp.json`. (readme의 `~/.claude/mcp.json`은 공식 문서에 없는 경로, 부록 B)
- n8n-mcp 설정 예시는 슬라이드에 띄우되 API 키 자리는 `<본인 키>`로. "절대 저장소에 커밋하지 말 것"을 여기서 한 번 말한다.

### 근거
- Claude Code 공식: Skills, Subagents, Slash commands, MCP 문서 (부록 C)
- n8n-mcp README, Context7 README, Playwright MCP 문서 (부록 C)

### 시각 자료
- 슬라이드 12~14는 각각 실제 파일 경로 + 최소 frontmatter 예시 코드 블록. 슬라이드 15는 아래 설정 스니펫.

```json
{
  "mcpServers": {
    "n8n-mcp-tools": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "<본인의 n8n API 키로 교체>",
        "WEBHOOK_SECURITY_MODE": "moderate"
      }
    }
  }
}
```

---

## 4. 아키텍처 (4분)

### 슬라이드
16. **파일 트리** — `.claude/` 아래 agents 4 · commands 1 · skills 10 (arch.md 트리 + `n8n-workflow-reuse`, 스킬 폴더는 `SKILL.md` + 보조 문서 구성까지)
17. **계층별 역할**

| 계층 | 위치 | 역할 |
|------|------|------|
| 오케스트레이터 | `skills/n8n-workflow-manager`, `skills/n8n-env-setup` | 사용자 요청을 받아 절차를 주도. 워크플로우 작업 / 환경 셋업으로 진입점 분리 |
| 절차 스킬 | `skills/n8n-workflow-reuse` | 매니저의 1~2단계에서 호출. 작업 크기 분류, 기존 워크플로우 현황 감사, 재사용 제안, 조건부 딥 인터뷰 |
| 에이전트 | `agents/*` 4종 | 단계별로 위임받는 실행 주체 (분석 / 리서치 / 빌드 / 환경) |
| 커맨드 | `commands/n8n-setup.md` | `/n8n-setup` 단축 진입점 |
| 지식 스킬 | `skills/n8n-*` 7종 | 리서처·빌더가 참조하는 n8n 도메인 지식 |

18. **호출 흐름 다이어그램** — arch.md "호출 흐름" 그대로: 요청이 두 갈래(환경 / 워크플로우)로 나뉘고, 워크플로우 갈래는 7단계 각각 담당 에이전트로 이어짐
19. **팀 패턴으로 다시 읽기** — 같은 흐름을 revfactory/harness의 6가지 팀 아키텍처 패턴 언어로

| 킷의 구조 | 해당 패턴 | 설명 |
|-----------|-----------|------|
| 요청 → 환경 셋업 / 워크플로우 관리자 분기 | 전문가 풀 (Router → A or B) | 요청 유형에 따라 진입점 선택 |
| 분석 → 리서치 → 계획 → 실행 → 보고 | 파이프라인 (A → B → C → D) | 순차 워크플로우, 단계 사이에 사람 확인 게이트 |
| 실행 → validate → (에러 시) autofix → 재검증 | 생성-검증 (생성 → 검증 → 재시도) | 빌더가 만든 변경을 자동 검증·반복 |
| 출처별 리서처 병렬 조사 → 통합 | 팬아웃/팬인 (A ⊢ {B, C, D} ⊣ E) | 첫 버전은 리서처 1명이 순차 조사였고, 보완 후 출처별 병렬 조사 후 통합 (섹션 8) |

20. **Progressive Disclosure 3계층을 파일 트리에 대응** — `description`(항상 로드, 트리거 판단용) → `SKILL.md` 본문(트리거 시) → `README.md` · `ERROR_CATALOG.md` · `EXAMPLES.md` 같은 보조 문서(필요 시). 지식 스킬 7종이 모두 이 구조
21. **지식 스킬 7종 한눈에** — MCP 도구 사용법 / 노드 파라미터 설정 / 검증 에러 해석 / Code 노드 JS / Code 노드 Python / 표현식 문법 / 워크플로우 패턴 5종(webhook, HTTP API, DB, 스케줄, AI Agent)

### 발표자 노트
- "오케스트레이터가 절차를 쥐고, 에이전트가 손발, 지식 스킬이 참고서"라는 3층 구조로 설명.
- 슬라이드 19가 이 발표의 두 줄기("절차"와 "경량 도메인 특화")가 만나는 지점. 킷은 패턴 네 개(전문가 풀 + 파이프라인 + 생성-검증 + 팬아웃/팬인)를 조합한 작은 하네스라고 정리한다. 패턴 이름은 harness README에 있는 6가지 중에서 가져온 것이며, 킷 문서가 이 용어를 쓰는 것은 아니므로 "이렇게 읽을 수 있다"로 말한다.
- 슬라이드 20에서 "40개 스킬을 항상 로드하는 게 아니라, 트리거될 때만 본문을 읽는다"를 arch.md의 실제 파일명으로 보여준다. 검증 스킬에는 에러 카탈로그와 오탐 목록, 표현식 스킬에는 예제집과 흔한 실수 목록. "팀 노하우가 파일로 쌓인다"는 섹션 7의 근거이기도 하다.
- 산출물은 프로젝트 루트 `_workspace_n8n/`에 남는다. 감사 추적의 근거.

### 근거
- `arch.md` 전체 (트리, 계층별 역할, 호출 흐름)
- `reference.md` "6가지 팀 아키텍처 패턴", "Progressive Disclosure"
- revfactory/harness README: 6 패턴 명칭 확인 (부록 A)

### 시각 자료
- 슬라이드 16은 코드 블록 트리보다 폴더 아이콘 도식으로 재구성 권장. 슬라이드 18은 arch.md 흐름도를 그대로 그림으로.
- 슬라이드 19는 슬라이드 18의 흐름도 위에 패턴 이름을 색 테두리로 덧씌운 형태. 슬라이드 20은 3단 피라미드(항상 / 트리거 시 / 필요 시).

---

## 5. 동작 원리 7단계 딥다이브 (4분)

### 슬라이드
22. **단계 → 담당 → 도구 매핑 표**

| 단계 | 담당 | 하는 일 | 사용하는 도구 |
|------|------|---------|---------------|
| 1 분석 | `n8n-workflow-analyst` | 대상 워크플로우 JSON을 직접 읽어 노드/연결 구조 파악 (추측 금지). 신규 생성이나 큰 수정이면 인스턴스의 기존 워크플로우 목록에서 후보를 추려 구조를 비교하는 현황 감사까지 | `n8n_get_workflow`, `n8n_list_workflows` |
| 2 요건 명확화 | 오케스트레이터 + `n8n-workflow-reuse` | 작업 크기를 S / M / L로 분류. 재사용 후보가 있으면 Execute Sub-workflow 재사용 여부를 질문. L이면 기존 워크플로우 사실을 근거로 한 딥 인터뷰. S는 모호한 부분만 질문 | `AskUserQuestion` |
| 3 요건 확인 (필수) | 오케스트레이터 | 이해한 내용 요약 후 매번 재확인 | `AskUserQuestion` |
| 4 리서치 | `n8n-workflow-researcher` | context7 공식 문서 + WebSearch + 로컬 지식 스킬, 3개 출처 모두 조사 (백그라운드 병렬, 보완 후 출처별 팬아웃 → 통합) | `resolve-library-id`, `query-docs`, `WebSearch` |
| 5 계획 수립 | 오케스트레이터 | todo 목록을 파일로 남기고 실행 전 승인 | `AskUserQuestion` |
| 6 실행 | `n8n-workflow-builder` | n8n MCP 도구로만 변경 적용, 매 단계 후 자동 검증 + 오토픽스 | `n8n_update_partial_workflow` / `n8n_create_workflow` → `n8n_validate_workflow` → 오류 시 `n8n_autofix_workflow` |
| 7 보고 | 오케스트레이터 | 완료/실패 항목 정리, 피드백 요청, `_workspace_n8n/`에 기록 | 파일 쓰기 |

23. **1~2단계 확대: 새로 만들기 전에 이미 있는 걸 먼저 본다** — `n8n-workflow-reuse` 스킬
    - **작업 크기 분류**: 요청을 S(노드 1~2개 수정) / M(노드 3개 이상, 분기 추가, 새 외부 서비스) / L(신규 워크플로우, 트리거 변경, 결제·삭제·대량 발송 같은 부수효과)로 나눔. S에는 개입하지 않음
    - **현황 감사** (M · L): `n8n_list_workflows`로 목록을 받아 이름·태그로 후보를 최대 5개 추리고, 후보만 `n8n_get_workflow` structure 모드로 읽어 트리거·핵심 노드를 비교
    - **재사용 제안**: 비슷한 워크플로우가 있으면 자동 결정 대신 AskUserQuestion으로 A(기존을 Execute Sub-workflow로 호출) / B(복제 후 수정) / C(새로 만들기)를 근거와 함께 제시
    - **딥 인터뷰** (L만): 기존 워크플로우에서 확인한 사실을 선택지로 넣어 질문. 예: "에러 처리는 기존 워크플로우 3개처럼 실패 시 ops 채널로 보낼까요?" 라운드 3회·질문 3개 상한, 모호 항목 체크리스트(트리거, 입력, 성공 조건, 실패 처리, 부수효과, 자격증명)가 채워지면 종료
24. **validate → autofix 루프** — 변경 직후 검증 자동 실행, 에러 시 자동 복구 시도, 실패하면 원인과 결과를 명확히 보고
25. **왜 "MCP 도구로만" 변경하는가** — UI 수동 조작이나 JSON 직접 편집을 배제해 모든 변경이 API를 거치게 함. 도구 단위 로그가 남고, 필요하면 `DISABLED_TOOLS`로 쓰기 도구를 차단할 수도 있음

### 발표자 노트
- 표는 한 번에 다 읽지 말고 1 → 2 → 4 → 6만 짚는다. 특히 4단계 "3개 출처 모두"는 하나만 보고 끝내는 게 아니라 셋을 교차 확인한다는 뜻.
- 슬라이드 23은 "왜 작은 요청에는 안 묻는가"부터 말한다. 섹션 1에서 비판한 "작은 작업에 큰 회의"를 우리도 만들지 않으려고 S / M / L 분류를 맨 앞에 뒀다는 흐름. 그다음 "새로 만들기 전에 이미 있는 걸 먼저 본다"로 넘어가고, 재사용 제안이 자동 결정이 아니라 선택지라는 점을 강조한다. 이것이 reference.md의 "현황 감사 → 중복 검토" 원칙을 하네스 파일이 아니라 n8n 워크플로우 층위에 적용한 것이라고 한 문장으로 연결.
- 도구 이름은 n8n-mcp 공식 README에 실재하는 이름(부록 A). "단계별 어떤 도구를 쓰는지"는 readme의 기술과 n8n-mcp 도구 목록을 대응시킨 것이며, 킷 내부 프롬프트를 직접 읽고 확인한 것은 아님을 발표자는 인지.
- 슬라이드 23의 기능은 `spec-workflow-reuse.md` 명세 기준이다. 발표 전 체크리스트(섹션 8)에 구현·트리거 테스트 항목이 있으니, 미구현이면 이 슬라이드를 섹션 8 "다음 단계"로 옮긴다.
- 슬라이드 25에서 거버넌스 관점 한 마디: "어느 도구를 열고 닫을지 환경변수로 정할 수 있다".
- 섹션 4의 슬라이드 19(패턴)에서 이미 말한 파이프라인·생성-검증은 반복하지 않는다.

### 근거
- `readme.md` "동작 원리", `arch.md` "호출 흐름"
- `spec-workflow-reuse.md` (크기 분류, 현황 감사, 재사용 질문, 인터뷰 종료 조건)
- n8n 공식 Execute Sub-workflow / Execute Sub-workflow Trigger 노드 문서, n8n-mcp README(`n8n_list_workflows`, `n8n_get_workflow` 모드, `DISABLED_TOOLS`) (부록 A)

### 시각 자료
- 슬라이드 23은 요청 → S / M / L 분기 → (M·L) 현황 감사 → 후보 있음 → A / B / C 질문 → (L) 딥 인터뷰 → 요건 확인으로 이어지는 흐름도 한 장. 슬라이드 8의 7단계 화살표에서 1·2단계만 확대한 형태로 그리면 섹션 2와 연결된다.
- 슬라이드 24는 3상태 순환도(변경 → 검증 → 통과 / 오토픽스 → 재검증 / 실패 보고).

---

## 6. 데모 (녹화 / 스크린샷, 4분)

### 슬라이드
26. **시나리오 A: "n8n 켜줘"** (1분 30초)
27. **시나리오 B: "결제 알림 워크플로우에 Slack 알림 노드 추가해줘"** (2분 30초)

### 발표자 노트
- 영상은 음소거하고 발표자가 내레이션. 각 컷이 7단계 중 어디인지 화면 구석에 배지로 표시해두면 청중이 따라오기 쉽다.
- 시나리오 B에서 반드시 멈춰서 보여줄 컷: (1) 요건 재확인 질문 화면, (2) 계획 승인 질문 화면, (3) validate → autofix 로그, (4) `_workspace_n8n/` 산출물 폴더.
- "제가 말 안 한 요구까지 물어봤다"는 순간이 있으면 그 컷이 발표의 하이라이트.

### 데모 시나리오 상세

**시나리오 A — 환경 기동**

```
사용자: n8n 켜줘
→ n8n-env-setup 스킬이 현재 OS(Mac/Windows)를 감지 → 로컬 n8n 기동 → Playwright MCP 기동
```

캡처 컷: ① OS 감지 로그 ② 스크립트 경로 자동 탐지·캐싱 메시지 ③ n8n 기동 완료 (브라우저에서 `http://localhost:5678` 열린 화면) ④ Playwright MCP 기동 확인

**시나리오 B — 워크플로우 수정**

```
사용자: 결제 알림 워크플로우에 Slack 알림 노드 추가해줘
→ n8n-workflow-manager → 워크플로우 분석 → 요건 확인(AskUserQuestion) → 리서치 → 계획 승인 → 실행 → 검증
```

캡처 컷: ① 분석 결과 요약(기존 노드/연결) ② 요건 재확인 질문(예: 어떤 채널, 어떤 조건에서 알림) ③ 리서치 결과(Slack 노드 최신 파라미터 근거) ④ todo 계획과 승인 질문 ⑤ 변경 적용 + validate 통과 로그(또는 autofix 발동 장면) ⑥ n8n UI에서 Slack 노드가 붙은 워크플로우 ⑦ `_workspace_n8n/` 산출물 목록

이 요청은 S 등급(노드 1개 추가)이라 현황 감사·딥 인터뷰가 개입하지 않는 것이 정상 동작이다. 컷 ②에서 "작은 요청이라 질문이 짧다"를 한 마디 짚는다(슬라이드 23의 S / M / L 분류와 연결).

**시나리오 C (선택, 15초 스크린샷 1~2장) — 재사용 제안**

```
사용자: 고객 알림 워크플로우 새로 만들어줘
→ 현황 감사에서 기존 "customer-notify" 발견 → AskUserQuestion:
   A. 기존 customer-notify를 Execute Sub-workflow로 호출해 재사용 (권장)
   B. customer-notify를 복제해서 수정
   C. 새로 만든다
```

캡처 컷: ① `_workspace_n8n/<작업ID>/01b-audit.md`의 후보·판정·근거 ② A/B/C 선택지 질문 화면. 시간이 부족하면 슬라이드 23의 흐름도로 대체.

### 녹화 사전 준비 체크리스트
- [ ] 로컬 n8n 실행 가능 상태 (Mac 또는 Windows), 포트 5678 비어 있음
- [ ] n8n API 키 발급: n8n UI → **Settings → n8n API → Create an API key**. 키는 `~/.claude.json`(user) 또는 `.mcp.json`(project)의 `N8N_API_KEY`에만 넣고 화면 녹화 전 마스킹 확인
- [ ] `n8n-mcp`, `context7`, Playwright MCP 3종 등록 확인
- [ ] 더미 "결제 알림" 워크플로우 준비 (Webhook 트리거 → 조건 → 이메일 정도의 3노드), Slack 자격증명은 테스트용
- [ ] 킷 설치: `.claude/` 병합, `CLAUDE.md`에 트리거 포인터 추가
- [ ] (시나리오 C를 찍을 경우) 인스턴스에 `customer-notify` 같은 재사용 후보 워크플로우를 미리 만들어 두고, Execute Sub-workflow Trigger 노드 포함 여부를 확인
- [ ] 터미널 글꼴 크기 키우고, 녹화 해상도 1920×1080 이상
- [ ] 각 캡처 컷마다 정지 스크린샷을 별도로 저장 (영상 재생 실패 대비)
- [ ] API 키, 이메일, 사내 URL이 화면에 노출되지 않는지 최종 확인

### 근거
- `readme.md` "빠른 시작" (명령 문구 그대로). 예상 출력은 문서 기술 기준이며 이 구성안 작성 시점에 실제 기동으로 검증하지 않음
- n8n API 키 발급 경로: n8n 공식 문서 (부록 A)

---

## 7. 효과와 차별점 (3분)

### 슬라이드
28. **Before / After, 3묶음으로**

| 묶음 | Before | After |
|------|--------|-------|
| 안전 (오해 방지 · 변경 안전성 · 감사 추적) | 확인 없이 즉시 변경, 실수 발견 늦음, 기록 없음 | 변경 전 요약·재확인, 변경 직후 validate → autofix, 분석·요건·리서치·계획·결과가 `_workspace_n8n/`에 저장 |
| 최신성 (최신 문법 반영) | 기억·학습 데이터 의존 → 구식 파라미터/`typeVersion` | 매번 context7 공식 문서 + WebSearch로 최신 스펙 확인 후 적용 |
| 재사용 (환경 셋업 · 이식성 · 팀 지식) | 셋업 삽질 반복, 절대 경로 박힌 스크립트, 노하우가 개인에게만 | OS 자동 감지 + 경로 탐지·캐싱, 프로젝트 루트/환경변수 기준 경로, 지식 스킬 7종이 프로젝트 자산 |

29. **다른 방식과 무엇이 다른가** — 같은 "Claude로 n8n 워크플로우 고치기"를 네 가지 방식으로 놓고 비교

| 항목 | 순정 Claude Code + n8n-mcp | 범용 멀티에이전트 프레임워크 | revfactory/harness로 생성한 팀 | 이 킷 |
|------|---------------------------|------------------------------|-------------------------------|--------|
| 절차 강제 | 없음. 프롬프트에 따라 바로 변경 | 범용 계획·실행·검증 에이전트. n8n 절차는 아님 | 파이프라인 패턴으로 순차 구조는 생성 가능 | 7단계 고정. 요건 재확인과 계획 승인은 건너뛸 수 없는 필수 게이트 |
| n8n 도메인 지식 | n8n-mcp의 노드 문서 조회에 의존 | 없음. 일반론 리뷰 | 사용자가 준 도메인 문서를 스킬·references로 생성 | 지식 스킬 7종이 이미 들어 있음. 검증 에러 카탈로그·오탐 목록, 표현식 흔한 실수, 노드 파라미터 의존 관계, 패턴 5종 |
| 최신 스펙 확인 | 사용자가 시킬 때만 | 없음 | 생성 시점의 문서 기준 | 매 작업마다 context7 + WebSearch + 로컬 스킬 3출처 교차 확인 |
| 변경 안전성 | validate를 따로 불러야 함 | 범용 QA 에이전트 | 생성 범위 밖 | 변경 직후 validate → autofix → 실패 시 보고가 빌더에 내장. 변경은 MCP 도구로만 |
| 작은 작업 처리 | 가볍지만 확인 없음 | 모든 작업에 같은 오케스트레이션 오버헤드 | 패턴 선택은 생성 시 1회 고정 | S / M / L 분류로 노드 1~2개 수정에는 개입하지 않음 |
| 새로 만들기 전 기존 확인 | 없음 | 없음 | 하네스 파일 중복 검토 (워크플로우 층위는 아님) | 인스턴스 현황 감사 → Execute Sub-workflow 재사용 제안 → L만 딥 인터뷰 |
| 감사 추적 | 대화 기록뿐 | 도구별 상이 | 생성 범위 밖 | 분석·요건·리서치·계획·결과가 `_workspace_n8n/` 파일로 남음 |
| 로컬 환경 | 사용자가 직접 설치·기동 | 없음 | 생성 범위 밖 | `n8n-env-setup`이 Mac / Windows 감지 → n8n + Playwright MCP 기동, 경로 자동 탐지·캐싱 |
| 컨텍스트·토큰 부담 | 가볍지만 재작업이 생기면 그만큼 반복 | 모든 작업에 계획·검증 에이전트 대화가 붙음. 스킬 설명 상시 로드는 측정상 작은 비용(슬라이드 30) | 생성한 스킬 수만큼. 개입 조절은 직접 설계 | S 작업은 오케스트레이션 없음. 분석·리서치 출력은 서브에이전트 안에 격리. 설명 10개만 상시, 본문은 트리거 시 |

30. **토큰 관점: 어디서 아끼고, 어디서 더 쓰는가** — 절감률 수치가 아니라 구조로 말한다

| 구분 | 내용 | 근거 |
|------|------|------|
| 아끼는 곳 ① | **작은 작업에 오케스트레이션을 붙이지 않음.** S 등급(노드 1~2개)은 분류 → 기존 게이트만. 범용 프레임워크가 모든 작업에 계획·검증 대화를 여는 것과 대비 | spec S / M / L, reference.md |
| 아끼는 곳 ② | **서브에이전트 출력 격리.** 분석가가 읽은 워크플로우 JSON, 리서처가 긁은 문서 본문은 서브에이전트 컨텍스트에 남고 메인에는 요약만 돌아옴 | Claude Code Subagents 문서 "Output isolation" |
| 아끼는 곳 ③ | **재작업 감소.** 변경 직후 validate → autofix, 3출처로 최신 typeVersion 확인. "고쳐줘 → 깨짐 → 다시 고쳐줘" 왕복이 줄어드는 것이 총 토큰의 가장 큰 변수 | readme 동작 원리 (실측은 token-benchmark.md) |
| 아끼는 곳 ④ | **가볍게 읽기.** 현황 감사는 이름·태그로 후보 5개만 추려 `n8n_get_workflow` structure 모드로 읽음. full 모드 금지 | spec 7절, n8n-mcp README 모드 |
| 더 쓰는 곳 | 요건 재확인 질문, 계획 승인, 3출처 리서치, validate 호출. **첫 요청 한 번의 토큰은 순정보다 많다.** 비교는 "검증 통과까지의 총 토큰"으로 | token-benchmark.md 측정 원칙 1 |
| 측정해 본 것 | 로컬에 설치된 범용 프레임워크 스킬 37개의 `description` 합계 ≈ 5,900자(약 1,500토큰 추정). 본문 합계 ≈ 447,000자(약 112,000토큰 추정)지만 공식 문서상 본문은 호출 시에만 로드됨. **"스킬이 많아 상시 컨텍스트가 무겁다"는 토큰 수로는 작은 논점** | 2026-09-13 로컬 측정, Claude Code Skills 문서 |

31. **이 킷의 특별한 점 한 장** — 다섯 가지로 압축
    1. **n8n 전용으로 완성된 하네스**: 설치 즉시 동작. 도메인 지식 7종과 절차가 이미 들어 있어 "하네스를 설계하는 일"이 필요 없음
    2. **사람 게이트가 절차에 박혀 있음**: 요건 재확인 · 계획 승인 두 번은 옵션이 아니라 필수. 적게 말해도 알아서 물어봄
    3. **검증 루프 내장**: 변경 → validate → autofix → 보고가 빌더 안에 있어 "고쳐놓고 깨진" 상태가 사용자에게 오지 않음
    4. **작은 일엔 조용하고 큰 일엔 깊게**: S / M / L 분류와 기존 워크플로우 현황 감사로, 노드 하나 추가는 빠르게, 신규 설계는 재사용 제안과 딥 인터뷰로
    5. **환경까지 한 묶음**: 워크플로우 작업과 로컬 n8n 셋업이 같은 킷의 두 진입점. Mac / Windows 어디서든 "n8n 켜줘" 한 마디

### 발표자 노트
- 원본 표는 7행인데 발표에서는 3묶음으로 압축. 부록에 7행 원본을 두고 "자세한 건 자료에".
- 슬라이드 29 비교표는 "우리가 낫다"가 아니라 "각 방식이 커버하는 범위가 다르다"로 말한다. revfactory/harness는 팀 구조를 생성해 주는 메타 스킬이고 이 킷은 그 결과물에 해당하는 n8n 전용 완성본이므로 경쟁 관계가 아니다. "생성 범위 밖"은 harness의 산출물(에이전트 · 스킬 · references · CLAUDE.md 포인터)에 포함되지 않아 직접 설계해야 한다는 뜻이며, reference.md의 생성 예시 트리를 근거로 한다.
- 범용 프레임워크 열은 reference.md의 정리와 발표자 경험 기준이다. 타 도구 벤치마크 수치는 쓰지 않는다(부록 B 7번). 특정 제품명은 표에 넣지 않는다.
- 슬라이드 30은 "몇 % 절감"을 말하지 않는다. 실측 전이기 때문이며, 실측 후에도 S 과제에서는 하네스가 더 쓸 수 있다. 말할 것은 네 가지 구조적 절감 지점과 "첫 요청은 더 쓰고, 검증 통과까지는 덜 쓴다"는 비교 기준이다.
- 슬라이드 30 "측정해 본 것" 행은 reference.md의 "40개 스킬이 컨텍스트를 오염시킨다"는 주장을 토큰 수로는 뒷받침하기 어렵다는 결과다. 설명 합계 약 1,500토큰은 세션당 무시할 수준이고, 본문은 호출 시에만 로드된다. 그래서 발표에서는 "컨텍스트 오염"을 토큰 비용이 아니라 트리거 판단 혼선(관련 없는 스킬이 잘못 호출되는 문제)으로 말하고, 토큰 절감의 근거는 ①~④로 잡는다. 이 측정은 발표자 로컬 설치본 기준이며 제품명은 슬라이드에 넣지 않는다.
- 슬라이드 31은 청중이 가져갈 한 장. 다섯 개 중 4번(작은 일엔 조용하고 큰 일엔 깊게)이 섹션 1의 문제 제기에 대한 직접 답이므로 여기서 가장 힘을 준다.
- 토큰·비용 수치는 이 구성안 작성 시점에 실측값이 없다. `token-benchmark.md` 프로토콜로 A(하네스 없음) / B(하네스 있음) 실측을 마친 뒤 "과제별 총 토큰 + 수정 요청 수" 두 열짜리 표를 이 섹션에 한 장 추가한다. 실측 전에는 어떤 절감률도 말하지 않는다. S 등급 과제는 하네스가 오히려 토큰을 더 쓸 수 있으며, 그 경우 "작은 작업에는 개입을 최소화한다"의 근거로 쓴다.
- 한 문장 요약: "적게 요청해도 남은 요구사항을 알아서 물어보고 계획적으로 진행한다".

### 근거
- `readme.md` / `report.md` 장점 표, "동작 원리", "커스터마이징"
- `arch.md` 지식 스킬 보조 문서 목록(ERROR_CATALOG, FALSE_POSITIVES, COMMON_MISTAKES, DEPENDENCIES, 패턴 5종)
- `spec-workflow-reuse.md` (S / M / L, 현황 감사, 재사용 제안)
- `reference.md` "기존 도구들의 문제", "revfactory/harness" 생성 예시 트리, "Progressive Disclosure"
- harness README(6 패턴, 산출물 범위), n8n-mcp README(validate / autofix 도구, `n8n_get_workflow` 모드), Claude Code Skills 문서(description 기반 로드), Subagents 문서(출력 격리) (부록 A)
- `token-benchmark.md` "측정 1: 상시 메타데이터" (로컬 측정값)

### 시각 자료
- 슬라이드 28은 좌우 대비 표. Before는 회색, After는 강조색.
- 슬라이드 29는 4열 비교표. 셀은 한 줄 이내로 줄이고 "이 킷" 열만 강조색. 화면이 좁으면 행을 절차 · 지식 · 안전 · 크기별 처리 · 환경 5개로 줄인다.
- 슬라이드 30은 좌측 "아끼는 곳 4개 / 더 쓰는 곳 1개" 카드, 우측에 "첫 요청 토큰 ↑, 검증 통과까지 총 토큰 ↓(실측 예정)" 개념 그래프. 수치 축은 비워 둔다.
- 슬라이드 31은 아이콘 5개 + 굵은 제목 + 한 줄 설명.

---

## 8. 첫 버전의 한계와 보완 (2분)

### 슬라이드
32. **첫 버전에서 스스로 적어둔 한계 3가지** — 하네스 진화 관점에서 "어느 단계가 비어 있었는가"
    - 트리거 문구(should / should-not) 정식 테스트와 전체 파이프라인 드라이런 미수행 → **검증 단계**가 비어 있었음
    - 리서치 범위가 넓은 작업(대규모 신규 설계)은 리서처 1명이 순차 조사 → **팬아웃/팬인 패턴** 미적용
    - Windows 스크립트가 OneDrive 폴더 자동 탐지(`$env:OneDriveCommercial` / `$env:OneDrive`)에 의존 → 회사 OneDrive가 없는 PC에서는 수동 설정 필요
33. **보완: "실행 후 피드백으로 진화시킨다"의 실례**

| 첫 버전의 한계 | 보완 내용 | 보여줄 증거 |
|----------------|-----------|-------------|
| 트리거 미검증, 드라이런 미수행 | should / should-not 트리거 문구 테스트와 전체 파이프라인 드라이런을 수행하고, 결과를 각 스킬의 `description`에 반영 | 트리거 테스트 케이스 표(요청 문구 → 기대 스킬 → 실제 결과), 드라이런 산출물 `_workspace_n8n/` 스크린샷 |
| 단일 리서처 순차 조사 | 출처별(context7 공식 문서 / WebSearch / 로컬 지식 스킬) 리서처를 백그라운드 서브에이전트로 팬아웃하고, 통합 단계에서 교차 검증 | 병렬 리서처 에이전트 파일 목록, 같은 요청의 보완 전·후 리서치 소요 시간 또는 결과 비교 |
| OneDrive 자동 탐지 의존 | 탐지 후보 경로를 확장하고, 탐지 실패 시 `paths.env` 안내로 폴백 | Windows 스크립트 변경 diff 요약, OneDrive 없는 PC에서의 기동 캡처 |

34. **남은 다음 단계** — 한계가 아니라 확장 방향
    - 커맨드 → 스킬 통합: 공식 권장에 맞춰 `/n8n-setup`을 스킬로 이관
    - 롤백: n8n-mcp의 `n8n_workflow_versions`(버전 diff / rollback)를 실행 단계에 연결
    - 안전장치: Hooks(PreToolUse)로 `n8n_delete_workflow` 같은 파괴적 도구 호출 차단
    - 도메인 확장: 사내 API 등 도메인 전문 에이전트를 추가하면 리서처가 자동 활용 (코드 수정 불필요)
    - 진화 이력: 변경 이력을 `CLAUDE.md` 또는 별도 파일에 기록해 퇴행 방지

### 발표자 노트
- 이 섹션의 메시지는 "한계를 적어두고, 실사용 피드백으로 채웠다". reference.md의 "하네스는 진화하는 시스템" 원칙이 말이 아니라 실제로 돌아갔다는 증거로 쓴다.
- 슬라이드 33은 "보여줄 증거" 열이 핵심. 외부 청중은 "보완했다"는 말보다 캡처 한 장을 믿는다. 세 항목 모두 증거 캡처가 준비되지 않으면 그 항목은 슬라이드 34 "다음 단계"로 내리는 것이 안전하다.
- **발표 전 확인 필수**: 이 구성안 작성 시점의 `readme.md` / `report.md` "알려진 제한사항"은 세 항목을 아직 미보완으로 기술하고 있고, 킷 소스는 이 구성안 작성 환경에서 확인하지 못했다. 발표에서 보완 완료로 말하려면 ① readme·report의 제한사항 섹션을 보완 내역으로 갱신하고 ② 아래 체크리스트의 증거를 실제 킷에서 확보해야 한다.
- 발표 전 증거 체크리스트:
  - [ ] 트리거 테스트: should / should-not 문구 각 5개 이상, 기대 스킬과 실제 호출 스킬 일치 여부 표
  - [ ] 드라이런: 데모 B와 같은 요청을 끝까지 돌린 `_workspace_n8n/` 산출물(분석·요건·리서치·계획·결과 파일)
  - [ ] 병렬 리서처: `.claude/agents/` 에 출처별 리서처 파일이 있고, 오케스트레이터 `SKILL.md`가 팬아웃 → 통합을 기술
  - [ ] Windows: OneDrive 환경변수가 없는 PC에서 `n8n 켜줘`가 기동까지 가는 캡처
  - [ ] readme.md / report.md / arch.md가 현재 구조를 반영 (arch.md 트리에 병렬 리서처와 `n8n-workflow-reuse` 스킬 포함)
  - [ ] 재사용 감지(섹션 5 슬라이드 23): `.claude/skills/n8n-workflow-reuse/SKILL.md`가 존재하고, `spec-workflow-reuse.md` 9절의 트리거 테스트 6건(S 건너뜀 / L 인터뷰 / 재사용 후보 제시 / 환경 요청 미호출)이 통과한 표
  - [ ] 재사용 제안 캡처: 후보가 있는 요청에서 A / B / C 질문 화면과 `01b-audit.md`
- 에이전트 팀(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)은 reference.md가 기본 실행 모드로 권하지만 이 킷은 서브에이전트 위임으로 동작하므로, 질문이 나오면 "팬아웃 리서치를 더 키울 때 검토할 선택지"로만 답한다.

### 근거
- `readme.md` "알려진 제한사항"(첫 버전 기준), "커스터마이징"
- 보완 내용: 발표자 진술 기준 (이 구성안 작성 시점에 문서·소스로 확인되지 않음, 부록 B)
- `reference.md` "7단계 워크플로우"(검증·진화 단계), "하네스는 진화하는 시스템", "6가지 팀 아키텍처 패턴", "Hooks"
- Claude Code Subagents 문서(백그라운드 병렬), Slash commands 문서(스킬 통합), n8n-mcp README(`n8n_workflow_versions`, `n8n_delete_workflow`), harness README(에이전트 팀 환경변수) (부록 A)

### 시각 자료
- 슬라이드 32 → 33은 같은 3행 표를 "한계" 열만 있는 상태에서 "보완" 열이 채워지는 애니메이션. 슬라이드 33의 증거는 캡처 썸네일로 표 옆에.

---

## 9. 마무리 & Q&A (1분 + 조절)

### 슬라이드
35. **설치 3단계** — ① `.claude/` 병합 ② `CLAUDE.md`에 트리거 포인터 추가 ③ (선택) `paths.env` 설정, 없으면 첫 실행 시 자동 탐지
36. **한 줄 요약 + 연락처 / 자료 링크** — "좋은 하네스는 처음부터 크게 태어나지 않는다. 도메인을 아는 작은 에이전트 몇 개로 시작해, 실제 작업으로 검증하고, 부족한 부분을 채운다"

### 발표자 노트
- 설치는 압축 해제 수준이라는 점을 강조. 트리거 포인터 예시는 슬라이드에 그대로. 포인터 4줄이 CLAUDE.md에 들어가는 전부라는 점이 "CLAUDE.md에는 포인터만" 원칙의 실물.

```markdown
## n8n 워크플로우 하네스

**트리거:** n8n 워크플로우 관련 작업 요청 시 `n8n-workflow-manager` 스킬을 사용하라.
n8n 로컬 환경(설치/기동/포트 충돌 등) 관련 요청은 `n8n-env-setup` 스킬 또는 `/n8n-setup` 커맨드를 사용하라. (Mac/Windows 자동 감지)
```

### 근거
- `readme.md` "설치 방법"
- `reference.md` "결론: 경량화된 도메인 특화가 답이다"

---

## 예상 Q&A

| 질문 | 답변 요지 | 근거 |
|------|-----------|------|
| API 키가 유출될 위험은? | 키는 개인 설정 파일(`~/.claude.json` 또는 `.mcp.json`)에만 두고 저장소에 커밋하지 않는다. n8n에서 키에 만료 기간을 둘 수 있고, 엔터프라이즈는 스코프 제한도 가능 | readme 주의 문구, n8n 공식 인증 문서 |
| AI가 워크플로우를 잘못 바꾸면 되돌릴 수 있나? | 현재 킷은 validate → autofix → 실패 시 보고까지. n8n-mcp에는 `n8n_workflow_versions`(diff / rollback)가 있어 다음 단계로 연결 예정 | n8n-mcp README |
| 쓰기 도구를 아예 막고 분석만 시킬 수 있나? | 두 겹으로 가능. 서브에이전트는 `tools` 필드로 읽기 도구만 허용할 수 있고(공식 문서 기준, 킷의 분석가 파일 설정은 미확인), n8n-mcp 쪽은 `DISABLED_TOOLS`로 update / autofix 등 차단 | Claude Code Subagents 문서, n8n-mcp README |
| 커맨드 대신 왜 스킬을 쓰나? | 공식 문서상 커맨드는 스킬로 통합됐고 신규 작업은 스킬 권장. 이 킷도 `/n8n-setup` 하나만 커맨드이고 나머지는 스킬 | Claude Code Slash commands 문서 |
| n8n 클라우드에서도 되나? | 킷 문서는 로컬 n8n(Mac/Windows) 기준으로 기술. n8n-mcp 자체는 `N8N_API_URL`로 원격 인스턴스도 가리킬 수 있으나, 이 킷에서 검증된 범위는 로컬 | readme 사전 요구사항, n8n-mcp README |
| 리서치가 매번 돌면 느리지 않나? | 리서처는 백그라운드 서브에이전트로 실행. 첫 버전은 리서처 1명이 순차 조사라 대규모 설계에서 느렸고, 보완 후 출처별 리서처를 팬아웃해 병렬 조사 후 통합 | 섹션 8 보완 내역, Subagents 문서 |
| 토큰이 얼마나 줄었나? | 실측 진행 중이라 절감률은 말하지 않는다. 구조적으로는 작은 작업에 오케스트레이션을 붙이지 않고, 분석·리서치 출력을 서브에이전트에 격리하며, validate → autofix로 재작업 왕복을 줄인다. 첫 요청 한 번은 순정보다 더 쓰고, 검증 통과까지의 총 토큰으로 비교해야 한다. 참고로 스킬 설명 상시 로드는 측정상 세션당 약 1,500토큰 수준이라 절감의 주된 근거가 아니다 | 슬라이드 30, token-benchmark.md |
| 한계 3가지를 어떻게 검증했나? | 트리거 should / should-not 테스트 표, 드라이런 산출물, OneDrive 없는 PC 기동 캡처를 자료에 포함 (섹션 8 증거 체크리스트) | 섹션 8 |
| 비슷한 워크플로우가 있는지 어떻게 아나? 오탐은? | 이름·태그로 후보를 추리고 구조 모드로 트리거·핵심 노드를 비교해 "재사용 가능 / 참고만 / 무관"으로 판정. 판정은 LLM이 하므로 오탐이 있을 수 있어 자동 결정하지 않고 A / B / C 선택지로만 제시하며, 근거를 노드 타입으로 적는다 | spec-workflow-reuse.md 6절, n8n-mcp README |
| 딥 인터뷰 때문에 모든 요청이 느려지지 않나? | 작업 크기 S / M / L 분류로 노드 1~2개 수정 같은 S 등급은 개입하지 않는다. L만 인터뷰하고, 라운드 3회·질문 3개 상한과 종료 조건이 있다 | spec-workflow-reuse.md 5절 |
| 재사용하려는 워크플로우에 호출 트리거가 없으면? | Execute Sub-workflow로 호출하려면 대상에 Execute Sub-workflow Trigger 노드가 있어야 한다. 판정 시 확인하고 없으면 "Trigger 노드 추가"를 계획에 포함해 사용자에게 알린다 | n8n 공식 Sub-workflows 문서, spec-workflow-reuse.md 10절 |
| 실제 요청 예시를 더 보여달라 | 데모 B 외에 "webhook 받아서 DB 적재" 같은 패턴은 `n8n-workflow-patterns` 스킬에 5종 패턴 문서가 있음 | arch.md |
| 기존 멀티에이전트 프레임워크를 쓰면 되지 않나? | 범용 프레임워크는 스킬 수십 개가 매 세션 로드되고 n8n 도메인 지식이 없다. 이 킷은 n8n에 필요한 스킬 10개·에이전트 4개만 두고 트리거될 때만 본문을 로드한다. 작은 작업에 큰 오케스트레이션이 붙지 않는다 | reference.md 설계 원칙, arch.md |
| revfactory/harness로 "n8n 팀 구성해줘" 하면 같은 게 나오지 않나? | harness는 에이전트·스킬·references·CLAUDE.md 포인터를 생성해 주는 메타 스킬이다. 그 위에 n8n-mcp 검증 루프, 3출처 리서치, S / M / L 분류와 현황 감사, Mac / Windows 환경 셋업을 얹어 실사용으로 다듬은 결과물이 이 킷이다. 생성 도구와 완성본의 관계이지 경쟁이 아니다 | reference.md 생성 예시, harness README, 섹션 7 비교표 |
| 이 구조를 다른 도메인에 옮기려면? | 원칙은 동일: 파일로 존재, CLAUDE.md는 포인터만, 필요할 때만 로드, 실행 후 진화. revfactory/harness는 도메인 설명 한 문장으로 이런 팀 구조를 생성해주는 메타 스킬이며 6가지 팀 패턴을 제공 | reference.md, harness README |
| 에이전트 팀(Agent Teams)은 안 쓰나? | 이 킷은 서브에이전트 위임으로 구성. 에이전트 팀은 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`로 켜는 실험 기능이며, 팬아웃 리서치를 확장할 때 검토할 선택지 | harness README, reference.md |

---

## 부록 A. 사실 확인 표 (공식 문서 기준)

| 항목 | 확인 내용 | 출처 |
|------|-----------|------|
| Claude Code 스킬 | `.claude/skills/<name>/SKILL.md`. frontmatter `name` / `description`. `description` 기반 자동 호출. 같은 폴더에 보조 파일·스크립트 번들 가능. 프로젝트 스킬은 저장소에 커밋해 팀 공유 | code.claude.com/docs/en/skills |
| Claude Code 서브에이전트 | `.claude/agents/<name>.md`. frontmatter `name` / `description` 필수, `tools` / `model` / `disallowedTools` 선택. 독립 컨텍스트 창, 백그라운드 병렬 실행 | code.claude.com/docs/en/sub-agents |
| Claude Code 커맨드 | `.claude/commands/<name>.md` → `/name`. 커맨드는 스킬로 통합, 기존 파일 계속 동작, 신규는 스킬 권장 | code.claude.com/docs/en/slash-commands |
| Claude Code MCP 설정 | user 범위 `~/.claude.json`, project 범위 `.mcp.json`. stdio 서버는 `type` / `command` / `args` / `env` | code.claude.com/docs/en/mcp |
| n8n-mcp | MIT. 노드 2,755개(core 832 + community 1,923). 관리 도구 21종(`n8n_list_workflows`, `n8n_get_workflow`, `n8n_create_workflow`, `n8n_update_partial_workflow`, `n8n_update_full_workflow`, `n8n_validate_workflow`, `n8n_autofix_workflow`, `n8n_test_workflow`, `n8n_workflow_versions` 등) + 코어 도구 7종(`validate_node`, `validate_workflow`, `search_nodes`, `get_node` 등). env: `N8N_API_URL`, `N8N_API_KEY` 필수, `WEBHOOK_SECURITY_MODE`(strict / moderate / permissive), `DISABLED_TOOLS` 선택 | github.com/czlonkowski/n8n-mcp (README, docs/CLAUDE_CODE_SETUP.md) |
| n8n API 키 | Settings → n8n API → Create an API key. 요청 헤더 `X-N8N-API-KEY` | docs.n8n.io/connect/n8n-api/authentication |
| Context7 MCP | 도구 `resolve-library-id`, `query-docs`. 설치 `npx ctx7 setup --claude` 또는 `claude mcp add context7 -- npx -y @upstash/context7-mcp@latest`. API 키는 선택(레이트 리밋 상향) | github.com/upstash/context7 |
| Playwright MCP | `claude mcp add playwright npx @playwright/mcp@latest`, 패키지 `@playwright/mcp` | playwright.dev/docs/getting-started-mcp |
| Claude Code 내장 도구 | `AskUserQuestion`(사용자에게 선택지 질문), `WebSearch`(웹 검색). 킷 문서가 요건 확인·계획 승인·리서치 단계에 명시한 도구이며, 이 세션의 Claude Code에서도 동일 이름으로 제공됨을 확인 | readme.md "동작 원리", Claude Code 세션 도구 목록 |
| revfactory/harness | Apache 2.0. README에 확인됨: 6가지 팀 아키텍처 패턴(Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation), 설치 `/plugin marketplace add revfactory/harness` → `/plugin install harness@harness-marketplace`, 에이전트 팀 활성화 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, "Progressive Disclosure for efficient context management" 문구, Phase 1~6 워크플로우(도메인 분석 → 팀 아키텍처 설계 → 에이전트 생성 → 스킬 생성 → 통합·오케스트레이션 → 검증·테스트) | github.com/revfactory/harness |
| n8n-mcp 추가 도구 | `n8n_delete_workflow`(워크플로우 영구 삭제)가 관리 도구 21종에 포함. Hooks 차단 예시의 근거. `n8n_list_workflows`는 필터·페이지네이션 지원, `n8n_get_workflow`는 full / details / structure / minimal 모드 제공 (재사용 감지의 근거) | github.com/czlonkowski/n8n-mcp README |
| n8n Sub-workflow | Execute Sub-workflow 노드(예전 이름 Execute Workflow)로 부모 워크플로우가 다른 워크플로우를 ID 등으로 호출. 호출받는 워크플로우에는 Execute Sub-workflow Trigger 노드("When executed by another node")가 필요. 공식 가이드가 모듈화 방식으로 권장 | docs.n8n.io Execute Sub-workflow, Execute Sub-workflow Trigger, Sub-workflows, Break workflows into smaller parts |

## 부록 B. 킷 문서와 공식 문서의 불일치

1. **MCP 설정 파일 경로** — readme / report는 `~/.claude/mcp.json`을 언급하나 공식 문서에 없는 경로. 슬라이드에서는 `~/.claude.json`(user) / `.mcp.json`(project)로 표기.
2. **커맨드 vs 스킬** — `.claude/commands/n8n-setup.md`는 정상 동작하지만 공식은 스킬 통합을 권장. "다음 단계"로 소개.
3. **`WEBHOOK_SECURITY_MODE`** — n8n-mcp README의 env 목록에는 있으나 Claude Code 설정 가이드 예시에는 없음. 선택값으로 표기.
4. **데모 예상 출력** — readme "빠른 시작"의 흐름 기술 기준. 이 구성안 작성 시점에 킷을 실제로 기동해 검증하지 않았으므로 녹화 시 실제 출력에 맞춰 슬라이드 문구를 조정.
5. **reference.md의 harness 워크플로우 단계 수** — reference.md는 Phase 0(현황 감사)~Phase 7(진화)의 8단계로 서술하나, harness README는 Phase 1~6만 명시. 슬라이드에서는 단계 번호를 쓰지 않고 "검증 단계", "진화" 같은 이름으로만 언급.
6. **Progressive Disclosure 3계층** — README는 "Progressive Disclosure" 문구만 있고 metadata / SKILL.md / references 3계층 서술은 reference.md의 정리. 슬라이드 20은 Claude Code 공식 스킬 문서(description 기반 트리거, 보조 파일 번들)와 arch.md 파일 구조로 뒷받침되므로 유지하되, 출처는 "reference.md 정리 + Claude Code 스킬 문서"로 표기.
7. **타 도구 벤치마크 수치** — reference.md의 통과율·토큰 오버헤드·비용 배수 표는 독립 출처를 확인하지 못함. 슬라이드·발표에서 인용하지 않음.
8. **에이전트 팀 기본 사용 원칙** — reference.md의 설계 원칙 2("에이전트 팀을 기본 실행 모드로")는 이 킷 문서에 대응하는 기술이 없어 슬라이드 10의 원칙 표에서 제외.
9. **한계 보완 여부** — 섹션 8은 발표자 진술에 따라 제한 3가지가 보완된 것으로 구성. 그러나 이 구성안 작성 시점의 `readme.md` / `report.md`는 세 항목을 미보완("아직 수행되지 않았습니다", "현재 단일 리서처", "OneDrive 자동 탐지에 의존")으로 기술하고, `arch.md` 트리에도 병렬 리서처가 없으며, 킷 소스는 작성 환경에 없어 확인하지 못함. 발표 전 문서 갱신과 섹션 8 증거 체크리스트 확보가 전제.
10. **재사용 감지·조건부 딥 인터뷰 기능** — 섹션 5 슬라이드 23과 매핑 표 1~2단계, 섹션 4의 절차 스킬 행, 스킬 수 10개 표기는 `spec-workflow-reuse.md` 설계 명세 기준이며 발표자 결정에 따라 킷의 기본 기능으로 서술. 킷 문서(readme / report / arch)에는 해당 기능이 없고, 유사도 판정 도구는 n8n-mcp에 없어 킷이 LLM 판단으로 구현해야 함. 발표 전 체크리스트의 구현·트리거 테스트 항목이 전제.
11. **다른 방식과의 비교표(슬라이드 29)** — 순정 Claude Code + n8n-mcp 열은 n8n-mcp README 도구 목록 기준, 범용 프레임워크 열은 reference.md의 정리와 발표자 경험 기준, harness 열은 README(6 패턴)와 reference.md의 생성 예시 트리 기준. 어느 열도 실측·벤치마크가 아니며 "범위가 다르다"는 서술로 한정. 특정 제품명은 슬라이드에 넣지 않음.
12. **상시 메타데이터 측정(슬라이드 30)** — 발표자 로컬에 설치된 범용 프레임워크 플러그인의 `skills/*/SKILL.md` 37개에서 frontmatter `description`(공식 문서상 목록 표시 상한 1,536자 적용)을 합산한 값. 토큰은 문자 수 ÷ 4의 추정치이며 한글 비율에 따라 실제와 다를 수 있음. 이 킷의 설명 10개는 실제 파일이 없어 명세의 설명 1개(191자)로만 가늠. 결론은 "설명 상시 로드 비용은 양쪽 모두 작다"이며, reference.md의 컨텍스트 오염 주장은 토큰이 아니라 트리거 판단 혼선으로 재해석해 발표.

## 부록 C. 출처 링크

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code Slash commands: https://code.claude.com/docs/en/slash-commands
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- n8n-mcp: https://github.com/czlonkowski/n8n-mcp
- n8n-mcp Claude Code 설정 가이드: https://github.com/czlonkowski/n8n-mcp/blob/main/docs/CLAUDE_CODE_SETUP.md
- n8n 공개 API 인증: https://docs.n8n.io/connect/n8n-api/authentication
- Context7: https://github.com/upstash/context7
- Playwright MCP: https://playwright.dev/docs/getting-started-mcp
- revfactory/harness: https://github.com/revfactory/harness
- n8n Execute Sub-workflow 노드: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow
- n8n Execute Sub-workflow Trigger 노드: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflowtrigger
- n8n Sub-workflows 가이드: https://docs.n8n.io/flow-logic/subworkflows/
- 킷 문서: `readme.md`, `report.md`, `arch.md` (이 폴더)
- 추가 기능 명세: `spec-workflow-reuse.md` (이 폴더)
- 설계 원칙 참고: `reference.md` (이 폴더, 경량 도메인 특화 하네스 글)
