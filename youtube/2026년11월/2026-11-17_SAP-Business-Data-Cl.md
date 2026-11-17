# YouTube Tech — 2026-11-17

## SAP

### SAP Business Data Cloud의 SAP Lakehouse 신기능 요약
https://www.youtube.com/watch?v=PMcDfp9PGTM

- SAP Business Data Cloud 내 SAP Lakehouse의 새로운 기능을 소개하는 영상입니다.
- Philipp Herzig가 SAP 및 비-SAP 시스템 간 불필요한 데이터 이동 없이 데이터를 접근·조회·공유하는 방법을 설명합니다.
- Dremio 통합을 통해 데이터를 이동하지 않는 연합 데이터 접근(Federated data access)을 지원합니다.
- 네이티브 Apache Iceberg와 Apache Polaris 기반 카탈로그를 제공합니다.
- 이를 통해 기업 시스템 전반의 데이터 상호운용성을 높이는 구성을 다룹니다.

## NVIDIA Developer

### VSS 3.3과 Cosmos로 NVIDIA Jetson 기반 시각 AI 에이전트 가속화
https://www.youtube.com/watch?v=c0gdviC_OeI

- NVIDIA Jetson 엣지 AI 플랫폼에서 VSS 3.3 블루프린트, Cosmos, Jetson 에이전트 스킬을 결합한 시각 AI 에이전트 개발 워크플로우를 다룹니다.
- Jetson Agent Skills를 사용해 코딩 에이전트가 대상 하드웨어 리소스를 점검하고 JetPack 및 컨테이너 호환성을 확인해 런타임과 추론 환경을 구성합니다.
- VSS 3.3 에이전트 스킬을 활용해 자연어 기반 애플리케이션 요청을 설정된 배포 구성으로 변환합니다.
- Cosmos가 이벤트 검증을 위한 영상 이해를 제공하며, 영상 검색·알림·이벤트 검토 기능을 Jetson 상의 단일 워크플로우로 통합합니다.
- 엣지 환경의 메모리 및 연산 제약을 고려해 배포를 검증하고 기능을 추가하는 과정을 안내합니다.

### 두 개의 프롬프트로 학습용 데이터셋 구축하기: Encord·Voxel51 사례 | Cosmos Labs
https://www.youtube.com/watch?v=c5or9gzM6Zg

- NVIDIA Cosmos Data Factory 스킬과 블루프린트를 사용해 한 번의 프롬프트로 환경을 설정하고 다음 프롬프트로 데이터 워크플로우를 실행하는 방법을 다룹니다.
- NVIDIA, Voxel51, Encord가 참여해 자율주행, 로보틱스, 비전 AI 에이전트용 학습 데이터 큐레이션·증강·생성·라벨링 기법을 소개합니다.
- Voxel51은 Porsche가 NVIDIA Cosmos Data Factory를 기반으로 자율주행 차량 데이터를 큐레이션하고 증강하는 사례를 발표합니다.
- Encord는 ANYbotics와 함께 Cosmos Data Factory를 활용해 로봇 점검의 이상 탐지용 합성 데이터를 구축한 사례를 설명합니다.
- 기존 데이터 증강과 희소 학습 예제 생성 방법을 다루며, NVIDIA Cosmos 3의 사후 학습 및 배포에 대한 실시간 질의응답도 진행됩니다.

### vLLM으로 두 대의 NVIDIA DGX Station에서 GLM-5.3 서빙하기
https://www.youtube.com/watch?v=opRXPRnSkxk

- 7,530억 파라미터 MoE 모델인 GLM-5.3의 NVFP4 체크포인트(약 464GB)가 단일 NVIDIA GB300 GPU 메모리(252GB)를 초과하므로, ConnectX-8로 연결한 두 대의 NVIDIA DGX Station에 vLLM과 텐서 병렬화를 적용해 CPU 오프로드 없이 GPU 메모리에만 가중치를 적재한다.
- 두 DGX Station에서 RDMA 연결용 네트워크 값을 수집하고 고정(pinned) 체크포인트를 내려받아 두 번째 시스템에 복사한 뒤, 양쪽에서 동일한 vLLM 스크립트를 실행해 단일 OpenAI 호환 API로 모델을 서빙한다.
- API 헬스 체크, TCP 소켓으로 폴백하지 않고 GPU가 네트워크를 통해 직접 통신하는지 확인하는 RDMA 검사, 각 GPU의 vLLM 워커를 확인하는 nvidia-smi 점검 및 채팅 요청 응답 확인으로 서비스를 검증한다.
- NVIDIA AIPerf와 SPEED-Bench Coding 프롬프트로 동시 요청 수 1과 8의 테스트 및 1·8·16·32 기준 참고 결과를 제시해 동시성 증가에 따른 사용자당 처리량과 요청 지연 시간 변화를 측정한다.
- 전체 벤치마크와 단계별 실행 명령어가 정리된 NVIDIA 기술 블로그 및 두 대의 DGX Station 연결 플레이북(Connect Two DGX Stations playbook) 링크를 제공한다.

