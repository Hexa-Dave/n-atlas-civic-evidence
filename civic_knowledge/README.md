# Civic knowledge and official-source retrieval

This directory manages the curated source collection used to answer procedural civic-literacy questions. It must remain logically separate from witness testimony and model-extracted allegations.

## Intended contents

- `sources/` — source registry with publisher, title, URL, jurisdiction, publication/update date, access date, and review status.
- `ingestion/` — fetching, parsing, normalization, and refresh workflows.
- `retrieval/` — indexing and retrieval components.
- `evaluation/` — retrieval tests, citation checks, and answer-grounding evaluation.

## Source policy

Prefer authoritative, relevant sources such as official laws, regulations, election-management bodies, courts, and recognized public agencies. Record jurisdiction and effective dates. Do not treat an unverified page or model-generated summary as an official source.

## Answer policy

- Return source titles, links, and relevant sections where possible.
- Distinguish sourced procedural information from statements supplied by a witness.
- If sources conflict, are outdated, or do not answer the question, say so.
- Do not invent legal citations, deadlines, procedures, or quotations.
- Present civic guidance as informational, not individualized legal advice.

Document source freshness and retrieval limitations. Check a retrieved source for relevance and authority before using it in a report.
