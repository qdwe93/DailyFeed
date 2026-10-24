# 사용 가능한 무료 모델

- 점검 시각: 2026-10-24T12:01:02+09:00 (KST)
- opencode 무료 모델 9개 발견, 정상 응답 9개
- 이번 실행 사용 순서: `opencode/nemotron-3-ultra-free` → `opencode/glm-5.3-flash-free` → `opencode/nemotron-3.5-super-vl-free` → `opencode/mimo-v2.6-flash-free` → `opencode/nemotron-3.5-lightning-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 3.5 |  |
| `opencode/nemotron-3-ultra-free` | ✅ | 100 | 4.6 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 100 | 6.7 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 7.7 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 100 | 11.0 |  |
| `opencode/beam-free` | ✅ | 95 | 17.4 |  |
| `opencode/flint-40b-free` | ✅ | 95 | 26.4 |  |
| `opencode/big-pickle` | ✅ | 95 | 32.9 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 90 | 47.7 |  |
