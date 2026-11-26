# YouTube Tech — 2026-11-26

## NAVER D2

### OmniEvaluator: AI 모델과 에이전트를 위한 통합 평가 프레임워크
https://www.youtube.com/watch?v=UML-8sdLDH4

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 모달리티마다 별도로 구성해야 했던 평가 환경을 통합해 텍스트·이미지·비디오·오디오를 한 번의 설치와 명령으로 평가하고 실행을 재현할 수 있게 만든 시스템을 소개한다.
- AI 서비스 기획자의 후보 모델·API·툴 조합 정량 비교와 AI 엔지니어의 패치·버전·서빙엔진별 차이 확인 등을 주요 활용 대상으로 다룬다.
- 평가의 어려움에서 출발해 OmniEvaluator 구조, Agent Harness, 리더보드·샘플 뷰어·Trigger를 포함한 대시보드를 설명한다.
- Claude Plugin과 팀 운영 사례까지 목차에 포함해 통합 평가 환경 구축 내용을 공유한다.

### AI가 만든 결과를 그대로 믿고 계신가요?
https://www.youtube.com/watch?v=d0Ulw-4u2Z8

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 테스트를 전부 통과했지만 실제로는 결함이 남아 있던 경험에서 출발해 AI의 자기 보고를 기계가 반증하게 만든 방법을 공유한다.
- 돌연변이 테스팅, 훅, 에이전트 팀이라는 세 가지 검증 방식을 핵심 내용으로 다룬다.
- AI가 짠 테스트의 신뢰성, 규칙 준수 여부, AI의 자기검증 가능성 등 세 단계의 문제를 차례로 짚는다.
- AI가 생성한 코드·테스트 검증과 여러 AI 에이전트를 활용한 개발·리뷰에 관심 있는 대상을 위해 구성되었다.

### 운영자의 시간을 아끼는 AI 에이전트 1부 - RCA·Q&A 운영 지식 그래프
https://www.youtube.com/watch?v=0Ed8CUSrZgo

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 세션을 공개한 영상이다.
- 운영자의 장애 분석 시간을 줄이기 위해 흩어져 있던 RCA와 Q&A를 운영 지식 그래프로 구축하고 운영한 경험을 소개한다.
- 기존 운영 문의 응답 방식과 운영 문의 속 RCA 구조를 분석하고 대화를 그래프로 구성해 검색 정확도를 높이는 과정을 다룬다.
- 진단이 아닌 질문 중심의 Q&A 처리 방식과 함께 최종 구조 및 Care AI 구성을 설명한다.
- AI 에이전트로 반복되는 운영 업무를 효율화하려는 대상을 위해 성과와 향후 계획까지 공유한다.

### 운영자의 시간을 아끼는 AI 에이전트 2부 - MCP 부터 Agent 설계까지
https://www.youtube.com/watch?v=DRghWwm3dt8

- 네이버 사내 기술 교류 행사인 NAVER Engineering Day 10th에서 발표된 2부 세션을 공개한 영상이다.
- 운영자용 AI 에이전트를 만들기 위해 MCP 기반 도구 설계부터 컨텍스트 구성, 에이전트의 판단과 실행 흐름까지 실제 구현 경험을 소개한다.
- 초기 에이전트 제작, MCP 응답 설계, 모델과 코드의 역할 비교, 답변 설계, 결과 순으로 발표를 전개한다.
- 주문 데이터 문의부터 답변까지의 과정을 다루는 데모가 목차에 포함되어 있다.
- LLM 에이전트의 운영 업무 적용, MCP 서버·도구 설계, 답변 정확도와 신뢰성 향상에 관심 있는 대상을 위해 구성되었다.

## NVIDIA Developer

### Google Cloud와 함께하는 GPU 기반 JAX 활용
https://www.youtube.com/watch?v=StEoOVLOIEc

