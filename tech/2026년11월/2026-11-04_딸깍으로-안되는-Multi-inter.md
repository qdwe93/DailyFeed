# Tech Feeds — 2026-11-04

## NAVER D2

### 딸깍으로 안되는 Multi-interest 개발기
원문: https://d2.naver.com/helloworld/9639872

- NAVER Engineering Day 10th에서 발표된 세션으로, 다양한 관심사 추천 모델인 Multi-interest를 여러 지면에 적용하며 겪은 문제 해결 과정을 공유한다.
- Multi-interest 추천 모델(MINER)의 KREAM 실서비스 적용 사례를 주제로 다룬다.
- 인기 상품 목록에서 특정 상품이 전체 유저에게 동시 노출되는 hubness 문제가 발생했다.
- 점수를 유저 의존 성분과 유저 무관 성분으로 분해하고 가설 3개를 실측으로 검증했다.
- 유저 무관 성분 제거(centering, bias 분리), 추천 결과 다양화, 분포 지표 기반 평가 체계 도입으로 과노출 상품이 전량 제거되고 노출 상품 종류는 25% 늘었으며 구매 지표는 유지됐다.

### FE News 26년 11월 소식을 전해드립니다
원문: https://d2.naver.com/news/1095957

- Tailwind Labs가 Shopify에 합류하며 Tailwind CSS 등 오픈소스 프로젝트는 계속 MIT 라이선스로 남고 Tailwind 팀이 Shopify의 지원을 받아 유지보수를 이어간다.
- Cloudflare와 VoidZero가 TypeScript 컴파일러를 Rust로 옮기는 tsrs를 Oxc 툴체인 안에서 개발한다고 발표했고, 초기 벤치마크에서 TypeScript 7.0보다 최대 8배 빠르고 메모리를 약 70% 덜 썼다.
- React Context 값이 바뀔 때의 재렌더링 비용을 React Compiler로 줄이는 방법을 다룬 글이 소개됐고, 라디오 버튼 5,000개 예제에서 클릭 처리 시간이 useSyncExternalStore 스토어나 React.memo 방식과 비슷한 수준이 됐다.
- React 19.3에서 실험 단계였던 <ViewTransition>과 Fragment Refs가 안정화되고 browser() API와 Trusted Types 지원이 추가됐다.
- Remix 3가 첫 안정 버전으로 출시되어 라우터, 데이터베이스 관리, 스키마 검증, 에셋 서버, React가 아닌 자체 UI 런타임을 담았고, 10월 23일 나온 3.1은 코드 변경 없이 서버 렌더링을 약 두 배 빠르게 했다.

### FE News 26년 10월 소식을 전해드립니다
원문: https://d2.naver.com/news/8711937

- Visual Studio Code 공식 채널이 약 1시간 38분 분량의 다큐멘터리를 공개해 취리히 팀의 Monaco Editor 제작부터 데스크톱 VS Code 발표와 오픈 소스 전환까지를 30여 명의 인터뷰로 다뤘다.
- 2020년 React Native 전면 도입을 선언했던 Shopify가 모바일 앱을 다시 Swift와 Kotlin 네이티브로 옮긴다고 발표했고, Shop 앱은 12주 만에 재구축했다.
- 토스 Front AI 팀이 AI로 만든 결과물을 검증하는 방법을 소개했으며, 코드에서 시나리오를 추론해 E2E 테스트를 자동 생성하려던 시도는 실패한 뒤 테스트를 직접 작성하는 방식으로 진행했다.
- penpot은 브라우저에서 쓰거나 직접 설치해 운영할 수 있는 오픈소스 디자인·프로토타이핑 플랫폼으로, MCP 서버를 통해 AI 에이전트가 컴포넌트·토큰·레이어 구조를 읽고 수정할 수 있다.
- DeepLearning.AI와 JetBrains가 만든 명세 주도 개발 강좌가 마크다운 명세를 먼저 쓰고 코딩 에이전트가 이를 구현하게 하는 흐름을 WebStorm과 Claude Code로 Next.js 예제 앱을 만들며 보여 준다.

## Tabelog Tech Blog

### AI에 QA 판단을 맡기다: AI 트리아지 정확도를 2배로 높인 QA 컨텍스트 설계
원문: https://tech-blog.tabelog.com/entry/connecting-qa-data-for-ai-driven-test-repair

