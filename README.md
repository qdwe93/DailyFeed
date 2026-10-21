# DailyFeed

기술 뉴스, 기술 블로그, 기술 YouTube 영상과 GitHub Trending을 Markdown으로 보관하는 저장소입니다.
수집·요약·업로드는 로컬 PC에서 `run.py auto` 하나로 자동 실행되며, 요약은 opencode의 **무료 LLM**이 맡습니다.

- 기준 시간대: **Asia/Seoul (KST)**
- **매일 12:00 KST** (Windows 작업 스케줄러): GeekNews / Tech Feeds / YouTube Tech
  - 수집 범위: **직전 실행 이후** 새로 올라온 글 전부. PC가 꺼져 실행을 건너뛰어도 다음 실행이 빈 구간을 모두 가져옵니다.
  - 파일 날짜: **실행일**
- **GitHub Trending Weekly**: 월요일 실행 때, 또는 마지막 스냅샷 후 7일이 지났으면 그다음 실행 때 보충
- 외국어 제목과 요약은 한국어로 번역하고 원문 URL은 그대로 유지합니다.
- 실행 결과(성공·실패)는 Discord/Slack 웹훅으로 알립니다.

## 저장 구조

```text
DailyFeed/
├─ README.md / AGENT.md
├─ run.py                 # 오케스트레이터 (auto = 정기 실행 전체)
├─ pipeline/              # 수집·대체 수집·요약·렌더·발행
├─ models/
│  ├─ available.md        # 매 실행 전 점검한 무료 모델 목록과 점수 (자동 갱신)
│  └─ priority.txt        # 사용할 모델 우선순위 (사용자가 편집)
├─ state/run_state.json   # 채널별 마지막 실행 시각, 마지막 사용 모델
├─ log/YYYY-MM-DD.md      # 실행 로그: 수집 실패 원인과 대체 시도 기록
├─ geeknews/ tech/ youtube/ github/
│  └─ YYYY년M월/YYYY-MM-DD_주요기사.md
```

파일명은 `날짜_주요기사20자.md`이며, 주요기사는 파일의 첫 항목 제목을 20자로 줄인 값입니다.

> `github/2026년10월/2026-10-17_claude-plugins-offic.md`는 초기 설정 과정에서 생성한 Daily Trending 테스트 스냅샷입니다.
> 2026-10-20까지의 파일은 "대상일 = 전날" 방식, 2026-10-21부터는 "직전 실행 이후" 방식입니다.

## 무료 모델 관리

1. 매 실행 전 `opencode models`에서 opencode 무료 모델(`-free`, 가격 0)을 찾아 같은 요약 과제로 시험합니다.
2. 결과를 [`models/available.md`](./models/available.md)에 올립니다(응답 여부, 점수, 응답 시간, 새로 생기거나 사라진 모델).
3. [`models/priority.txt`](./models/priority.txt)에 한 줄에 하나씩 모델을 적으면 위에서부터 사용합니다. GitHub 웹에서 고쳐도 다음 실행이 먼저 `git pull`해서 반영합니다.
4. 우선순위가 비어 있거나 모두 실패하면 **마지막으로 성공한 모델 → 점수순**으로 넘어갑니다.
5. opencode 무료 모델이 하나도 응답하지 않을 때만 OpenRouter `:free` 모델을 씁니다. 그것도 없으면 GeekNews만 올리고 Tech/YouTube는 다음 실행으로 보류합니다.

## 수집 실패 대응

소스 요청이 실패하면 원인을 먼저 분류하고(DNS, Cloudflare 차단, 403/404/429/5xx, 파싱 오류, 빈 피드 등) 아래 순서로 다시 시도합니다.

1. 피드 주소 자동 탐색 (404·파싱 오류일 때, 찾으면 `pipeline/overrides.json`에 자동 반영)
2. crawl4ai (헤드리스 브라우저)
3. Apify `web-fetch` (실행당 최대 20회, 회당 약 $0.0016)
4. Playwright
5. opencode 에이전트 웹 검색 (게시 시각이 확인된 원문 URL만 채택)

