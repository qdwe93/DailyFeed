# Tech Feeds — 2026-11-24

## NAVER D2

### Jetpack Compose 기반 커스텀 3D 캐러셀 개발기
원문: https://d2.naver.com/helloworld/2957037

- NAVER Engineering Day 10th에서 공개된 세션으로, ThingsBook Tech의 윤여준이 ThingsBook 서비스의 카드 덱 UI를 개발한 경험을 공유한다.
- 카드가 비스듬히 겹쳐 쌓이고 넘길 때마다 간격과 기울기가 변하는 3D 카드 덱을 LazyRow 대신 Jetpack Compose로 직접 구현했다.
- Float 값 하나로 모든 카드를 움직이는 구조를 통해 매 프레임 변하는 값을 리컴포지션 없이 화면에 반영하는 방법을 설명한다.
- 3D로 기울인 UI에서 터치 영역이 어긋나는 버그를 직접 판정으로 해결한 과정과 LazyRow 없이 Paging3의 다음 페이지 로드를 제어한 방법을 다룬다.
- 복잡한 인터랙션 UI나 성능·설계에 관심 있는 Android 개발자 및 AI를 활용해 복잡한 UI를 만들고 싶은 개발자를 대상으로 하며, AI와 함께 만들며 빨라진 부분과 안 됐던 부분도 소개한다.

### 부족한 건 모델이 아니라 팀 문서였다: 팀 공유 지식층 Third Brain 구축기
원문: https://d2.naver.com/helloworld/2622882

- NAVER Engineering Day 10th에서 발표된 세션으로, NAVER 테크 플랫폼에서 Observability를 담당하는 이권재와 김보규가 작성했다.
- AI가 답을 맞히지 못하는 이유가 모델 자체가 아니라 팀 문서의 부재에 있음을 확인한 과정을 다룬다.
- 팀 위키를 AI가 읽고 쓸 수 있는 공유 지식층인 'Third Brain'으로 구축해 운영한 경험을 공유한다.
- 목차에는 문서를 작성할 위치, 문서 업데이트 주체, AI가 작성한 내용의 신뢰성과 실제 동작 여부 등이 포함된다.
- 팀 지식을 정리하는 방법을 고민하는 개발자를 주요 발표 대상으로 삼고 있다.

### Devops Agent 리포트 오이데~ 평가 야호~
원문: https://d2.naver.com/helloworld/0118355

- NAVER Engineering Day 10th에서 공개된 세션으로, 네이버 검색 FE Infrastructure 팀의 윤정현과 조문기가 발표했다.
- 통합검색 알람이 발생했을 때 1분 이내에 장애 1차 진단 리포트를 이슈로 남기는 Devops Agent를 소개한다.
- 에이전트가 생성한 진단 리포트 결과를 평가해 시스템 정확도를 도출한 이야기를 다룬다.
- 목차는 Devops Agent 소개와 에이전트 특성으로 인한 문제, 평가 기준 설정, 평가 시스템 구성·구축 및 미래 방향으로 구성된다.
- LLM 기반의 이상 신호 분석 시스템이나 평가 시스템을 운영하려는 독자를 발표 대상으로 한다.

### 온톨로지, 구축에서 활용까지. 질문이 답을 설계한다.
원문: https://d2.naver.com/helloworld/5037527

- NAVER Engineering Day 10th에서 공개된 세션으로, NAVER Cloud의 FDE(Forward Deployed Engineer) 이영륜이 물류회사 가상 사례를 통해 온톨로지의 구축과 활용 전 과정을 소개한다.
- 스키마 대신 고객 질문에서 출발해 Object, Property, Link, Action 네 요소를 도출했으며, 데모 모델은 Object Type 60개, Link 63개, Action 31개로 구성되었다.
- 화면 데모에서는 Explorer·에이전트·운영 앱이 같은 모델로 답을 내고 용어를 정규화하며, Human 승인이 필요할 때 에이전트가 승인 대기 상태로 정지하는 과정을 보여준다.
- LLM 단독의 환각 위험과 RAG의 최신 상태 보장 어려움에 비해 온톨로지는 정확한 조회와 쓰기 Action을 지원하지만 가장 높은 비용이 든다고 비교한다.
- 고객 요구를 여섯 가지 항목으로 분해하는 FDE의 역할을 설명하며, 온톨로지가 모든 질문의 정답은 아니므로 질문에 가장 맞는 도구를 골라야 한다고 정리한다.

### Spark 배치 파이프라인 Distributed Tracing 도입
원문: https://d2.naver.com/helloworld/2526679

