# 사용 가능한 무료 모델

- 점검 시각: 2026-11-06T12:00:54+09:00 (KST)
- opencode 무료 모델 10개 발견, 정상 응답 10개
- 이번 실행 사용 순서: `opencode/deepseek-v4.1-flash-free` → `opencode/pulse-alpha-free` → `opencode/crouton-alpha-free` → `opencode/nemotron-3.5-super-vl-free` → `opencode/flint-40b-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/pulse-alpha-free` | ✅ | 100 | 4.4 |  |
| `opencode/crouton-alpha-free` | ✅ | 100 | 5.8 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 100 | 8.2 |  |
| `opencode/flint-40b-free` | ✅ | 100 | 9.4 |  |
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 10.1 |  |
| `opencode/beam-free` | ✅ | 100 | 11.8 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 13.0 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 13.6 |  |
| `opencode/big-pickle` | ✅ | 95 | 20.8 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 95 | 27.5 |  |
