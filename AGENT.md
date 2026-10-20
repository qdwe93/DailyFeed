# DailyFeed 작업 규칙

이 문서는 DailyFeed를 갱신하는 에이전트가 따라야 하는 기준 문서입니다.

## 1. 실행 기준

- 기준 시간대: `Asia/Seoul`
- 일일 실행: 매일 `08:00`
  - `geeknews/<YYYY년M월>/<YYYY-MM-DD>_<주요기사>.md`
  - `tech/<YYYY년M월>/<YYYY-MM-DD>_<주요기사>.md`
  - `youtube/<YYYY년M월>/<YYYY-MM-DD>_<주요기사>.md`
- 주간 실행: 매주 월요일 `08:00`
  - `github/<YYYY년M월>/<YYYY-MM-DD>_<주요기사>.md`
- 일일 대상 날짜: 실행일의 전날(KST)
- GitHub Weekly 파일명의 날짜는 실행일(월요일)이다.
- 파일명의 `<주요기사>`는 그 파일의 첫 번째 항목 제목을 20자로 줄인 값이다.
  - 공백은 `-`로 바꾸고, 파일명에 쓸 수 없는 문자(`\ / : * ? " < > |`)는 제거한다.
  - 20자를 넘으면 자르고 끝의 `-`·`.`를 지운다. 항목이 없으면 `신규없음`을 쓴다.
- 같은 날짜 파일이 이미 있으면 새 파일을 만들지 않고, 이름이 달라졌을 때만 교체한다.

## 2. 공통 원칙

- 소스 목록은 `README.md`를 기준으로 한다.
- 공식 소스와 원문을 우선한다.
- 확인할 수 없는 정보를 추정하거나 만들어내지 않는다.
- 외국어 제목과 요약은 자연스러운 한국어로 번역한다.
- 원문 URL은 변경하지 않는다.
- 수량을 맞추기 위해 억지로 항목을 채우지 않는다.

## 3. 날짜 판정

1. 게시일 또는 업로드일이 명시된 콘텐츠는 해당 날짜를 사용한다.
2. 일일 파일에는 대상 날짜와 날짜가 일치하는 신규 콘텐츠만 수록한다.
3. 날짜가 없는 항목은 canonical/original URL 기준으로 과거 파일을 검색한다.
4. 과거 파일에 동일 URL이 있으면 다시 기록하지 않는다.
5. 날짜가 불명확하고 신규 여부도 확인할 수 없으면 수록하지 않는다.
6. 기존 글/영상의 단순 수정·재노출은 새 콘텐츠로 취급하지 않는다.
7. GitHub Trending은 위 날짜 판정 규칙 대신 매주 월요일 00:30 KST 시점의 Weekly Trending 스냅샷을 저장한다.

## 4. GeekNews 규칙

대상: 대상 날짜에 GeekNews에 새로 등록된 항목.

포함:
- AI / LLM / Agent
- 프로그래밍 / 개발 도구
- 운영체제 / 데이터베이스
- 클라우드 / 인프라 / 플랫폼
- 보안 / 프라이버시
- 데이터 / 분산시스템
- 오픈소스
- 하드웨어·반도체 등 IT 기술
- 개발자가 볼 가치가 분명한 기술 기사

제외:
- 기술 내용이 거의 없는 일반 비즈니스·마케팅
- 단순 행사 홍보
- 일반 사회·정치·연예·스포츠
- 기술적 내용이 없는 제품 광고
- 중복 항목

형식:
```markdown
# GeekNews — YYYY-MM-DD

- [한국어 제목](원문 또는 대표 URL)
- [한국어 제목](원문 또는 대표 URL)
```

- 요약을 붙이지 않는다.
- 원문 URL을 확인할 수 있으면 원문을 우선한다.

## 5. Tech Feeds 규칙

대상: GeekNews를 제외한 `README.md`의 Tech Feed 소스.

각 글 형식:
```markdown
## 소스명

### 한국어 제목
원문: https://...

- 핵심 내용 첫째 줄
- 핵심 내용 둘째 줄
- 핵심 내용 셋째 줄
```