- 먹로그 품질관리부가 QA 업무 전체를 AI가 담당하는 상태를 목표로 추진하는 AI4QA 프로젝트의 3번째로 트리아지와 수정 공정을 AI화한 사례다.
- 여기서 트리아지는 실패한 테스트의 원인이 프로덕트 코드, 요건 정의서, 테스트 중 어디에 있는지를 대략 구분하는 첫 선별 공정이다.
- 테스트 설계서, 실행 결과, 실행 이력, 불량표 4가지를 공통 키로 맞춰 하나의 데이터로 만들어 AI에 전달했다.
- AI에 대한 지시를 세세히 쓰는 대신 AI에 전달하는 컨텍스트를 설계하는 컨텍스트 엔지니어링 방식을 택했다.
- AI가 트리아지부터 수정, 재실행까지의 루프를 돌려 모든 테스트가 성공하는 상태에 도달했고, 실패한 테스트가 1회 수정으로 고쳐진 비율은 42%에서 85%로 올랐다.

## ZOZO TECH BLOG

### Claude Code 스킬로 하는 Google Cloud 비용 월간 예산·실적 관리: 금액은 쿼리, 원인 조사는 AI, 판단은 사람
원문: https://techblog.zozo.com/entry/gcp-cost-management-with-claude-code

- ZOZO 배송 인프라 블록은 PRD·QA·STG·DEV 4개 환경에서 SKU별 월별 견적과 실적을 관리하며, 이 작업에 매달 며칠이 걸렸다.
- BigQuery 요금 내보내기와 Google 스프레드시트를 기반으로 월별 비용 관리를 Claude Code 스킬로 자동화했다.
- 금액은 쿼리로 기계적으로 집계하고 AI에는 차이 원인 추정과 코멘트 작성을 맡기며, 확인과 판단은 사람이 한다.
- 과거 수치와 근거는 모두 스프레드시트에 남기고 스킬에는 작업 절차와 처리만 두었으며, 문제가 없다고 확인된 작업부터 순차적으로 자동화했다.
- 현재는 사람의 확인·판단 외 작업을 모두 스킬 호출로 실행하며, 이 방식은 처음에 Codex로 운영했고 다른 AI 에이전트로도 가능하다.

## 당근 Tech

### 국내 최초 광고 MCP를 출시하며, 개발자의 역할은 어디까지 넓어졌을까?
원문: https://medium.com/daangn/%EA%B5%AD%EB%82%B4-%EC%B5%9C%EC%B4%88-%EA%B4%91%EA%B3%A0-mcp%EB%A5%BC-%EC%B6%9C%EC%8B%9C%ED%95%98%EB%A9%B0-%EA%B0%9C%EB%B0%9C%EC%9E%90%EC%9D%98-%EC%97%AD%ED%95%A0%EC%9D%80-%EC%96%B4%EB%94%94%EA%B9%8C%EC%A7%80-%EB%84%93%EC%96%B4%EC%A1%8C%EC%9D%84%EA%B9%8C-8dea7fe41c07?source=rss----4505f82a2dbd---4

- 당근은 국내에서 처음으로 공식 광고 MCP를 출시했으며, 해외에서는 구글·메타·아마존이 이미 MCP를 공개했다.
- 광고주가 Claude 같은 AI에 광고 성과를 물으면 AI가 광고 MCP를 통해 당근 광고의 계정·광고·성과 데이터를 가져와 답한다.
- 백엔드 엔지니어인 제이크는 개발뿐 아니라 로드맵과 PRD 작성부터 출시까지 맡았고, PRD는 PTBSMAF 프레임워크로 작성했다.
- 범위는 광고주에게 손해가 없는지, AI가 화면보다 편한지, 더 많은 광고주에게 도움이 되는지를 기준으로 정했고 리스크가 낮은 조회 기능부터 열었다.
- API를 그대로 MCP 도구로 만들면 AI가 적절한 도구를 고르기 어려워하고 필요한 정보를 놓쳐 잘못된 답을 할 수 있다는 문제를 확인했다.

## 우아한형제들 기술블로그

### 아이폰 카메라로 B마트 상품을 찾는다고?
원문: https://techblog.woowahan.com/27810/