본문 추출이 비는 글은 2~4번으로 본문을 다시 가져옵니다. GeekNews RSS(최신 50건)가 직전 실행 시점까지 닿지 않으면 `news.hada.io/past` 날짜 페이지로 빈 구간을 채웁니다. 모든 시도와 결과는 `log/`에 남깁니다.

## 로컬 실행

```bash
uv venv .venv && uv pip install -r requirements.txt   # 최초 1회
.venv/Scripts/python.exe run.py auto                 # 정기 실행과 동일 (수동 실행도 이것)
.venv/Scripts/python.exe run.py models               # 무료 모델 점검만
.venv/Scripts/python.exe run.py doctor               # 저장소·소스 점검
.venv/Scripts/python.exe run.py collect --date 2026-10-20   # 특정 하루만 수집 (구 방식)
```

- 알림 웹훅은 공개 저장소에 두지 않습니다. `%USERPROFILE%\.dailyfeed\config.json`에
  `{"discord_webhook": "..."}` 또는 `{"slack_webhook": "..."}`를 적습니다.
- Apify는 환경 변수 `APIFY_TOKEN`을 씁니다.
- 상세 규칙은 [`AGENT.md`](./AGENT.md)를 참조합니다.

## 정기 생성 파일

### 1. GeekNews — 매일

경로: `geeknews/YYYY년M월/YYYY-MM-DD_주요기사.md`

- 직전 실행 이후 새로 등록된 글 중 **AI·IT·개발·소프트웨어·인프라·보안·데이터·오픈소스 등 기술 관련 항목만** 수록합니다.
- 형식은 **한국어 제목 + 링크**만 사용합니다.

### 2. Tech Feeds — 매일

경로: `tech/YYYY년M월/YYYY-MM-DD_주요기사.md`

- GeekNews를 제외한 아래 기술 피드 및 공식 채널을 확인합니다.
- 각 글은 **한국어 제목 + 원문 URL + 핵심 내용 5줄**로 정리합니다.
- 새 글이 없는 피드는 표시하지 않습니다.

### 3. YouTube Tech — 매일

경로: `youtube/YYYY년M월/YYYY-MM-DD_주요기사.md`

- 아래 지정 채널에서 직전 실행 이후 공개된 **기술 영상**을 확인합니다.
- 형식은 **한국어 제목 + YouTube URL + 핵심 내용 5줄**입니다.
- Shorts, 회사 홍보, 채용 홍보, 행사 티저, 일반 마케팅 등 **기술적 내용이 부족한 영상은 제외**합니다.
- 공식 설명과 공개 메타데이터로 요약하고, 설명이 부족하면 추측하지 않고 제외합니다.

### 4. GitHub Trending Weekly — 매주 월요일

경로: `github/YYYY년M월/YYYY-MM-DD_주요기사.md`

- GitHub 공식 Trending의 **Weekly / All Languages 상위 10개**를 확인합니다. 파일명의 날짜는 실행일입니다.
- 저장소명, GitHub URL, 주 언어, 주간 증가 Star 수, README 기반 한국어 설명 2줄을 기록합니다.
- 월요일 실행을 놓쳐 마지막 스냅샷 후 7일이 지났으면 다음 실행 때 바로 수집합니다.

## 날짜 및 중복 처리 규칙

1. 게시 시각이 직전 실행 시각 이후이고 이번 실행 시각 이전인 콘텐츠만 수록합니다.
2. 같은 canonical URL이 과거 파일에 있으면 다시 기록하지 않습니다.
3. 기존 콘텐츠의 단순 수정·재노출은 신규로 취급하지 않습니다.
4. 날짜나 신규 여부를 확인할 수 없으면 추정해서 수록하지 않습니다.
5. 같은 날 다시 실행하면 그날 파일에 새 항목을 합칩니다(이미 올린 항목은 유지).

# Tech Feed 구독 소스

총 **33개 소스**입니다. RSS/Atom 32개와 공식 웹페이지 1개(Anthropic Newsroom)로 구성됩니다.

