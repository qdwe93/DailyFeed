# YouTube Tech — 2026-11-24

## NAVER D2

### Spark 배치 파이프라인 Distributed Tracing 도입
https://www.youtube.com/watch?v=j5JTYVcYNC0

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- Apache Spark가 지원하지 않는 분산 추적을 비즈니스 로직 수정 없이 플러그인 형태로 제공하는 방법을 소개한다.
- 분산 추적을 통해 배치 파이프라인 내 연관된 애플리케이션들을 하나의 흐름으로 연결하는 해결 과정을 다룬다.
- 관측 결과를 성능 개선과 AI Agent 진단에 연결해 활용한 경험과 결과를 공유한다.
- Observability와 OpenTelemetry 개념을 포함하며 Spark 배치 처리의 관측성 확보와 성능 최적화에 관심 있는 개발자를 대상으로 한다.

### GPU 노드 검증 자동화: 상시 점검부터 부하 검증까지
https://www.youtube.com/watch?v=bbIkpqdsKQg

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 워크로드가 시작되기 전에 GPU 노드의 하드웨어 고장을 탐지하는 검증 시스템을 소개한다.
- 상시 점검, 부하 검증, preflight로 구성된 검증 설계와 이를 Kubernetes Operator로 자동화한 구현 과정을 다룬다.
- 검증 시스템 도입의 필요성과 함께 실제 운영 현황 및 남은 과제를 공유한다.
- Kubernetes 기반 GPU 클러스터를 운영하는 플랫폼 엔지니어, MLOps 및 Infra 엔지니어, ML 엔지니어를 대상으로 한다.

### 뇌를 닮은 세컨드 브레인: 토큰 낭비 없는 RAG
https://www.youtube.com/watch?v=-bt-Jci53no

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 기존 RAG의 텍스트 덤프 방식과 요청마다 토큰이 다시 읽히며 발생하는 토큰 낭비 문제를 다룬다.
- 인지 메모리 논문 기법을 결합해 지식 자율 진화와 99% 재현율을 달성하는 AI 메모리 아키텍처 Haema(해마)의 구조를 소개한다.
- 구현 후 측정한 결과와 실제 팀에 적용하는 내용을 목차로 구성하여 설명한다.
- RAG의 검색 효율 및 답변 품질 개선과 AI 에이전트 메모리 관리 및 토큰 비용 절감에 관심 있는 개발자를 대상으로 한다.

### 새벽 3시 54분, Agent가 먼저 분석하고 처리했습니다
https://www.youtube.com/watch?v=I3Is_hHuRUI

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션이다.
- 개발과 운영 당번을 함께 맡으며 새벽 알림에 대응하는 업무에서 원인 파악부터 직접 조치까지 AI Agent에 맡긴 경험을 공유한다.
- 발표 내용은 어느 조직에나 있는 운영 문제에 대한 도입부로 시작해 1단계 '조사하는 Agent', 2단계 '손을 쓰는 Agent', 결론 순으로 구성된다.
- 개발과 서비스 온콜 운영을 겸하는 엔지니어와 AI Agent에게 조사·조치 같은 실제 운영 업무를 맡기려는 개발자를 주요 대상으로 한다.
- 사내 환경에서 Agent 도입을 검토하는 팀이 참고할 수 있는 단계별 적용 사례를 다룬다.

### AI 신입사원을 뉴스 데이터 시니어로 키우는 레포, news-data
https://www.youtube.com/watch?v=OcjEEEgL8Do

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션이다.
- AI 에이전트가 뉴스 데이터를 직접 찾고 추출·분석까지 수행하는 하네스 레포지토리 'news-data'를 소개한다.
- 작업마다 배운 내용을 회고와 PR로 되돌려 도메인을 모르던 에이전트를 시니어 수준으로 성장시키는 과정과 운영 중 겪은 한계 및 향후 방향을 공유한다.
- AGENTS.md, 스킬, 규칙 등으로 에이전트의 작업 방식을 설계하거나 사내 도메인·데이터 업무를 맡기려는 개발자와 데이터 엔지니어·분석가를 대상으로 한다.
- 스키마의 한계와 흩어진 문서 등 도입 배경부터 배운 순서대로 지식을 쌓고 스스로 점검하며 실제 업무를 처리하는 방식, 한계와 향후 방향 순으로 진행된다.

