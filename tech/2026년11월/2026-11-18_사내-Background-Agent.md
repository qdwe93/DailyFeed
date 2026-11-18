# Tech Feeds — 2026-11-18

## LayerX Engineering Blog

### 사내 Background Agent ‘haro’에 알람 대응을 맡겼더니 실행할수록 똑똑해졌다
원문: https://tech.layerx.co.jp/entry/haro-alert-loop

- LayerX의 바쿠라쿠 근태 개발팀은 평일 9시부터 21시까지 1시간 간격으로 사내 Background Coding Agent ‘haro’를 스케줄 실행해 Slack 알람 순찰과 분류를 맡기고 있다.
- 기존에는 본번 환경에만 하루 수십 건씩 쏟아지는 알람 노이즈와 실제 장애를 사람이 일일이 확인해야 했고, 기출 에러 여부가 개인 기억에 의존하며 검증 환경까지는 관리가 미치지 못했다.
- ‘haro’는 1회 순찰마다 본번과 검증 환경의 모든 알람 채널에서 최근 1시간 알림을 수집해 순찰용 Wiki의 ‘알려진 사상’ 및 판정 기준과 대조하여 대응 필요, 확인 필요, 대응 불필요로 분류한다.
- 대응 필요나 확인 필요 건은 Datadog 로그와 코드를 추적해 사내 프로덕트의 HTML 아티팩트 조사 페이지에 정리하고, 수정 방법이 명확하면 draft PR을 생성해 Slack에 공유한다.
- 에이전트는 PR을 직접 병합하거나 본번 데이터를 변경하지 않으며, 순찰 마지막 단계에서 사람이 정한 제약 범위 안에서 조사 절차를 기록한 순찰용 Wiki를 스스로 갱신한다.

### Snowflake Parquet Direct의 사양을 문서와 실측으로 이해하기
원문: https://tech.layerx.co.jp/entry/snowflake-parquet-direct

- Parquet Direct는 오브젝트 스토리지에 저장된 Parquet 파일을 이동하거나 복사하지 않고 읽기 전용 Iceberg 테이블의 데이터 파일로 등록해 Snowflake에서 조회하는 기능이다.
- 2026년 11월 18일 기준 Public Preview 상태이며, 파일을 테이블 스토리지로 복사하는 `COPY INTO ... LOAD_MODE = ADD_FILES_COPY`와 달리 복사·저장 비용이 발생하지 않고 Snowflake에서 데이터를 변경할 수 없다.
- Hive-style Partitioning을 지원해 `date=2026-11-11/`처럼 파일 내부가 아닌 경로에 포함된 `key=value`에서 파티션 열과 값을 도출함으로써 재로드 없이 파티션 테이블로 참조할 수 있다.
- 테이블 생성 후 스토리지에서 파일이 추가·변경·삭제되면 이벤트 알림 기반 자동 갱신 또는 `ALTER ICEBERG TABLE ... REFRESH` 수동 명령으로 테이블 메타데이터에 반영해야 한다.
- 이 글은 2026년 11월 11일 기준 공식 문서와 11월 11일~17일 Amazon S3 테스트 데이터 실측을 토대로 파일 갱신, 프루닝, 캐시 유무에 따른 조회, 스키마 진화, Variant·UTF-8 처리 사양을 검증한다.

## RIDI Tech

### 리디, ‘만타(Manta)’ 독립 창작자 자유 연재 공간 ‘Creator’s Alley’ 오픈
원문: https://ridicorp.com/2026/11/ridi_manta_creatorsalley/

- 리디 주식회사는 글로벌 콘텐츠 플랫폼 ‘만타(Manta)’에 독립 창작자를 위한 자유 연재 공간 ‘Creator’s Alley’를 17일 오픈한다고 밝혔다.
- 북미 코믹콘의 ‘아티스트 앨리’에서 이름을 딴 ‘Creator’s Alley’에서는 만화와 소설 장르 창작자 누구나 만타 프로필을 개설하고 크리에이터 스튜디오를 통해 작품을 등록해 연재할 수 있다.
- 웹코믹·망가·웹소설 독자층이 모인 만타 플랫폼 안에서 만화와 소설이 하나의 공간에 함께 연재되어 창작자가 장르와 형식의 경계를 넘어 팬덤 접점을 넓힐 수 있는 것이 특징이다.
- 이번 공간 신설은 만타의 콘텐츠 참여 범위를 독립 창작자까지 확대해 글로벌 독자와의 만남과 새로운 작품 발견 기회를 넓히기 위해 마련됐다.
- 만타는 향후 참여 창작자를 위해 수익화 프로그램, 만타 정식 연재, 다양한 장르와 매체로의 IP 확장 기회 등 성장 지원 방안을 단계적으로 마련할 계획이다.