- 배민은 2026년 8월 아이폰 Visual Intelligence를 앱에 연동해, 검색 결과에서 비슷한 B마트 상품을 바로 확인할 수 있게 했다.
- Visual Intelligence는 카메라나 화면에 보이는 것을 인식해 관련 정보를 보여 주고 여러 앱의 검색 결과로 연결하는 Apple Intelligence 기능이다.
- 사용하려면 iOS 26 이상, iPhone 15 Pro 이상, Apple Intelligence 켜짐 조건을 모두 갖춰야 한다.
- 카메라, 스크린숏, 사진 앱 세 가지 방식으로 검색할 수 있으며 iOS 27부터는 사진 앱에서도 이미지 검색이 가능하다.
- iOS 18에서는 카메라 검색과 Apple·구글 결과만 지원됐지만, iOS 26부터 스크린숏 검색과 서드파티 앱 통합이 가능해졌다.

## 컬리 기술 블로그

### 기획서 하나로 결함 등록까지, QA AI Hub를 만들며 배운 것
원문: https://helloworld.kurly.com/blog/ai-qa-from-spec-to-defect/

- 컬리 QA 트라이브는 테스트 준비에 드는 시간을 줄이기 위해 QA AI Hub 프로젝트를 시작했고, 9개월 뒤 기획서에서 결함 등록까지 이어지는 사내 플랫폼을 만들었다.
- 2025년 실측에서 QA 총 투입 시간의 절반 이상이 테스트 설계와 TC 작성에 쓰였고, 준비 구간 비중은 커머스 50%, 물류 58%, TC 재활용률은 5% 미만이었다.
- QA AI Hub는 요구사항 분석, 테스트 설계, TC 생성, 테스트 실행, 결함 등록의 다섯 단계로 이어지며 앞 단계 산출물이 다음 단계 입력이 된다.
- 서버는 Next.js 15 단일 앱으로 웹 UI·API·SQLite를 맡고, QA 각자 PC의 Node.js 워커가 Claude Code를 헤드리스로 실행해 Playwright와 Mobile MCP로 화면을 조작한다.
- BLOCKED 재분류와 FAIL 확인, 최종 판정은 QA가 맡고, 실행 결과의 FAIL 건은 Jira 이슈 자동 생성으로 이어진다.

## 字节跳动技术团队 (ByteDance Tech)

### 스토리지 에이전트 개선을 추적 가능하게: Storage Agent Family 평가 엔지니어링 실천
원문: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&mid=2247524007&idx=1&sn=a8f5f0e536fc1ef3b0d7d2cc8e0e20cc

- Storage Agent Family는 클라우드에 배포된 지능형 비서 모음으로, 사용자의 클라우드 스토리지 자원 설정 조회, 증설 비용 추정, 접근 장애 진단 등을 돕는다.
- 프롬프트, 스킬, CLI, 실행 프레임워크가 서로 얽혀 한 부분을 고치면 다른 시나리오가 깨질 수 있어, 출시 전 인위적 테스트만으로는 부작용 판단과 문제 위치 파악이 어려웠다.
- 오프라인 회귀 실험으로 변경 후 응답과 도구 호출 과정을 검증하고, 호출 체인(Trace)으로 문제 모듈을 특정하며, 온라인 실제 대화에서 드러난 전형적 문제를 평가 세트에 계속 축적한다.
- 평가 세트는 사용자 의도와 Skill 체인, 경계 조건을 기준으로 구성해 정상 작업 완료뿐 아니라 자원 ID 미제공, 도구 오류, 권한 초과 삭제 같은 예외·월권 요청에 대한 응답도 검사한다.
- LLM 평가자는 과제 이해와 응답 집중, 사실 근거와 신뢰도, 과제 완수도, 능력 경계와 운영 안전, 표현 명확성의 5개 차원을 평가하고, Code 평가자는 빈 응답·실행 오류·도구 호출 제약을 검사한다.

## 小红书技术REDtech (Xiaohongshu REDtech)

### 샤오홍슈 스토리지 기반 분해 02 | AI를 팀의 일원으로: 스토리지 데이터베이스 어시스턴트 실천
원문: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247496958&idx=1&sn=bafda0c7a7030b5542ae6c54f26876d5