## NAVER D2

### 네이버 전 지면의 사용자 행동을 학습하는 추천 모델 개발기
https://www.youtube.com/watch?v=Cc22uWO8i5c

- NAVER Engineering Day 10th 사내 기술 교류 행사에서 발표된 세션으로, 네이버의 검색·피드·광고 등 다양한 도메인 데이터와 추천 기술을 연결하는 버티컬 추천 모델의 개발 및 서비스 적용 경험을 소개한다.
- 목차상 개발 배경과 목표, VMs 시스템 구조, VMs 리트리버와 통합 랭커, 지면별 적용 현황과 성과를 차례로 다룬다.
- 여러 서비스와 도메인의 사용자 행동 데이터를 활용한 크로스 도메인 추천과 시퀀스 기반 추천·생성형 추천 등 다양한 추천 모델의 개발 및 서비스 적용에 관심 있는 대상을 위한 세션이다.
- 대규모 추천 모델의 실시간 추론, GPU 서빙 최적화 및 VMs 서빙과 최적화 내용을 공유한다.
- 파운데이션 모델(Foundation Model)의 지식을 경량 모델로 전이하는 지식 증류(Knowledge Distillation) 기반의 도메인 간 지식 전이 방향과 향후 계획을 설명한다.

## NVIDIA Developer

### NVIDIA Nemotron 3.5 Super VL을 활용한 오픈 모델 인도 언어 AI
https://www.youtube.com/watch?v=qtsh2OmbQqM

- NVIDIA와 IIT Madras AI4Bharat 연구소가 22개 인도 언어를 지원하는 오픈 모델 기반 인도 언어 AI 협력을 소개하는 라이브스트림 세션이다.
- 22개 언어에 걸친 3조 토큰 규모의 오픈 인도 언어 데이터셋과 선별된 영어 콘텐츠를 인도 언어 학습 데이터로 변환하는 데이터 생성 파이프라인을 다룬다.
- 수학, STEM, 코드 및 인도 언어 특화 역량을 포함한 15개 이상의 평가 항목으로 구성된 인도 언어 LLM 벤치마크 스위트의 구축과 공개 내용을 설명한다.
- 텍스트와 이미지를 처리·추론하고 대량의 특화 작업을 수행하는 자율 에이전트용으로 제작된 멀티모달 오픈 모델 Nemotron 3.5 Super VL의 아키텍처와 학습 기법, 설계 원칙을 소개한다.
- 공개된 가중치·학습 레시피·데이터셋을 활용한 도메인 및 작업별 커스터마이징 가능성과 멀티 모델 에이전트 파이프라인 통합 방법을 다룬다.

### 음성 인식을 넘어: Nemotron 3.5 Transcribe | Nemotron Labs
https://www.youtube.com/watch?v=HXMbNl5KgeA

- Nemotron 3.5 Transcribe는 약 40억 개의 활성 파라미터를 갖는 300억 파라미터 규모의 오픈 웨이트 MoE 모델로, 단일 체크포인트에서 40개 언어 전사, 화자 식별, 번역 및 오디오 이해를 제공한다.
- NVIDIA 엔지니어와 Hugging Face 파트너가 모델의 기능을 소개하고 녹음된 오디오로 라이브 데모를 진행하며 Hugging Face에서 NVIDIA NeMo 또는 transformers로 실행하는 방법을 설명한다.
- 이름, 전문 용어, 도메인 어휘에 대한 인식 정확도를 높이기 위해 문맥 기반 프롬프팅을 활용하는 방법을 다룬다.
- 단일 체크포인트에서 화자 식별과 번역이 작동하는 원리와 Granary v2 데이터셋을 사용해 모델을 자체 도메인에 맞게 적응시키는 방법을 소개한다.
- 녹음된 오디오에 적합한 오프라인 모델과 실시간 사용을 위한 스트리밍 인식기를 각각 언제 사용해야 하는지 설명한다.

## NAVER D2

### 카페 관리도구 개편기: 문서는 낡았고, 사람은 떠났고, 코드만 남았다.
https://www.youtube.com/watch?v=RnRZR-rz5ks

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 코드만 남아 있던 14년 된 구 카페 관리도구를 AI와 함께 분석한 내용을 다룬다.
- Storybook과 MSW로 화면과 동작을 재현하며 새로운 카페 스튜디오를 개발한 과정을 설명한다.
- 개발 과정에서 기획, 디자인, BE와의 협업 및 일하는 방식이 어떻게 달라졌는지 공유한다.
- 레거시 시스템 개편 개발자, AI 실무 활용 엔지니어, 화면과 정책을 함께 검증하려는 기획자·디자이너를 대상으로 프로젝트 개요, 구 관리도구 분석, 신규 스튜디오 개발, 일하는 방식, 마무리 순서로 진행한다.