| # | Feed / Source | RSS / URL | 분류 | 유형 |
|---:|---|---|---|---|
| 1 | 44BITS | https://www.44bits.io/ko/feed/all | 개발 뉴스 | RSS |
| 2 | Banksalad Tech | https://blog.banksalad.com/rss.xml | 기타 Tech | RSS |
| 3 | Coupang Engineering | https://medium.com/feed/coupang-engineering | AI · Agent · Platform | RSS |
| 4 | DeNA Engineering | https://engineering.dena.com/blog/index.xml | Japan Tech Blogs | RSS |
| 5 | Devsisters Tech | https://tech.devsisters.com/rss.xml | AI · Agent · Platform | RSS |
| 6 | GeekNews | https://news.hada.io/rss/news | 개발 뉴스 | RSS |
| 7 | Hyperconnect Tech | https://hyperconnect.github.io/feed.xml | AI · Agent · Platform | RSS |
| 8 | Kakao Enterprise Tech | https://tech.kakaoenterprise.com/feed | 기타 Tech | RSS |
| 9 | kakao tech | https://tech.kakao.com/feed/ | 핵심 Tech | RSS |
| 10 | LayerX Engineering Blog | https://tech.layerx.co.jp/rss | Japan Tech Blogs | RSS |
| 11 | LY Corporation Tech Blog (KO) | https://techblog.lycorp.co.jp/ko/feed/index.xml | 핵심 Tech | RSS |
| 12 | MUSINSA Tech | https://medium.com/feed/musinsa-tech | AI · Agent · Platform | RSS |
| 13 | NAVER D2 | https://d2.naver.com/d2.atom | 핵심 Tech | Atom |
| 14 | NHN Cloud Meetup | https://meetup.nhncloud.com/rss | 기타 Tech | RSS |
| 15 | PRND Tech | https://medium.com/feed/prnd | 기타 Tech | RSS |
| 16 | RIDI Tech | https://www.ridicorp.com/feed | 기타 Tech | RSS |
| 17 | SmartHR Tech Blog | https://tech.smarthr.jp/feed | Japan Tech Blogs | RSS |
| 18 | Tabelog Tech Blog | https://tech-blog.tabelog.com/feed | Japan Tech Blogs | RSS |
| 19 | Toss Tech | https://toss.tech/rss.xml | 핵심 Tech | RSS |
| 20 | WATCHA Tech | https://medium.com/feed/watcha | 기타 Tech | RSS |
| 21 | Yogiyo Tech | https://techblog.yogiyo.co.kr/feed | 기타 Tech | RSS |
| 22 | Zigbang Tech | https://medium.com/feed/zigbang | 기타 Tech | RSS |
| 23 | ZOZO TECH BLOG | https://techblog.zozo.com/feed | Japan Tech Blogs | RSS |
| 24 | 당근 Tech | https://medium.com/feed/daangn | 핵심 Tech | RSS |
| 25 | 우아한형제들 기술블로그 | https://techblog.woowahan.com/feed/ | 핵심 Tech | RSS |
| 26 | 컬리 기술 블로그 | https://helloworld.kurly.com/feed.xml | 핵심 Tech | RSS |
| 27 | 字节跳动技术团队 (ByteDance Tech) | https://wechat2rss.xlab.app/feed/4025ea55575daf8bfd8227e68b28d9638b073267.xml | China Tech Blogs | RSS |
| 28 | 小红书技术REDtech (Xiaohongshu REDtech) | https://wechat2rss.bestblogs.dev/feed/0f8c47df6fd304112518544776e0bbf1d98ba0b9.xml | China Tech Blogs | RSS |
| 29 | 美团技术团队 (Meituan Tech) | https://tech.meituan.com/rss.xml | China Tech Blogs | RSS |
| 30 | Google Official Blog | https://blog.google/rss/ | AI · Official | RSS |
| 31 | Google DeepMind | https://deepmind.google/blog/rss.xml | AI · Official | RSS |
| 32 | OpenAI | https://openai.com/news/rss.xml | AI · Official | RSS |
| 33 | Anthropic Newsroom | https://www.anthropic.com/news | AI · Official | 공식 웹페이지 |

# YouTube Tech 모니터링 소스

## AI · Cloud · Developer 공식 채널

