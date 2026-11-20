# YouTube Tech — 2026-11-20

## NAVER D2

### Jetpack Compose 기반 커스텀 3D 캐러셀 개발기
https://www.youtube.com/watch?v=0dY6pODrF2U

- NAVER Engineering Day 10th에서 발표된 세션으로, 3D 캐러셀 UI를 LazyRow 없이 Jetpack Compose로 구현한 개발 과정을 다룹니다.
- 배치, 스크롤, 보이는 요소만 컴포즈하는 세 가지 기준을 중심으로 LazyRow를 쓰지 않은 이유와 Float 값 하나로 모든 카드를 움직이는 구조를 설명합니다.
- 매 프레임 이동 시 리컴포지션을 0으로 유지하는 방법과 3D로 기울어진 UI의 터치 판정 이슈 해결 사례를 소개합니다.
- LazyRow 없이 Paging3를 연동해 처리하는 과정에서 마주한 이슈와 해결 방안을 공유합니다.
- 복잡한 UI를 AI와 함께 구현하면서 속도가 빨라진 부분과 한계가 있었던 부분을 함께 다룹니다.

### 부족한 건 모델이 아니라 팀 문서였다: 팀 공유 지식층 Third Brain 구축기
https://www.youtube.com/watch?v=fxGi9Emms-0

- NAVER Engineering Day 10th에서 발표된 세션으로, 팀 지식을 정리하는 방법을 고민하는 개발자를 대상으로 합니다.
- 에이전트가 팀 업무를 제대로 처리하지 못한 원인이 모델이 아니라 팀 문서의 부재에 있음을 확인한 과정을 공유합니다.
- 팀 위키를 AI가 직접 읽고 쓰는 공유 지식층인 Third Brain으로 구축해 운영한 경험을 설명합니다.
- 문서를 작성하는 위치, 업데이트 담당 주체, AI가 작성한 내용의 신뢰성에 대한 논의를 다룹니다.
- 구축 이후의 실제 동작 여부와 운영 결과를 점검하며 발표를 마무리합니다.

### Devops Agent 리포트 오이데~ 평가 야호~
https://www.youtube.com/watch?v=_btg9xR_i50

- NAVER Engineering Day 10th에서 발표된 세션으로, LLM 기반 이상 신호 분석 및 평가 시스템을 운영하려는 독자를 대상으로 합니다.
- 통합검색 알람 발생 시 1분 이내에 장애 1차 진단 리포트를 이슈로 남기는 Devops Agent를 소개합니다.
- 에이전트 구조로 인해 발생하는 문제와 결과를 검증하기 위한 평가 기준 수립 과정을 설명합니다.
- 에이전트의 출력 결과를 평가해 시스템 정확도를 도출하는 평가 시스템의 구성과 구축 과정을 다룹니다.
- 구축된 평가 시스템의 향후 발전 방향과 미래에 대한 내용을 함께 제시합니다.

### 온톨로지, 구축에서 활용까지. 질문이 답을 설계한다.
https://www.youtube.com/watch?v=eXXV-j1QO_Y

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 가상의 물류회사가 매일 받는 화물 위치와 예외 여부에 관한 질문에서 출발해 온톨로지 구축부터 활용까지를 소개한다.
- 사람과 AI가 구축된 온톨로지 위에서 정보를 찾아보고 업무를 처리하는 과정을 실제 화면 데모로 보여준다.
- 발표 목차에는 온톨로지의 정의와 구축 및 활용 방법 외에 LLM 단독, RAG, 온톨로지 비교 내용이 포함된다.
- FDE와 고객 실증 사례를 다루며 온톨로지가 정답이 아니라는 주제로 세션을 마무리한다.

## kakao tech

### 카카오의 사용자 선택권 존중 데이터 관리 체계 | 서비스 사이에서 사용자 맥락을 잃지 않으려면: 카카오가 AI 메모리를 설계하며 마주한 질문들 | AI 방향성
https://www.youtube.com/watch?v=CCaYLjkfUcA