- 스토리지 데이터베이스 팀의 AI 어시스턴트 SDBP는 출시 두 달여 만에 1,000여 명의 내부 사용자를 지원하고 수천 건의 문제를 독립적으로 해결했다.
- 일평균 독립 해결 문제 수는 전문가 한 명의 5배 이상이며, 약 30%의 문제는 비업무 시간에 해결됐다.
- 하나의 OpenClaw 인스턴스를 여러 명이 공유하는 방식은 신원·파일·권한 격리 문제가, 개인별 독립 배포 방식은 저빈도 시나리오의 자원 유휴와 상태 복구 문제가 있었다.
- 세션 상태와 실행 환경을 분리해 세션·도구 호출 기록은 PostgreSQL에, 워크스페이스 파일과 읽기 전용 자원은 NFS에 저장해 실행 노드가 교체돼도 작업을 이어갈 수 있다.
- RAG와 LLM Wiki를 시도했으나 원자료에 없거나 낡은 정보를 보완하지 못해, DMS 코드 질의응답 소규모 샘플에서 코드를 지식 소스로 포함한 세 가지 방식을 비교했다.

## Google Official Blog

### 싱가포르 대학들과의 연구 협력 확대
원문: https://blog.google/innovation-and-ai/technology/research/partnering-singapore-advance-scientific-discovery/

- Google은 싱가포르에 새 연구 허브를 설립하고 MedGemma 같은 오픈 모델을 일선 진료 현장에 도입하는 등 기존 보건 연구 이니셔티브를 확장하고 있다.
- NUS와 NTU에 600만 달러 이상의 신규 연구 보조금과 역량 구축 이니셔티브를 투자한다.
- NUS는 3,500건 이상의 글로벌 신청 중 선정돼 신경퇴행성 질환 연구를 위한 AI for Science Google.org Impact Challenge 보조금 150만 달러를 받는다.
- NUS에는 지속 가능한 컴퓨팅과 모델 서빙 최적화, 지역 언어 처리를 위한 50만 달러가, NTU에는 AI 안전·보안 연구 4건을 위한 34만 달러가 지원된다.
- NTU의 75만 달러 AI for Science Capacity Fund Grant는 동남아시아 전역의 상설 연구 역량을 구축하며, Google.org와 Google DeepMind는 INSEAD의 Thrive Lab에 300만 달러를 지원한다.

### 새 연구로 확인된 Guided Learning의 학생 지원 효과
원문: https://blog.google/products-and-platforms/products/education/guided-learning-uk-japan/

- Google은 실제 환경에서 Guided Learning이 학생과 교사를 지원하는 방식을 보여주는 두 건의 새 연구를 공개하고, Google Classroom에 Guided Learning 배포를 시작했다.
- Guided Learning은 직접적인 답을 주기보다 복잡한 개념을 단계별로 이해하도록 돕는 것을 목표로 한다.
- 도쿄대에서 300여 명의 학생을 대상으로 한 무작위 대조 실험에서 표준 웹 도구만 쓴 집단은 5.3%포인트, Guided Learning을 쓴 집단은 8.1%포인트 점수가 올랐다.
- 이는 반나절 학습 세션에서 1.5배 더 높은 학습 성과로, 학생들은 빠른 답 대신 연습 퀴즈와 단계별 도움, 맞춤 시각 자료를 자주 요청했다.
- Ark와 함께 영국 중등학교 3곳에서 4개 과목으로 4주 파일럿을 진행했으며, 교사들은 독립 학습 중 초기 학생 질문을 Guided Learning이 처리해 개별 지원 시간이 늘었다고 평가했다.

### 구글, 교사용 AI를 만드는 단체에 950만 달러 지원
원문: https://blog.google/products-and-platforms/products/education/google-org-funding-ai-education/

- Google.org가 교육자와 함께 AI를 만드는 5개 단체에 950만 달러 이상의 자금을 지원한다.
- 뉴욕시립대(CUNY)는 CITE 이니셔티브를 통해 교육자의 디지털·컴퓨팅 리터러시 함양을 지원한다.
- Fab AI는 Google DeepMind, 게이츠 재단과 협력해 수업 계획과 초기 읽기 지원을 위한 오픈 모델을 만든다.
- Krause Center for Innovation은 학군이 책임 있는 AI 교육을 교실에 도입하도록 돕는다.
- Teaching Lab은 실시간 지원을 제공하는 운영체제 Coherence OS를 시범 운영하고, 1EdTech Global은 신뢰할 수 있는 학습 표준을 위한 공공 인프라를 구축한다.

### 학습 시대의 AI: 구글 교육 포트폴리오 주요 업데이트
원문: https://blog.google/products-and-platforms/products/education/ai-learning-era-2026/