- 보통 3줄로 요약한다.
- 마케팅 문구를 그대로 옮기지 말고 기술적 핵심을 사실 위주로 요약한다.
- 해당 날짜에 신규 글이 없는 소스는 생략한다.
- 전체 Tech 소스에서 신규 글이 없으면 `해당 날짜에 확인된 신규 글 없음.`이라고 기록한다.

## 6. GitHub Trending Weekly 규칙

### 실행 및 기준

- 실행: **매주 월요일 00:30 KST**
- 1차 소스: `https://github.com/trending?since=weekly`
- 조건: **Weekly / All Languages**
- 수량: 상위 **10개 repository**
- 결과 경로: `github/YYYYMMDD_github_weekly.md`
- 파일명의 날짜는 실행일(월요일)이다.
- 관측 시점의 GitHub Weekly Trending을 그대로 스냅샷으로 저장한다.
- GitHub Trending은 과거 특정 주차를 공식적으로 직접 조회할 수 있는 데이터가 아니므로 소급 생성은 원칙적으로 하지 않는다.
- 공식 페이지가 일시적으로 확인되지 않을 때만 신뢰 가능한 아카이브/트래커를 보조적으로 사용하고, 사용한 경우 파일에 표시한다.

### 각 항목

```markdown
## 1. owner/repository

https://github.com/owner/repository

- 언어: Python
- 이번 주 증가: +1,234 stars
- 무엇을 하는 프로젝트인지 한국어로 설명
- 핵심 특징 또는 사용 가치
```

- 순서는 관측된 Trending 순서를 유지한다.
- 주간 증가 Star 수와 언어는 확인 가능한 경우만 적는다.
- 저장소 README/Description을 확인해 단순 영문 description 번역보다 실제 용도를 우선 파악한다.
- `왜 유행하는지`가 자료로 확인되지 않으면 임의의 원인을 만들지 않는다.
- 기존의 `github/20261017_github.md`는 초기 Daily 테스트 파일이므로 향후 정기 실행 대상에서 제외한다.

## 7. YouTube Tech 규칙

### 대상

- `README.md`의 **YouTube Tech 모니터링 소스**만 확인한다.
- 개인 채널은 현재 **Cole Medin만 예외적으로 포함**한다.
- `WorldofAI`, `AgentOS`, `조코딩`, `AI는 야근중`, `인공지능팩토리`는 제외한다.

### 날짜

- 대상 날짜 `00:00:00~23:59:59 KST`에 공개된 영상을 대상으로 한다.
- YouTube가 UTC 등 다른 시간대로 표시되면 KST로 환산해 판정한다.
- 가능하면 채널 ID/공식 채널 페이지/YouTube 메타데이터를 우선 사용한다.
- 검색 결과의 상대 날짜(`1 day ago`)만으로 날짜를 확정하지 않는다.

### 포함 주제

- AI / LLM / Agent / Agent Harness
- 코딩 에이전트 / 개발도구 / IDE
- 클라우드 / 인프라 / 플랫폼 / DevOps
- 데이터 / 보안 / 소프트웨어 아키텍처
- SAP / ABAP / SAP BTP / SAP 개발
- 게임 개발 / 게임 디자인 / 엔진
- Unity / Unreal / Blender / 3D / 그래픽스
- 개발자가 실제 업무나 제작에 활용할 기술 세션

### 제외

- Shorts 형식의 가벼운 홍보성 영상
- 회사 소개 / 기업 PR / 채용 홍보
- 행사 개최 알림이나 티저만 있는 영상
- 개발 내용이 없는 제품 광고
- 일반 금융·생활·예능 콘텐츠
- 기술과 관계없는 회사 공식 영상
- 동일 영상 재업로드 또는 이미 과거 파일에 기록된 URL

### 작성 형식

```markdown
# YouTube Tech — YYYY-MM-DD

## 채널명

### 한국어 제목
https://www.youtube.com/watch?v=...

- 핵심 내용 첫째 줄
- 핵심 내용 둘째 줄
- 핵심 내용 셋째 줄
```

