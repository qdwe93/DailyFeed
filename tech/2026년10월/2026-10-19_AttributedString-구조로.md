# Tech Feeds — 2026-10-19

## LY Corporation Tech Blog

### AttributedString 구조로 풀어낸 대규모 iOS 설정 시스템
원문: https://techblog.lycorp.co.jp/ko/a-large-scale-ios-configuration-system-implemented-with-an-attributedstring-structure

- LINE iOS 앱의 약 60개 모듈이 사용하는 약 700개 동적 설정 키를 한 파일에서 관리하면서 순환 의존, 중복 디코딩, 스레드 안전성 문제가 발생했다.
- Swift Foundation의 `AttributedString` 설계를 참고해 키·스코프·동적 멤버 조회를 조합하고, 각 모듈이 설정 키와 타입을 직접 선언하도록 재설계했다.
- `Sendable`과 잠금으로 동시 접근을 관리하고 기본값·인코딩·디코딩 책임을 개별 키로 옮겨 유지보수성과 타입 안전성을 높였다.

### AI 기반 개발 속도를 뒷받침하는 자동화·에이전트 하네스 구축
원문: https://techblog.lycorp.co.jp/ja/20261019b

- LINE 기프트 SRE 팀에서 GitHub Actions로 릴리스 브랜치의 백머지를 자동화하고, E2E 변이 테스트·Lefthook·OpenAPI 정비로 AI 생성 코드의 검증을 강화했다.
- 특정 코딩 도구에 종속되지 않는 에이전트 실행 구조를 검토한 뒤 `flue`를 선택하고, 컨테이너 격리·권한 분리·단계 수와 타임아웃 제한을 적용했다.
- 모니터링 경고나 테스트 실패를 계기로 AI가 로그·메트릭·코드를 조사하고 Slack 스레드에 원인 후보와 다음 조치를 제시하는 이벤트 기반 1차 조사 흐름을 구현했다.

## LayerX Engineering Blog

### 자체 Slack Bot·Notion 헬프데스크를 전문 서비스로 전환한 운영 사례
원문: https://tech.layerx.co.jp/entry/helpdesk-migration

- 기존에는 Slack 문의를 자체 Bot이 Notion DB 티켓으로 만들고, 담당자·기한·상태를 별도 관리해 Slack과 Notion을 오가야 했다.
- 전문 헬프데스크 도입 후 Slack 대화 확인, 요청 폼, 담당자 자동 배정 기능을 통합했지만 처리 시간 감소는 아직 정량적으로 검증하지 못했다.
- AI가 답변하는 것만으로 끝나지 않는 권한 변경 등은 승인 절차를 거친 반자동 실행이 필요하며, 기존 Notion 지식과 신규 지식의 동기화도 과제로 남았다.

> 수집 참고: 일부 등록 RSS는 직접 조회할 수 없어 공식 웹페이지와 검색 가능한 원문에서 2026-10-19 게시일을 확인한 항목만 수록했습니다. 이는 전체 소스에 신규 글이 없었다는 뜻이 아닙니다.
