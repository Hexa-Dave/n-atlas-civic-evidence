# Evidence index

Point each claim to the artifact that proves it. Do not cite aspirational work.

| Capability | Evidence location | Verified? |
| --- | --- | --- |
| Backend API and services | `backend/`, `docs/api-reference.md` | No |
| Reviewer interface | `apps/web/`, `docs/user-guide.md` | No |
| N-ATLAS integration | `ml/src/atlas_client.py`, `ml/configs/base_model.yaml` | No |
| Fine-tuning pipeline | `ml/training/`, `artifacts/model-adapters/` | No |
| Benchmark results | `data/benchmark/`, `artifacts/evaluation-reports/` | No |
| Civic source registry | `civic_knowledge/sources/source_registry.yaml` | No |
| Tests | `backend/tests/`, `ml/tests/`, `civic_knowledge/evaluation/` | No |
| Deployment | `infra/`, `docs/deployment.md` | No |

Update the "Verified?" column only after reproducible evidence exists.
