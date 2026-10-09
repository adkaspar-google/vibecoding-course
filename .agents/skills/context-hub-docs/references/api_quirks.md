# Known API & SDK Quirks Reference (`references/api_quirks.md`)

- **`stripe/webhooks` (`py`, `v2026.1`)**: `Webhook.construct_event` requires the raw unparsed HTTP request bytes (`request.body`), never a deserialized JSON dictionary.
- **`openai/chat` (`py`, `v1.60.0`)**: Pass `reasoning_effort="medium"` for balanced tool-calling latency; set `additionalProperties: False` on strict tool schemas.
