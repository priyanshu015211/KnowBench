# KnowBench

### A Controlled Benchmark for RAG and Open Knowledge Format in LLM Question Answering

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/RAG-Benchmark-orange?style=for-the-badge" alt="RAG">
  <img src="https://img.shields.io/badge/OKF-v0.2-green?style=for-the-badge" alt="OKF">
  <img src="https://img.shields.io/badge/Research-Experimental-purple?style=for-the-badge" alt="Research">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>How does knowledge representation and access strategy affect LLM question answering?</b>
</p>

---

## What is KnowBench?

**KnowBench** is a research-oriented benchmark for comparing two controlled knowledge-access configurations for Large Language Models:

1. **RAG** — retrieval-augmented generation over an unstructured document corpus.
2. **OKF** — an Open Knowledge Format v0.2 knowledge bundle consumed through an explicit navigation/retrieval policy.

The project does **not** assume that one approach is universally better. Instead, it keeps the knowledge corpus, questions, LLM, generation contract, and evaluation methodology fixed and measures where the systems differ.

> **Important:** RAG is a retrieval/generation architecture, while OKF is a knowledge representation format. KnowBench therefore compares concrete **system configurations**, not the abstract concepts as if they were identical layers.

---

## Research Question

> **Under a controlled corpus, question set, and LLM, how do a conventional RAG pipeline and an OKF-based knowledge-navigation pipeline differ in answer quality, evidence retrieval, robustness, and efficiency?**

### Secondary questions

- Does performance change by question type?
- Which system retrieves required evidence more consistently?
- How do the systems behave on multi-hop, temporal, contradictory, and unanswerable queries?
- How do latency and token consumption differ?
- How do the representations behave when knowledge is updated or corrected?

---

## Why this is different from a typical RAG project

KnowBench is **not** primarily a chatbot. The main deliverable is an experimental framework that lets us answer measurable questions about knowledge representation.

```text
                         SAME SOURCE CORPUS
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
            ┌──────────┐                  ┌──────────┐
            │   RAG    │                  │   OKF    │
            └────┬─────┘                  └────┬─────┘
                 │                             │
          Dense retrieval              Concepts + links
                 │                     + navigation
                 └──────────────┬──────────────┘
                                │
                                ▼
                         SAME LLM + PROMPT
                                │
                                ▼
                         SAME BENCHMARK
                                │
                                ▼
                    ┌─────────────────────┐
                    │  KnowBench Metrics  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          Correctness      Evidence        Efficiency
          & Grounding      Retrieval        & Cost
```

---

## Phase 1 — Research Foundation

**Current status: Complete**

Phase 1 establishes the research protocol before implementation begins.

| Area | Status |
|---|:---:|
| Research question | ✅ |
| Domain selection | ✅ |
| RAG system definition | ✅ |
| OKF system definition | ✅ |
| Fairness rules | ✅ |
| Benchmark categories | ✅ |
| Ground-truth schema | ✅ |
| Evaluation metrics | ✅ |
| Reproducibility protocol | ✅ |
| Benchmark schema | ✅ |
| Sample benchmark | ✅ |
| Validator | ✅ |

See [`docs/research-protocol.md`](docs/research-protocol.md) for the complete protocol.

---

## Initial Research Domain

### Open-source software security knowledge

The first benchmark is designed around publicly available software-security information, with candidate sources including:

- NVD vulnerability records
- CISA Known Exploited Vulnerabilities
- MITRE ATT&CK
- Eligible vendor/project security advisories

The final corpus will be frozen to a dated snapshot and documented in [`data/SOURCES.md`](data/SOURCES.md).

This domain provides direct facts as well as relationships, versions, dates, mitigations, and provenance—useful for evaluating both passage retrieval and structured knowledge navigation.

---

## Benchmark Design

KnowBench will test at least eight question categories:

| Category | What it tests |
|---|---|
| Direct lookup | Straightforward evidence retrieval |
| Paraphrase | Semantic matching beyond exact wording |
| Multi-hop | Combining multiple evidence units |
| Relationship | Following entity/dependency relationships |
| Temporal | Date/version-sensitive knowledge |
| Unanswerable | Correct abstention |
| Contradictory | Handling conflicting evidence |
| Distractor | Resistance to plausible but irrelevant evidence |