- if(kakao)26에서 공개된 세션으로 사용자의 동의와 삭제 통제를 바탕으로 서비스 간 필요한 맥락만 연결하는 카카오의 AI 메모리 플랫폼 설계 과정을 공유한다.
- AI가 사용자 맥락을 기억하는 시대에 데이터를 잘 저장하는 것보다 잘 지우는 것이 중요하다는 문제의식을 다룬다.
- 김용현 발표자는 여러 서비스의 사용자 신호를 안전하게 전달하기 위한 AI 메모리의 수집·제공 인터페이스와 처리 구조 설계를 맡고 있다.
- 전지선 발표자는 AI 스튜디오에서 사용자가 스스로 데이터 활용 범위를 선택하고 통제할 수 있도록 돕는 AI 메모리 관리 체계와 정책을 담당한다.
- 최미현 발표자는 여러 서비스의 사용자 신호가 하나의 맥락으로 이어져 서비스 경험에 활용되도록 AI 메모리의 구조를 설계한다.

## Google Cloud Tech

### AI 에이전트가 Google Calendar를 직접 다루지 못하게 하는 방법
https://www.youtube.com/watch?v=pnaERetXD9c

- 정리되지 않은 음성 발화를 Google Calendar 일정, 작업, 개발 티켓으로 변환하는 Scribant의 3단계 Agent Development Kit(ADK) 파이프라인 구조를 설명한다.
- 1단계에서는 LLM 오버헤드 없이 빠른 음성 전사를 수행하기 위해 Google Cloud Speech to Text를 사용한다.
- 2단계에서는 모델이 달력 날짜 계산을 추측하지 않도록 결정론적 날짜 리졸버(deterministic date resolver)와 함께 누적 요약 및 작업 추출을 담당하는 두 전문 ADK 에이전트를 나란히 실행한다.
- 3단계에서는 사용자가 승인을 클릭하기 전까지 Google Calendar나 개발 워크스페이스에 접근하지 못하도록 전체 과정을 엄격한 읽기 전용 Execution Gate로 감싼다.
- 이 3단계 시스템은 단일 세션에서는 작동했으나 여러 날에 걸친 사용에서는 문제가 발생했으며, Laxmi Harikumar와 Miles Libbey가 발표자로 참여하고 Gemini 플랫폼, Antigravity, Vertex AI Memory Bank 등이 언급된 제품에 포함된다.

### 모두가 AI에서 그래프를 이야기하는 이유(그리고 건너뛰어야 할 때)
https://www.youtube.com/watch?v=2sS9XS-Fw90

- Annie Wang이 단순 스크립트와 그래프 방식의 아키텍처 트레이드오프를 포함해 AI 분야에서 그래프가 주목받는 이유와 사용하지 않아도 되는 경우를 설명하는 심층 튜토리얼이다.
- 첫 번째 파트에서는 단일 에이전트만으로 충분하지 않은 이유와 함께 Google의 Agent Development Kit(ADK)로 병렬, 라우팅, 트리, 루프 패턴의 노드와 엣지를 갖춘 워크플로우 그래프를 구축하는 방법 및 트레이드오프를 다룬다.
- 두 번째 파트에서는 벡터 RAG와 GraphRAG를 비교하고, 고객 환불(customer refund) 앱 데모를 통해 연결된 레코드를 탐색하는 데이터(지식) 그래프의 동작을 보여준다.
- BigQuery Graph와 GQL을 이용해 데이터 그래프를 쿼리하는 방법과 트레이드오프를 설명하며, 워크플로우 그래프와 데이터 그래프를 함께 결합하는 구성도 다룬다.
- 영상 설명란에는 ADK 그래프 워크플로우, ADK Human-in-the-Loop 도구 확인, BigQuery Graph 개요, 그래프 엔지니어링 코드랩 등의 참고 링크가 함께 제공된다.

## Unreal Engine

### 알아두어야 할 Unreal MCP 설정과 콘솔 명령어
https://www.youtube.com/watch?v=2KnEEa0yTpQ

