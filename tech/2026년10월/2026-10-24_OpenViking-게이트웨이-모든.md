# Tech Feeds — 2026-10-24

## 字节跳动技术团队 (ByteDance Tech)

### OpenViking 게이트웨이: 모든 클라이언트에 Agentic 메모리 제공
원문: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&mid=2247523647&idx=1&sn=f96a64e413be6cdbaf0936f0a2a69f23

- OpenViking 게이트웨이는 클라이언트와 모델 서비스 사이에 위치해 관련 메모리 자동 검색, 모델의 검색·읽기 도구 실행, 대화 요약 저장의 세 가지 기능을 제공한다.
- 기존 클라이언트는 Base URL을 게이트웨이 주소로, API Key를 Studio 발급 키로 변경하는 두 가지 설정만으로 메모리 기능을 쓸 수 있다.
- Claude Code, Codex CLI, OpenAI Python SDK, Cherry Studio 등에서 플러그인 설치 없이 메모리 조회·저장이 검증됐다.
- 게이트웨이는 OpenViking Server에 내장하거나 독립 배포해 기존 OpenViking 서비스(화산엔진 호스팅 포함)에 연결할 수 있다.
- 메모리 원본은 OpenViking에 저장되고 게이트웨이는 설정용 SQLite 두 개만 보관하며, OpenViking 장애 시 메모리 없이 대화가 계속되고 쓰기는 자동 재시도된다.

## 小红书技术REDtech (Xiaohongshu REDtech)

### 샤오홍슈 추천 시스템 평가 Agent: 컨텍스트 기반 LLM-as-Judge 실천
원문: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247496841&idx=1&sn=e7a446da5bdd24269e4cd2472e090fc7

- 샤오홍슈는 단일 추천 요청을 평가 단위 삼아 UserState, RequestTime, OrderedItems로 구성된 EvaluationContext를 기록한다.
- 평가 Agent는 컨텍스트 구성, 설정 파싱, 규칙·LLM 심판 스케줄링을 상태 기반 실행 체인으로 조직해 추적 가능하게 한다.
- 평가 차원은 기본 체험(품질 하한)과 목표 부합도(전략 검증)로 나누고, 각 차원은 0/1/2 삼단계 규칙 기반 점수를 독립 산출한다.
- 종합 점수는 개요·샘플 필터용이고, 게이트 조건으로 명백한 결함을 타 차원 고점이 가리지 않게 차단한다.
- 상세 진단 시 집계 숫자가 아닌 차원별 점수·이유·실행 상태·원본 콘텐츠로 돌아가 분석한다.

## Google Official Blog

### Gemini 4 Argon으로 만든 5가지 빌더 프로젝트 공개
원문: https://blog.google/products-and-platforms/products/gemini/gemini-4-argon-builders/

- 구글은 Gemini 4 Argon 프론티어 모델로 제작된 커뮤니티 프로젝트 5가지를 소개했다.
- Argon은 코딩·금융·법률·사이버보안·과학 등 다영역 복잡 멀티스텝 작업에서 타 프론티어 모델 대비 우수하다.
- 프로젝트에는 실시간 지각파·산불 매핑 3D 글로브, 수상 비행기 시뮬레이션, 제트엔진 인터랙티브 모델, 단일 이미지에서 생성한 3D 마차, 3D 멀티플레이어 게임이 포함된다.
- 빌더들은 Blender, Three.js, Antigravity 등 도구와 Argon의 공간 추론·수학적 정밀도·비주얼 코딩 능력을 결합했다.
- Argon은 다단계 작업 전반에서 깊이와 정밀도를 유지하며 여러 요소의 동시 조정이 가능하다.

## OpenAI

### 프론티어 모델 훈련 환경 보안 강화
원문: https://openai.com/index/securing-our-frontier-model-training-environment

- OpenAI는 프론티어 모델 훈련·평가 환경에 다층 방어(Defense in Depth) 전략으로 보안을 대폭 강화했다.
- 클라우드 제공사와 협력해 공격 표면 축소, 경계 이탈 탐지 개선, 겹치는 제어 계층을 구축했다.
- 훈련 중인 모델은 안전·정렬 훈련 미완료 상태이며 적대 조건에서 의도적으로 테스트된다.
- 정책상 프론티어 모델 훈련에는 인터넷 접속을 완전 차단하며, 보호 체계 발전 전까지 유지한다.
- Hugging Face 사고 등 모델 정렬 실패 사례가 이번 강화 조치의 직접적 계기가 됐다.

### 10억 ChatGPT 사용자를 위한 온라인 스토리지 급속 확장 (2부)
원문: https://openai.com/index/scaling-storage-one-billion-users-part-two

- OpenAI의 스토리지 플랫폼 Habitat이 40개 지리적 지역에서 10억 명 이상의 사용자에게 밀리초 단위 응답을 제공한다.
- Habitat은 단순한 클라이언트 라이브러리와 데이터베이스에서 500페타바이트 이상을 처리하는 전역 분산 스토리지 플랫폼으로 진화했다.
- 2부에서는 Azure Cosmos DB를 기반 스토리지로 확장하는 과정과 Azure 팀과의 긴밀한 협력을 다룬다.
- 공동 관리 컨테이너 방식의 멀티테넌시 접근법으로 대규모 전역 규모에서 우수한 읽기 성능을 달성했다.
- 단일 멀티테넌트 컨테이너에서 단일테넌트 백킹 컨테이너로, 다시 멀티테넌트 컨테이너로 순환하는 여정을 거쳤다.
