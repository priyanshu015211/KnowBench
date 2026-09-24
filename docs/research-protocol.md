# KnowBench Research Protocol

**Status:** Phase 1 — finalized for implementation  
**Version:** 0.1  
**Last updated:** 2026-09-24

## 1. Research objective

KnowBench studies how **knowledge representation and access strategy** affect LLM question answering. The primary experiment compares a conventional Retrieval-Augmented Generation (RAG) pipeline with an **OKF v0.2 knowledge-base consumer** over the same underlying source corpus.

The experiment is intentionally framed as a comparison of **system configurations**, not as a claim that RAG and OKF are competing technologies at the same abstraction layer. RAG is a retrieval/generation architecture; OKF is a knowledge representation format. The OKF system therefore includes an explicit navigation/retrieval procedure defined by this project.

## 2. Primary research question

> **RQ1: Under a controlled corpus, question set, and LLM, how do a conventional RAG pipeline and an OKF-based knowledge-navigation pipeline differ in answer quality, evidence retrieval, robustness, and efficiency?**

### Secondary questions

- **RQ2:** Does the relative performance change by question type (direct lookup, paraphrase, multi-hop, unanswerable, contradictory, temporal)?
- **RQ3:** Which system retrieves the required evidence more consistently?
- **RQ4:** How do the systems differ in latency and token usage under the same generation model?
- **RQ5:** How does each representation respond to knowledge updates and corrections?

## 3. Domain selection

### Initial domain: open-source software security knowledge

The benchmark will use public, machine-readable and/or openly accessible software-security information, with preference for sources that provide stable identifiers and explicit provenance. Candidate source families are:

- NVD vulnerability records
- CISA Known Exploited Vulnerabilities catalog
- MITRE ATT&CK technique information
- Vendor or project security advisories where redistribution terms permit use

The final corpus will be frozen to a dated snapshot before evaluation. The exact source list, versions, retrieval dates, and licenses will be recorded in `data/SOURCES.md` before data collection begins.

### Why this domain?

Software-security knowledge naturally contains entities, relationships, versions, dates, mitigations, identifiers, and source provenance. This makes it suitable for testing both passage retrieval and explicit concept/link navigation without requiring a proprietary dataset.

## 4. Unit of comparison

Each benchmark item is associated with one or more **gold evidence units**.

- In RAG, an evidence unit is a source passage/chunk identified by a stable `evidence_id`.
- In OKF, an evidence unit is an OKF concept file or a defined concept fragment identified by a stable `evidence_id`.
- Both evidence forms must trace back to the same underlying source material.

The generated answer is evaluated separately from evidence retrieval so that a system cannot receive full credit simply because the LLM produced a plausible answer.

## 5. Controlled variables

The following are held constant for the primary comparison:

| Variable | Controlled condition |
|---|---|
| Source corpus | Same frozen source snapshot |
| Information content | Same facts; OKF transformation may reorganize, not invent, facts |
| Question set | Same benchmark items |
| Ground truth | Same gold answers and evidence IDs |
| LLM | Same model and model version |
| Generation prompt | Same answer-generation contract |
| Temperature | 0 where supported |
| Output limits | Same token limit |
| Hardware | Same execution environment where practical |
| Evaluation code | Same evaluator and scoring implementation |

The retrieval configuration itself is intentionally allowed to differ because it is part of the system under evaluation. Its exact settings must be logged for every run.

## 6. Primary system definitions

### 6.1 RAG configuration

```text
Source documents
  -> normalization
  -> deterministic chunking
  -> embeddings
  -> vector index
  -> top-k retrieval
  -> common generation prompt
  -> answer + evidence IDs
```

The initial baseline is dense retrieval. BM25, hybrid retrieval, and reranking are planned as controlled extensions rather than being mixed into the first baseline.

### 6.2 OKF configuration

```text
Source documents
  -> information-preserving OKF conversion
  -> OKF concepts + links + metadata
  -> lexical/metadata candidate selection
  -> bounded link traversal
  -> common generation prompt
  -> answer + evidence IDs
```

The retrieval/navigation procedure is **KnowBench-defined**; it is not presented as an intrinsic property of the OKF specification.

## 7. Fairness constraint for OKF construction

The OKF corpus must not contain facts absent from the source corpus. During conversion:

1. Every concept must retain source provenance.
2. Any derived relationship must be traceable to source evidence or explicitly marked as derived.
3. No benchmark answer may be encoded directly into an OKF concept solely to improve the OKF system's score.
4. The transformation process and prompt/tool version used to create the OKF bundle must be versioned.
5. Manual curation decisions must be logged.

This is essential because better curation can otherwise become a hidden source of experimental advantage.

## 8. Hypotheses

These are **testable hypotheses**, not expected conclusions.

