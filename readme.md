# N8N 오케스트레이션 어때요?

Claude Code로 n8n 워크플로우를 **읽기 → 요건 확인 → 리서치 → 계획 → 실행**까지 구조화된 절차로 안전하게 수정·생성하고, 로컬 n8n 개발 환경(Mac/Windows)을 자동으로 세팅해주는 스킬/에이전트/커맨드 모음입니다.

## 포함된 것

```
.claude/
├── agents/
│   ├── n8n-workflow-analyst.md      워크플로우 읽기 전용 분석
│   ├── n8n-workflow-researcher.md   context7+WebSearch+로컬스킬 기반 리서치
│   ├── n8n-workflow-builder.md      n8n MCP로 실제 변경 실행+검증
│   └── n8n-env-setup.md             로컬 환경 설치/기동/트러블슈팅
├── commands/
│   └── n8n-setup.md                 /n8n-setup 슬래시 커맨드
└── skills/
    ├── n8n-workflow-manager/        메인 오케스트레이터 (핵심)
    ├── n8n-env-setup/               환경 셋업 오케스트레이터 + Mac/Windows 스크립트 번들
    ├── n8n-mcp-tools-expert/        n8n MCP 도구 사용법
    ├── n8n-node-configuration/      노드별 파라미터 설정
    ├── n8n-validation-expert/       검증 에러 해석
    ├── n8n-code-javascript/         Code 노드 JS 작성법
    ├── n8n-code-python/             Code 노드 Python 작성법
    ├── n8n-expression-syntax/       {{ }} 표현식 문법
    └── n8n-workflow-patterns/       워크플로우 아키텍처 패턴
```

## 실제 사용법

### 사전 요구사항