- Google Cloud AI 엔지니어 Ivan Nardini와 NVIDIA 개발자 애드보킷 Ekaterina Sirazitdinova가 NumPy 프로토타입을 다중 NVIDIA GPU 학습으로 확장하는 JAX 실습을 진행합니다.
- NVIDIA NGC 컨테이너에서 시작해 JAX의 GPU 인식 여부를 확인하고, `jit`, `grad`, `vmap`을 사용해 코드를 컴파일·미분·배치 처리하는 방법을 설명합니다.
- Google Cloud와 NVIDIA의 공동 학습 경로 노트북을 따라 다중 GPU 메시(mesh)에 학습 배치를 샤딩(shard)하는 과정을 다룹니다.
- XProf와 NVIDIA Nsight Systems를 활용해 재컴파일(recompilation) 및 데이터 전송 병목을 진단하는 방법을 보여줍니다.
- 사전 녹화된 세션 방영 중 발표자들이 채팅을 통해 시작 방법, 성능 튜닝, 워크로드 확장에 관한 질의응답에 참여하며, 관련 학습 경로 링크가 함께 제공됩니다.

## kakao tech

### 73.3%로 떨어진 4비트 양자화 | 어? 이게 되네. 병목 분석부터 커널 개발까지 Throughput 극대화를 위한 Kanana 서빙 최적화 딥다이브 | Model & Agent
https://www.youtube.com/watch?v=w5FNLA03o-o

- 제목에 따라 73.3%로 떨어진 4비트 양자화 사례와 함께 병목 분석부터 커널 개발까지 처리량(Throughput) 극대화를 위한 Kanana 서빙 최적화 내용을 다룹니다.
- 카카오 AI Engineering팀에서 모델 경량화와 서빙 엔진 최적화를 연구·개발하는 김형주(jacob.crux)가 발표자로 참여합니다.
- 프로덕션 환경에서 Kanana MoE 모델을 서빙할 때 GPU 메모리 부족으로 발생하는 KV 캐시 제한과 처리량 저하 문제를 해결한 과정을 공유합니다.
- 모델 가중치부터 서빙 엔진, 커널 단계까지 각 영역의 병목을 찾아내고 최적화한 LLM 서빙 노하우를 소개합니다.
- ifkakao26의 Model & Agent 세션으로, 설명란에 안내된 공식 타임테이블 링크(sessionId=70)에서 발표자료를 확인할 수 있습니다.

## SAP

### 클라우드 PLM에 대한 10가지 오해 바로잡기 | SAP Integrated Product Development
https://www.youtube.com/watch?v=sr6larqxSvA

- SAP 글로벌 마케팅의 몬태나와 SAP PLM 교육·도입 총괄 아네트 가르시아 로렌조가 출연해 SAP Integrated Product Development(SAP IPD)에 대한 10가지 오해를 다룬다.
- 이 영상은 다양한 규모와 산업의 기업이 제품 개발과 공급망을 연결해 제품을 설계·개발·관리할 수 있도록 돕는 SAP IPD의 역할을 소개한다.
- 챕터 구성에는 모든 규모의 기업을 위한 확장성, 이산 및 공정 제조, 제품 데이터 제어 및 보안 주제가 포함된다.
- 또한 SAP S/4HANA 없이 시작하기, 기존 CAD 도구 연결, 전체 제품 데이터 마이그레이션 없이 시작하기, 기존 PLM 시스템에서의 데이터 마이그레이션이 다뤄진다.
- 제품 개발에서의 AI 어시스턴트와 에이전트, 지속가능성 및 규제 준수, 공식 SAP 교육·학습 자료 안내도 챕터에 포함된다.

## NVIDIA Developer

### RFP에서 제안서까지: NVIDIA DGX Station for Windows에서 AEC 워크플로우를 실행하는 에이전트형 AI
https://www.youtube.com/watch?v=hofffzgOLOE

