# Tech Feeds — 2026-11-19

## LayerX Engineering Blog

### 사내 Coding Agent "haro"를 활용한 전 서비스 횡단 레드티밍 기반
원문: https://tech.layerx.co.jp/entry/haro-readteam

- LayerX는 바쿠라쿠 전 서비스의 LLM 기능 취약점을 검증하기 위해 사내 백그라운드 코딩 에이전트 'haro' 위에서 동작하는 Claude로 레드티밍을 자동화하는 구조를 구축했다.
- 모든 공격 테스트는 자사 개발 환경에서 합성 데이터만 사용해 수행되며 운영 환경이나 고객 데이터에는 일절 접근하지 않는다.
- LLM이 입력을 데이터가 아닌 지시로 해석하는 취약점을 검증하기 위해 개발자의 수동 작업 대신 LLM 기능 개발을 자동 감지해 릴리스 전에 대량의 공격 문장을 시도하고 결과를 보고하는 방식을 도입했다.
- haro는 LLM 이용 지점마다 별도의 클라우드 Workspace Pod를 생성해 리소스 경합 없이 병렬로 실행할 수 있으며, 장시간 소요되는 작업과 검증 환경으로 제한된 안전한 실행을 지원한다.
- 구축된 파이프라인은 전 서비스에서 LLM 이용 지점을 탐지한 뒤 각 지점의 Workspace Pod에서 Claude가 코드 분석, Promptfoo provider 작성, 공격 실행, 프로그램 기반 성공 검증을 수행하고 결과를 추려 보고하는 순으로 동작한다.

## NAVER D2

### 컨테이너처럼 쓰고, VM처럼 격리하기 1편 - 컨테이너와 VM의 차이, Kata Containers의 Pod 실행 구조
원문: https://d2.naver.com/helloworld/8055238

- 이 연재는 Kata Containers 4.1.0, Kubernetes 1.34 이상, NVIDIA HGX B200 8-GPU 베어메탈 서버 환경을 기준으로 GPU 서버의 다중 사용자 격리 문제와 해결 방안을 다룬다.
- 컨테이너와 VM을 구분하는 기준은 커널로, 컨테이너는 호스트 커널을 공유하고 VM은 자체 커널을 별도로 부팅한다.
- 컨테이너는 네임스페이스로 PID·네트워크·마운트 등 프로세스가 보는 범위를 분리하고 cgroup으로 CPU와 메모리 사용량을 제한하지만 시스템 콜을 처리하는 커널은 공유한다.
- GPU를 사용하는 컨테이너는 저수준 런타임인 runc와 GPU 연결 도구인 NVIDIA Container Toolkit을 거쳐 생성된다.
- 커널을 공유하는 구조에서는 runc(CVE-2024-21626 등)와 NVIDIA Container Toolkit(CVE-2024-0132, CVE-2025-23266 등)의 취약점이 호스트 파일 시스템 접근이나 호스트 root 권한 획득 같은 컨테이너 탈출로 이어질 수 있다.

### 컨테이너처럼 쓰고, VM처럼 격리하기 2편 - GPU 패스스루 계층과 GPU 8장 VM의 부팅·메모리 구성
원문: https://d2.naver.com/helloworld/1376800

- GPU 1장을 VM에 연결할 때와 달리 GPU 8장을 하나의 VM에 연결하자 제한 시간 내 부팅 실패, 요청보다 작은 VM 생성, 호스트 소켓 구조를 모르는 게스트 메모리 할당 문제가 발생했다.
- 네이버 클라우드가 구성한 B200 서버 한 대에는 GPU 8장과 컴퓨트 IB NIC 8개가 PCIe 스위치마다 한 쌍씩 연결되어 있고, 소켓 0의 스위치 4개에 로컬 NVMe 4장이, 소켓별 별도 스위치에 스토리지 IB NIC 2개가 배치되어 있다.
- 호스트에 장착된 GPU를 VM 내부 컨테이너에서 사용하려면 IOMMU, VFIO, CDI의 세 계층을 거쳐야 한다.
- PCIe 장치의 DMA는 CPU를 거치지 않아 게스트 물리 주소가 자동 변환되지 않으므로, IOMMU가 변환 테이블을 통해 게스트 물리 주소를 호스트 물리 주소로 바꾸고 게스트 메모리 외부로의 DMA 접근을 차단한다.
- IOMMU를 활성화하려면 BIOS에서 VT-d 같은 기능을 켜고 커널 부팅 옵션에 intel_iommu=on(AMD는 amd_iommu=on) 등을 지정해야 한다.