| 채널 | URL | 비고 |
|---|---|---|
| OpenAI | https://www.youtube.com/@OpenAI | OpenAI 공식 |
| Claude | https://www.youtube.com/channel/UCV03SRZXJEz-hchIAogeJOg | Anthropic / Claude |
| Google for Developers | https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw | Google 개발자 공식 |
| Google DeepMind | https://www.youtube.com/@googledeepmind | AI 연구·모델 |
| Google Cloud Tech | https://www.youtube.com/channel/UCJS9pqu9BzkAMNTmzNMNhvg | Cloud·Agent·플랫폼 |
| NVIDIA Developer | https://www.youtube.com/channel/UCBHcMCGaiJhv-ESTcWGJPcw | AI·CUDA·로보틱스·그래픽스 |
| Meta Developers | https://www.youtube.com/@MetaDevelopers | Meta 개발자 공식 |
| AWS Developers | https://www.youtube.com/channel/UCT-nPlVzJI-ccQXlxjSvJmw | AWS 개발자 공식 |
| Microsoft Developer | https://www.youtube.com/@MicrosoftDeveloper | Microsoft 개발자 공식 |
| SAP | https://www.youtube.com/channel/UCVnIv2xF2wyMMCSKv1qF3pA | SAP 공식 |
| SAP TechEd | https://www.youtube.com/channel/UCUJdXZAAOsNuPBpLa50XUxQ | SAP 기술 세션 |
| NAVER D2 | https://www.youtube.com/channel/UCNrehnUq7Il-J7HQxrzp7CA | NAVER 기술 공식 |
| LINE Developers Korea | https://www.youtube.com/channel/UC3Vp8t2iPX1cz4eWw-XezGA | LINE/LY 개발자 기술 콘텐츠 |
| kakao tech | https://www.youtube.com/channel/UCdQF7F6hwjSpulj_fwB9iDQ | 카카오 기술 공식 |
| 당근 팀 | https://www.youtube.com/channel/UCwNwSGlLJNZTatOnE2t33tg | 기술 관련 영상만 |
| 토스 | https://www.youtube.com/channel/UCeg5g-vWgtgzQ0cYNV2Cyow | 기술 관련 영상만 |

## 게임 제작 · 3D

| 채널 | URL | 비고 |
|---|---|---|
| Unreal Engine | https://www.youtube.com/channel/UCBobmJyzsJ6Ll7UbfhI4iwQ | Unreal 공식 |
| Unity Korea | https://www.youtube.com/channel/UCQArZVLg7Omzg4cBReJTS3w | Unity 한국 공식 |
| Blender Guru | https://www.youtube.com/channel/UCOKHwx1VCdgnxwbjyb9Iu1g | Blender 제작 실전 |
| GDC Festival of Gaming | https://www.youtube.com/channel/UC0JB7TSe49lg56u6qH8y_MQ | 게임 개발 세션 |
| Game Maker's Toolkit | https://www.youtube.com/channel/UCqJ-Xo29CKyLTjn6z2XwYAw | 게임 디자인·제작 |
| Masahiro Sakurai on Creating Games | https://www.youtube.com/channel/UCv1DvRY5PyHHt3KN9ghunuw | 게임 제작 원리 |
| Maker's Muse | https://www.youtube.com/channel/UCxQbYGpbdrh-b2ND-AfIybg | 3D 제작·메이킹 |

## 개인 채널 예외

| 채널 | URL | 포함 이유 |
|---|---|---|
| Cole Medin | https://www.youtube.com/channel/UCMwVTLZIRRUyyVrkjDpn4pA | Agent·AI coding·하네스·로컬 AI 중심 |

### YouTube 제외 원칙

- `WorldofAI`, `AgentOS`, `조코딩`, `AI는 야근중`, `인공지능팩토리`는 DailyFeed 모니터링 대상에서 제외합니다.
- X는 안정적으로 추적할 공식 기술 YouTube 채널을 현재 목록에 넣지 않습니다.
- 일반 회사 채널(당근, 토스 등)은 기술/개발 관련 영상만 수록합니다.

## 작업 규칙

자동 수집·작성 시 세부 규칙은 [`AGENT.md`](./AGENT.md)를 따릅니다.
