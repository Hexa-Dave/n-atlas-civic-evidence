# Requirements checklist

Mark each item only when it is implemented and verified.

## Core workflow

- [ ] Case creation with recorded consent
- [ ] Audio upload with validation, hashing, and access control
- [ ] Transcription via a supported speech-to-text path
- [ ] N-ATLAS claim extraction bound to transcript segments
- [ ] Human review (accept/edit/reject/flag) with notes
- [ ] Official-source retrieval kept separate from testimony
- [ ] Report generation with provenance and citations
- [ ] Report export

## Safety and trust

- [ ] No model-extracted claim is presented as verified
- [ ] Every claim links to a source segment
- [ ] Report finalization requires human review
- [ ] Model/retrieval failures fail loudly, never fabricate

## Evidence

- [ ] Tests for permissions, schema validation, and provenance
- [ ] Base vs fine-tuned benchmark on a held-out set
- [ ] Reproducible deployment and verification steps
- [ ] Model card and benchmark methodology documented