### 컨테이너처럼 쓰고, VM처럼 격리하기 3편 - Fabric Manager 파티션과 DRA를 이용한 GPU 할당
원문: https://d2.naver.com/helloworld/6180316

- GPU 8장이 장착된 서버에서는 GPU 간 고속 통신에 쓰이는 NVLink가 하드웨어에서 허용한 조합끼리만 연결되므로 임의의 GPU를 묶어 VM에 제공할 수 없다.
- 기존 Kubernetes 장치 플러그인은 노드의 남은 GPU 개수만 보고 할당해 원하는 조합을 보장하지 못했기 때문에 DRA(동적 리소스 할당) 기반의 자체 드라이버를 구현했다.
- 네이버 클라우드의 B200 서버에서는 NVSwitch 칩이 GPU 8장을 NVLink로 연결하며, VM 환경에서는 NVSwitch를 호스트에 남겨 두는 Shared NVSwitch 모드로 NVIDIA Fabric Manager를 실행한다.
- Fabric Manager는 NVLink로 함께 묶을 수 있는 GPU 조합인 fabric partition을 미리 정하며, 같은 GPU를 포함한 두 파티션은 동시에 활성화할 수 없다.
- B200 서버 한 대에서 Fabric Manager가 보고한 파티션은 8장 1개, 4장 2개, 2장 4개, 1장 8개이며, 물리 GPU 번호는 PCI 주소 순서와 다르고 파티션 목록도 서버마다 다를 수 있다.

### 컨테이너처럼 쓰고, VM처럼 격리하기 4편 - IB 네트워크와 로컬 NVMe, vCPU 배치, 베어메탈 대비 성능
원문: https://d2.naver.com/helloworld/5896967

- 분산 학습 시 TCP 소켓은 시스템 콜과 커널 소켓 버퍼 복사를 거쳐 처리 시간이 학습 시간에 더해지므로, RDMA와 IB 네트워크를 사용해 CPU와 커널 네트워크 스택을 거치지 않고 등록된 메모리 간 직접 통신을 수행한다.
- GPUDirect RDMA(GDR)는 NIC가 GPU 메모리의 BAR 영역을 DMA로 직접 읽고 쓸 수 있어 호스트 메모리로의 복사가 필요 없으며, NCCL은 GPU와 NIC가 가까이 연결된 환경에서 이 경로를 사용한다.
- 호스트의 /dev/infiniband 장치 파일은 VM 내부에서 사용할 수 없기 때문에 IB NIC를 vfio-pci에 바인딩해 VFIO로 게스트에 연결하고 게스트 커널에 mlx5와 IB 드라이버를 포함해 빌드했다.
- B200 서버에는 GPU와 1:1로 짝지어진 컴퓨트 NIC 8개와 스토리지 네트워크용 NIC 2개가 있으며, 한 번에 하나의 VM에만 연결할 수 있는 제약 때문에 스토리지 NIC에는 SR-IOV를 적용했다.
- SR-IOV는 NIC 펌웨어에서 활성화한 뒤 sysfs의 sriov_numvfs에 개수를 기록해 물리 기능(PF)당 여러 가상 기능(VF)을 생성하며, 각 VF의 독립된 PCI 주소와 IOMMU 그룹을 이용해 컴퓨트 NIC는 PF 통째로, 스토리지 NIC는 VF로 나누어 VM에 연결한다.

## SmartHR Tech Blog

### 막연한 불안을 눈에 보이는 형태로 — System Risk Records를 도입해 얻은 3가지 안심
원문: https://tech.smarthr.jp/entry/2026/11/19/113553

- SmartHR의 신고 서류(届出書類) 개발팀은 개인의 기억에만 의존해 잊히거나 우선순위를 정하기 어렵고 혼자 떠안게 되는 개발·운영 리스크를 해결하고자 담당 SRE의 제안으로 System Risk Records를 도입했다.
- 팀원들이 개발과 운영 과정에서 신경 쓰이던 잠재적 리스크 22건을 포스트잇에 적어 공유한 뒤, 이를 바탕으로 Notion에 문제 내용과 사용자·서비스에 미칠 수 있는 영향을 함께 정리한 목록을 구축했다.
- 우선순위 점수를 산출하기 위해 리스크마다 임팩트(CUJ 기준 1~5점), 발생 가능성(1~5점), 영향 범위(1~4점), 대응 공수(1~5점)의 4가지 항목을 기록했다.
- Notion에 설정된 '우선순위 = (임팩트 × 발생 가능성 × 영향 범위) ÷ 대응 공수' 계산식을 통해 임팩트가 크고 발생 가능성이 높으며 영향받는 사용자가 많은 리스크일수록 높은 우선순위가 자동 산출되도록 했다.
- 리스크를 시각화해 관리함으로써 잊지 않고 기록할 수 있고, 무엇부터 대응해야 할지 판단할 수 있으며, 혼자 고민을 떠안지 않아도 되는 세 가지 안심을 얻었다.

