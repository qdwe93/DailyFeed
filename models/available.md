# 사용 가능한 무료 모델

- 점검 시각: 2026-11-07T12:00:43+09:00 (KST)
- opencode 무료 모델 11개 발견, 정상 응답 10개
- 이번 실행 사용 순서: `opencode/deepseek-v4.1-flash-free` → `opencode/glm-5.3-flash-free` → `opencode/crouton-alpha-free` → `opencode/nemotron-3.5-super-vl-free` → `opencode/mimo-v2.6-flash-free`
- 새로 생김: `opencode/iceman-free`, `opencode/inkling-2-small-free`
- 사라짐: `opencode/pulse-alpha-free`

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `opencode/glm-5.3-flash-free` | ✅ | 100 | 3.0 |  |
| `opencode/crouton-alpha-free` | ✅ | 100 | 4.7 |  |
| `opencode/nemotron-3.5-super-vl-free` | ✅ | 100 | 6.2 |  |
| `opencode/mimo-v2.6-flash-free` | ✅ | 100 | 6.8 |  |
| `opencode/iceman-free` | ✅ | 100 | 7.9 |  |
| `opencode/beam-free` | ✅ | 100 | 10.8 |  |
| `opencode/deepseek-v4.1-flash-free` | ✅ | 100 | 12.0 |  |
| `opencode/big-pickle` | ✅ | 100 | 12.6 |  |
| `opencode/nemotron-3.5-lightning-free` | ✅ | 100 | 14.4 |  |
| `opencode/flint-40b-free` | ✅ | 95 | 17.1 |  |
| `opencode/inkling-2-small-free` | ❌ | 0 | 2.5 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