- 2026년 11월 23일 NAVER D2에 등록된 글로, 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th 발표 세션을 공개한 내용이다.
- NAVER Data Solution 소속 김경범과 박남규가 작성했으며 Spark 배치 처리의 관측성 확보와 성능 최적화에 관심 있는 개발자를 발표 대상으로 한다.
- Apache Spark가 지원하지 않는 분산 추적을 비즈니스 로직 수정 없이 플러그인 형태로 제공해 연관 애플리케이션들을 한 흐름으로 잇는 방법을 소개한다.
- 관측 결과를 성능 개선과 AI Agent 진단에 연결한 경험을 공유한다.
- 목차상 Observability, 분산추적과 OpenTelemetry, 배치 파이프라인, 해결 과정 및 결과와 AI Agent를 순서대로 다룬다.

### GPU 노드 검증 자동화: 상시 점검부터 부하 검증까지
원문: https://d2.naver.com/helloworld/7131556

- 2026년 11월 23일 NAVER D2에 등록된 NAVER Engineering Day 10th 공개 세션이며, NAVER Cloud의 AI Cloud Product 소속 유용혁과 이지환이 작성했다.
- GPU 노드의 하드웨어 고장을 워크로드 시작 전에 찾아내는 검증 시스템을 소개한다.
- 상시 점검, 부하 검증, preflight로 구성된 검증 설계를 Kubernetes Operator로 자동화한 구현 과정과 운영 현황 및 남은 과제를 다룬다.
- Kubernetes 기반 GPU 클러스터 플랫폼 엔지니어와 장애 탐지·검증 자동화를 추진하는 MLOps 및 Infra 엔지니어를 대상으로 한다.
- 대규모 학습 중 느린 노드나 고장 노드를 겪어 본 ML 엔지니어도 발표 대상에 포함된다.

### 뇌를 닮은 세컨드 브레인: 토큰 낭비 없는 RAG
원문: https://d2.naver.com/helloworld/5087915

- 2026년 11월 23일 NAVER D2에 등록된 NAVER Engineering Day 10th 공개 세션으로, NAVER Chat Platform의 신동민이 작성했다.
- 기존 RAG의 텍스트 덤프와 토큰 낭비 한계를 극복하고 인지 메모리 논문 기법을 결합해 지식 자율 진화와 99% 재현율을 달성하는 AI 메모리 아키텍처 Haema(해마)를 소개한다.
- 기억 저장, 불러오기, 작업 기억, 세션 나누기, 판정 게이트로 이루어진 Haema의 층 구조와 질문 처리 여섯 단계 및 긴 대화를 위한 세션 롤오버를 설명한다.
- 문장 고르기, 중복 제거, 통째로 넣는 RAG와의 재현율·토큰 비교, 세션 롤오버, 긴 코딩 과제 기억 시험 등 실측 결과를 제시한다.
- RAG 검색 효율·답변 품질 개선이나 AI 에이전트의 메모리 관리와 토큰 비용 절감에 관심 있는 개발자를 대상으로 팀 적용 시 설정과 측정 지표를 다룬다.

### 새벽 3시 54분, Agent가 먼저 분석하고 처리했습니다
원문: https://d2.naver.com/helloworld/1126768

- 2026년 11월 23일 NAVER D2에 등록된 NAVER Engineering Day 10th 공개 세션으로, NAVER WEBTOON에서 Data Engineering을 담당하는 김시온이 작성했다.
- 개발과 운영 당번을 함께 맡아 새벽 알림에 대응하던 온콜 업무에서 원인 탐색부터 직접 조치까지 AI Agent에게 맡기도록 구성한 열한 달의 경험을 공유한다.
- 1단계인 조사하는 Agent 단계에서는 알림을 한 곳으로 모으고 기억과 지식을 제공하며 응답 형식을 정해 조사 사례를 다룬다.
- 2단계인 손을 쓰는 Agent 단계에서는 능력, 판정, 안전망에 대한 세 가지 기준을 검토하고 무인 조치 사례를 정리한다.
- 개발과 서비스 운영(온콜)을 겸하는 엔지니어, 운영 업무에 AI Agent를 적용하려는 개발자, 사내 Agent 도입을 검토하는 팀을 대상으로 운영 결과와 향후 계획을 제시한다.

### AI 신입사원을 뉴스 데이터 시니어로 키우는 레포, news-data
원문: https://d2.naver.com/helloworld/3284900

- NAVER Engineering Day 10th에서 발표된 세션으로, AI 에이전트가 뉴스 데이터를 직접 찾고 추출·분석까지 수행하는 하네스 레포 news-data를 소개한다.
- 스키마만으로 컬럼 의미를 알기 어렵고 문서가 wiki·GitHub·코드 주석 및 담당자 머릿속에 흩어져 있어 SQL과 Spark는 잘 쓰지만 조직 사정은 모르는 AI 에이전트의 문제를 해결하고자 만들었다.
- 처음부터 문서를 모두 모으지 않고 실제 업무를 맡기며 작업마다 회고를 쓰고 PR로 레포에 되돌리는 작업 루프로 에이전트를 성장시킨다.
- 요청 한 건은 규칙 로드, 스킬 선택, 요청·데이터 파악, 승인 후 실행·검증, 회고·반영의 다섯 단계를 거쳐 처리된다.
- 업무 40건을 처리하며 이슈부터 회고 PR까지 중앙값 1.6시간을 기록했고, 검토 병목·정합성·방향성의 세 가지 한계에 부딪혀 다음 단계로 계획과 실행을 리모트 데이터 에이전트로 옮기는 방향을 제시한다.

