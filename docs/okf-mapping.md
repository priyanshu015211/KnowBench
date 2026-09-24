# OKF Mapping Protocol

KnowBench uses **Open Knowledge Format v0.2** for the structured representation experiment.

## Canonical OKF rules used by KnowBench

An OKF concept is a UTF-8 Markdown document with YAML frontmatter. The OKF v0.2 specification requires a non-empty `type`; `title`, `description`, `resource`, and `tags` are recommended. The specification also supports provenance/trust fields and ordinary Markdown cross-links.

KnowBench will declare the target version with `okf_version: "0.2"` in the bundle root and will not invent a private replacement schema for the experiment.

## Security-domain concept types

The project will use descriptive type values rather than pretending they are globally registered:

- `Vulnerability`
- `Product`
- `Version`
- `Vendor`
- `Technique`
- `Mitigation`
- `Advisory`
- `Reference`

## Mapping example

```text
Source record
   |
   +--> Vulnerability concept
   |       +--> affected product
   |       +--> affected versions
   |       +--> severity
   |       +--> mitigation
   |       +--> sources
   |
   +--> Product concept
   |       +--> versions
   |
   +--> Mitigation concept
```

Links must use normal Markdown references so the knowledge graph remains human-readable and version-control friendly.

## Information-preservation rule

The OKF representation may reorganize content and expose relationships that are implicit in the source, but it must not introduce unsupported facts. Every substantive concept should retain source provenance.

## Transformation ledger

Every generated OKF bundle should have a companion transformation record containing:

- source corpus version
- converter version/commit
- extraction model/version, if any
- transformation timestamp
- manual curation steps
- rejected or ambiguous transformations

This makes OKF curation an observable experimental variable rather than an undocumented advantage.
