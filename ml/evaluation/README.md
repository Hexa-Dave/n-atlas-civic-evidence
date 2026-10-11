# Model evaluation

This directory measures whether fine-tuning improves the defined civic-literacy task compared with the base N-ATLAS model.

## Benchmark protocol

1. Freeze a held-out benchmark with at least 500 examples, as required by the challenge brief.
2. Create independently reviewed expected outputs and annotation guidance.
3. Run the base and fine-tuned model on the same examples with recorded settings.
4. Save per-example predictions, validation failures, errors, and model/configuration identifiers.
5. Calculate task-appropriate metrics and compare the two systems.
6. Review critical errors, including fabricated details, unsupported certainty, misclassification, and missing source links.
7. Generate a report reproducible from saved inputs and outputs.

Potential measures include field-level precision/recall/F1, classification macro-F1, structured-field accuracy, schema-validity rate, and source-span alignment. Explain metric definitions and limitations; use the challenge's official requirements as the authority for the final metric set.

Proposed command names are examples until implemented. Never publish placeholder numbers as measured results.