- 구글은 Guided Learning을 Google Classroom에 전 세계적으로 출시한다.
- Guided Learning 기능을 Google Search에도 도입한다.
- Gemini, Gemini Notebook, Gemini in Classroom, Google Search의 K-12 학생 계정 통제 방식에 대한 접근을 업데이트한다.
- 새로운 연구 결과와 Google.org의 신규 자금 지원을 공개한다.
- 교육자 대상 AI 교육을 확대하고, AI in Education 보고서를 함께 공개한다.

### 학습을 위한 책임 있는 AI 설계
원문: https://blog.google/products-and-platforms/products/education/ai-learning-era-updates-2026/

- 구글은 AI 제품이 학생이 압도되지 않으면서 도전을 이어가는 '생산적 고투(productive struggle)'를 지원해야 한다고 본다.
- Gemini의 Guided Learning은 열린 질문과 단계별 분해를 통해 문제 해결 과정을 코칭하는 학습 도구다.
- 구글 연구에 따르면 Guided Learning은 측정 가능한 학습 성과 향상을 보였다.
- Google Search의 Guided Learning은 이번 달 말 미국 일부 학교에서 시범 운영 후 다른 학군으로 확대될 예정이다.
- Google Classroom의 Guided Learning은 오늘부터 전 세계에서 제공되며, 교사에게는 수업 지원이 필요한 지점을 알려주는 실시간 정보를 제공한다.

### 아시아태평양 지역 사기 대응을 위한 협력
원문: https://blog.google/company-news/inside-google/around-the-globe/google-asia/fight-against-apac-scams/

- 유엔 보고서에 따르면 2025년 동아시아, 동남아시아, 호주, 뉴질랜드의 사기 피해액이 최대 1,141억 달러에 달했다.
- ASEAN 소비자의 40% 이상이 사기를 겪었다고 응답했다.
- Android는 AI 기반 전화 사칭을 탐지하는 Fake Call Detection을 출시했고, Pixel에는 주요 메시징 앱의 사기 탐지 기능이 내장됐다.
- Google Play 외부에서 유통되는 악성 앱 대응을 위해 Android 개발자 검증을 확대한다.
- Google.org는 아시아재단과 Tech for Good Institute에 600만 달러를 지원해 소상공인과 개인의 온라인 안전 역량을 높인다.

### 구글 AI 교육자 시리즈, 새 국가로 확대
원문: https://blog.google/products-and-platforms/products/education/google-ai-educator-series-global-expansion-november-2026/

- 구글은 교사들이 즉시 활용할 수 있는 실무 AI 역량을 무료 주문형으로 제공하는 Google AI Educator Series(GES)를 만들었다.
- GES는 올해 초 미국에서 시작해 인도·한국·말레이시아·필리핀·영국 및 아일랜드로 확대됐으며, 향후 브라질·멕시코·스페인·호주·사하라 이남 아프리카에도 제공될 예정이다.
- 인도에서는 9월 교육으로 8만 명의 교육자를 교육했고, 국가교육정책 2020에 맞춰 영어와 6개 현지어로 자기주도 온라인 모듈을 제공한다.
- 필리핀에서는 교육부·고등교육위원회·기술기능개발청과 협력해 100만 명 이상의 교육자에게 AI 교육을 제공하고, 교육부는 GES를 전국 교직원에게 공식 권장하는 메모를 발표했다.
- 말레이시아 교사들은 GES 이후 주제별 교육과정·평가·시각자료 준비에 3~5시간을 절약했다고 보고했으며, 구글은 현지 파트너와 트레이너 양성 부트캠프를 시작할 예정이다.

## Google DeepMind

### 구글 안티그래비티의 에이전트 기반 화학정보학
원문: https://deepmind.google/blog/agentic-cheminformatics-with-google-antigravity/

- 구글 딥마인드는 분자 데이터 정리에 드는 시간을 줄이기 위해 Google Antigravity용 화학정보학 스킬 모음을 만들었다.
- 이 스킬은 언어 모델이 워크플로 조정·데이터베이스 탐색·과학적 추론을 맡고, 결정론적 화학 도구가 분자 계산을 수행하도록 역할을 나눈다.
- 스킬은 20년 넘게 개발된 오픈소스 화학정보학 툴킷 RDKit과 ChEMBL·PubChem의 정제된 자원 연결을 기반으로 하며, 도메인 모범 사례를 에이전트 워크플로에 담았다.
- 같은 분자가 논문의 IUPAC 이름, 특허의 Markush 구조, 카탈로그의 SDF 등 여러 형태로 존재하고 오류가 생길 수 있어, 원자나 결합 하나만 바뀌어도 다른 화합물이 된다.
- 글은 약효를 높이는 고전적 기법인 경직화를 예로 들며, 회전 결합으로 여러 3D 형태를 취하는 유연한 분자가 표적에 결합하려면 하나의 활성 형태로 고정돼야 한다고 설명한다.

