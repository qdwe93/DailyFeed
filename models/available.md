# 사용 가능한 무료 모델

- 점검 시각: 2026-11-10T12:01:58+09:00 (KST)
- opencode 무료 모델 12개 발견, 정상 응답 12개
- 이번 실행 사용 순서: `opencode/deepseek-v4.1-flash-free` → `opencode/inkling-2-small-free` → `opencode/minimax-m3.1-flash-free` → `opencode/glm-5.3-flash-free` → `opencode/nemotron-3.5-super-vl-free`
- 새로 생김: `opencode/longcat-2.5-free`, `opencode/minimax-m3.1-flash-free`
- 사라짐: `opencode/crouton-alpha-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/inkling-2-small-free` | ✅ | 100 | 3.9 |  |
| `opencode/minimax-m3.1-flash-free` | ✅ | 100 | 4.2 |  |
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 7.2 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 100 | 9.0 |  |
| `opencode/big-pickle` | ✅ | 100 | 9.7 |  |
| `opencode/beam-free` | ✅ | 100 | 10.5 |  |
| `opencode/longcat-2.5-free` | ✅ | 100 | 10.8 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 11.2 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 11.2 |  |
| `opencode/iceman-free` | ✅ | 95 | 15.1 |  |
| `opencode/flint-40b-free` | ✅ | 95 | 17.4 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 90 | 88.1 |  |