- Unreal Engine(UE5)에서 Unreal MCP 설정이 위치한 경로를 안내하는 빠른 참고 영상이다.
- Editor Preferences 내 Model Context Protocol 섹션을 다시 살펴본다.
- 해당 섹션에 포함된 Auto Start Server와 Enable Tool Search 옵션을 확인한다.
- ModelContextProtocol 관련 콘솔 명령어들을 훑어본다.
- 이 강좌에서 다루는 모든 도구가 에디터 전용(editor-only)인 이유를 설명한다.

### 도구 호출 시간을 46초에서 1초로 줄이는 5가지 Unreal MCP 팁
https://www.youtube.com/watch?v=E-aygTcDK5g

- Unreal Engine(UE5) 강좌 제작 과정에서 정리한 다섯 가지 Unreal MCP 팁을 소개한다.
- 테스트 결과 백그라운드 CPU 스로틀링을 끄면 46초가 걸리던 MCP 호출 시간이 약 1초로 단축된다고 설명한다.
- 구현 전에 먼저 계획을 세우고, 복잡한 로직에는 블루프린트(Blueprints) 대신 C++ 사용을 고려할 것을 권장한다.
- agent.md 파일을 활용한 지속적 개선 루프를 적용할 것을 제안한다.
- 컨텍스트 크기가 작은 모델을 사용할 때는 필요한 툴셋만 선택적으로 활성화할 것을 권장한다.

### Unreal MCP 개념 설명: MCP, 모델, 하네스, 컨텍스트 및 툴셋
https://www.youtube.com/watch?v=EP_LMWhWizM

- Unreal MCP를 설정하기 전에 강좌 전반에서 사용되는 여섯 가지 주요 용어를 소개한다.
- 설명 대상 용어는 MCP, 모델(model), 하네스(harness), 컨텍스트(context), agent.md, 툴셋(toolset)이다.
- 각 용어의 의미와 이들이 서로 어떻게 맞물려 작동하는지 다룬다.
- 사용자가 자신에게 맞는 AI 도구를 선택해 Unreal MCP와 함께 작업할 수 있는 구조를 설명한다.
- 프로젝트의 다른 구성을 변경하지 않고도 Claude나 Codex 같은 모델을 교체해 사용할 수 있음을 안내한다.

### Unreal MCP 시작하기 | UE 5.8에서 AI로 작업 수행하기
https://www.youtube.com/watch?v=OjffwpbcQsQ

- Unreal MCP는 에이전트형 AI 도구를 언리얼 엔진에 직접 연결하는 에픽게임즈 공식 지원 방식이며, 언리얼 엔진 5.8에서 실험적(Experimental) 기능으로 제공된다.
- 개방형 MCP 표준을 기반으로 구축되어 AI 에이전트가 프로젝트를 이해하고 에디터에서 생성, 수정, 테스트 및 반복 작업을 수행할 수 있게 한다.
- 시니어 언리얼 엔진 강사 Sam Deiter가 Unreal MCP 시작에 필요한 주요 용어와 7단계 설정 과정을 설명한다.
- 문제 해결과 디버깅, 툴셋, 에디터 내 Terminal 플러그인 워크플로, 구성 설정을 다룬다.
- 작업 시간 절약 팁과 가장 자주 묻는 질문에 대한 답변도 함께 제공한다.

### Unreal MCP 터미널 플러그인: 언리얼을 벗어나지 않고 AI 에이전트 사용하기
https://www.youtube.com/watch?v=QxXNoHfTLcY

- 언리얼 엔진을 벗어나지 않고 AI 에이전트와 프로젝트를 하나의 워크플로 안에서 다루는 방법을 소개한다.
- 에디터에서 Terminal 플러그인을 활성화하는 방법을 설명한다.
- 에디터 내 터미널이 .mcp.json 파일이 있는 폴더를 가리키도록 지정하는 과정을 다룬다.
- 언리얼 엔진 내부에서 직접 AI 에이전트를 실행하는 방법을 안내한다.
- 터미널 텍스트가 올바르게 표시되지 않을 때 적용할 수 있는 간단한 해결 방법도 포함한다.

