# n8n Orchestration Kit — 아키텍처 (파일 구조)

`readme.md`의 "포함된 것" 섹션을 파일 단위까지 펼친 구조도입니다.
각 스킬 폴더는 `SKILL.md`(진입점) + 보조 레퍼런스 문서로 구성됩니다.

## 전체 구조

```
n8n-orchestration-kit/
├── README.md                              킷 소개 / 설치 / 사용법
└── .claude/
    ├── agents/
    │   ├── n8n-workflow-analyst.md        워크플로우 읽기 전용 분석
    │   ├── n8n-workflow-researcher.md     context7 + WebSearch + 로컬 스킬 기반 리서치
    │   ├── n8n-workflow-builder.md        n8n MCP로 실제 변경 실행 + 검증
    │   └── n8n-env-setup.md               로컬 환경 설치 / 기동 / 트러블슈팅
    ├── commands/
    │   └── n8n-setup.md                   /n8n-setup 슬래시 커맨드
    └── skills/
        ├── n8n-workflow-manager/          메인 오케스트레이터 (핵심)
        │   └── SKILL.md                   분석 → 요건 확인 → 리서치 → 계획 → 실행 → 보고 절차
        ├── n8n-env-setup/                 환경 셋업 오케스트레이터 + Mac/Windows 스크립트 번들
        │   ├── SKILL.md                   OS 감지, 스크립트 경로 탐지·캐싱, 기동 절차
        │   └── paths.env.example          로컬 경로 설정 템플릿 (복사해서 paths.env 생성)
        ├── n8n-mcp-tools-expert/          n8n MCP 도구 사용법
        │   ├── SKILL.md
        │   ├── README.md
        │   ├── SEARCH_GUIDE.md            노드/워크플로우 검색 도구 사용 가이드
        │   ├── WORKFLOW_GUIDE.md          워크플로우 생성·수정 도구 사용 가이드
        │   └── VALIDATION_GUIDE.md        validate / autofix 도구 사용 가이드
        ├── n8n-node-configuration/        노드별 파라미터 설정
        │   ├── SKILL.md
        │   ├── README.md
        │   ├── DEPENDENCIES.md            파라미터 간 의존 관계 (A를 켜면 B가 필요 등)
        │   └── OPERATION_PATTERNS.md      노드 operation별 설정 패턴
        ├── n8n-validation-expert/         검증 에러 해석
        │   ├── SKILL.md
        │   ├── README.md
        │   ├── ERROR_CATALOG.md           검증 에러 유형별 원인 / 해결 카탈로그
        │   └── FALSE_POSITIVES.md         무시해도 되는 오탐 목록
        ├── n8n-code-javascript/           Code 노드 JS 작성법
        ├── n8n-code-python/               Code 노드 Python 작성법
        ├── n8n-expression-syntax/         {{ }} 표현식 문법
        │   ├── SKILL.md
        │   ├── README.md
        │   ├── EXAMPLES.md                표현식 예제 모음
        │   └── COMMON_MISTAKES.md         자주 하는 표현식 실수
        └── n8n-workflow-patterns/         워크플로우 아키텍처 패턴
            ├── SKILL.md
            ├── README.md
            ├── webhook_processing.md      Webhook 수신·처리 패턴
            ├── http_api_integration.md    외부 HTTP API 연동 패턴
            ├── database_operations.md     DB 조회·적재 패턴
            ├── scheduled_tasks.md         스케줄(Cron) 기반 작업 패턴
            └── ai_agent_workflow.md       AI Agent 노드 활용 패턴
```

## 계층별 역할

| 계층 | 위치 | 역할 |
|------|------|------|
| **오케스트레이터** | `skills/n8n-workflow-manager`, `skills/n8n-env-setup` | 사용자 요청을 받아 절차를 주도. 워크플로우 작업과 환경 셋업으로 진입점이 나뉨 |
| **에이전트** | `agents/*` | 오케스트레이터가 단계별로 위임하는 실행 주체 (분석 / 리서치 / 빌드 / 환경) |
| **커맨드** | `commands/n8n-setup.md` | `/n8n-setup`으로 환경 셋업을 직접 호출하는 단축 진입점 |
| **지식 스킬** | 나머지 `skills/n8n-*` 7종 | 리서처·빌더가 참조하는 n8n 도메인 지식 (MCP 도구, 노드 설정, 검증, Code 노드, 표현식, 패턴) |

## 호출 흐름

```
사용자 요청
  │
  ├─ "n8n 켜줘" / 환경 문제 ──▶ n8n-env-setup (스킬) 또는 /n8n-setup (커맨드)
  │                              └─▶ agents/n8n-env-setup ─▶ OS 감지 → 스크립트 실행 → n8n + Playwright MCP 기동
  │
  └─ 워크플로우 수정/생성 ──▶ n8n-workflow-manager (스킬)
                               ├─ 1. 분석      agents/n8n-workflow-analyst
                               ├─ 2~3. 요건 확인   AskUserQuestion (매번 재확인)
                               ├─ 4. 리서치    agents/n8n-workflow-researcher
                               │                 ├─ context7 (공식 문서)
                               │                 ├─ WebSearch
                               │                 └─ 지식 스킬 7종
                               ├─ 5. 계획 승인  AskUserQuestion
                               ├─ 6. 실행      agents/n8n-workflow-builder
                               │                 └─ n8n MCP → validate → (에러 시) autofix
                               └─ 7. 보고      결과를 _workspace_n8n/ 에 기록
```

## 참고

- 오케스트레이터가 남기는 산출물(분석·요건·리서치·계획·실행 결과)은 프로젝트 루트의 `_workspace_n8n/`에 저장됩니다.
- 로컬 경로 설정은 `n8n-env-setup/paths.env.example`을 복사해 `paths.env`를 만들거나, 첫 실행 시 자동 탐지에 맡깁니다.
