# YouTube Tech — 2026-11-09

## Unity Korea

### USD Toolkit 소개
https://www.youtube.com/watch?v=TpDuKFR5Bko

- NVIDIA와의 협업을 통해 자유로운 입력과 출력이 가능한 OpenUSD를 다루는 영상이다.
- Unity 엔지니어 두 명이 OpenUSD의 개념과 개요를 설명한다.
- 게임 및 산업 동향과 USD Toolkit의 개요를 차례로 소개한다.
- USD Toolkit 데모와 시작하는 방법, 고객 사례를 포함한다.
- Live Sync와 설치 및 시작하기 내용을 다룬다.

### Unity 6.6에서 무엇이 바뀌었을까요?
https://www.youtube.com/watch?v=FvcjaJKtiMs

- Unity 6.7 LTS를 준비하는 여정의 마지막 단계인 Unity 6.6 에디터의 변경 사항을 소개한다.
- 에디터 변화와 패키지 변화를 차례로 설명한다.
- Content Directory와 분석 도구 변화를 다룬다.
- Compute Light Baker와 UI 변화를 소개한다.
- Web 빌드 강화 내용을 포함한다.

### [2D 게임 개발 꿀팁 시리즈] 모바일 성능과 쓰로틀링
https://www.youtube.com/watch?v=z0bkXem0g7o

- 2D 게임 개발 꿀팁 시리즈의 모바일 성능과 쓰로틀링 편이다.
- 쓰로틀링의 개념을 알아본다.
- 모바일에서의 성능을 최적화하기 위한 방법을 다룬다.
- 2D 게임 최적화 팁을 제시하는 영상이다.
- 해당 영상은 AI를 활용하여 제작되었다고 밝히고 있다.

## NAVER D2

### worklog-system 주간보고 자동화 구축 경험기
https://www.youtube.com/watch?v=DXErrGHYw2M

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 대 AI 시대에 본인의 업무 기록을 수집하고 TODO 및 회의록을 기록하는 시스템을 소개한다.
- 주간보고 수집의 불편과 누락 문제를 다룬다.
- 재택과 사무실, 업무 도구 하나로 통합하는 과정을 에피소드로 구성했다.
- Slack, Jira, Confluence, GitHub 등 사내 협업 도구를 엮어 개인 생산성 도구를 만드는 내용을 포함한다.

## NVIDIA Developer

### Roboflow와 NVIDIA Cosmos 3로 구현하는 비디오 추론과 모델 파인튜닝
https://www.youtube.com/watch?v=NS9bMGAnPG0

- NVIDIA와 Cosmos Coalition 파트너인 Roboflow가 함께 NVIDIA Cosmos 3와 Roboflow로 비전 AI 애플리케이션을 구축하는 방법을 소개한다.
- 영상 추론을 실제로 시연하고, 이것이 조립 단계 검증과 사이클 타임 분석을 어떻게 지원하는지 보여준다.
- Roboflow에서 Cosmos 3 Edge를 사용하고, 자체 영상으로 파인튜닝해 어떤 동작이 언제 발생하는지 인식하는 방법을 다룬다.
- 라벨링부터 모델 예측까지의 워크플로를 Roboflow의 Cosmos 3 평가에서 얻은 실무 교훈과 함께 따라간다.
- 예측된 동작 타임라인을 SOP와 비교해 조립 단계를 검증하고, 평가 결과를 바탕으로 프롬프팅과 장면 구성을 개선하는 방법을 설명한다.

### 인간 시연에서 로봇 학습 데이터로 | RLWRLD와 Cosmos Labs
https://www.youtube.com/watch?v=09igP-kQXtw

- 사람이 작업하는 영상을 로봇이 학습할 수 있는 훈련 데이터로 바꾸는 파이프라인을 NVIDIA와 RLWRLD가 소개한다.
- 동기화된 영상 캡처와 손-물체 재구성부터 로봇별 동작 리타기팅과 NVIDIA Isaac Sim 렌더링까지의 과정을 따라간다.
- RLWRLD가 자사 RLHND 핸드 트래킹 시스템에서 NVIDIA Cosmos 3 기능을 어떻게 활용하는지 살펴본다.
- 의류 패킹과 다양한 로봇 구성에 대해 월드 모델이 생성한 관측값의 연구 데모를 검토한다.
- 로봇공학 개발자와 연구자를 위해 데이터 품질 선택, 현재 결과가 보여주는 것, 아직 평가가 남은 부분을 다룬다.

## Microsoft Developer

