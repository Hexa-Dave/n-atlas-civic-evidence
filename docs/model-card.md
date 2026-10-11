# Model card

## Intended use

Decision support for authorized reviewers: extract claims from testimony and
classify civic incidents into structured, source-linked records. Not a truth
determination and not a substitute for human review or legal advice.

## Model

- Integration: N-ATLAS over the configured API endpoint.
- Model id/version: pin the exact identifier in `ml/configs/base_model.yaml`.
- Fine-tuning: optional LoRA adapter recorded in `ml/src/model_registry.py`.

Record the exact model, version, adapter, and inference settings with every run.

## Limitations and risks

- Extraction can miss claims or produce unsupported claims.
- Source attribution can be lost; the UI marks claims with no linked segment.
- Performance on unseen jurisdictions or languages is not established.
- Outputs must never be presented as verified facts.

## Evaluation

Compare base and fine-tuned models on a held-out, human-verified set under
identical settings. Report task metrics and safety failures. See
`docs/benchmark-methodology.md`.