### Output Log와 MCP Inspector로 Unreal MCP 디버깅하는 방법
https://www.youtube.com/watch?v=RvtqksJix-Y

- 도구 호출이 정확히 어느 지점에서 실패하는지 파악하는 디버깅 방법을 다룬다.
- Output Log에서 MCP 활동 내역을 추적하는 방법을 설명한다.
- 개방형 MCP 표준의 공식 디버깅 클라이언트인 MCP Inspector를 설정하는 과정을 안내한다.
- AI 에이전트를 거치지 않고 MCP Inspector로 도구 목록을 조회해 직접 호출하는 방법을 보여준다.
- MCP Inspector에서 직접 호출했을 때도 실패한다면 원인이 프롬프트가 아니라 도구나 서버 측에 있음을 구분할 수 있다고 설명한다.

### Unreal MCP 툴셋 설명: 툴 레지스트리, 툴 검색 및 사용자 지정 도구
https://www.youtube.com/watch?v=ekLlS4Csu8w

- AI 에이전트가 프로젝트에서 수행하는 모든 작업은 툴셋에서 시작된다고 설명합니다.
- 툴셋과 툴 레지스트리가 함께 작동하는 방식을 다룹니다.
- Tool Search가 수백 개의 도구 대신 세 개의 탐색 도구만 에이전트에게 보여주는 이유를 설명합니다.
- ModelContextProtocol.RefreshTools를 실행해야 하는 시점을 안내합니다.
- Python이나 C++로 작업 방식에 맞는 사용자 지정 툴셋을 구축할 때 어디서부터 시작해야 하는지 다룹니다.

### Unreal MCP FAQ: 안전성, 로컬 모델, 엔진 버전 등 주요 질문 정리
https://www.youtube.com/watch?v=qS1G6VTXH2k

- Unreal MCP가 연결되지 않는 이유와 지원되는 엔진 버전에 대한 답변을 제공합니다.
- Epic이 공식 지원하는 플러그인과 커뮤니티 서버의 비교 및 로컬 모델 사용에 관한 내용을 다룹니다.
- 보안과 기기 외부로 나가는 데이터의 범위, 그리고 AI 에이전트가 프로젝트에서 할 수 있는 일과 없는 일을 설명합니다.
- 직접 도구를 작성하는 방법과 팀 단위 사용, 소스 컨트롤, 실행 취소(Undo) 관련 질문을 다룹니다.
- Unreal MCP가 프로덕션 환경에 적용할 준비가 되었는지 여부에 대해서도 답합니다.

### UE 5.8에서 Unreal MCP 설정하는 방법 | Claude Code, Cursor 등 연결하기
https://www.youtube.com/watch?v=sudSws4rauU

- Claude Code, Cursor, Visual Studio Code, Gemini CLI, Codex 등의 에이전트형 AI 도구를 7단계로 언리얼 엔진에 연결하는 방법을 설명합니다.
- 프로젝트를 생성한 뒤 Unreal MCP 및 All Toolsets 플러그인을 활성화하고 Auto Start Server를 켜는 과정을 다룹니다.
- 클라이언트 설정을 생성하고 서버를 시작하는 절차를 안내합니다.
- 프로젝트 루트에서 실행 하네스를 구동하는 방법을 설명합니다.
- 선택된 액터 확인부터 조명이 적용된 큐브 12개를 고리 형태로 배치하는 작업까지 첫 프롬프트로 테스트하는 과정을 다룹니다.

### Unreal MCP가 연결되지 않을 때: '에이전트가 도구를 찾지 못함' 문제 해결 방법
https://www.youtube.com/watch?v=uZ5Vb13Y2cg