### Work IQ: SharePoint MCP 도구
https://www.youtube.com/watch?v=9RN7lsKIbc0

- Work IQ의 SharePoint MCP Tools는 에이전트가 MCP 인터페이스를 통해 SharePoint 콘텐츠와 워크플로를 다루게 해주는 기능이다.
- 고정된 도구 목록을 미리 불러오는 대신, 에이전트가 런타임에 /sharepoint 경로를 발견하고 스키마를 확인해 필요한 작업을 고른다.
- 사이트 콘텐츠 검색, 파일·폴더 정리, 목록과 문서 라이브러리 유지, 협업 워크플로 지원에 활용된다.
- 모든 작업은 로그인한 사용자의 기존 SharePoint 권한과 테넌트 거버넌스 정책 범위 안에서 실행된다.
- 읽기 시나리오에는 WorkIQ.Read, 콘텐츠·설정 변경에는 WorkIQ.Act 권한이 필요하며 읽기 전용 토큰으로는 쓰기 경로가 노출되지 않는다.

## Cole Medin

### 코딩 에이전트는 코드는 알지만 실제 앱은 모른다 (해결책)
https://www.youtube.com/watch?v=EMIRXv2iE_Q

- 코딩 에이전트가 저장소의 모든 파일을 읽어도 데이터 연결, 의존 관계, 배포 위치, 장애 원인은 코드가 아닌 실행 플랫폼에 있어 알 수 없다는 문제를 제기한다.
- OutSystems MCP를 통해 Claude Code, Cursor, GitHub Copilot 같은 코딩 에이전트가 OutSystems Developer Cloud에 연결된다.
- 에이전트는 실제 엔티티, 화면, 로직, 역할을 조회하고 의존성을 매핑할 수 있다.
- 빌드를 Mentor에 넘기고 배포하며 로그와 트레이스를 읽는 작업을 한 세션에서 수행한다.
- OutSystems에서 이미 가진 권한으로 동작하며, Personal Edition은 무료이고 OutSystems MCP가 켜져 있다.

## Claude

### Salesforce가 Claude Code를 사용하는 방법
https://www.youtube.com/watch?v=4ZsVR-6YOzs

- Salesforce는 Claude Code를 수천 명의 엔지니어로 확대했고 실질 산출량이 두 배가 되었으며 코드 라인당 버그는 이전보다 줄었다.
- 스탠퍼드 연구진과 함께 만든 'effective output' 점수로 AI 코딩 ROI를 측정한다고 설명한다.
- 에이전트 성숙 곡선을 통해 엔지니어들이 단순 프롬프트에서 소프트웨어 개발 생애주기 전반의 자율 에이전트로 이동했다.
- 수십 년 된 코드베이스를 1년이 아니라 몇 주 만에 헤드리스로 전환했고, 에이전트 스킬 공유 마켓플레이스와 담당 팀을 자동으로 찾는 인시던트 에이전트도 다룬다.
- 사람의 시도가 실패한 버그를 Claude Opus가 24시간 만에 찾아냈으며, '검증 없는 자율성은 자신감 연극'이라는 원칙을 제시한다.

## Google Cloud Tech

### Knowledge Catalog로 신뢰할 수 있는 시맨틱 모델에 에이전트 근거 부여하기
https://www.youtube.com/watch?v=IW5XI2_1ctI

- Google Cloud Knowledge Catalog는 LookML, BigQuery Graph, dbt MetricFlow, Databricks Unity Catalog, Snowflake, SAP의 시맨틱 레이어를 자동으로 인덱싱한다.
- AI 에이전트에 필요한 비즈니스 컨텍스트와 시맨틱을 제공해 거버넌스가 적용된 정확한 답변을 내놓는다.
- 동적 컨텍스트 그래프로 데이터 자산, 시맨틱 모델, 스키마, 조인, 리니지, 거버넌스의 연결 관계를 시각적으로 탐색한다.
- 기준선 에이전트와의 비교에서 Knowledge Catalog 기반 에이전트는 도구 호출 3번 만에 인증된 비즈니스 로직을 담은 정확한 SQL을 생성했다.
- 이 비교에서 지연 시간과 토큰 사용량이 약 67% 줄었다.

## OpenAI

### LifeVal: 일상에서 중요한 과제에 대한 AI 발전 측정
https://www.youtube.com/watch?v=hJOwOkLHRN0