### Image AI 서빙 최적화: CPU와 GPU의 빈 시간을 줄여 H100 67장을 절감하기까지
https://www.youtube.com/watch?v=FHbA-aaQbGg

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- SNOW의 16개 Image AI 서비스에서 응답 속도와 안정성을 높이면서 H100 환산 약 67장의 GPU 자원을 절감한 경험을 공유한다.
- 기존 서빙 구조의 문제를 살펴보고 LitServe 전환을 통해 불필요한 연산과 CPU·GPU 대기 시간을 줄인 과정을 소개한다.
- 실제 트래픽에 맞춘 파라미터 조정과 작업 분리 및 여러 서비스의 GPU 공유 적용 과정을 다룬다.
- 총 절감 기여량과 누적 개선 및 향후 과제를 정리하며 Image AI 서빙 엔지니어를 발표 대상으로 한다.

### Image AI 서빙 최적화: CPU와 GPU 유휴 시간을 줄여 H100 GPU 67장 절감하기
https://www.youtube.com/watch?v=w3EL9TSPK3U

- SNOW의 16개 이미지 AI 서비스를 LitServe로 이전한 발표 영상으로 한국어 버전 링크도 함께 안내한다.
- 지연 시간과 안정성을 개선하면서 H100 환산 약 67대의 GPU 자원을 절감한 과정을 설명한다.
- 연산 간소화, CPU·GPU 유휴 시간 감소, 트래픽 기반 튜닝, GPU 공유를 통한 최적화 기법을 소개한다.
- 목차는 도입, LitServe 전환, 파라미터 튜닝, GPU 공유 및 추가 최적화, 결과와 향후 과제로 구성된다.
- 지연 시간을 줄이고 GPU 활용률을 높이려는 이미지 AI 모델 서빙 엔지니어를 대상으로 한다.

### 노트북을 닫아도 개발은 계속된다: 자율 그래프 주도 개발
https://www.youtube.com/watch?v=kVLht_OuxA4

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상입니다.
- 자율 그래프 주도 개발은 사람의 직접적인 지시 없이 그래프가 프로젝트 진행을 주도하는 방식입니다.
- 스펙 문서와 코드는 AI Agent 루프가 작성하며, 결정론적 코드가 이를 기계적으로 검사합니다.
- 발생한 결함은 피드백 루프를 통해 자동으로 바로잡고, AI가 필요할 때만 사람을 호출하여 주도권을 역전시킵니다.
- 자율 그래프 주도 개발 방법론에 관심 있는 개발자와 기획자를 대상으로 배경, 실행 과정, 어려움 극복, 성과 및 임팩트 순서로 진행됩니다.

## Cole Medin

### 내가 검증하는 속도보다 빠르게 코드를 작성하는 AI 에이전트
https://www.youtube.com/watch?v=83NRvB_Gusk

- Sonar의 2027 State of Code 보고서에서 개발자와 엔지니어링 매니저의 76%는 검증 가능한 속도보다 빠르게 AI 코드를 생성한다고 응답했습니다.
- 영상 제작자는 에이전트가 24시간 풀 리퀘스트를 여는 소프트웨어 팩토리를 운영하며 동일한 문제를 겪고 있다고 설명합니다.
- AI 코드는 겉보기에 올바른 경우가 많아지면서 미묘한 버그가 검수를 빠져나가는 현상이 나타납니다.
- 이를 다루기 위해 에이전트가 코드를 자유롭게 작성하더라도 에이전트가 제어하지 않는 검사를 통과해야만 병합되도록 제한합니다.
- Sonar와의 협업으로 제작된 영상이며 본문에 해당 보고서 전체를 확인할 수 있는 링크가 포함되어 있습니다.

## Unreal Engine

### Bluey’s Happy Snaps | 게임 프로필 | Unreal Engine
https://www.youtube.com/watch?v=TWD7bTUEZKs

- 게임로프트 브리즈번(Gameloft Brisbane)이 언리얼 엔진 5의 애니메이션 도구와 기술을 활용해 2D 애니메이션 《블루이(Bluey)》의 세계를 3D로 구현한 사례를 소개한다.
- 《Bluey’s Happy Snaps》는 블루이와 빙고가 원작 애니메이션의 장소를 탐험하며 아빠의 오래된 카메라로 사진을 찍어 스크랩북을 채우는 게임이다.
- 개발팀은 원작 특유의 시각적 스타일을 게임에 담아내기 위해 언리얼 엔진을 전면적으로 도입했다.
- 영상에서는 언리얼 엔진 5의 애니메이션 툴셋이 게임 속 캐릭터들을 구현하는 데 수행한 역할을 살펴본다.
- 메타데이터 해시태그로 Sequencer, ControlRig, UnrealInsights 등의 언리얼 엔진 관련 도구가 함께 명시되어 있다.