1. **Claude Code** (최신 버전)
2. **n8n MCP 서버** — Claude Code의 MCP 설정(`~/.claude/mcp.json` 또는 프로젝트의 `.mcp.json`)에 아래와 같이 등록합니다.

   [`n8n-mcp`](https://www.npmjs.com/package/n8n-mcp) 패키지가 다음 도구를 제공합니다.

   - `n8n_list_workflows`
   - `n8n_get_workflow`
   - `n8n_create_workflow`
   - `n8n_update_partial_workflow`
   - `n8n_update_full_workflow`
   - `n8n_validate_workflow`
   - `n8n_autofix_workflow`
   - `n8n_test_workflow`
   - `validate_node` 등

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

   - `N8N_API_URL`은 `n8n-env-setup`으로 로컬 n8n을 띄웠다면 기본값(`http://localhost:5678`) 그대로 두면 됩니다.
   - `N8N_API_KEY`는 n8n 실행 후 **Settings → n8n API → Create an API key**에서 발급받습니다.
   - **주의: API 키는 절대 이 README나 저장소에 커밋하지 마세요.** `mcp.json`은 개인 설정 파일이므로 각자 자신의 키를 직접 입력해야 합니다.
3. **Context7 MCP 서버** — 최신 n8n 공식 문서 조회용 (리서처 에이전트가 사용)
4. **로컬 n8n 실행 환경** — 로컬에서 n8n을 직접 띄워 테스트하려면 Mac 또는 Windows PC가 필요합니다. (`n8n-env-setup` 스킬 지원)

### 설치 방법

#### 1. 압축 해제

이 ZIP을 프로젝트 루트에 압축 해제합니다.

이미 `.claude/agents`, `.claude/skills`, `.claude/commands`가 있는 프로젝트라면 폴더를 병합(merge)하면 됩니다. 다른 이름의 스킬이나 에이전트와 충돌하지 않습니다.

#### 2. CLAUDE.md 설정 (권장)

프로젝트의 `CLAUDE.md`에 아래 트리거 포인터를 추가합니다.

```markdown
## n8n 워크플로우 하네스

**트리거:** n8n 워크플로우 관련 작업 요청 시 `n8n-workflow-manager` 스킬을 사용하라.
n8n 로컬 환경(설치/기동/포트 충돌 등) 관련 요청은 `n8n-env-setup` 스킬 또는 `/n8n-setup` 커맨드를 사용하라. (Mac/Windows 자동 감지)
```

선택 사항이지만 권장합니다. 없어도 스킬 description을 통해 자동 트리거되지만, 명시해두면 더 안정적으로 동작합니다.

#### 3. 환경 경로 설정 (선택)

로컬 n8n을 직접 사용할 경우 `.claude/skills/n8n-env-setup/paths.env.example`을 참고해 `paths.env`를 직접 생성할 수 있습니다.

설정하지 않아도 첫 실행 시 자동 탐지 후 필요한 값을 채워줍니다.

### 빠른 시작

**n8n 실행**

```
사용자: n8n 켜줘
→ n8n-env-setup 스킬이 현재 OS(Mac/Windows)를 감지 → 로컬 n8n 기동 → Playwright MCP 기동
```

**워크플로우 수정**

```
사용자: 결제 알림 워크플로우에 Slack 알림 노드 추가해줘
→ n8n-workflow-manager → 워크플로우 분석 → 요건 확인(AskUserQuestion) → 리서치 → 계획 승인 → 실행 → 검증
```

## 동작 원리

`n8n-workflow-manager`는 다음 순서로 동작합니다.

1. **분석** — `n8n-workflow-analyst`가 대상 워크플로우의 JSON을 직접 읽어 노드/연결 구조를 파악 (추측 금지)
2. **요건 명확화** — 모호한 부분만 AskUserQuestion으로 질문
3. **요건 확인 (필수)** — 이해한 내용을 요약해 매번 AskUserQuestion으로 재확인한 뒤에만 다음 단계로 진행
4. **리서치** — `n8n-workflow-researcher`가 context7 공식 문서 + WebSearch + 로컬 n8n 스킬 3개 출처를 모두 조사 (백그라운드 병렬)
5. **계획 수립** — todo 목록을 파일로 남기고, 실행 전 다시 한번 AskUserQuestion으로 승인
6. **실행** — `n8n-workflow-builder`가 n8n MCP 도구로만 변경을 적용하고, 매 단계 후 자동 검증+오토픽스
7. **보고** — 완료/실패 항목을 정리해 보고, 피드백을 요청

## 기존 n8n 사용 대비 장점

| 항목 | 기존 방식 | 이 킷 사용 시 |
|------|-----------|---------------|
| **요구사항 오해 방지** | AI에게 바로 "이렇게 고쳐줘"라고 요청하면 요구사항을 잘못 이해한 채 워크플로우가 변경될 수 있음 | 실제 변경 전에 이해한 내용을 반드시 요약·재확인(AskUserQuestion)하여 엉뚱한 변경을 방지 |
| **최신 문법 반영** | 사람의 기억이나 AI 학습 데이터에 의존하여 오래된 노드 파라미터 또는 typeVersion 사용 위험 | 매번 Context7 공식 문서와 Web Search를 통해 최신 스펙을 확인한 후 적용 |
| **변경 안전성** | UI에서 수동 수정 시 실수를 즉시 발견하기 어려움 | 변경 직후 `n8n_validate_workflow` 자동 실행 → 오류 발생 시 `n8n_autofix_workflow`로 자동 복구 시도 → 실패 시 원인 및 결과를 명확하게 보고 |
| **감사 추적(Audit Trail)** | 무엇을, 왜 변경했는지 기록이 남지 않음 | 분석, 요구사항, 리서치, 계획, 적용 결과가 모두 `_workspace_n8n/`에 저장되어 추후 검토 가능 |
| **환경 셋업** | "n8n 설치 방법이 뭐였지?", "스크립트 위치가 어디였지?" 같은 반복 작업 발생 | OS(Mac/Windows) 자동 감지 및 스크립트 경로 자동 탐지·캐싱으로 한 번의 요청만으로 실행 가능 |
| **이식성** | 개인 PC 절대 경로가 스크립트나 문서에 포함되어 다른 사람이 재사용하기 어려움 | 프로젝트 루트 및 환경변수 기준으로 경로를 동적으로 해석하여 누구의 PC에서도 동일하게 실행 가능 |
| **팀 지식 축적** | Code 노드 문법, Expression 문법 등의 노하우가 개인에게만 축적됨 | 로컬 n8n 스킬 7종을 통해 팀의 운영 노하우가 프로젝트 자산으로 축적되고 지속적으로 재사용 가능 |

## 알려진 제한사항

- 트리거 문구(should/should-not) 정식 테스트와 전체 파이프라인 드라이런은 아직 수행되지 않았습니다 — 실사용하며 description 튜닝이 필요할 수 있습니다.
- 대규모 워크플로우 신규 설계처럼 리서치 범위가 매우 넓은 작업은 현재 단일 리서처가 순차로 조사합니다 (병렬 다각도 리서치는 필요 시 확장 가능한 구조).
- Windows 환경 스크립트는 OneDrive 동기화 폴더 자동 탐지(`$env:OneDriveCommercial`/`$env:OneDrive`)에 의존합니다 — 회사 OneDrive를 쓰지 않는 환경이라면 `paths.env`에 직접 경로를 지정하세요.

## 커스터마이징

- 특정 도메인(예: 사내 서비스 API) 지식이 필요하면, 그 도메인을 다루는 별도 에이전트를 만들어두면 `n8n-workflow-researcher`가 "관련 도메인 전문 에이전트가 존재하면 호출" 단계에서 자동으로 활용합니다. 코드 수정 불필요.
- 워크스페이스 폴더명(`_workspace_n8n/`), 요건 확인 재질문 횟수(기본 2회) 등은 `n8n-workflow-manager/SKILL.md`에서 직접 조정할 수 있습니다.

## 결론: 잔말말고 n8n 오케스트레이션으로 틀어

요구사항을 적게 요청해도 알아서 사용자에게 남은 요구사항을 물어보고 계획적으로 진행하는 똑똑한 오케스트레이션이 필요했습니다.

써보니 적은 요청이라도 찰떡같이 조사를 진행하면서, 제가 생각지 못한 요구들도 보완해주더라구요. 그래서 좋았습니다.