- NVIDIA GB300 Grace Blackwell Ultra Superchip 기반 단일 NVIDIA DGX Station for Windows에서 에이전트가 제안요청서(RFP)를 건축·엔지니어링·건설(AEC) 콘셉트 패키지로 전환하는 과정을 시연한다.
- Windows on Arm 환경에서 Hermes Agent가 로컬 호스팅 오픈 웨이트 모델 및 전용 스킬과 연동해 Rhino, SAP2000, FreeCAD, Blender, ComfyUI 같은 Windows 앱을 가시적 워크플로우로 제어한다.
- 복합용도 트윈타워 콘셉트 시연에서 에이전트는 프로젝트 데이터와 규정 준수 점검이 담긴 Microsoft Excel 통합 문서를 생성하고 매싱·구조 모델을 만들어 SAP2000에서 구조 진단을 수행한다.
- 이후 IFC 내보내기를 지원하는 FreeCAD BIM 모델, A2 규격 도면 7장 세트, 렌더링된 프레젠테이션 이미지를 제작하며, 추론과 렌더링은 클라우드 없이 워크스테이션 내에서 처리돼 데이터가 온프레미스에 유지된다.
- 생성된 결과물은 최종 발행 엔지니어링 설계가 아닌 전문가 검토용 콘셉트 수준 산출물이며, 해당 워크스테이션은 최대 748GB 일관성 메모리와 최대 20페타플롭스의 FP4 성능을 지원한다.

## OpenAI

### 부재 중에도 dot으로 업무를 계속 진행하는 방법
https://www.youtube.com/watch?v=A4UNP-axGHU

- 부재 중에 진행 중인 프로젝트를 감시하고 확인이 필요한 사항을 알리며 이동 중에도 다음 단계를 검토·승인할 수 있도록 돕는 dot 활용 워크플로를 소개한다.
- 지정한 시각과 시간대까지 특정 Slack 채널과 온콜 채널을 모니터링하도록 지시하는 프롬프트 예시를 제공한다.
- 관련 피드백은 기존 Linear 티켓에 묶고 새로운 요청이나 문제인 경우 새 티켓을 생성해 Slack 메시지를 연결하도록 설정한다.
- 서비스 장애, 심각한 인시던트, 핵심 기능 오작동에 대한 다수 보고가 발생한 경우에만 알림을 보내도록 조건을 제한한다.
- Codex가 활성화된 환경에서는 Codex 스레드를 실행해 온콜 경보를 조사하고 결과를 보고하되 검토 전에는 코드를 변경하지 않도록 지시한다.

## Google Cloud Tech

### AlloyDB Express 출시: 몇 초 만에 PostgreSQL 배포하기
https://www.youtube.com/watch?v=g6NOVhxWGGk

- AlloyDB Express는 에이전트 기반 개발을 위해 즉시 프로비저닝과 유휴 시 0으로 축소되는 기능을 지원하는 AlloyDB for PostgreSQL의 새 등급이다.
- 긴 프로비저닝 대기나 유휴 컴퓨팅 비용 없이 몇 초 만에 데이터가 채워지고 연결된 PostgreSQL 18 데이터베이스를 구축하는 과정을 시연한다.
- Google Antigravity와 AlloyDB Model Context Protocol(MCP) 서버를 활용해 클러스터와 기본 인스턴스를 프로비저닝한다.
- 샘플 데이터가 포함된 관계형 리테일 스키마를 생성하고 AlloyDB Auth Proxy를 통해 로컬 터미널에서 연결하는 방법을 보여준다.
- ADK나 AI 지원 도구와 AlloyDB 원격 MCP를 함께 사용하는 코드랩 및 Auth Proxy, 공식 문서 링크를 함께 안내한다.

## Google for Developers

### Gemini 4 활용을 위한 개발자 팁 5가지
https://www.youtube.com/watch?v=WN5O4vWCa54

