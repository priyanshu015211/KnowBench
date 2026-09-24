#!/usr/bin/env python3
"""Validate a KnowBench benchmark file using only the Python standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CATEGORIES = {
    "direct_lookup",
    "paraphrase",
    "multi_hop",
    "relationship",
    "temporal",
    "unanswerable",
    "contradictory",
    "distractor",
}
DIFFICULTIES = {"easy", "medium", "hard"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(path: Path) -> int:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(errors, f"file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid JSON: {exc}")
    else:
        if not isinstance(payload, dict):
            fail(errors, "top level must be an object")
        else:
            if not isinstance(payload.get("benchmark_version"), str):
                fail(errors, "benchmark_version must be a string")
            questions = payload.get("questions")
            if not isinstance(questions, list) or not questions:
                fail(errors, "questions must be a non-empty array")
            else:
                seen: set[str] = set()
                for index, item in enumerate(questions):
                    prefix = f"questions[{index}]"
                    if not isinstance(item, dict):
                        fail(errors, f"{prefix} must be an object")
                        continue

                    qid = item.get("question_id")
                    if not isinstance(qid, str) or not qid:
                        fail(errors, f"{prefix}.question_id must be a non-empty string")
                    elif qid in seen:
                        fail(errors, f"duplicate question_id: {qid}")
                    else:
                        seen.add(qid)

                    category = item.get("category")
                    if category not in CATEGORIES:
                        fail(errors, f"{prefix}.category must be one of {sorted(CATEGORIES)}")

                    if item.get("difficulty") not in DIFFICULTIES:
                        fail(errors, f"{prefix}.difficulty must be easy/medium/hard")

                    if not isinstance(item.get("question"), str) or len(item["question"].strip()) < 5:
                        fail(errors, f"{prefix}.question must contain at least 5 characters")

                    answerable = item.get("answerable")
                    if not isinstance(answerable, bool):
                        fail(errors, f"{prefix}.answerable must be boolean")
                        continue

                    facts = item.get("gold_facts")
                    evidence = item.get("gold_evidence_ids")
                    sources = item.get("sources")
                    if not all(isinstance(x, list) for x in (facts, evidence, sources)):
                        fail(errors, f"{prefix}.gold_facts, gold_evidence_ids, and sources must be arrays")
                        continue

                    if category == "unanswerable" or not answerable:
                        if evidence:
                            fail(errors, f"{prefix}: unanswerable items must not contain gold evidence IDs")
                    else:
                        if not evidence:
                            fail(errors, f"{prefix}: answerable items need at least one gold evidence ID")

    if errors:
        print("Benchmark validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    count = len(payload["questions"])
    print(f"Benchmark validation passed: {count} question(s)")
    return 0


if __name__ == "__main__":
    benchmark = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/benchmark/questions.sample.json")
    raise SystemExit(validate(benchmark))
