# Tech Feeds — 2026-10-26

## DeNA Engineering

### EDGE POKER에서 익스플로잇 전략 AI 구현에 도전하다
원문: https://engineering.dena.com/blog/2026/10/intern-edge-poker-exploit/

- 2026년 DeNA AI 스페셜리스트 서머 인턴십 참가자가 4주간 EDGE POKER 활용을 위한 익스플로잇 전략 포커 AI 개발에 도전했다.
- EDGE POKER는 DeNA와 POKER ROOM이 개발한 스마트폰 포커 게임 앱이며 EDGE AI 등의 기능을 제공한다.
- 포커 전략은 GTO 전략과 익스플로잇 전략으로 나뉘며, GTO는 안정적이지만 상대의 약점을 이용한 추가 이익을 놓칠 수 있다.
- EDGE AI는 GTO에 가까운 전략 기반이어서 AI 리뷰 기능도 GTO 기반 평가를 제시한다.
- 대부분의 대전·분석용 포커 AI는 GTO 전략 기반이며, 익스플로잇 전략 AI를 응용한 제품은 세계적으로 거의 없다고 한다.

## LY Corporation Tech Blog (KO)

### Flava MCP Hub가 걸어온 길: AI 시대를 위한 배관 공사
원문: https://techblog.lycorp.co.jp/ko/flava-mcp-hub-ai-infrastructure

- LLM은 학습 시점 이후 정보와 사내 데이터에 직접 접근할 수 없으며, MCP는 필요한 순간 외부 도구와 데이터에서 컨텍스트를 가져오는 규격이다.
- 사내 MCP 서버 운영에서는 통제 없는 확산, 팀별 상이한 인증, 사내 인증 체계와 MCP 표준 간 간극, 사용 현황 파악 어려움 네 가지 문제가 발생했다.
- Flava MCP Hub는 사내 공통 프라이빗 클라우드 Flava 위의 전사 공통 MCP 플랫폼으로 카탈로그, 런타임, Gateway 역할을 제공한다.
- 사내 카탈로그에서 MCP 서버를 1분 안에 연결할 수 있고, 인증을 갖춘 새 MCP 서버도 5분 안에 배포할 수 있다.
- 플랫폼 위에서 동작하는 MCP 서버는 650개 이상, 사용 팀은 200팀 이상, 누적 도구 호출 수는 1,150만 건을 넘었다.
