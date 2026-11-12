# 사용 가능한 무료 모델

- 점검 시각: 2026-11-12T12:01:07+09:00 (KST)
- opencode 무료 모델 12개 발견, 정상 응답 12개
- 이번 실행 사용 순서: `opencode/deepseek-v4.1-flash-free` → `opencode/minimax-m3.1-flash-free` → `opencode/inkling-2-small-free` → `opencode/glm-5.3-flash-free` → `opencode/nemotron-3.5-super-vl-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/minimax-m3.1-flash-free` | ✅ | 100 | 3.5 |  |
| `opencode/inkling-2-small-free` | ✅ | 100 | 5.6 |  |
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 5.9 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 6.2 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 100 | 6.7 |  |
| `opencode/big-pickle` | ✅ | 100 | 7.3 |  |
| `opencode/beam-free` | ✅ | 100 | 8.5 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 10.6 |  |
| `opencode/iceman-free` | ✅ | 100 | 12.7 |  |
| `opencode/flint-40b-free` | ✅ | 100 | 13.2 |  |
| `opencode/longcat-2.5-free` | ✅ | 95 | 23.0 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 95 | 34.1 |  |