## 字节跳动技术团队 (ByteDance Tech)

### 80개 이상의 오디오·비디오 기능을 Claude Code에 통합한 뒤 FFmpeg 매뉴얼을 덮었다
원문: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&mid=2247524506&idx=1&sn=0d9dab639998e69bde48db3e1dadf652

- AI MediaKit은 바이트댄스의 영상 처리 알고리즘을 바탕으로 화산엔진(Volcano Engine)이 공개한 스마트 비디오, 이미지 AI, 오디오, 범용 등 80개의 원자적 처리 능력 집합이다.
- 제품 구조는 가장 안쪽의 원자 능력, 각 기능을 터미널 명령어로 감싸 MIT 라이선스로 GitHub에 오픈소스 공개한 중간층 mediakit-cli, 그리고 Claude Code의 Skill 규격으로 패키징한 최외곽 5개 에이전트 스킬(byted-mediakit-video, editing, image, audio, shared)의 3계층으로 이루어진다.
- 동일한 명령 인터페이스로 로컬 FFmpeg를 동기·무료로 실행하는 --local 모드와 클라우드 연산을 활용하는 --cloud 모드를 함께 지원하는 이중 모드를 제공하며, API Key 하나를 환경 변수로 설정해 인증한다.
- 실제 테스트에서 480p(3.87MB) 데모 영상에 대해 클라우드 화질 개선(video enhance-video)을 요청하자 에이전트가 standard 등 4가지 선택지를 제시했고, 비동기 task_id를 자동 폴링해 3분 45초 만에 결과 영상을 내려받았다.
- 해당 화질 개선 테스트를 통해 영상 해상도는 496×864에서 1080×1880으로, 비트레이트는 2.0Mbps에서 7.1Mbps로, 파일 크기는 3.87MB에서 13.7MB로 증가했다.

## Google Official Blog

### 11월 Google Marketing Platform 업데이트: 연말 쇼핑 시즌 ROI 향상 기능 공개
원문: https://blog.google/products/marketingplatform/360/google-marketing-platform-drop-november/

- 미국과 인도의 Display & Video 360 구매자는 이제 Spotify 광고 인벤토리 전반에서 Google Audiences를 활용해 동영상 및 오디오 광고를 집행할 수 있다.
- Display & Video 360 광고주는 Pinterest의 프리미엄 동영상 및 디스플레이 인벤토리와 구매 의도가 높은 잠재고객에 프로그래매틱 방식으로 접근할 수 있다.
- 세로형 동영상 통합(Vertical Video Unification) 기능을 통해 미디어 투자를 통합할 수 있으며, Ford Motors는 이를 통해 순 도달률 26% 증가와 순 사용자당 비용 19% 절감을 기록했다.
- Search Ads 360 모범 사례에서는 고급 입찰 조합을 활용해 잠재 수요를 포착하는 'Fuel It, Power It, Maximize It' 공식을 안내한다.
- Display & Video 360의 Commerce Media Suite에 캐나다 최대 식료품 유통업체 Loblaw 연동이 추가되어, Walmart 및 Costco 등과 함께 Loblaw Advance 잠재고객 도달과 SKU 단위의 폐쇄 루프 매출 측정이 가능해졌다.

### 제품을 구축하고 발전시키는 새로운 방식, Stitch Loop 소개
원문: https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-loop/

