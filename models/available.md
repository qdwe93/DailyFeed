# 사용 가능한 무료 모델

- 점검 시각: 2026-10-28T12:03:07+09:00 (KST)
- opencode 무료 모델 9개 발견, 정상 응답 0개
- 이번 실행 사용 순서: `openrouter/thinkingmachines/inkling-small:free` → `openrouter/recursive/flint-v1.0:free` → `openrouter/cohere/north-mini-code:free` → `openrouter/thinkingmachines/inkling:free` → `openrouter/nvidia/nemotron-3.5-lightning:free`
- ⚠️ opencode 무료 모델이 모두 실패해 OpenRouter `:free` 모델을 점검했다.

우선순위는 [`priority.txt`](./priority.txt)에 한 줄에 하나씩 적는다. 비어 있으면 마지막으로 성공한 모델 → 점수순.

점수(100점): 응답 40 · JSON 형식 20 · 5줄 준수 15 · 한국어 15 · 속도 10(15초 이하 10, 45초 이하 5).

| 모델 | 상태 | 점수 | 응답(초) | 비고 |
|---|---|---:|---:|---|
| `openrouter/thinkingmachines/inkling-small:free` | ✅ | 100 | 3.9 |  |
| `openrouter/recursive/flint-v1.0:free` | ✅ | 100 | 10.2 |  |
| `openrouter/cohere/north-mini-code:free` | ✅ | 100 | 11.8 |  |
| `openrouter/thinkingmachines/inkling:free` | ✅ | 95 | 15.3 |  |
| `openrouter/nvidia/nemotron-3.5-lightning:free` | ✅ | 95 | 17.3 |  |
| `openrouter/nvidia/nemotron-3.5-super-vl:free` | ✅ | 95 | 17.9 |  |
| `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | ✅ | 95 | 21.9 |  |
| `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | ✅ | 95 | 27.0 |  |
| `openrouter/liquid/lfm-2.5-2.6b:free` | ✅ | 95 | 31.3 |  |
| `openrouter/nvidia/nemotron-3.5-content-safety:free` | ❌ | 0 | 0.8 | {"type": "provider.invalid-request", "message": "No endpoints found that support tool use. Try disabling \"edit\". To le |
| `opencode/glm-5.3-flash-free` | ❌ | 0 | 1.1 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/mimo-v2.6-flash-free` | ❌ | 0 | 1.2 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/nemotron-3-ultra-free` | ❌ | 0 | 1.2 | {"type": "provider.invalid-request", "message": "Upstream request failed: Model is unavailable.", "status": 400, "respon |
| `opencode/nemotron-3.5-super-vl-free` | ❌ | 0 | 1.4 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/nemotron-3.5-lightning-free` | ❌ | 0 | 1.7 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/deepseek-v4.1-flash-free` | ❌ | 0 | 2.2 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/beam-free` | ❌ | 0 | 2.5 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/flint-40b-free` | ❌ | 0 | 2.6 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `opencode/big-pickle` | ❌ | 0 | 2.8 | {"type": "provider.quota", "message": "Free usage limit reached. Free models work in OpenCode (https://opencode.ai); sub |
| `openrouter/google/gemma-4-31b-it:free` | ❌ | 0 | 89.7 | {"type": "provider.rate-limit", "message": "Provider returned error", "status": 429, "response": {"body": "{\"error\":{\ |
| `openrouter/google/gemma-4-26b-a4b-it:free` | ❌ | 0 | 93.8 | {"type": "provider.rate-limit", "message": "Provider returned error", "status": 429, "response": {"body": "{\"error\":{\ |
| `openrouter/xingchen-agi/xing4.0-29b-a4b:free` | ❌ | 0 | 104.8 | {"type": "provider.rate-limit", "message": "Provider returned error", "status": 429, "response": {"body": "{\"error\":{\ |