## kakao tech

### 같은 문장인데 토큰이 달라지는 이유 | 음성 언어모델은 어디서부터 시작될까? LM-SPT 개발 및 모델 적용기 | Model & Agent
https://www.youtube.com/watch?v=8GQQaDh1_ac

- 카카오의 기술 행사 ifkakao26에서 진행된 세션 영상이다.
- 최신 음성 언어모델의 성능과 효율을 좌우하는 '음성의 토큰화' 방식을 핵심 주제로 다룬다.
- 기존 코덱의 한계를 보완하기 위해 자체 개발한 새로운 음성 코덱 'LM-SPT'의 설계 과정을 설명한다.
- 자체 개발한 'LM-SPT'를 카카오의 옴니모달 모델 'Kanana-o'에 적용해 얻은 결과를 공유한다.
- 카카오에서 멀티모달 및 옴니모달 언어모델을 연구·개발하는 조대진과 강우영이 발표를 맡았다.

## Cole Medin

### 해커들이 노리는 AI 코딩 에이전트 보안 강화 방법
https://www.youtube.com/watch?v=0q0UbO4oqgQ

- 공격자들이 AI를 활용해 취약점을 더 빠르게 찾고 악용하며 최근 다수의 공격이 코딩 에이전트를 직접 겨냥하고 있다는 점을 다룬다.
- 백도어를 다운로드하는 설정 파일과 키를 탈취하는 패키지 등 최근 몇 주간 실제 발생한 공격 사례를 소개한다.
- 대화 기록에 남은 자격 증명, 허용 목록에 저장된 비밀번호, 탈취된 AI 키를 악용하는 LLM재킹(LLMjacking) 등 주요 보안 위협을 설명한다.
- 에이전트가 실행하는 내용을 점검하고 모든 API 키에 한도를 설정하며 비밀 정보를 에이전트로부터 분리하는 기본 보안 조치를 안내한다.
- 시크릿 보호 훅(secrets guard hook)이 포함된 무료 agent-config-audit 스킬을 GitHub에 공개하고 에이전트 설정 전체를 감사하는 실행 과정을 시연한다.

## Claude

### 이번 달 Claude의 모든 신규 업데이트
https://www.youtube.com/watch?v=EuOg5f_Egns

- 지난 달 출시된 Claude의 주요 신규 기능과 함께 놓치기 쉬운 소규모 업데이트들을 소개한다.
- 주요 출시 항목으로 Claude Fable 5.2, Claude Duet, Personal Finance in Claude를 다룬다.
- 추가 업데이트 항목으로 Claude Meetings와 Claude Whiteboards, Claude Sheets, Claude Data를 안내한다.
- 인터랙티브 커넥터(Interactive connectors)와 데스크톱용 Claude Code(Claude Code on desktop) 업데이트도 함께 포함한다.
- 소개된 기능 중 여러 항목이 베타 단계이거나 순차적으로 배포 중이며 설명란의 링크를 통해 각 항목의 세부 내용을 확인할 수 있다.

## Google Cloud Tech

### 구글 엔지니어들이 프로덕션 환경에서 AI 에이전트를 구축하는 방법 (전체 로드맵)
https://www.youtube.com/watch?v=BKVDdL1InsA