- Google Labs는 코드베이스와 실시간 지표에 연결해 수정 사항을 찾고 목표 달성까지 24시간 지속적으로 작동하는 장기 실행 제품 에이전트 Stitch Loop를 공개했다.
- 사용자는 180개 이상의 통합 기능, 커스텀 MCP 서버 또는 로컬 CLI 업로드를 통해 GitHub와 로그, 사용자 행동, 피드백 등의 제품 맥락을 연결할 수 있다.
- 각 루프는 제품 데이터 기반의 제안, 트레이드오프와 범위가 포함된 해결책, 클라우드 샌드박스 내 코드 작성 및 풀 리퀘스트 생성, 실시간 데이터 모니터링 및 반영의 4단계로 동작한다.
- 생성된 GitHub 풀 리퀘스트에는 관련 작업의 스크린샷과 동영상이 포함되며, 사용자가 직접 검토하고 승인하기 전까지는 병합되지 않는다.
- Stitch Loop에는 사이버 보안, 지연 시간, 접근성을 위한 3개의 기본 루프가 내장되어 있으며, 결제 전환율 개선과 같은 사용자 지정 루프도 추가할 수 있다.

### 저용량 메모리 Android 기기에서도 Gemini 앱 사용 가능
원문: https://blog.google/innovation-and-ai/products/gemini-app/gemini-lower-memory-devices/

- Google은 메모리가 적은 하드웨어에서도 핵심 Gemini 환경이 원활히 작동하도록 앱을 재설계하여 지원되는 Android(Go edition) 기기에 Gemini 앱을 출시했다.
- 이전에는 하드웨어 제한으로 인해 저용량 메모리 Android 기기에서 기본적인 음성 명령만 사용할 수 있었다.
- 사용자는 Gemini Live를 통해 45개 이상의 언어로 긴 프롬프트를 입력하는 대신 대화하거나 소리 내어 면접 연습을 할 수 있다.
- 카메라로 노트나 양식을 비춰 학습 및 번역을 수행하거나 Nano Banana 기능을 이용해 주말 베이커리 세일 전단지와 같은 맞춤형 이미지를 생성할 수 있다.
- Gemini 앱은 Google Play에서 다운로드하거나 지원되는 스마트폰의 전원 버튼을 길게 눌러 사용할 수 있으며, Transsion 등 파트너사의 향후 출시 기기에 사전 탑재될 예정이다.

### 11월 Demand Gen 업데이트: 연말 쇼핑 시즌을 위한 유튜브 캠페인 기능 공개
원문: https://blog.google/products/ads-commerce/demand-gen-drop-november-2026/

- Demand Gen은 YouTube에서 가치가 높은 쇼핑객을 찾아 전환을 유도하고 연말 캠페인을 대화형 스토어프런트로 전환하기 위한 솔루션을 제공한다.
- YouTube에서 카탈로그 항목을 직접 노출하는 제품 피드를 Demand Gen과 함께 활용한 Petco는 구매 의도 6% 증가, 매장 방문 71% 급증, 전체 옴니 ROAS 30% 상승을 달성했다.
- YouTube 내 구매 경로는 결제 링크(checkout links) 또는 Universal Commerce Protocol 기반 결제를 통해 단축할 수 있다.
- 크리에이터 파트너십 부스트를 활용한 Javvy Coffee는 전환율이 50% 상승했으며, 제휴 파트너십 부스트로 마켓플레이스 내 태그된 콘텐츠를 증폭한 Shopee 등의 판매자는 평균 9배의 ROI를 기록했다.
- Demand Gen 캠페인에 새로 도입된 계절성 조정(Seasonality Adjustments)을 타겟 CPA 또는 타겟 ROAS 스마트 자동 입찰과 함께 사용하면 단기 프로모션 기간의 예상 전환율 상승을 반영하고 이후 기준선으로 복귀할 수 있다.

### Google for Mexico: 비즈니스를 넘어선 기술의 영향력
원문: https://blog.google/company-news/inside-google/around-the-globe/google-latin-america/google-for-mexico-2026-november/

- 구글은 최신 경제 영향 보고서를 통해 2025년 자사 도구가 멕시코 전역에서 하루 10억 페소 이상, 연간 총 3,820억 멕시코 페소가 넘는 경제 활동에 기여했다고 밝혔다.
- 보고서에 따르면 기업은 구글 애즈에 1페소를 투자할 때마다 평균 8페소의 상업적 수익을 올렸다.
- 구글은 Google for Mexico 2026에서 기상 악화 예보 지원과 스마트폰 실시간 경보 전달을 위해 국가수자원위원회(CONAGUA) 및 국립기상청과 협력한다고 밝혔다.
- 구글의 기상 예측 기술은 시간 단위로 최대 15일 앞선 예보를 제공한다.
- 구글은 멕시코에서 메모리가 적은 안드로이드 기기용으로 재설계한 Gemini 앱을 출시한다.