## Toss Tech

### 판단에만 집중하세요: 토스 타겟팅 모델 개발 자동화
원문: https://toss.tech/article/targeting-model-automation

- 토스는 고객 타겟팅 모델 개발 프레임워크 TASTE를 통해 설정 파일 하나로 피쳐 수집부터 평가까지 실행하여 모델 학습 시간을 2주에서 1일로 단축했다.
- 기존에는 모델 사용 여부를 판단하기 위해 필요한 4가지 비교·평가 및 모니터링 과정을 MLE가 수작업으로 수행해야 했으나, 이를 TASTE 파이프라인에 자동화해 통합했다.
- 최적 피쳐 수를 고르는 `auto_k`는 중요도 급감 지점(Elbow) 기준이 앞쪽에서 잘려 성능 기여 피쳐를 놓치는 한계를 해결하기 위해 중요도 순으로 피쳐를 늘리며 성능을 직접 측정해 개선이 멈추는 지점을 선택한다.
- 검증 실험에서 후보 피쳐 458개 중 유의한 성능 손실 없이 피쳐를 84% 줄인 75개만 사용했고, 다른 상품 모델의 `auto_k` 적용 상위 1% 고객 발송 실험에서는 규칙 기반 세그먼트 대비 클릭률 약 5배, 신청 전환율 약 2.6배를 기록했다.
- 퍼널 모델 구조 선택에서는 노출·진입·클릭·신청 단계별 트리 모델을 따로 학습해 점수를 곱하던 방식이 앞 단계 신호를 뒤 단계로 전달하지 못하는 한계가 있어 트리와 딥러닝 구조를 동일 데이터·평가셋에서 나란히 비교한다.

### 지표 뒤에 숨은 맥락을 한눈에: New20 Timeline Hub 만들기
원문: https://toss.tech/article/new20-timeline-hub

- 토스는 페이스페이 프로모션 New20의 맥락을 파악하기 위해 회의록, GitHub PR, 정책 문서, 디자인 보드, 세그먼트 정의, 대시보드에 흩어져 있던 기록을 하나의 시간축으로 연결한 New20 Timeline Hub를 구축했다.
- Meta의 Timeline 형식 내부 도구를 커머스 도메인 배포 조회 도구에 적용한 사례를 참고해, 날짜 축을 하나로 유지하면서 제품 맥락을 다섯 가지 갈래로 나누어 질문에 따라 확인할 수 있게 구성했다.
- 타임라인의 점은 PR이나 배포로 개발 반영이 확인된 변경(채운 점)과 논의 기록만 있고 개발 반영이 확인되지 않은 항목(빈 점)으로 상태를 구분해 확실성을 달리 읽을 수 있도록 했다.
- 여러 채널에 나뉘어 기록되는 하나의 제품 변경(예: 9월 8일 '현장참여 사후적립 출시'의 PR 9건과 회의록 5건)을 읽기 쉬운 단위의 변경으로 묶되 판단 근거로 삼은 원문을 함께 연결했다.
- 시간축 외에도 질문별 관점으로 맥락을 조회하는 화면을 제공해 세그먼트 화면에서 현재 대상 조건과 변경 이력을 함께 살펴볼 수 있게 했다.

## 당근 Tech

### GitHub Actions 모니터링의 빈칸: Exporter로 ARC Runner 관측하기
원문: https://medium.com/daangn/github-actions-%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EC%9D%98-%EB%B9%88%EC%B9%B8-exporter%EB%A1%9C-arc-runner-%EA%B4%80%EC%B8%A1%ED%95%98%EA%B8%B0-cbe1a46a9e71?source=rss----4505f82a2dbd---4

- 당근 SRE팀 딜리버리 파트는 Kubernetes 기반 사내 배포 플랫폼 Kontrol과 GitHub Actions 중심의 전사 CI 시스템을 운영하며, Kubernetes 오퍼레이터인 ARC로 self-hosted Runner를 Runner Scale Set 단위로 관리한다.
- GitHub 장애나 Job 요청 급증으로 Job이 Queued 상태에 머무를 때, ARC 기본 메트릭만으로는 대기 중인 Job 수와 대기 시간, 특정 Job이 실행되는 Runner Pod를 파악하기 어려웠다.
- Runner Pod에 Job 정보를 라벨로 추가하는 ARC 이슈 방식은 컨트롤러 변경과 권한 추가, 라벨 메트릭 수집 구성이 필요해 적용까지 시간이 걸리는 문제가 있었다.
- 이에 Runner Pod에 Job 이름을 붙이는 Collector, 대기 중인 Job을 추적하는 Webhook, 상태를 저장하는 StateStore 세 바이너리로 구성된 action-runner-job-exporter를 제작했다.
- ARC에서는 각 Runner Scale Set의 Listener Pod가 GitHub과 세션을 맺고 배정된 Job과 최소·최대 Runner 설정을 바탕으로 필요한 Runner 수를 계산해 EphemeralRunnerSet의 replicas를 변경한다.