- 구글 엔지니어 5명이 제미나이 같은 모델을 기반으로 프롬프트 엔지니어링에서 벗어나 루프 및 하네스 엔지니어링으로 전환하는 프로덕션 AI 에이전트 아키텍처를 설명한다.
- 1단계(Learn)에서는 간결한 맵과 영구 마크다운 메모리로 컨텍스트를 관리하며, 오픈소스 Agent Skills와 Google Cloud Developer Plugin이 발견·활성화·실행의 3단계 점진적 공개를 통해 컨텍스트 창을 초과하지 않고 도메인 지식을 제공한다.
- 2단계(Guard)에서는 에이전트가 테스트를 우회해 통과시키지 못하도록 빠르고 결정론적인 가드레일, Git 훅, 시크릿 스캐너, 엄격한 재시도 제한으로 에이전트 동작을 통제한다.
- 3단계(Review)에서는 대화형 요약, Repo Walkthrough 시각화 도구, 제미나이를 활용한 멀티모달 UI 비디오 QA, 오디오 리뷰로 대규모 AI 생성 풀 리퀘스트를 검토하는 방법을 다룬다.
- 4단계(Score)에서는 도구 사용, 비결정론적 궤적, 멀티턴 메모리, 멀티 에이전트 핸드오프를 다루는 4가지 실전 평가 패턴을 소개한다.

## AWS Developers

### Strands Box로 명령어 한 줄에 AI 에이전트 샌드박스 실행하기
https://www.youtube.com/watch?v=Z18kFF3uhSA

- Strands Box는 AWS가 공개한 무료 오픈소스 에이전트 샌드박스로, Mac과 Linux에서 컨테이너나 VM, AWS 계정 없이 명령어 하나로 Claude Code, Codex, Kiro CLI의 접근 범위를 제한해 실행한다.
- Open, Scoped, 읽기 전용 정책을 바탕으로 에이전트가 접근할 파일, 네트워크 대상, 도구를 선택할 수 있으며 Amazon Bedrock 사용 등 기존 Claude Code 설정을 가져와 초기 프로필을 구성한다.
- 데모에서는 .env 파일 읽기를 차단하는 과정과 Dogwood 정책 및 사용자 정의 Slack 프로필 구성을 시연한다.
- 에이전트가 실제 토큰을 확인하지 못하도록 하는 자격 증명 주입 방식과 감사 로그 및 10분 규칙을 설명한다.
- 정책 편집과 원격 에이전트 실행, 그리고 실행 중 정책 변경 방법을 다룬다.

## Google Cloud Tech

### 단순 RAG가 에이전트 메모리로 실패하는 이유와 대안
https://www.youtube.com/watch?v=gau6i7AJ6jw

- 단순 벡터 RAG는 "뉴욕에서 샌프란시스코로 이사했다"와 같은 정보 변경 시 두 진술을 모두 검색해 충돌을 해결하거나 어느 쪽이 현재 사실인지 구분하지 못한다.
- 이 영상은 플랫 프롬프팅(Flat Prompting), 벡터 DB 기반 단순 RAG(Naive RAG), 오픈 지식 그래프(Open Knowledge Graphs) 등 3가지 표준 에이전트 메모리 옵션을 비교한다.
- Gemini 플랫폼의 Vertex AI Memory Bank가 백그라운드에서 비동기로 실행되며 엔티티 추출, 중복 제거, 충돌 해결, 사실 업데이트를 몇 줄의 코드로 처리하는 방식을 설명한다.
- Laxmi Harikumar와 Miles Libbey가 발표자로 참여하며 제목 아래 링크된 AI Agent Clinic 전체 빌드 에피소드를 안내한다.
- 관련 제품 및 태그로 Antigravity, Gemini, Gemini 플랫폼, Google Cloud, Agent Development Kit(ADK), Vertex AI Memory Bank가 명시되어 있다.

## Google for Developers

### Google Antigravity 활용 사례: 오프라인 야생동물 도감 만들기
https://www.youtube.com/watch?v=fpQcDQJQLhg

- Google for Developers 채널의 영상으로, 크리에이티브 테크놀로지스트 겸 하드웨어 빌더 Arden Schager(xWF)가 GemmaDex 제작 과정을 시연한다.
- GemmaDex는 포켓 크기의 100% 오프라인 야생동물 및 식물 도감으로, Raspberry Pi 5에서 실행된다.
- 이 프로젝트는 Antigravity와 Gemma 4를 활용해 구현되었다.
- 영상 메타데이터에는 언급된 제품으로 Antigravity와 Gemma가 명시되어 있다.
- 설명란에서는 Antigravity 개발 리소스 링크와 Gemini 4 Neon 안내 링크를 함께 제공한다.