- 원래 제목이 외국어면 자연스러운 한국어로 번역한다.
- 한국어 원제는 과도하게 바꾸지 않는다.
- 자막/스크립트를 확인할 수 있으면 이를 가장 우선한다.
- 자막이 없으면 영상 설명, 챕터, 공식 설명 등 공개 메타데이터로 요약한다.
- 실제 영상을 분석하지 못했고 설명도 부족하면 내용을 추측하지 말고 그 영상은 제외하는 편을 우선한다.
- 대상 날짜에 해당하는 기술 영상이 하나도 없으면 `해당 날짜에 확인된 신규 기술 영상 없음.`이라고 기록한다.

## 8. 중복 방지

- URL 비교 시 추적용 query string(예: `utm_*`)은 제거해 canonical URL 기준으로 비교한다.
- 동일 canonical URL이 과거 일자 파일에 존재하면 다시 기록하지 않는다.
- 제목이 달라도 URL이 동일하면 중복으로 본다.
- YouTube는 `youtu.be`, `youtube.com/watch`, 공유 파라미터를 정규화해 video ID 기준으로 중복을 판정한다.

## 9. 저장 및 커밋

- 채널 폴더는 `geeknews/`, `tech/`, `youtube/`, `github/` 이고, 그 아래 `YYYY년M월` 월 폴더를 둔다.
- 파일명은 `YYYY-MM-DD_주요기사20자.md` 형식이다(1장 참조).
- 이미 같은 날짜 파일이 있으면 새 파일을 만들지 말고 필요한 경우 갱신한다.
- 권장 커밋 메시지:
  - `daily: add YYYY-MM-DD GeekNews`
  - `daily: add YYYY-MM-DD tech feeds`
  - `daily: add YYYYMMDD YouTube tech`
  - `weekly: add YYYYMMDD GitHub trending`
- 자동 실행 후 채팅에는 내용을 다시 길게 출력하지 말고 성공/실패와 생성된 GitHub 경로만 간단히 알린다.

## 10. 로컬 실행 파이프라인

수집은 결정론적 스크립트가 맡고, 요약만 에이전트가 맡는다.

```bash
uv venv .venv && uv pip install -r requirements.txt        # 최초 1회
python run.py doctor                                      # 저장소·소스 상태 점검
python run.py collect --date YYYY-MM-DD                   # RSS·YouTube·본문 수집
python run.py render  --date YYYY-MM-DD --publish         # 마크다운 생성 후 커밋·푸시
python run.py weekly  && python run.py render-weekly --publish
```

- `collect` 결과는 `work/<날짜>/candidates.json`, `stats.json`, `prompt.md`에 남는다(`work/`는 커밋하지 않는다).
- 에이전트는 `prompt.md`를 읽고 `work/<날짜>/summaries.json`을 작성한다.
  - 형식: `{"date": "...", "items": {"tech-1": {"title_ko": "...", "bullets": ["...","...","..."]}}}`
  - 요약할 수 없는 항목은 `{"skip": true, "reason": "..."}`로 표시한다.
- `render`는 candidates와 summaries를 id로 병합해 파일을 쓰고, 같은 날짜의 이름이 다른 기존 파일은 지운다.
- 소스 목록의 기준은 계속 `README.md`다. 피드 URL이 깨졌을 때만 `pipeline/overrides.json`에 대체 URL을 적는다.
- 실행 결과는 `log/YYYY-MM-DD.md`에 남긴다. 실패한 소스와 원인을 숨기지 않는다.

## 11. 품질 원칙

- 실제 새 콘텐츠가 적은 날은 적게 기록해도 된다.
- 날짜·제목·URL·내용이 충돌하면 원문/공식 채널을 우선한다.
- 원문 확인이 불가능하면 그 사실을 숨기지 않는다.
- 정보량보다 **정확성, 기술 관련성, 중복 방지**를 우선한다.
