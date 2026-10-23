# 사용 가능한 무료 모델

- 점검 시각: 2026-10-23T12:00:54+09:00 (KST)
- opencode 무료 모델 9개 발견, 정상 응답 9개
- 이번 실행 사용 순서: `opencode/nemotron-3-ultra-free` → `opencode/beam-free` → `opencode/glm-5.3-flash-free` → `opencode/deepseek-v4.1-flash-free` → `opencode/big-pickle`
- 사라짐: `opencode/longcat-2.5-preview-free`, `opencode/minimax-m3.1-flash-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/beam-free` | ✅ | 100 | 4.5 |  |
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 5.3 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 6.1 |  |
| `opencode/big-pickle` | ✅ | 100 | 7.1 |  |
| `opencode/nemotron-3-ultra-free` | ✅ | 100 | 10.8 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 14.7 |  |
| `opencode/flint-40b-free` | ✅ | 95 | 15.2 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 95 | 18.6 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 95 | 33.6 |  |