- Google DeepMind의 Patrick Löber와 Geneviève Huskens가 길고 복잡한 엔지니어링 작업을 Gemini 4에 위임하는 5가지 팁을 공유한다.
- 장기 작업 실행 전 Google AI Studio의 플랜 모드로 의도를 맞추고 이미지나 화면 녹화 같은 멀티모달 자료를 참조로 제공하는 방법을 다룬다.
- 테스트 스위트나 브라우저 스크린샷처럼 모델이 작업 결과를 직접 검증할 수 있는 구체적인 수단을 부여하는 방법을 설명한다.
- Gemini 4를 상위 오케스트레이터로 사용하여 더 작은 하위 에이전트들에게 작업을 위임하는 구성을 소개한다.
- 세션을 회고해 재사용 가능한 SKILL.md 파일로 정리하고 Gemini API 스킬을 설치해 기존 프로젝트를 업그레이드·연동하는 내용도 포함한다.

## NVIDIA Developer

### Roboflow와 NVIDIA Cosmos 3를 활용한 비디오 추론 및 모델 파인튜닝
https://www.youtube.com/watch?v=IvNCYllEBZw

- NVIDIA와 Cosmos Coalition 파트너인 Roboflow가 NVIDIA Cosmos 3 및 Roboflow를 이용해 비전 AI 애플리케이션을 구축하는 방법을 다룬다.
- Roboflow에서 Cosmos 3 Edge를 사용해 비디오 추론을 수행하는 방법을 설명한다.
- 라벨링부터 모델 예측까지의 워크플로우에 따라, 라벨링된 비디오로 Cosmos 3 Edge를 파인튜닝해 동작과 발생 시점을 인식하는 과정을 보여준다.
- 예측된 동작 타임라인을 SOP와 비교해 조립 단계를 검증하고 사이클 타임을 분석하는 방법을 다룬다.
- Roboflow의 Cosmos 3 평가 결과에서 얻은 교훈을 활용해 프롬프팅과 장면 구도를 개선하는 방법을 소개한다.

## Cole Medin

### AI 공격에 대비하는 최선의 방어: 내 프로젝트 먼저 해킹하기
https://www.youtube.com/watch?v=f1gAilgILeI

- 공격자들이 AI를 이용해 버그를 빠르게 찾아 악용하는 방식과 동일한 접근법을 자신의 프로젝트에 먼저 적용하는 과정을 다룬다.
- 공격자 에이전트가 취약점을 찾기 위해 가장 먼저 실행하는 빠른 점검 항목과 다섯 가지 질문을 소개한다.
- 1시간 만에 치명적인 버그가 발견된 Java4Shell 사례를 다룬다.
- 무료 오픈소스인 Cloudflare의 보안 감사 스킬(security-audit-skill)을 설치하고 본인 프로젝트에 실행해 헌터(Hunters)와 검증자(Verifiers)가 작동하는 과정을 보여준다.
- 발견된 버그를 증명하고 수정하는 방법과 함께 자신의 앱만을 대상으로 주기적으로 점검해야 한다는 점을 설명한다.

## NVIDIA Developer

### CUDA 13.5의 새로운 기능
https://www.youtube.com/watch?v=A94A2hccFoM

- CUDA 13.5는 NVIDIA Vera Rubin 지원을 정식 출시(GA)로 제공하고 NVIDIA DGX Station for Windows까지 Windows on Arm 지원을 확장한다.
- 멀티 다이 GPU에 작업과 데이터를 배치하는 방법과 로컬리티 도메인 내 균등 SM 파티션 및 전체 가용 SM 선택 기준을 다룬다.
- Multi-Process Service(MPS) v3로 GPU를 공유하고 유휴 SM을 바쁜 워크로드에 할당하는 방식을 코드 워크스루로 설명한다.
- 퍼블릭 프리뷰 단계인 CUDA Tile 커널에서의 SIMT 라이브러리 함수 호출과 NVLink 연결 GPU 간 연산·통신 결합 방법을 소개한다.
- 업그레이드 전 확인 사항과 함께 드라이버 호환성, CCCL 3.5의 CUB 튜닝, CUDA Python의 배치 복사 등 CUDA 13.5 시작 방법을 안내한다.
