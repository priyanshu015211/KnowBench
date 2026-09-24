# KnowBench Benchmark Specification

## Version

`benchmark/v0.1`

## Purpose

This specification defines the machine-readable format for benchmark questions used by both the RAG and OKF systems.

## Required fields

| Field | Type | Description |
|---|---|---|
| `question_id` | string | Globally unique benchmark ID |
| `category` | enum | Question type |
| `difficulty` | enum | `easy`, `medium`, or `hard` |
| `question` | string | User-facing question |
| `answerable` | boolean | Whether the corpus contains enough evidence to answer |
| `gold_answer` | string/object | Reference answer or abstention contract |
| `gold_facts` | array | Atomic facts required for a correct answer |
| `gold_evidence_ids` | array | Evidence units that support the answer |
| `sources` | array | Source provenance |

## Allowed categories

- `direct_lookup`
- `paraphrase`
- `multi_hop`
- `relationship`
- `temporal`
- `unanswerable`
- `contradictory`
- `distractor`

## Evidence IDs

Evidence IDs must be stable across the two system representations.

Example:

```json
"gold_evidence_ids": [
  "CVE-EXAMPLE-001#affected-versions",
  "CVE-EXAMPLE-001#mitigation"
]
```

The RAG representation maps these IDs to source passages/chunks, while the OKF representation maps them to concept files or concept fragments derived from the same source.

## Answer contract

### Answerable question

```json
{
  "answerable": true,
  "gold_answer": "Versions 1.2 through 1.4 are affected.",
  "gold_facts": [
    "1.2 is affected",
    "1.3 is affected",
    "1.4 is affected"
  ]
}
```

### Unanswerable question

```json
{
  "answerable": false,
  "gold_answer": {
    "type": "abstain",
    "reason": "The benchmark corpus does not contain evidence for this claim."
  },
  "gold_facts": []
}
```

## Annotation rules

1. Write questions that can be answered from the frozen corpus without external browsing.
2. Do not put the expected answer wording into the question.
3. Store facts atomically; avoid a single long paragraph as the gold standard.
4. Prefer stable source identifiers over URLs as evidence IDs.
5. Record all evidence needed for a complete answer, not just the first supporting passage.
6. For contradictory questions, record the conflicting evidence explicitly.
7. For temporal questions, record the relevant date boundary.
8. For relationship questions, record the nodes/edges required to reach the answer.

## Quality-control checklist

Each benchmark item should be reviewed for:

- factual correctness
- answerability
- evidence completeness
- ambiguity
- category correctness
- duplicate questions
- leakage
- source provenance