## OpenAI

### GPT-6 Cyber로 리눅스 취약점 조사하기
https://www.youtube.com/watch?v=w-ltt0Np2cY

- OpenAI 채널의 영상으로, GPT-6 Cyber를 활용해 리눅스 취약점을 조사하는 내용을 다룬다.
- 한 차례의 실행에서 GPT-6 Cyber는 948개의 리눅스 커널 취약점을 검증하고 사람이 검토할 수 있는 후보 패치를 생성하는 데 활용되었다.
- 사이버 연구원 Kyle Zeng과 응용 사이버 연구 리드 Clint Gibler가 대담에 참여한다.
- 두 사람은 취약점 연구 파이프라인을 구축한 방법과 리눅스 메인테이너들과 협력해 수정 사항을 업스트림에 반영한 과정을 논의한다.
- 설명란에는 전체 연구 내용을 확인할 수 있는 OpenAI 링크가 첨부되어 있다.

## Claude

### Claude의 CRISPR 유사 패턴 발견 설명
https://www.youtube.com/watch?v=ANcPabMDH14

- Claude 채널에서 공개한 영상으로, Claude의 CRISPR 유사 발견을 설명한다.
- 본문은 CRISPR가 세균 DNA의 특이한 반복 패턴에서 시작되어 이를 설명하는 데 수년이 걸렸다고 언급한다.
- Claude는 최근 바이러스 DNA에서 이와 유사해 보이는 패턴을 포착했다.
- 현재 Anthropic 과학자들이 이 패턴에 대한 실험을 진행하고 있다.
- 진행 중인 실험은 바이러스 DNA의 해당 패턴이 CRISPR와 비슷하게 작동하는지 알아보기 위한 것이다.

## NVIDIA Developer

### NVIDIA와 Together AI: 모든 워크로드를 위한 더 빠르고 비용 효율적인 AI 추론
https://www.youtube.com/watch?v=ClfOWvsj164

- NVIDIA Developer 채널의 영상으로, Together AI 엔지니어링 팀이 AI 추론 워크로드 배치 방식을 설명한다.
- 새로운 GPU 세대가 나오더라도 모든 워크로드를 이전할 필요는 없다는 점을 다룬다.
- Together AI 엔지니어들은 메모리 요구량, 지연 시간 목표, 서빙 비용을 기준으로 워크로드를 NVIDIA Hopper와 Blackwell에 매칭한다.
- CUDA를 활용해 Hopper와 Blackwell 두 환경 모두에서 최적화를 수행한다.
- 영상은 모든 워크로드에 대해 더 빠르고 비용 효율적인 AI 추론을 구현하는 방안을 주제로 한다.

## kakao tech

### 남산타워까지 알아본 비전 인코더의 학습법 | Kanana Vision Encoder: 글로벌 최고 수준에 도전하는 자체 비전 인코더 개발기 | Model & Agent
https://www.youtube.com/watch?v=X7nW9HABy8M

- 카카오가 자체 기술력으로 밑바닥부터(From scratch) 학습한 카나나 비전 인코더의 개발 과정을 다루는 if kakao 26 발표 영상이다.
- 카나나 조직에서 멀티모달 언어모델을 연구·개발하는 카카오 엄지환(Polar)이 발표자로 참여했다.
- 다음 토큰 예측을 기반으로 카나나 언어모델을 활용해 학습과 추론 모두에서 효율을 높인 설계를 소개한다.
- 온디바이스 환경 적용을 위한 비전 인코더의 경량화 과정을 공유한다.
- 언어모델이 발전할수록 비전 인코더도 함께 발전하는 선순환 구조를 다루며 세션 발표 자료 링크를 함께 제공한다.