- **H1:** Performance differs by question type rather than being uniform across the benchmark.
- **H2:** Explicit relationships can affect performance on multi-hop and dependency questions.
- **H3:** Dense RAG can be competitive on direct and paraphrased passage-level questions.
- **H4:** The two systems can fail on different questions even when aggregate scores are similar.
- **H5:** Updating a structured concept may require different work from updating a retrieved document index.

## 9. Benchmark categories

The benchmark must contain at least these categories:

| Category | Purpose |
|---|---|
| Direct lookup | Tests straightforward retrieval |
| Paraphrase | Tests semantic matching beyond lexical overlap |
| Multi-hop | Requires combining multiple evidence units |
| Relationship | Tests entity/dependency/link navigation |
| Temporal | Tests date/version-sensitive evidence |
| Unanswerable | Tests abstention when evidence is absent |
| Contradictory | Tests conflicting source handling |
| Distractor | Tests resistance to plausible but irrelevant evidence |

The first research run should target **at least 80 questions**, with a balanced distribution across categories. A 120-question benchmark is the preferred target once annotation resources are available.

## 10. Ground-truth policy

Each benchmark question must define:

- a stable `question_id`
- a category
- a difficulty label
- an answerability flag
- one or more acceptable reference answers or required facts
- one or more gold evidence IDs
- source provenance
- optional notes on acceptable variations

For unanswerable questions, the gold answer is an **abstention**, not a guessed statement.

## 11. Evaluation policy

### Retrieval metrics

- Recall@K
- Precision@K where a denominator is well-defined
- MRR
- nDCG@K where graded relevance is available

### Answer metrics

- Fact-level correctness
- Reference-answer semantic similarity where appropriate
- Faithfulness/grounding
- Abstention correctness

### Evidence metrics

- Gold evidence recall
- Citation/evidence precision
- Evidence coverage of required facts

### Efficiency metrics

- End-to-end latency
- Retrieval latency
- Input tokens
- Output tokens
- Estimated model cost when pricing is available

### Maintenance metrics

- Corpus ingestion time
- Update propagation time
- Number of artifacts touched per update
- Re-index/rebuild requirements

## 12. Evaluation hierarchy

Human/ground-truth labels are the primary source for correctness where feasible. Automated LLM judges may be used as a secondary evaluator and must be validated on a manually checked subset.

No single composite score will be used as the sole basis for conclusions. Results will be reported by metric and question category.

## 13. Statistical plan

For the final study:

- Report aggregate metrics with the number of evaluated items.
- Report category-level metrics.
- Use paired comparisons because both systems answer the same questions.
- Report confidence intervals or bootstrap intervals where appropriate.
- Record failed runs and exclusions rather than silently dropping them.
- Include an error-analysis section with representative failure categories.

## 14. Main threats to validity

### Representation bias

OKF construction can inject human/agent curation decisions that RAG does not receive. The provenance and transformation log are therefore part of the experiment.

### Retrieval-policy bias

Because OKF does not prescribe a retrieval algorithm, the chosen OKF navigation policy can materially affect results. Its configuration must be treated as an experimental factor and reported explicitly.

### LLM evaluator bias

LLM-as-judge can favor certain answer styles. Ground-truth evidence and manually audited subsets should therefore remain part of the evaluation protocol.

### Corpus bias

Results from software-security knowledge cannot automatically be generalized to every knowledge domain. The paper must state the domain and corpus boundaries clearly.

### Benchmark leakage

Benchmark answers and gold evidence must not be embedded into prompts, retrieval metadata, or OKF concepts in a way that leaks the expected answer.

## 15. Reproducibility requirements

Every experiment must record:

- Git commit
- benchmark version
- corpus version/hash
- OKF bundle version/hash
- embedding model/version
- LLM/model version
- retrieval settings
- traversal settings
- prompt version
- random seed where applicable
- timestamp
- hardware/runtime information

The machine-readable experiment configuration template is in `configs/baseline.yaml`.

## 16. Phase-1 exit criteria

Phase 1 is complete when:

- [x] Research question is fixed.
- [x] Domain and corpus-selection policy are fixed.
- [x] RAG and OKF system boundaries are defined.
- [x] Fairness rules for OKF construction are defined.
- [x] Benchmark categories are defined.
- [x] Ground-truth schema is defined.
- [x] Evaluation metrics are defined.
- [x] Reproducibility requirements are defined.
- [x] Benchmark JSON schema is implemented.
- [x] A sample benchmark file validates against the schema/rules.

## References

1. Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (2020): https://arxiv.org/abs/2005.11401
2. Google Cloud, *Open Knowledge Format* (official specification): https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
3. Google Cloud, *Introducing the Open Knowledge Format* (2026): https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