- AI 에이전트가 Unreal MCP를 볼 수는 있지만 프로젝트에서 작업을 수행할 수 없을 때 확인해야 할 세 가지 사항을 안내합니다.
- 에이전트를 실행한 위치와 서버가 실행 중인지 여부를 점검하는 내용을 다룹니다.
- 활성화된 툴셋이 있는지 확인해야 한다는 점을 설명합니다.
- 긴 도구 호출 중에 에디터가 멈춘 것처럼 보일 수 있는 이유를 설명합니다.
- 큰 작업을 더 작은 요청으로 나누어 반복 작업을 원활하게 이어가는 방법을 다룹니다.

## AWS Developers

### Claude Code와 AWS: 채팅에서 비밀 정보 노출 방지하기
https://www.youtube.com/watch?v=doWO-WBk0A4

- Agent Toolkit for AWS의 aws-core 플러그인은 Claude Code에 최신 AWS 문서 및 CloudTrail에 기록되는 AWS API 호출을 지원하는 AWS MCP 서버와 작업 필요 시에만 로드되는 검증된 스킬을 제공합니다.
- 이 플러그인은 직접적인 비밀 정보 조회를 차단하는 훅을 추가해 평문 시크릿이 모델 컨텍스트나 디스크의 세션 파일에 기록되지 않도록 막습니다.
- 비밀 정보 직접 조회가 거부되면 에이전트는 평문 값을 보지 않고도 플레이스홀더와 asm-exec를 통해 시크릿을 안전하게 사용합니다.
- 블로그용 10가지 테스트에서 해당 훅은 Python 스크립트 내부에 포함된 boto3 호출을 비롯한 모든 비밀 정보 조회를 차단하고 일반 명령은 통과시켰습니다.
- 영상은 이 기능이 완전한 보안 경계가 아닌 최선형 방어 수단이므로 하단에 최소 권한 IAM을 유지해야 한다고 안내하며, /plugin install aws-core@claude-plugins-official 설치 방법과 CLI 설정 시 유의사항을 다룹니다.

## Google DeepMind

### Gemini와 AGI로 가는 길: Koray Kavukcuoglu 대담
https://www.youtube.com/watch?v=FORdPIWOH5k

- Hannah Fry 교수가 Google DeepMind 런던 오피스에서의 마지막 대화 이후 7년 만에 Google DeepMind SVP 겸 Google 최고 AI 아키텍트인 Koray Kavukcuoglu와 재회해 대담을 나눕니다.
- 과거 특화된 기술 혁신에 집중하던 시기에서 현재 Gemini를 중심으로 범용 지능을 추구하게 된 Google DeepMind의 변화 과정을 살펴봅니다.
- 실제 제품이 범용 인공지능(AGI) 구축에 필수적인 이유와 Gemini의 아키텍처 및 모델이 지속적으로 진화하는 방식을 논의합니다.
- 최근 주요 화두인 재귀적 자기 개선(RSI)을 별도 주제로 다루며 관련 논의를 진행합니다.
- 안전 및 에이전트 팀의 역할과 벤치마크에 관한 내용도 챕터별로 다룹니다.

## Google Cloud Tech

### Google Antigravity와 Gemini 4 Argon으로 소프트웨어 팩토리 구축하기
https://www.youtube.com/watch?v=EFejzwBLAVo

- Antigravity DevRel 팀의 Rody Davis가 Gemini 4 Argon 기반의 Google Antigravity에서 멀티 플랫폼 코드베이스의 기술 부채를 지속적으로 감사, 현대화 및 정리하는 자동화된 '소프트웨어 팩토리' 구축 데모를 시연합니다.
- Web(Node.js), Android(Jetpack Compose), iOS(SwiftUI)용 전문 '팩토리 라인' 역할을 하는 커스텀 서브에이전트를 Markdown으로 구성하는 단계별 과정을 보여줍니다.
- 지원해야 할 과거 브라우저 및 모바일 OS 버전 범위를 명시하는 플랫폼 버전 정책 설정을 정의하고 Gemini 4 Argon으로 'Evergreen Platform' 감사를 실행합니다.
- 각 커스텀 서브에이전트는 격리된 자체 컨텍스트 창에서 병렬로 실행되어 메인 채팅의 컨텍스트 압축을 피하며, 읽기 전용 도구 권한으로 코드 수정을 방지하고 오래된 폴리필과 미사용 레거시 API를 제거하는 Git 이력 최신성 보고서를 생성합니다.
- /learn을 통한 워커 동작 개선, 실시간 작업을 조정하는 직접 서브에이전트 메시징, Google I/O 및 WWDC 주기에 맞춰 정기 감사를 예약하는 자동화 패널, 장기 실행을 위한 /boost 및 Teamwork Preview 활용 패턴을 다룹니다.