### GitHub Actions 모니터링 공백 해소: Exporter로 ARC Runner 관측하기
원문: https://medium.com/daangn/closing-the-github-actions-monitoring-gap-observing-arc-runners-with-an-exporter-0a8f39c3b70b?source=rss----4505f82a2dbd---4

- 당근(Karrot) SRE팀 딜리버리 파트는 Kubernetes 기반 사내 배포 플랫폼 Kontrol과 GitHub Actions 중심의 전사 CI 시스템을 운영하며, 대기 중인 Job과 실행 중인 Runner를 파악하기 위해 exporter를 구축하고 운영 환경에서 개선했다.
- GitHub Actions에서는 push나 pull request 같은 이벤트 발생 시 Workflow가 실행되며, 테스트와 빌드 등의 Job으로 나뉘어 Runner에서 실행되거나 가용한 Runner가 없을 때 대기한다.
- 당근은 자체 Kubernetes 클러스터에서 주로 self-hosted Runner를 사용하며, 이를 ARC(Actions Runner Controller) 오퍼레이터로 Runner Scale Set 단위로 묶어 최소·최대 수 범위 내에서 Job 수요에 따라 조절한다.
- 오토스케일링에도 불구하고 GitHub 장애나 Job 요청 급증 시 Job이 Queued 상태에 머무르는데, ARC 기본 내장 메트릭은 Runner와 Job의 집계 수치만 보여주어 대기 중인 Job 수, 대기 시간, 특정 Job을 실행하는 Runner Pod를 알기 어려웠다.
- 해결 방안을 찾는 과정에서 Runner Pod에 Job 정보를 라벨로 추가하자는 ARC 저장소 이슈를 발견했으나, 컨트롤러 변경과 추가 권한 등이 필요했다.

## 우아한형제들 기술블로그

### 이래라저래라 하지 마라: 주니어를 성장시키는 파트너십 대화법
원문: https://techblog.woowahan.com/28524/

- 우아한테크코스 교육자로 일한 글쓴이는 2024년 1년간 다섯 번에 그쳤던 원온원을 2025년 반년 동안 60번 넘게 진행하게 된 과정과 동기면담 연습 경험을 공유한다.
- MBTI가 ISTJ이고 NEO 성격검사에서 사회성과 온정성이 매우 낮음으로 나온 글쓴이는 과거 정답을 주고 고쳐 주는 데 집중해 정답을 못 줄 것 같은 원온원을 부담스러워하며 피했다.
- 교육자 경력 8년을 포함해 약 12년간 지식을 전달해 왔으나, 교육을 듣는 동안과 직후에 만족한 사람들도 돌아가서는 거의 변하지 않는 한계를 겪었다.
- 온라인 커뮤니티에서 잘못된 부분을 바로잡던 글쓴이는 자신이 똑같은 피드백을 받았을 때 기분이 좋지 않았고 오히려 공감과 지지 답글이 더 좋은 영향을 준다는 점을 깨달았다.
- 이후 윌리엄 밀러와 스티븐 롤닉이 만든 동기면담 교육을 계기로 정답을 제시하는 대신 상대 안의 답을 함께 찾으며 공감과 반영을 연습했고, 2026년부터는 AX 업무에서 동료들이 AI를 스스로 쓰도록 돕는 일에 이 대화법을 적용하고 있다.

## 字节跳动技术团队 (ByteDance Tech)

### 비즈니스 흐름에 맞추는 데이터: EFS 데이터 플로우로 재편하는 AI 시대의 파일 스토리지
원문: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&mid=2247524318&idx=1&sn=e834fd29a169549dd609f81979109eb9