## SmartHR Tech Blog

### '개발자 커뮤니티와의 관계 발전 모델' 공개
원문: https://tech.smarthr.jp/entry/2026/11/24/101808

- 2023년 8월 출범한 SmartHR의 DevRel 유닛이 3주년을 기념해 개발자 커뮤니티와의 관계 구축을 다루는 사내 문서인 '개발자 커뮤니티와의 관계 발전 모델'을 공개했다.
- Google 스프레드시트 형태의 이 표는 종합 레벨, 활동 항목, 종합 레벨별 상태 이미지의 세 블록으로 나뉘며 항목마다 5개 레벨을 정의한다.
- SmartHR은 Ruby나 프론트엔드 등 개별 커뮤니티별 표와 일본 개발자 커뮤니티 전체의 종합 레벨만 기록한 표를 만들어 연초 위치를 셀 색상으로 기록해 연도별 추이를 추적하고 DevRel 로드맵을 수립한다.
- 레벨의 기준은 인간관계를 관계 구축기 5계층과 관계 붕괴기 5계층으로 나타낸 'Knapp's relational development model'에서 관계 구축기만 참고해 설정했다.
- SmartHR은 CRE와 Ruby 커뮤니티를 종합 레벨 4로, 그 외 대부분을 레벨 1~2로 두고 있으며, 종합 레벨에 연동되는 활동 항목으로 테크 블로그 전문 지식 발신, 협찬, 이벤트 참가, 이벤트 운영, 등단, 코드 기여의 6가지를 운영한다.

## Toss Tech

### 목적마다, 상품마다 늘던 모델을 하나로: 금융 도메인에 멀티태스크 학습 적용하기
원문: https://toss.tech/article/multi-task-learning-in-finance

- 토스는 새 마케팅 목적이나 상품이 생길 때마다 개별 트리 모델을 하나씩 추가하면서 모델 수가 수십~수백 개로 늘어나 운영과 개선 부담이 커지는 문제를 겪었다.
- 여러 과제를 함께 학습해 얻은 공유 표현을 다른 모델에 전달하던 이전 글(TASTE)과 달리, 이번 글은 금융 도메인에서 여러 과제의 예측값 자체를 하나의 멀티태스크 모델(MTL)로 맞혀 마케팅과 서비스에 바로 적용하는 데 집중했다.
- 개별 모델이 수백 개로 늘어나면 모델별 학습·배포·모니터링 파이프라인과 장애 지점이 증가하고 잦은 재학습과 새 데이터 실험이 어려워지며 데이터가 적은 과제나 신규 상품에는 적용하기 어렵다.
- 멀티태스크 학습은 입력을 요약하는 공통 부분은 공유하고 과제별 예측을 내는 출력층만 분리해 파이프라인과 재학습을 하나로 통합하며, 새 과제는 출력층 추가로, 새 상품은 상품 정보 입력으로 대응해 확장성을 확보한다.
- 토스가 구축한 두 MTL 모델은 예측 대상은 서로 다르지만 사내 ML 플랫폼 위에서 데이터 준비·학습·예측·평가와 매일 재학습이 돌아가는 동일한 뼈대를 공유한다.

## ZOZO TECH BLOG

### '어느 것이 최신?'을 없애다 — md 파일의 SSOT로 시작하는 생성형 AI 활용
원문: https://techblog.zozo.com/entry/20261124-knowledge-base

- ZOZOMO부 OMO블록 팀은 Devin과 Claude 등 여러 LLM을 개발·운영에 활용하면서 Slack·Confluence·Box의 정보를 원정보로 취급하고 Git으로 관리하는 md 파일만을 신뢰할 수 있는 유일한 정보원(SSOT)으로 정했다.
- 원정보를 생성형 AI에 직접 읽히면 다른 프로젝트 내용에 필요한 정보가 묻히고 오래되거나 모순된 정보가 섞여 잘못된 답이 나오며 토큰 소비 비용도 커지는 문제가 발생했다.
- 변경 이력과 리뷰가 남고 AI가 직접 읽고 쓰며 차분을 검토하기 쉽도록 Git과 md 형식을 선택했으며, 각 기사에는 출처 URL을 남기고 Slack·Confluence·Google Meet 회의록 등에서 필요한 내용을 추출해 등록하는 흐름을 지향한다.
- SSOT의 정확성을 유지하기 위해 기사마다 유효·초안·비권장·아카이브 상태와 리뷰 주기를 부여하고 린터와 CI 검증, 신선도 및 링크 헬스 체크, 생성형 AI를 통한 기사 간 사실 모순 검출을 자동화했다.
- 개발 중에는 MCP를 통해 리포지토리를 벗어나지 않고 지식을 검색·등록할 수 있으며, Claude Code의 Routines를 사용해 아직 동기화되지 않은 머지 PR을 1회 최대 5건씩 꺼내 도메인 규칙이나 API·DB 설계 등의 변경 사항을 지식 베이스에 반영한다.

