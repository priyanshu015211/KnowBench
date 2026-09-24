# KnowBench Metric Definitions

## Retrieval

### Recall@K

Fraction of benchmark questions for which at least one gold evidence unit appears in the top K retrieved units.

`Recall@K = questions with gold evidence in top K / answerable questions`

For multi-hop questions, an additional **evidence-completeness** measure will record whether all required evidence units were retrieved.

### MRR

For each question, record the reciprocal rank of the first relevant evidence unit. Report the mean over evaluated answerable questions.

## Answer quality

### Fact correctness

Compare generated claims against the atomic `gold_facts` list. A question can receive partial credit when some required facts are correct and others are missing or wrong.

### Faithfulness / grounding

Measure whether substantive claims in the generated answer are supported by retrieved evidence. This metric is distinct from whether the answer happens to match the reference answer.

### Abstention accuracy

For unanswerable questions, score whether the system correctly abstains instead of fabricating a claim.

## Evidence quality

### Evidence precision

Fraction of returned evidence units that are relevant to the question's gold evidence set, where relevance labels are available.

### Evidence coverage

Fraction of required gold facts that have supporting retrieved evidence.

## Efficiency

Record raw values rather than collapsing them into a single score:

- end-to-end latency (ms)
- retrieval/navigation latency (ms)
- input tokens
- output tokens
- estimated cost per query, when pricing is known

## Reporting rule

KnowBench will report per-category distributions and aggregate metrics. No overall weighted score is defined in Phase 1 because weighting accuracy against latency/cost would introduce a subjective preference into the benchmark.
