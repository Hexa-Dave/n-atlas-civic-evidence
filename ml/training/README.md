# Model training and fine-tuning

This directory contains reproducible scripts for preparing training data and fine-tuning the selected N-ATLAS model for the defined civic-literacy task.

## Before training

- Verify that the selected N-ATLAS model supports the proposed fine-tuning method.
- Confirm access, license, compute requirements, and permitted use.
- Document data provenance, consent or license, redaction, annotation guidance, and exclusion criteria.
- Split data by source/person/event where appropriate to reduce leakage.
- Keep benchmark examples out of training, prompt development, and model selection.

Each training run should record the source revision, dataset and split identifiers, configuration, random seed where applicable, software and model versions, compute environment, output checkpoint/adapter, and logs. Do not commit private raw audio, credentials, or large generated checkpoints by default.

A training script being present does not establish that fine-tuning succeeded. Report actual results only after the run completes and outputs are verified.