## NVIDIA Developer

### 배달 로봇이 예기치 못한 상황에 대비하도록 돕는 방법
https://www.youtube.com/watch?v=Xi_NPUw0wkc

- 코코 로보틱스(Coco Robotics)의 배달 로봇은 Uber Eats, DoorDash, Deliveroo, Wolt 등의 플랫폼을 통해 배달을 수행하고 있다.
- 이 영상은 한 번의 배달 주행 기록을 여러 엣지 케이스(edge-case) 테스트 세트로 활용하는 방식을 다룬다.
- 코코 로보틱스는 NVIDIA Cosmos를 사용해 실제 운행 중인 로봇의 주행 영상(fleet video)을 새로운 장면 변형으로 변환한다.
- 이를 통해 로봇이 실제 도로에서 드문 돌발 상황을 마주하기 전에 사전에 대응 연습을 할 수 있도록 한다.
- NVIDIA Developer 채널에서 공개한 영상으로 #Robotics, #robotdelivery, #NVIDIACosmos 태그가 포함되어 있다.

## Google Cloud Tech

### Looker CLI 심층 분석
https://www.youtube.com/watch?v=3FmEdUNeqIw

- Google Cloud Tech 채널에서 Chrissie Goodrich가 진행하는 Looker CLI 관련 심층 논의 영상이다.
- Looker CLI는 Looker 및 에이전트(Agents)와 함께 수행할 수 있는 작업 범위를 확장해 주는 도구다.
- 이 도구는 성능 보고서, 지속적 개발(continuous development) 도구, 전체 API 엔드포인트 모음을 제공한다.
- 영상에는 Looker CLI를 활용해 워크플로우 속도를 높이는 방법을 다루는 데모와 예제가 포함되어 있다.
- 관련 제품으로 Looker가 언급되었으며 추가 학습을 위한 별도 유튜브 영상 링크가 함께 안내되어 있다.

## Cole Medin

### AI 소프트웨어 팩토리의 5가지 유형 설명
https://www.youtube.com/watch?v=r5iPi8RL7A8

- AI 소프트웨어 팩토리의 개념과 대표적인 다섯 가지 유형의 장단점을 설명하며 통제와 자율성의 균형을 다룹니다.
- 다섯 가지 유형으로 다크 팩토리, 플릿 팩토리, PR 팩토리, 릴리스 팩토리, 자가 개선 팩토리를 순서대로 소개합니다.
- 인간 개입(Human in the Loop)의 수준과 그 변화 방식을 함께 살펴봅니다.
- 발표자의 릴리스 팩토리 내부 구성 사례를 공유하고 상황별 팩토리 선택 기준을 제시합니다.
- 오픈소스 AI 소프트웨어 팩토리 저장소(coleam00/ai-software-factory)와 12월 2일 라이브 부트캠프 정보를 안내합니다.

## NVIDIA Developer

### GTC DC 개발자 커뮤니티 애프터 아워즈
https://www.youtube.com/watch?v=SdmuM4NLEsM

- NVIDIA Developer가 GTC DC를 주제로 진행하는 개발자 중심의 라이브 대담이다.
- 오픈 모델, AI 에이전트, AI 안전성, 가속 컴퓨팅 등 GTC DC의 주요 기술 주제를 다룬다.
- 헬스케어, 금융 서비스, 피지컬 AI, 정부 분야에서의 기술 적용 잠재력을 논의한다.
- 기술들이 실제 워크플로와 연결되는 방식과 GTC DC에서 살펴볼 내용을 소개한다.
- 학습 및 구축 기회를 찾을 수 있는 곳을 안내하며 실시간 질문을 받아 대화를 이어간다.

### GTC DC 개발자 커뮤니티 스포트라이트
https://www.youtube.com/watch?v=ON4Jq8aajWI

- NVIDIA Developer가 GTC DC에서 AI 에이전트의 산업별 적용을 주제로 진행하는 세션이다.
- 개발자가 특화 에이전트에 접근하는 방식과 모델을 기업 지식에 연결하는 방법을 살펴본다.
- 안전성 및 배포 관련 과제를 해결하는 방안을 다룬다.
- 대담과 데모를 통해 헬스케어, 금융 서비스, 정부 분야의 행사 주제를 개발자용 실무 내용으로 연결한다.
- 다음 프로젝트에 활용할 도구와 리소스를 소개하고 실시간 청중 질의응답을 진행한다.
