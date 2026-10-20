"""Relevance filtering for GeekNews items (AGENT.md section 4)."""

from __future__ import annotations

INCLUDE_KEYWORDS = [
    # AI / LLM / Agent
    "ai", "llm", "agent", "에이전트", "모델", "gpt", "claude", "gemini", "llama",
    "딥러닝", "머신러닝", "인공지능", "프롬프트", "rag", "mcp", "임베딩", "추론",
    "transformer", "diffusion", "학습", "파인튜닝", "fine-tun", "token", "토큰",
    # dev / tooling
    "코드", "code", "프로그래밍", "개발", "라이브러리", "프레임워크", "sdk", "api",
    "ide", "컴파일", "디버그", "깃허브", "github", "오픈소스", "open source", "cli",
    "터미널", "vim", "rust", "python", "자바스크립트", "typescript", "golang", "go ",
    "node", "deno", "bun", "wasm", "webassembly",
    # os / db
    "리눅스", "linux", "커널", "윈도우", "macos", "postgres", "sqlite", "mysql",
    "데이터베이스", "db", "쿼리", "스토리지", "파일시스템", "container", "컨테이너",
    # cloud / infra
    "클라우드", "cloud", "aws", "gcp", "azure", "쿠버네티스", "kubernetes", "k8s", "도커",
    "docker", "서버", "배포", "ci/cd", "인프라", "devops", "terraform", "nginx",
    "네트워크", "dns", "cdn", "엣지", "serverless", "람다", "observability",
    # security / privacy
    "보안", "취약", "해킹", "암호", "encryption", "privacy", "프라이버시",
    "cve", "악성", "랜섬", "피싱", "인증", "oauth", "sandbox",
    # data / distributed
    "데이터", "분산", "kafka", "스트리밍", "etl", "벡터", "검색 엔진", "인덱스",
    # open source / hardware
    "오픈소", "깃허브", "하드웨어", "반도체", "gpu", "cpu", "nvidia", "엔비디아",
    "칩", "애플 실리콘", "로보틱스", "드론", "3d 프린팅", "임베디드",
    # general tech context
    "성능", "최적화", "아키텍처", "리팩토링", "테스트", "버그", "릴리스", "버전",
]

EXCLUDE_KEYWORDS = [
    # non-tech news / entertainment
    "연예", "아이돌", "드라마", "영화 흥행", "스포츠", "축구", "야구", "정치",
    "대통령", "국회", "부동산", "집값", "주가", "주식", "코인 폭락", "가상자산 거래소",
    "레시피", "여행", "맛집", "다이어트", "명상", "운세", "결혼", "출산",
    # marketing / hiring / events
    "채용", "구인", "모집", "웨비나", "얼리버드", "할인", "출시 기념", "프로모션",
    "광고", "협찬", "설문", "경품", "슈퍼 얼리버드",
]


def _hit(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)


def classify_geeknews(item: dict) -> tuple[bool, str]:
    """Return (include, reason). Trusts topic title + short summary only."""
    text = f"{item.get('title', '')} {item.get('summary', '')[:400]}"
    if len(text.strip()) < 4:
        return False, "empty"
    if _hit(text, EXCLUDE_KEYWORDS) and not _hit(text, INCLUDE_KEYWORDS):
        return False, "non-tech"
    if _hit(text, INCLUDE_KEYWORDS):
        return True, "tech"
    return False, "no-tech-keyword"


def filter_items(items: list[dict]) -> tuple[list[dict], list[dict]]:
    kept, dropped = [], []
    for item in items:
        ok, reason = classify_geeknews(item)
        if ok:
            kept.append(item)
        else:
            dropped.append({"title": item.get("title", ""), "url": item.get("url", ""), "reason": reason})
    return kept, dropped