The target is **80+ questions** for the first research run, with **120 questions preferred** once annotation capacity allows.

The machine-readable benchmark format is defined in [`docs/benchmark-spec.md`](docs/benchmark-spec.md).

---

## Evaluation

### Retrieval

- Recall@K
- MRR
- Precision@K where applicable
- nDCG@K where graded relevance is available

### Answer quality

- Fact-level correctness
- Faithfulness / grounding
- Abstention accuracy

### Evidence

- Gold evidence recall
- Evidence precision
- Evidence coverage

### Efficiency

- End-to-end latency
- Retrieval/navigation latency
- Input tokens
- Output tokens
- Estimated cost where applicable

KnowBench intentionally avoids a single weighted "winner" score. Results will be reported by metric and question category.

---

## Reproducibility

Every experiment will record:

- Git commit
- Corpus version/hash
- Benchmark version
- OKF bundle version/hash
- Embedding model/version
- LLM/model version
- Retrieval settings
- OKF navigation settings
- Prompt version
- Seed where applicable
- Runtime information

The initial configuration template is [`configs/baseline.yaml`](configs/baseline.yaml).

---

## Repository Structure

```text
KnowBench/
├── configs/
│   └── baseline.yaml
├── data/
│   ├── SOURCES.md
│   └── benchmark/
│       └── questions.sample.json
├── docs/
│   ├── benchmark-spec.md
│   ├── metrics.md
│   ├── okf-mapping.md
│   ├── phase-1-checklist.md
│   └── research-protocol.md
├── experiments/
├── schemas/
│   └── benchmark.schema.json
├── scripts/
│   └── validate_benchmark.py
├── LICENSE
└── README.md
```

---

## Validate the Phase-1 Benchmark

The sample benchmark uses no third-party Python dependencies.

```bash
python scripts/validate_benchmark.py
```

Expected output:

```text
Benchmark validation passed: 6 question(s)
```

The sample file is explicitly marked **illustrative-only** and is not a research result.

---

## Research Methodology

KnowBench follows these principles:

1. **Same information:** the OKF transformation must not invent facts unavailable in the source corpus.
2. **Same questions:** both systems answer identical benchmark items.
3. **Same generation conditions:** the LLM and generation contract remain fixed for the primary comparison.
4. **Separate retrieval from answering:** retrieval/evidence quality is scored independently from final answer quality.
5. **No predetermined winner:** conclusions are based on measured results.
6. **Version everything:** corpus, benchmark, prompts, models, code, and configurations are tracked.

---

## Planned Roadmap

### Phase 2 — Corpus & RAG Baseline

- [ ] Freeze source corpus
- [ ] Implement ingestion
- [ ] Implement deterministic chunking
- [ ] Build dense retrieval baseline
- [ ] Implement common generation contract
- [ ] Implement evidence IDs

### Phase 3 — OKF Consumer

- [ ] Build information-preserving OKF converter
- [ ] Generate concepts and links
- [ ] Implement lexical/metadata candidate retrieval
- [ ] Implement bounded link traversal
- [ ] Map OKF concepts to stable evidence IDs

### Phase 4 — Evaluation Engine

- [ ] Retrieval metrics
- [ ] Answer metrics
- [ ] Evidence metrics
- [ ] Latency/token tracking
- [ ] Error analysis

### Phase 5 — Controlled Experiments

- [ ] RAG vs OKF baseline
- [ ] Category-level comparison
- [ ] Multi-hop experiment
- [ ] Unanswerable experiment
- [ ] Contradiction experiment
- [ ] Knowledge-update experiment
- [ ] Statistical analysis

### Phase 6 — Extensions

- [ ] BM25 RAG
- [ ] Hybrid RAG
- [ ] Reranking
- [ ] RAG + OKF hybrid system
- [ ] Interactive benchmark dashboard

---

## References

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — https://arxiv.org/abs/2005.11401
- Google Cloud, *Open Knowledge Format v0.2* — https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
- Google Cloud, *Introducing the Open Knowledge Format* — https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing

---

## License

This project is licensed under the [MIT License](LICENSE).