## Google Official Blog

### Introducing file slicing controls in the Gemini API
원문: https://blog.google/innovation-and-ai/technology/developers-tools/file-slicing-controls/



### A more tailored Google Search that’s uniquely yours
원문: https://blog.google/products-and-platforms/products/search/google-search-personal-intelligence-apps/



### Organize and share your holiday memories with these five updates in Google Photos.
원문: https://blog.google/products-and-platforms/products/photos/google-photo-tools-holiday-season-2026/



### See what 6 builders are making with Gemini 4 Hydrogen
원문: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-hydrogen-builders/



### Gemini Canvas로 활용할 수 있는 4가지 기능
원문: https://blog.google/innovation-and-ai/products/gemini-app/gemini-canvas-tasks/

- Gemini Canvas는 채팅 화면 옆에 배치되는 대화형 작업 공간을 제공한다.
- 3D 시각화 도구나 브라우저에서 플레이할 수 있는 게임 등의 웹 앱과 미니게임을 제작할 수 있다.
- 노트나 PDF 파일을 대화형 퀴즈, 플래시카드, 샌드박스 형태의 맞춤형 학습 도구로 변환할 수 있다.
- 스프레드시트를 매출 추적기, 가격 계산기, 작업 목록 같은 업무 생산성 도구로 바꿀 수 있다.
- 캔버스에서 텍스트를 직접 강조 표시해 어조를 조정하거나 문구를 다듬고 제안서 구조를 재편집할 수 있다.

## OpenAI

### Richpanel, 30일 만에 고객 지원 업무 50% 자동화 지원
원문: https://openai.com/business/customer-stories/richpanel-ai-customer-support

- Richpanel은 AI 고객 지원 에이전트의 도구 및 절차 구성에 GPT-6 Astra와 GPT-6.1 Sol을 사용하고, 고객 대화 처리에는 GPT-6 Luna를 활용한다.
- 현장 배치 엔지니어 역할을 대신해 에이전트 설정을 담당하는 AI 관리자인 Boss AI를 구축해 일선 지원 에이전트, 코파일럿, 품질 보증 에이전트의 도구 호출 절차를 작성하도록 했다.
- Boss AI에는 다른 에이전트가 따를 도구와 절차를 생성할 때 정확도를 우선시해 GPT-6 Astra와 GPT-6.1 Sol이 적용된다.
- 수십만 건의 대화를 처리하는 일선 지원 에이전트와 코파일럿, 품질 보증 에이전트에는 상호작용당 비용과 지능의 균형을 고려해 GPT-6 Luna 등 경제적인 모델을 사용한다.
- Richpanel CEO Amit RG에 따르면 회사는 2026년 10월 인터뷰 시점 기준 직전 6개월 동안 약 300건의 AI 고객 지원 도입을 완료했다.

### OpenAI와 Cisco, Shirudo 소개
원문: https://openai.com/index/introducing-shirudo

- OpenAI와 Cisco는 보안 팀이 패치를 배포하는 동안 리눅스 시스템을 보호할 수 있도록 지원하는 오픈소스 런타임인 Shirudo를 출시합니다.
- 통제된 테스트에서 Codex가 생성한 쉴드는 실행 중인 Elasticsearch 서비스를 재시작하지 않고도 Java4Shell 익스플로잇 시도를 차단했습니다.
- Shirudo는 리눅스 eBPF 기술을 사용해 의심스러운 활동을 관찰하고, 정상 요청은 통과시키면서 취약점을 노출하는 동작을 차단하는 쉴드를 사전 모니터링과 운영자 승인을 거쳐 실행 중인 시스템에 배포합니다.
- 또한 보안 팀이 배포 권한을 유지한 상태에서 에이전트가 프로그래밍 가능한 제어 기능으로 취약점을 조사하고 표적 쉴드를 개발·검증할 수 있도록 설계되고 있습니다.
- 쉴드는 로드 전 암호화 서명·검증과 리눅스 eBPF 검증기 및 커널 보안 제어를 거치며, TPM(Trusted Platform Module)을 통해 보호 기능의 로드·제거에 대한 검증 가능한 기록을 지원합니다.
