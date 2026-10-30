# 사용 가능한 무료 모델

- 점검 시각: 2026-10-30T12:00:45+09:00 (KST)
- opencode 무료 모델 8개 발견, 정상 응답 8개
- 이번 실행 사용 순서: `opencode/glm-5.3-flash-free` → `opencode/nemotron-3.5-lightning-free` → `opencode/deepseek-v4.1-flash-free` → `opencode/mimo-v2.6-flash-free` → `opencode/big-pickle`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/nemotron-3.5-lightning-free` | ✅ | 100 | 9.0 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 9.2 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 10.3 |  |
| `opencode/big-pickle` | ✅ | 100 | 12.0 |  |
| `opencode/beam-free` | ✅ | 100 | 13.7 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 95 | 15.4 |  |
| `opencode/flint-40b-free` | ✅ | 95 | 20.5 |  |
| `opencode/glm-5.3-flash-free` | ✅ | 95 | 20.8 |  |