## OpenAI

### 시스코, OpenAI로 머신 속도 방어 강화
원문: https://openai.com/index/cisco-cyber

- 시스코는 공격자가 AI로 자동화 공격과 익스플로잇을 머신 속도로 확장하는 상황에서, 방대한 네트워크 텔레메트리와 최전선 AI 추론을 결합해 방어를 강화한다.
- 시스코는 단일 보안 경계에서 마이크로서비스·컨테이너·클러스터 전반에 분산된 통제로 전환하고, 각 서비스·컨테이너·클러스터 앞에 소형 보안 스택을 두어 보안을 네트워크 구조에 융합한다.
- 애플리케이션 수준 통제로 각 서비스에 필요한 연결만 허용해 공격자가 확산할 수 있는 경로를 줄이고, 침해 시스템만 선택적으로 격리해 나머지 서비스는 계속 운영할 수 있다.
- AI 모델과 네트워크 인텔리전스를 결합해 머신 규모로 신호를 연관 분석하며, 개별로는 무해해 보이는 두 신호가 함께 의미 있는 패턴을 드러낼 수 있다고 설명한다.
- 시스코는 Daybreak와 GPT-6 Astra를 보안 태세의 단계적 개선으로 평가하며, 취약점 발견·패치와 조사·대응·교정 시간을 단축한다고 밝혔다.

### 헤임스타덴, OpenAI로 주거용 부동산 관리에 AI 도입
원문: https://openai.com/index/heimstaden

- 헤임스타덴은 2025년 6월 AI 투자를 가속하기로 하고 여러 플랫폼을 검토한 뒤 OpenAI를 선택해 직원 역량 강화와 핵심 프로세스 재설계를 추진했다.
- 회사는 AI가 필요를 예측하고 작업을 조정하며 의사결정을 지원하는, 점점 더 자율적으로 운영되는 건물로 나아가는 것을 목표로 한다.
- 공실 발생 시 임대료 산정은 ChatGPT Sites로 만든 도구의 인텔리전스와 권고를 활용하고, 광고는 AI가 이미지 스타일링과 아파트 설명을 작성하며, 에이전트가 모든 광고를 품질 기준과 대조해 검토한다.
- AI가 생성한 시장 피드백으로 임대 팀이 시정 조치를 취하고 가격을 더 동적으로 조정하지만, 의사결정의 검토와 승인은 직원이 맡는다.
- 회사는 부동산 이미지 제작 비용 99% 절감, Codex로 분석한 부동산 자산 20,112건, 2~3개월 내 직원 채택률 50%를 기록했다.

### 물리적 세계를 위한 엔지니어링 가속화
원문: https://openai.com/index/accelerating-engineering-for-the-physical-world

- OpenAI는 자사 모델이 엔지니어의 물리적 제품 설계·시뮬레이션·제작을 돕는 방식의 발전 내용을 공개했다.
- 이 기능들은 기계·전기 엔지니어링과 종단간 시스템 설계에 걸쳐 있으며, 내부 팀이 아이디어를 테스트하고 더 빠르게 반복하는 데 이미 활용되고 있다.
- 엔지니어는 특화 도구를 사용해 기계 설계, 전자, 소프트웨어, 제조 요구사항을 통합해야 하며, 모델은 도면 준비와 시뮬레이션 설정, 분야 간 변경 조율을 지원하도록 학습되고 있다.
- 멀티모달·컴퓨터 사용 워크플로에서 Astra의 성능을 시험하기 위해 인간의 직접 편집 없이 장치를 만드는 실험을 했고, GPT-6로 기능 요구사항 정의와 인클로저·PCB·소프트웨어 통합 설계를 수행했다.
- 두 팀원이 부수 프로젝트로 일주일 이내에 Astra와 테스트 장치를 설계했고, 계약 제조업체가 한 달 이내에 소량 프로토타입을 제작했다.
