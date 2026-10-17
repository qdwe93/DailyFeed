# DailyFeed

매일 구독 중인 기술 피드와 GeekNews를 확인해 날짜별 Markdown 파일로 보관하는 저장소입니다.

- 기준 시간대: **Asia/Seoul (KST)**
- 실행 시각: **매일 00:30 KST**
- 수집 대상 날짜: 실행 시점의 **전날 00:00~23:59 KST**
- GeekNews와 나머지 기술 피드를 **서로 다른 파일**로 저장합니다.
- 외국어 글은 제목과 요약을 **한국어로 번역**하고, URL은 원문을 유지합니다.

## 저장 구조

```text
DailyFeed/
├─ README.md
├─ AGENT.md
├─ geeknews/
│  └─ YYYY/
│     └─ MM/
│        └─ YYYY-MM-DD.md
└─ tech/
   └─ YYYY/
      └─ MM/
         └─ YYYY-MM-DD.md
```

예시:

```text
geeknews/2026/10/2026-10-17.md
tech/2026/10/2026-10-17.md
```

GitHub는 빈 폴더를 저장하지 않으므로 날짜별 Markdown 파일이 생성될 때 해당 폴더도 함께 만들어집니다.

## 매일 생성되는 파일

### 1. GeekNews

경로: `geeknews/YYYY/MM/YYYY-MM-DD.md`

- GeekNews에 대상 날짜에 새로 등록된 글 중 **AI·IT·개발·소프트웨어·인프라·보안·데이터·오픈소스 등 기술 관련 항목만** 수록합니다.
- 단순 홍보, 일반 비즈니스/마케팅, 기술과 직접 관련 없는 글은 제외합니다.
- 형식은 **한국어 제목 + 링크**만 사용합니다.
- 별도 요약은 작성하지 않습니다.

### 2. Tech Feeds

경로: `tech/YYYY/MM/YYYY-MM-DD.md`

- GeekNews를 제외한 아래 기술 피드 및 공식 채널을 확인합니다.
- 각 글은 **한국어 제목 + 원문 URL + 핵심 내용 약 3줄**로 정리합니다.
- 영어·일본어·중국어 등 한국어가 아닌 글은 제목과 요약을 한국어로 번역합니다.
- 새 글이 없는 피드는 표시하지 않습니다.
- 해당 날짜에 확인된 신규 글이 하나도 없으면 그 사실만 기록합니다.

## 날짜 및 중복 처리 규칙

1. 글에 명시된 게시 날짜가 있으면 그 날짜를 우선합니다.
2. 게시 날짜가 대상 날짜라면 수록합니다.
3. 날짜가 없는 소스는 **canonical/original URL**을 기준으로 이전 날짜 파일들과 중복 여부를 확인합니다.
4. 날짜 없는 글은 과거 파일에 같은 URL이 없고 대상 날짜에 새로 발견된 것으로 확인되는 경우에만 수록합니다.
5. 같은 사건을 여러 곳에서 다루더라도 각 구독 피드에 실제로 새 글이 게시된 경우에는 해당 피드의 글로 수록할 수 있습니다.
6. 확인되지 않은 날짜나 내용을 추정해서 작성하지 않습니다.

## 구독 소스

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
| 30 | Google Official Blog (News from Google) | https://blog.google/rss/ | AI · Official | RSS |
| 31 | Google DeepMind | https://deepmind.google/blog/rss.xml | AI · Official | RSS |
| 32 | OpenAI | https://openai.com/news/rss.xml | AI · Official | RSS |
| 33 | Anthropic Newsroom | https://www.anthropic.com/news | AI · Official | 공식 웹페이지 |

### 공식 채널 참고

- **Google Official Blog**: Google 전체 공식 뉴스입니다.
- **Google DeepMind**: Gemini·DeepMind 연구 및 모델 발표를 중심으로 확인합니다.
- **OpenAI**: OpenAI 공식 News RSS입니다.
- **Anthropic**: 공식 Newsroom을 확인합니다. 공개 공식 RSS가 확인되지 않아 웹페이지를 직접 확인합니다.

## 작업 규칙

자동 수집·작성 시 세부 규칙은 [`AGENT.md`](./AGENT.md)를 따릅니다.
