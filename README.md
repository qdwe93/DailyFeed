# DailyFeed

기술 뉴스, 기술 블로그, 기술 YouTube 영상과 GitHub Trending을 Markdown으로 보관하는 저장소입니다.

- 기준 시간대: **Asia/Seoul (KST)**
- **매일 00:30 KST**: GeekNews / Tech Feeds / YouTube Tech
- **매주 월요일 00:30 KST**: GitHub Trending Weekly
- 일일 수집 대상 날짜: 실행 시점의 **전날**
- 외국어 제목과 요약은 한국어로 번역하고 원문 URL은 그대로 유지합니다.

## 저장 구조

```text
DailyFeed/
├─ README.md
├─ AGENT.md
├─ geeknews/
│  └─ YYYY/MM/YYYY-MM-DD.md
├─ tech/
│  └─ YYYY/MM/YYYY-MM-DD.md
├─ github/
│  └─ YYYYMMDD_github_weekly.md
└─ youtube/
   └─ YYYYMMDD_youtube_tech.md
```

예시:

```text
geeknews/2026/10/2026-10-18.md
tech/2026/10/2026-10-18.md
youtube/20261018_youtube_tech.md
github/20261019_github_weekly.md
```

> `github/20261017_github.md`는 초기 설정 과정에서 생성한 Daily Trending 테스트 스냅샷이며, 이후 정기 파일은 Weekly 형식만 사용합니다.

## 정기 생성 파일

### 1. GeekNews — 매일

경로: `geeknews/YYYY/MM/YYYY-MM-DD.md`

- 대상 날짜에 새로 등록된 글 중 **AI·IT·개발·소프트웨어·인프라·보안·데이터·오픈소스 등 기술 관련 항목만** 수록합니다.
- 형식은 **한국어 제목 + 링크**만 사용합니다.
- 별도 요약은 작성하지 않습니다.

### 2. Tech Feeds — 매일

경로: `tech/YYYY/MM/YYYY-MM-DD.md`

- GeekNews를 제외한 아래 기술 피드 및 공식 채널을 확인합니다.
- 각 글은 **한국어 제목 + 원문 URL + 핵심 내용 약 3줄**로 정리합니다.
- 외국어 글은 제목과 요약을 한국어로 번역합니다.
- 새 글이 없는 피드는 표시하지 않습니다.

### 3. YouTube Tech — 매일

경로: `youtube/YYYYMMDD_youtube_tech.md`

- 아래 지정 채널에서 대상 날짜 **00:00~23:59 KST에 새로 공개된 기술 영상**을 확인합니다.
- 형식은 **한국어 제목 + YouTube URL + 핵심 내용 약 3줄**입니다.
- 외국어 영상은 제목과 요약을 한국어로 번역합니다.
- Shorts, 회사 홍보, 채용 홍보, 행사 티저, 일반 마케팅 등 **기술적 내용이 부족한 영상은 제외**합니다.
- 자막을 확인할 수 있으면 자막을 우선하고, 없으면 공식 설명과 공개 메타데이터로 요약합니다.

### 4. GitHub Trending Weekly — 매주 월요일

경로: `github/YYYYMMDD_github_weekly.md`

- **매주 월요일 00:30 KST**에 GitHub 공식 Trending의 **Weekly / All Languages 상위 10개**를 확인합니다.
- 파일명의 날짜는 **실행일(월요일)** 입니다.
- 저장소명, GitHub URL, 주 언어, 주간 증가 Star 수(확인 가능한 경우), 한국어 설명을 기록합니다.
- GitHub 공식 페이지를 우선하고 공식 페이지 확인이 어려울 때만 신뢰 가능한 아카이브/트래커를 보조적으로 사용합니다.
- 순위와 Star 수는 해당 시점의 GitHub Weekly Trending 스냅샷이며 별도의 주간 통계 재계산값이 아닙니다.

## 날짜 및 중복 처리 규칙

1. 게시 날짜/업로드 날짜가 명시된 콘텐츠는 해당 날짜를 우선합니다.
2. 날짜가 없는 소스는 canonical/original URL 기준으로 과거 파일과 중복 여부를 확인합니다.
3. 동일 URL은 다시 기록하지 않습니다.
4. 기존 콘텐츠의 단순 수정·재노출은 신규로 취급하지 않습니다.
5. 날짜나 신규 여부를 확인할 수 없으면 추정해서 수록하지 않습니다.
6. GitHub Trending은 일일 날짜 판정 규칙을 적용하지 않고 **매주 월요일 00:30의 Weekly Trending 스냅샷**을 저장합니다.

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