## AWS Developers

### Claude Code에 실제 AWS 스킬 적용하기
https://www.youtube.com/watch?v=qNljzI8Bj0k

- Agent Toolkit for AWS의 AWS MCP 서버와 AWS 스킬을 Claude Code에 설정하는 방법을 다룹니다.
- aws-core 플러그인은 최신 AWS 문서 조회와 CloudTrail에 기록되는 AWS API 호출 기능을 갖춘 AWS MCP 서버를 Claude Code에 제공합니다.
- aws-core 플러그인은 에이전트가 작업에 필요할 때만 불러와 사용하는 검증된 스킬들을 함께 제공합니다.
- 이 플러그인에는 직접적인 시크릿(secret) 조회를 차단하는 훅(hook)이 추가되어 있습니다.
- 해당 스킬 중 하나가 에이전트의 채팅에 시크릿이 포함되지 않도록 막는 모습을 시연합니다.

## NVIDIA Developer

### NVIDIA Cosmos 프레임워크로 Cosmos 외 모델 파인튜닝하기
https://www.youtube.com/watch?v=79lv9HPXbEY

- NVIDIA Cosmos 프레임워크가 Cosmos 계열 외의 모델 파인튜닝을 지원하며, 튜토리얼에서는 Qwen3-VL 파인튜닝을 시연합니다.
- 로봇 영상 질의응답을 위해 RoboVQA 데이터셋을 사용하여 Qwen3-VL 모델을 지도 학습(supervised fine-tuning)합니다.
- 에이전트 스킬을 통해 환경 설정, 모델과 데이터 다운로드, 학습 데이터 준비, 사전 점검(preflight checks), 기준 평가, 학습, 모델 내보내기 및 학습 후 점수 평가를 처리합니다.
- 코딩 에이전트가 단일 프롬프트로 전체 워크플로를 실행하고, 학습에서 제외된 검증용(held-out) 로봇 영상 클립에서 파인튜닝 전후 모델의 답변을 비교해 평가합니다.
- 시연에서는 NVIDIA GB300 하드웨어를 사용해 약 2시간 동안 학습을 진행한 사례를 보여줍니다.

### NVIDIA Alpamayo 2 Edge 소개: 차량 내 실시간 추론
https://www.youtube.com/watch?v=3cmv7AAQHH0

- NVIDIA Alpamayo 2 Edge는 NVIDIA DRIVE AGX Thor에서 실시간 차량 내 배포를 위해 설계된 20억 파라미터 규모의 추론형 비전-언어-행동(Vision-Language-Action) 모델입니다.
- NVIDIA Cosmos 3 Edge의 Nemotron 기반 추론 백본 위에 구축되었으며, 차량 내 연산 자원을 절약하기 위해 필요할 때만 추론하는 적응형 추론으로 주행 궤적과 인과적 설명을 생성합니다.
- Physical AI Research 부사장 Marco Pavone이 모델의 아키텍처, 주요 기능 및 자율주행 개발 워크플로 적용 방법을 설명합니다.
- AlpaGym에서 폐쇄 루프(closed-loop) 강화학습으로 사후 학습된 최초의 Alpamayo 모델이며, 자체 데이터를 활용한 플릿 맞춤형 파인튜닝을 지원합니다.
- 오픈 모델로 제공되며 모델 가중치는 Hugging Face에 공개되어 있습니다.