- 대규모 모델 학습과 추론 환경에서는 체크포인트 집중 입출력을 위한 TB/s급 대역폭 수요, 콜드 데이터 및 중복 저장에 따른 비용 부담, 수동 수명주기 관리의 한계가 주요 과제로 꼽힌다.
- 성능과 비용을 함께 맞추는 데이터 구성 방식에는 컴퓨팅 측 캐시 가속, 파일 스토리지 내부의 콜드·핫 계층화, 오브젝트 스토리지와 파일 스토리지 간 데이터 플로우 방식이 있다.
- 화산엔진(火山引擎) EFS 데이터 플로우는 고성능 파일 스토리지(EFS)와 오브젝트 스토리지(TOS)를 연동해 온디맨드 데이터·메타데이터 로딩으로 여러 TOS 버킷을 단일 POSIX 디렉터리 트리로 통합 제공한다.
- 파일의 마지막 접근 시간(atime)이 설정 기준을 초과하면 데이터를 TOS로 먼저 내려 무결성을 확보한 뒤 EFS의 데이터나 메타데이터를 제거하며, 이후 재접근 시 온디맨드 로딩이나 사전 워밍업으로 불러온다.
- EFS의 파일 인터페이스와 TOS의 오브젝트 인터페이스 간 양방향 동기화 및 선택적 동기 삭제를 지원하며, 디렉터리·파일 목록·속성 조건을 기준으로 한 일회성 배치 작업도 처리할 수 있다.

### 컴퓨팅 자원이 같은 관리 언어로 소통하도록: XPU 대역외 관리 표준 공동 구축
원문: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&mid=2247524318&idx=2&sn=f87733fff5a5bfdcae6f2ffba1b65a93

- 알리바바, 바이트댄스, 텐센트는 다양한 제조사와 세대의 XPU(GPU·NPU 등)가 혼재된 환경에서 발생하는 중복 어댑테이션과 운영 복잡도를 줄이기 위해 3종의 XPU 대역외(OOB) 관리 규격을 공동 발표했다.
- 《XPU 모듈 표준화 Redfish 인터페이스 설계 규격》은 독립 관리 컨트롤러를 갖춘 모듈을 대상으로 DMTF Redfish 기반 호스트 BMC와 모듈 BMC 간 리소스 모델 및 자산·상호연결·로그·펌웨어 업그레이드 동작을 규정한다.
- 《XPU 카드 PLDM 및 PDRs 정의 규격》은 PCIe 표준 카드와 OAM 폼팩터를 대상으로 대역외 통신 채널과 PLDM 프로토콜, 센서·제어 항목 등을 기술하는 PDRs의 식별 및 서술 방식을 통일한다.
- 《XPU(xMC 미탑재) 대역외 역량 표준 규격》은 서버 BMC가 직접 관리하는 장치를 대상으로 데이터 수집, 펌웨어 업그레이드, 로그 수집, 전력 제어, 안정성의 5가지 관리 역량 요구사항을 필수와 권장 항목으로 구분해 정의한다.
- 세 규격은 공통 관리 역량과 데이터 의미를 표준화해 서버·BMC·클라우드 운영 측의 제조사별 분기 개발 비용을 줄이면서도, 칩 아키텍처와 진단 깊이 등 제조사의 차별화 여지는 유지하도록 설계되었다.

## 小红书技术REDtech (Xiaohongshu REDtech)

### 샤오홍슈 스토리지 기반 해부 06 | RedDB: 자체 개발 멀티모달 데이터베이스의 설계와 실무
원문: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247497170&idx=1&sn=0b57353788f1e32f852d516e58a7d6c6

- RedDB는 샤오홍슈의 검색·추천·광고 분야 와이드 테이블 수요에서 출발해 향후 벡터와 그래프 모델까지 단일 기반으로 통합 지원하도록 개발된 분산 멀티모달 데이터베이스다.
- 내부 구조는 데이터 서비스, 분산 엔진, 스토리지 및 인덱스, 데이터 영속성의 4계층으로 나뉘며 통합 스토리지 데이터베이스 클라우드 플랫폼(DMS)이 자원 관리와 확축소 등 횡단 운영 기능을 담당한다.
- 분산 엔진은 기본키 범위 기반 샤드 관리, 논리적 분할과 물리적 마이그레이션의 분리, Raft 기반 일관성 복제 및 스냅샷·로그 복구, 로그 지연 기반 백프레셔 유량 제어를 제공한다.
- 현재 와이드 테이블 스토리지는 RocksDB 기반 로우 엔진을 사용해 단일 샤드 내 행 단위 원자적 부분 쓰기를 지원하며, 희소 스캔 시 존재하는 컬럼을 먼저 순회한 뒤 요청 필드를 필터링해 불필요한 탐색을 줄인다.
- 100KB, 500KB, 1MB 행 너비 조건의 단일 행 읽기·범위 스캔·일괄 읽기 평가에서 RedDB는 비교 대상 대비 처리량 증가율 중앙값 50% 초과, P99 지연시간 감소율 중앙값 약 60%를 기록했다.