### 라스베이거스 레이스 주간을 맞아 구글 플레이에 대규모 보상 혜택 제공
원문: https://blog.google/products-and-platforms/platforms/google-play/auction-google-play-las-vegas/

- 구글 플레이는 라스베이거스 레이스 주간을 맞아 맥라렌 레이싱, 제프 해밀턴, 랜도 노리스 등의 독점 상품과 보상을 제공하는 'The Auction by Google Play'를 온·오프라인으로 진행한다.
- 미국 Play Points 골드 이상 등급 회원은 You 탭과 Perks 탭의 디지털 리워드 케이스에서 포인트 부스트와 수집품 당첨 기회를 얻을 수 있으며, 모든 등급 회원은 Use 탭에서 랜도 노리스 친필 사인 버킷햇 등 한정판 아이템을 포인트로 교환할 수 있다.
- 오프라인 행사는 11월 18일부터 3일간 라스베이거스 ARIA 리조트 앤 카지노에서 열리며 누구나 무료로 입장할 수 있다.
- Play Points 회원은 우선 입장과 랜도 노리스 전용 굿즈 드롭, 등급별 기본 토큰 지급 혜택을 받으며, 모든 방문객은 대형 가챠 휠을 돌려 토큰을 모을 수 있다.
- 방문객은 토큰을 키체인 참 바나 3D 프린팅 레이스카 꾸미기에 사용하거나 11월 20일 오후 7시(태평양 표준시)에 경매사 필리스 카오가 진행하는 희귀 수집품 경매 입찰에 활용할 수 있다.

### Genie 4 이용 가능
원문: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/

- 구글은 자격을 갖춘 Google AI Ultra 구독자를 대상으로 Genie 4, 업그레이드된 Genie 3, Project Genie 에이전트, 커뮤니티 갤러리를 포함한 새로운 Project Genie 경험을 배포하고 있다.
- Project Genie는 월드 모델과 Gemini 모델을 결합해 사용자가 브라우저에서 직접 인터랙티브 월드를 생성하고 탐색하며 변형할 수 있도록 지원한다.
- Genie 4는 탐색 도중 프롬프트를 입력해 날씨 변경, 캐릭터 추가, 행동 방향 전환 등 환경을 실시간으로 편집할 수 있으며, 주변 음향과 캐릭터 대사 같은 실시간 적응형 네이티브 오디오를 제공한다.
- 모델 선택기에서 계속 이용할 수 있는 Genie 3는 생성당 탐색 시간이 기존 60초에서 최대 3분으로 연장되었으며, 다중 월드 연결, 360도 파노라마 이미지 기반 생성, 자연어 프롬프트 기반 실시간 월드 내 이벤트 기능이 추가되었다.
- 새로운 Project Genie 에이전트는 자연어 대화를 통해 구글의 멀티모달 모델을 조율하여 세계의 초기 비주얼과 맞춤형 배경 음악을 제작하며, 탐색 중 세션에 Gemini 모델을 불러올 수도 있다.

### Gemini 4 Neon 소개
원문: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/

- 구글은 복잡한 소프트웨어 엔지니어링, 지식 노동, 과학 워크플로우 작업을 빠르게 완료할 수 있는 Gemini 4 Neon을 공개했다.
- Gemini 4 Neon은 100만 토큰 컨텍스트 창에서 스프레드시트, PDF, 차트, 오디오, 비디오 입력을 종합해 구조화된 결과물로 변환할 수 있다.
- 벤치마크 평가에서 Artificial Analysis Intelligence Index(xhigh 추론 수준) 61점으로 전체 3위, Vals Index 2위(70.9%), Legal Research Bench·Tax Agent Bench·AutomationBench(56.3%)·Vending-Bench 2(16,843달러) 1위, 4,200개 이상의 실제 에이전트 세션을 평가한 Agent Arena Index(1336점) 및 조종성(steerability) 부문 2위를 기록했다.
- 구글 내부 Antigravity 테스트에서 역대 최저 수준의 허위 정보 생성(fabrication) 비율을 기록했으며, Chartography 73.5%, Agents' Last Exam v1.1 75.8%의 점수를 얻었다.
- 가격은 입력 토큰 100만 개당 3달러(캐시된 입력은 95% 할인된 0.15달러), 출력 토큰 100만 개당 15달러이며, Google AI Studio의 Gemini API, 기업용 Gemini, Google AI Pro 및 Ultra 유료 구독자용 Google Antigravity와 Gemini 앱에서 제공된다.