- OpenAI는 AGI가 모든 인류에 이롭기 위해서는 사람들이 가장 중요하게 여기는 일상 작업을 도와야 한다고 밝혔다.
- LifeVal은 수천 명의 ChatGPT 사용자 피드백을 바탕으로 만들어진 새로운 벤치마크다.
- 사용자들은 자녀 돌봄 찾기, 정부 서비스 이용, 개인 재정 관리 등 개인 비서의 도움을 가장 원하는 분야를 제시했다.
- OpenAI는 지난 1년간 LifeVal을 사용해 모델이 이런 일상 작업을 얼마나 잘 처리하는지 측정하고 개선했다.
- 자세한 내용은 openai.com/index/lifeval/에서 확인할 수 있다.

## NVIDIA Developer

### Red Hat 소형 모델 해커톤 우승팀 소개
https://www.youtube.com/watch?v=TVvViJUhAuo

- NVIDIA Developer Community가 미국 Raleigh에서 열린 NVIDIA x Red Hat Small Models Hack 우승팀과의 라이브 인터뷰를 진행한다.
- 해커톤 과제는 총 33B 파라미터 이하의 작고 개방된 모델로 실제 AI 애플리케이션을 구축하는 것이었다.
- 참가팀들은 소형 모델을 조정하고, 서로 협력시키고, 도구를 갖추게 하는 방법을 탐구했다.
- NVIDIA Nemotron Lightning 최우수 활용상을 받은 Escape Red Hat은 비상 상황에서 5명의 AI 점유자가 독립적으로 판단하는 대피 시뮬레이터를 만들었다.
- NeMo Gym 최우수 활용상을 받은 Unspoken은 음성, 입 모양, 시선, EEG 신호를 결합해 심각한 언어 장애가 있는 사람의 의사소통을 돕는 멀티모달 시스템을 만들었다.

### 전문가에게 묻다: Dory 루프 트랜스포머 모델 | Nemotron Labs
https://www.youtube.com/watch?v=_MEqhFwnp8o

- NVIDIA의 공개 연구 모델 Dory 1.0은 가중치를 바꾸지 않고 추론 시점에 연산량과 정확도를 맞바꿀 수 있는지 탐구하는 4B 모델이다.
- 루프 트랜스포머 구조로 공유 레이어 블록을 재사용하며, SWE-bench Verified 점수가 루프 1회에서 50.3, 4회에서 61.8로 나타났다.
- 세션에서는 루핑이 작동하는 방식과 마지막 루프 KV 캐싱이 메모리를 일정하게 유지하는 이유를 다룬다.
- 네이티브 NVFP4 사전 학습과 BF16, MXFP8, NVFP4 체크포인트가 DGX Spark와 Hopper, Blackwell GPU에서 실행된다.
- 추가 루프가 도움이 되지 않는 지점과 자신의 작업에서 루프 수에 따른 트레이드오프를 평가하는 방법도 설명한다.

### 월드 모델에서 영상 인텔리전스로: NVIDIA Cosmos를 활용한 Milestone Systems
https://www.youtube.com/watch?v=tKg0yX2fjiM

- NVIDIA와 Milestone이 함께 진행한 라이브스트림으로, 월드 파운데이션 모델을 산업용 영상 이해 솔루션으로 전환하는 방법을 다룬다.
- NVIDIA Cosmos에 도메인 특화 데이터와 평가 파이프라인을 결합해 특수 목적 AI를 만드는 과정을 설명한다.
- NVIDIA Cosmos를 파인튜닝한 Accidents VLM을 시연하며, 복잡한 교통 상황에서 측정 가능한 성능 향상을 보여준다.
- 실제 데이터와 합성 증강 데이터가 희귀 이벤트와 엣지 케이스를 처리하는 데 어떻게 기여하는지 다룬다.
- 도메인 특화 파인튜닝과 평가 파이프라인이 모델의 견고성과 일반화를 어떻게 개선하는지 공유한다.

## NAVER D2

### 로그인 화면, 이제 만들지 마세요 - n3r OIDC
https://www.youtube.com/watch?v=8Qewc762FuE

- NAVER Engineering Day 10th에서 발표된 세션으로, n3r.iam을 OIDC Provider로 확장하는 방법을 소개한다.
- 어떤 서비스에든 'n3r 계정으로 로그인' 기능을 붙이는 방식을 다룬다.
- n3r의 프로젝트·역할 정보를 표준 토큰에 담아내는 설계 결정을 공유한다.
- n3r은 네이버 사내 쿠버네티스 플랫폼이다.
- 발표는 로그인 화면을 만들 필요가 없는 이유, n3r.iam OIDC 적용 방법, 설계 결정과 다음 단계 순서로 구성된다.
