# KnowBench Source Manifest

Phase 1 defines the source policy but does not yet freeze the research corpus.

## Candidate public source families

| Source | Planned use | Status | Notes |
|---|---|---|---|
| NVD vulnerability records | CVE facts, affected products/versions, severity | To be reviewed | Record dataset/API version and retrieval date |
| CISA KEV catalog | Known exploitation and catalog metadata | To be reviewed | Record snapshot date |
| MITRE ATT&CK | Technique relationships and descriptions | To be reviewed | Preserve source identifiers |
| Vendor/project advisories | Detailed mitigations and version-specific information | To be reviewed | Include only sources whose redistribution/use terms permit the intended benchmark |

## Freeze policy

Before Phase 2 data ingestion:

1. Select the final source set.
2. Record URLs/API endpoints and license/terms.
3. Record retrieval timestamps.
4. Store immutable source identifiers and content hashes where practical.
5. Assign a corpus version such as `corpus-2026-09-24-v1`.
6. Never silently change the corpus while comparing RAG and OKF.

## Important

The benchmark must keep source provenance separate from model-generated answers. The source manifest is part of the reproducibility record.
