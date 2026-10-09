# Layer Dependency Contracts (`references/layer_contracts.md`)

- `domain/` -> may depend only on `domain/` (pure business logic and value objects).
- `service/` -> may depend on `domain/` and `service/`.
- `infra/` -> may depend on `domain/`, `service/`, and `infra/`.
- `ui/` -> may depend on `service/` and `domain/`, never directly on `infra/`.