## Google Official Blog

### 온라인으로 만나는 콜로니얼 윌리엄스버그 100주년
원문: https://blog.google/company-news/outreach-and-initiatives/arts-culture/colonial-williamsburg-centennial/

- Google Arts & Culture는 콜로니얼 윌리엄스버그(Colonial Williamsburg) 100주년을 맞아 올해 초 미국 건국 250주년을 기념해 출범한 디지털 허브를 확장해 새로운 스토리와 디지털화된 문화 자료를 공개했다.
- 온라인 인터랙티브 갤러리는 1926년 시작된 역사 지구 복원 과정을 다루며, 최초 복원 유적지인 총독 관저, 롤리 태번, 국회의사당의 희귀 기록 사진과 현대 사진, 시대 음악을 함께 제공한다.
- 특수 고해상도 테이블탑 스캐너를 활용한 협업을 통해 버지니아 가제트(Virginia Gazette) 희귀본과 훼손되기 쉬운 고문서 등 3,000점 이상의 디지털 이미지가 온라인에 처음으로 공개되었다.
- 새로 공개된 스토리들은 자연사 조사 자료와 초기 신문, 일상용품 등을 바탕으로 일반 시민의 경험과 역사적으로 소외된 목소리, 그리고 현장의 보존 작업 과정을 소개한다.
- 콜로니얼 윌리엄스버그 및 YouTube와의 협업으로 음식 역사가 맥스 밀러('Tasting History')가 킹스 암스 태번(King's Arms Tavern)의 셰프 아이비 보이드와 함께 18세기 디저트 스노우 에그(snow eggs)를 만드는 특별 에피소드를 촬영했다.

### 아시아태평양 지역의 Google Play Best of 2026
원문: https://blog.google/topics/google-asia/google-play-best-2026/

- 구글 플레이는 2026년 어워드를 통해 아시아태평양 지역 개발자들의 수상 앱과 게임 및 주요 트렌드를 발표했다.
- 중국 Gryphline의 Arknights: Endfield는 일본과 한국을 제외한 글로벌 시장에서 'Best Game'을, Perfect World의 NTE: Neverness to Everness는 여러 시장에서 'Best Cross-device Game'을 수상했다.
- 일본에서는 hololive Dreams가 'Best Game', LINE Music이 'Best for Entertainment', 식단 관리 앱 Asken이 AI 기반 영양 피드백 및 식단 추천으로 'Best App'에 선정되었다.
- 인도에서는 Scarfall 2.0이 'Best Made in India'와 Pocket FM이 'Best Entertainment App'을 받았고, 인도네시아에서는 Tukang Sate VS Ojol Rush가 'Best Made in Indonesia', 홍콩과 대만에서는 DramaBox가 'Best Entertainment App'을 수상했다.
- HoYoverse의 Zenless Zone Zero는 미주와 유럽 시장에서 'Best Ongoing Game'을 받았고, 한국에서는 NEXON의 MapleStory: Idle RPG가 'Best Game'에 올랐다.

### Google Play, 2026년 최고의 앱·게임·도서 발표
원문: https://blog.google/products-and-platforms/platforms/google-play/best-of-play-awards-2026/

- 구글 플레이는 연례 Best of Play 2026 어워드를 발표하며 미국 지역의 주요 수상 앱과 게임 목록을 공개했다.
- 올해 수상작에서는 일상 작업을 자동화하는 앱과 휴대폰, 태블릿, PC 간 전환 플레이를 지원하는 내러티브 중심 게임이 두드러졌다.
- 미국 종합 'Best App'에는 안드로이드용으로 네이티브 구축되어 자료와 대화하거나 학습 도우미·맞춤형 퀴즈를 생성하는 'Notability: AI & PDF Notes'가 선정되었다.
- 미국 종합 'Best Game'은 실시간 전투와 공장 건설·관리 메커니즘을 결합한 'Arknights: Endfield'가 수상했다.
- 크로스 디바이스 부문에서는 Wear OS 워치 및 잠금화면 위젯 연동을 제공하는 'Strava: Run, Bike, Walk'가 'Best Cross-device App'을, 'Moonlight Peaks'가 'Best Cross-device Game'을 차지했다.

### EmbeddingGemma 2 기술 보고서 공개
원문: https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2-technical-report/

- 구글은 기존 텍스트 전용 오픈 임베딩 모델에 네이티브 멀티모달 이해 기능을 확장한 EmbeddingGemma 2를 공개했다.
- EmbeddingGemma 2는 텍스트, 이미지, 오디오, 비디오 및 이들의 조합을 단일 임베딩 공간에 매핑한다.
- 이 모델은 백본을 더 콤팩트한 형태로 압축하면서도 통합된 벡터 공간을 학습한다.
- 모델의 설계에는 Gemma 4와 Gemini Embedding 2의 최신 기술을 기반으로 한 기법들이 적용되었다.
- 공식 기술 보고서에서는 학습 전략, 평가 방법론, 실험 결과를 확인할 수 있으며 5분 분량의 설명 영상도 함께 제공된다.

### 당신을 대신해 일하는 Gemini
원문: https://blog.google/innovation-and-ai/products/gemini-app/tasks-in-gemini-free-new-features/

- 구글은 사용자가 일상적인 작업을 Gemini에 맡겨 시간과 비용을 절약할 수 있도록 지원하는 업데이트를 발표했다.
- 이 업데이트는 새로운 Gemini 4 Hydrogen 모델을 기반으로 미국, 일본, 한국, 캐나다, 호주, 인도의 수억 명 사용자에게 무료로 순차 제공된다.
- 예시로 소개된 Gemini는 Google Maps로 인근 정비소 두 곳에 동시에 전화를 걸고 Google Calendar의 빈 시간을 확인해 5분 이내에 차량 정비 예약을 완료했다.
- Gemini는 통화 시 업체에 자신이 AI임을 즉시 밝히고 업체는 수신 거부를 선택할 수 있으며, 사용자의 승인 없이는 결제 정보나 비공개 계정 정보를 제공하지 않는다.
- 또한 새로운 Google Password Manager 연동과 이메일 내 과거 청구서 분석을 통해 피크 요금 시간대에 작동하던 히트 펌프가 높은 전기 요금의 주원인임을 찾아낸 사례도 소개되었다.

### 미국 10개 주, 구글과 무료 AI 교육 협력
원문: https://blog.google/company-news/outreach-and-initiatives/grow-with-google/ai-training-state-partnerships/

- Grow with Google은 NC LIVE를 통해 무료 디지털 및 AI 교육을 제공하는 노스캐롤라이나주가 열 번째 파트너로 합류함에 따라, 아칸소·코네티컷·델라웨어·조지아·매사추세츠·미주리·오클라호마·사우스다코타·버지니아를 포함한 10개 주와 협력하고 있다.
- 오클라호마에서 시작된 이 협력은 매사추세츠로 이어져 MassTech AI Hub 출시 6개월 만에 약 4만 명의 주민이 교육에 등록했다.
- 조지아, 오클라호마, 노스캐롤라이나는 주 전역 공공 도서관 시스템을 통해 무료 기초 과정과 디지털 자료를 제공하며, 노스캐롤라이나에서는 노스캐롤라이나 센트럴 대학교 AI 및 신흥 연구소의 창립 파트너 활동과 연계된다.
- 미주리는 K-12 학교와 대학, 지역 취업 센터에서 교육을 제공하고 코네티컷의 차터 오크 주립대학은 온라인 AI 아카데미를 개설했으며, 이는 미국 50개 주 500개 이상 교육기관이 참여한 Google AI for Education Accelerator를 기반으로 확대되었다.
- 버지니아, 델라웨어, 아칸소는 주 인력 프로그램, 경제개발위원회, 취업 센터에 AI 교육 과정을 통합해 주 공무원, 구직자, 지역 기업이 AI를 바로 활용할 수 있도록 하고 있다.

### 구글 검색 AI 모드에 임시 스레드 기능 도입
원문: https://blog.google/products-and-platforms/products/search/temporary-threads-ai-mode/

- 구글은 검색의 AI 모드에서 검색 기록이나 추천에 남기고 싶지 않은 질문을 탐색할 수 있는 임시 스레드 기능을 출시했다.
- 사용자는 별도 설정을 바꿀 필요 없이 AI 모드 오른쪽 상단의 임시 스레드 아이콘을 클릭해 바로 질문을 시작할 수 있다.
- 임시 스레드 세션은 사용자 계정과 완전히 분리되어 답변이 과거 선호도의 영향을 받지 않으며 향후 개인화나 검색 기록에 저장되지 않는다.
- 임시 스레드를 닫으면 대화 내용이 사라져 기존과 같이 일반 검색으로 돌아갈 수 있다.
- 이 기능은 AI 모드가 지원되는 모든 언어의 데스크톱 및 모바일 브라우저에서 전 세계적으로 출시되고 있다.

### 구글 홈의 최신 기능 업데이트
원문: https://blog.google/products-and-platforms/devices/google-nest/google-home-updates-november-2026/

- 안드로이드 사용자는 구글 월렛의 디지털 홈 키를 이용해 탭하거나 핸즈프리로 접근하는 방식으로 호환되는 현관문을 잠금 해제할 수 있다.
- Google Home Premium Advanced는 움직임으로 트리거된 카메라 및 초인종 이벤트 설명에서 개 짖는 소리나 유리 깨지는 소리 같은 오디오를 감지한다.
- 12월부터 미국과 캐나다의 Nest 온도조절기 사용자는 앱에서 추정 누적 절감액을 확인할 수 있다.
- 4세대 Nest 러닝 온도조절기 사용자는 호환되는 타사 실내 센서를 연동해 실내 온도 차이를 조절할 수 있다.
- Gemini for Home은 일상적인 요청을 최대 20% 더 빠르게 처리하며 인도와 브라질을 포함한 6개 신규 국가로 확대되고 있다.

### 구글 Vids, 개인 계정 사용자에게 무료 개인 아바타 기능 제공
원문: https://blog.google/products-and-platforms/products/workspace/vids-personal-avatars-no-cost/

- 구글은 개인 구글 계정을 가진 모든 사용자에게 Google Vids의 개인 아바타 기능을 무료로 제공한다.
- 사용자는 원하는 외형과 음성을 적용한 맞춤형 디지털 아바타를 만들어 영상에 출연시킬 수 있다.
- QR 코드를 스캔해 자신의 모습을 담은 개인 아바타를 생성하면 영상 프롬프트에 자동 추가되며, 원하는 대사를 입력해 영상을 만들 수 있다.
- 생성된 아바타는 Vids 프로젝트에 저장되어 모든 장면에 걸쳐 일관되게 재사용할 수 있다.
- 개인 아바타는 구글 계정에 연결되며 계정 소유자 본인의 모습으로만 제한되고, 데스크톱에서 vids.new에 접속해 사용할 수 있다.

### 미국에서 iOS용 Google Wallet 출시
원문: https://blog.google/products-and-platforms/platforms/google-pay/wallet-available-ios-united-states/

- Google이 미국 전역의 iOS 사용자를 대상으로 Google Wallet을 출시했다.
- Gmail 및 다른 Google 앱과 자동으로 동기화되어 배송 추적, 디지털 탑승권, 콘서트 티켓, 영수증을 기기 전반에서 관리할 수 있다.
- 사용자는 휴대폰 카메라로 포인트 카드와 헬스장 회원권 등 실물 카드를 스캔해 Google Wallet으로 가져와 디지털화할 수 있다.
- 결제 카드를 관리해 Google 및 Google Pay 지원 온라인 결제에 사용할 수 있으며, Google 내 에이전트 기반 구매의 주문 확인서·영수증·배송 업데이트도 한곳에서 관리할 수 있다.
- 현재 iOS 버전에서는 탭투페이(tap-to-pay) 기능이 지원되지 않는다.

### Gemini 4 Carbon을 활용한 개발자 5인의 프로젝트
원문: https://blog.google/products-and-platforms/products/gemini/gemini-4-carbon-builders/

- Google은 지난주 확대 배포한 Gemini 4 Carbon 모델을 활용해 커뮤니티 개발자들이 구현한 5가지 프로젝트를 소개했다.
- Glitter Gal은 Carbon을 이용해 CUDA와 C++로 52,000개의 야생화와 풀잎을 처음부터 코딩해 바람에 맞춰 움직이는 초원을 렌더링했다.
- Chubby는 WebGPU로 조류처럼 움직이는 1,048,576개 입자의 실시간 시뮬레이션을 제작했고, Andrew V는 두드리면 소리가 나고 떨어지면 산산조각 나는 스테인드글라스 블록 쌓기 게임을 만들었다.
- Giyu_codes는 흩어진 공공 데이터셋을 실시간 3D 시각화가 포함된 14개 인터랙티브 도구로 변환했으며, The Bugged Dev는 단일 참조 이미지로부터 실제 테스트와 조정이 가능한 92개 황동·유리 기구를 갖춘 19세기 파리 광학 실험실을 구현했다.
- Gemini 4 Carbon은 Google AI Studio 및 Android Studio의 Gemini API 유료 등급, Google AI Ultra 구독자용 서비스(Google Antigravity, AI Studio, Gemini 앱, 검색 AI 모드), 기업용 Gemini(API, 모델 드롭다운, Google Antigravity, CodeMender)에서 이용할 수 있다.

### 유전체 매핑이 연구자들의 질병 이해를 돕는 방법
원문: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphagenome-disease-research/

- 인간 유전체는 A, T, C, G 네 가지 염기 문자로 구성된 30억 쌍의 DNA 염기쌍을 포함하며, 유전자를 켜고 끄는 기능을 통해 질병 발생 여부에 관여한다.
- Google DeepMind의 Žiga Avsec 연구팀이 개발한 AlphaGenome은 100만 염기쌍 길이의 부분 DNA 서열을 입력받아 수천 가지 예측을 생성하는 모델이다.
- 각 염기 문자를 다른 세 문자로 바꿀 수 있어 총 90억 가지의 단일 문자 변이가 가능하며, 많은 유전 질환이 이러한 단일 문자 변화 하나로 발생한다.
- 연구팀은 AlphaGenome으로 90억 가지 단일 문자 변화 모두의 결과를 예측해 AlphaGenome Atlas라는 대규모 데이터셋을 구축함으로써 과학자들이 연구 대상을 더 빠르게 고를 수 있도록 했다.
- 과학계는 인간 DNA의 30억 염기쌍을 모두 읽을 수 있지만 유전자 발현과 질병 위험을 조절하는 비암호화 영역의 의미는 완전히 해독하지 못했으며, 기존 실험실(wet-lab) 연구는 비용과 시간이 많이 소요된다.

## OpenAI

### ChatGPT for Sales 소개
원문: https://openai.com/index/introducing-chatgpt-for-sales

- OpenAI는 영업팀이 고객을 파악하고 잠재 고객 발굴부터 고객과의 약속 이행까지 영업 주기를 단축할 수 있도록 돕는 ChatGPT for Sales를 공개했다.
- ChatGPT for Sales에는 영업 담당자 전용 스킬을 갖춘 새로운 Sales 플러그인과 ChatGPT 내 30개 이상의 신규 및 강화된 파트너 플러그인이 포함된다.
- OpenAI의 Sales 플러그인은 공략할 계정 선정, 통화 준비, 후속 메시지 초안 작성 등 일상적인 영업 업무에 바로 사용할 수 있는 워크플로를 제공한다.
- 파트너 플러그인을 통해 Confluence·Guru·Seismic의 자료 조회, ChatGPT Voice·Slides·Gamma·Figma·Canva·ChatGPT Sites를 활용한 발표·데모 제작, Salesforce·HubSpot·Close CRM·monday CRM의 계정 정보 통합을 지원한다.
- 또한 Apollo·Clay·Common Room의 계정 신호와 ChatGPT 웹 리서치, Outreach·Salesloft의 아웃리치 계획, ChatGPT Meetings 플러그인·Gong·Otter.ai·Granola의 통화 메모를 연계해 구매자 우선순위 파악에 활용할 수 있다.

### GPT-6.2 Astra 및 Sol 소개
원문: https://openai.com/index/introducing-gpt-6-2-astra-sol

- OpenAI는 고난도 프로젝트용 프론티어 모델 GPT-6.2 Astra와 일상 업무용 효율 모델 GPT-6.2 Sol을 공개했으며, 두 모델 모두 더 적은 출력 토큰으로 까다로운 작업에서 더 나은 결과를 제공한다.
- GPT-6.2 Astra는 슬라이드, 스프레드시트, 문서 작성 시 사용자가 제공한 템플릿과 해당 분야의 관행을 더 잘 따르며, 웹사이트, 게임, 3D 디자인 분야에서 코드와 프론트엔드 구현 품질을 높였다.
- GPT-6.2 Astra는 Agents’ Last Exam에서 GPT-6 Astra 대비 3분의 1 미만 비용으로 5.2점, Claude Fable 5.2 대비 5% 비용으로 5.5점 높은 최고 점수를 기록했고, Terminal-Bench-Science 0.1과 Vals Science Index에서도 최고치를 달성했다.
- API에서 GPT-6.2 Astra의 가격은 GPT-6 Astra 대비 입력·출력 토큰이 20% 낮고 캐시 입력은 60% 할인된 100만 토큰당 입력 8달러, 캐시 입력 0.40달러, 출력 40달러이며, GPT-6.2 Sol은 GPT-6.1 Sol의 API 토큰 가격을 유지한다.
- GPT-6.2 Sol은 GPT-6.1 Sol보다 동일 유료 요금제에서 더 많은 작업을 처리하고 다단계 에이전트 워크플로우를 수행하며, Cognition의 FrontierCode 2.0에서 최대 설정 기준 GPT-6.2 Astra의 약 5분의 1 비용으로 0.5점 이내의 점수를 기록했다.