## Google DeepMind

### Genie 4 출시
원문: https://deepmind.google/blog/genie-4-is-now-available/

- 구글 딥마인드는 자격 요건을 갖춘 Google AI Ultra 구독자에게 Genie 4, Genie 3 업그레이드, Project Genie 에이전트, 커뮤니티 갤러리가 포함된 새로운 Project Genie 경험을 제공하고 있다.
- Genie 4에서는 월드를 탐색하는 도중에 새 프롬프트를 입력해 날씨를 바꾸거나 캐릭터를 추가하고 행동을 전환하는 등 환경을 실시간으로 편집할 수 있다.
- Genie 4는 처음으로 주변 음향과 캐릭터 대사를 포함해 장면 전개에 맞춰 실시간으로 적응하는 네이티브 오디오를 영상과 함께 제공한다.
- Project Genie의 모델 선택기에서 계속 이용할 수 있는 Genie 3는 세션당 생성 탐험 시간이 60초에서 최대 3분으로 연장되었으며 다중 월드 연결, 360도 파노라마 이미지 기반 생성, 실시간 자연어 이벤트 기능을 지원한다.
- 새로운 Project Genie 에이전트는 사용자의 자연어 설명을 바탕으로 구글의 멀티모달 모델들을 조율해 초기 비주얼과 분위기에 맞춘 맞춤형 배경 음악을 생성한다.

### Gemini 4 Neon 소개
원문: https://deepmind.google/blog/introducing-gemini-4-neon/

- Gemini 4 Neon은 xhigh 사고 수준 기준 Artificial Analysis Intelligence Index에서 61점으로 전체 3위를 기록했고, Vals Index에서는 70.9%로 2위, Legal Research Bench와 Tax Agent Bench에서는 각각 1위를 차지했다.
- 4,200건 이상의 실제 에이전트 세션으로 평가한 Agent Arena Index에서 1336점으로 종합 2위 및 조종 가능성(steerability) 2위에 올랐으며, Google Antigravity 내부 테스트에서 자사 최저 환각(fabrication) 비율을 기록했다.
- 가격은 입력 토큰 100만 개당 3달러(캐시 입력 토큰은 95% 할인된 0.15달러), 출력 토큰 100만 개당 15달러이며 100만 토큰 컨텍스트 창에서 스프레드시트, PDF, 차트, 오디오, 비디오를 통합 처리한다.
- Surge AI의 금융·회계·스프레드시트 모델링·복합 제약 준수 대부분 벤치마크와 Zapier AutomationBench(56.3%), Andon Labs Vending-Bench 2(16,843달러)에서 1위를 차지했고 Chartography 73.5%, Agents' Last Exam v1.1 75.8%를 기록했다.
- Gemini 4 Neon은 Google AI Studio의 Gemini API, Gemini for business, 유료 Google AI Pro 및 Ultra 구독자 대상 Google Antigravity와 Gemini 앱에서 제공된다.

## OpenAI

### Codex 샌드박스 살펴보기
원문: https://openai.com/index/inside-the-codex-sandbox

- OpenAI는 에이전트 보호를 위한 심층 방어 접근의 일환으로, Codex가 사용자가 제어하는 파일시스템과 네트워크 제한 범위 내에서 명령을 실행하도록 Codex 샌드박스를 구축했다.
- 사용자는 Codex 세션의 파일시스템 및 네트워크 제한을 정의하는 권한 프로필을 통해 샌드박스를 설정할 수 있다.
- Git 저장소를 워크스페이스 루트로 삼는 기본 내장 :workspace 권한 프로필은 워크스페이스 내부 쓰기를 허용하되 .git과 .codex 같은 디렉터리는 읽기 전용으로 유지해 .codex/config.toml이나 .git/hooks 아래 Git 훅의 직접 변경을 방지한다.
- :workspace 프로필은 컴파일러, 런타임, 빌드 도구가 저장소 외부의 SDK, 라이브러리, 설정에 의존하기 때문에 사용자의 기존 OS 권한 범위 내에서 광범위한 파일시스템 읽기를 허용하지만, 이로 인해 API 키가 포함된 설정 파일 등 기기 내 민감한 파일도 읽힐 수 있는 트레이드오프가 있다.
- :workspace 프로필은 네트워크 접근을 비활성화해 명령이 읽을 수 있는 데이터를 외부 서비스로 직접 업로드하거나 유출하려는 시도를 차단한다.
