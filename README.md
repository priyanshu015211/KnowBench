# KnowBench

### A Comparative Benchmark for RAG and Open Knowledge Format in LLM Question Answering

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LLM-Research-purple?style=for-the-badge" alt="LLM">
  <img src="https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-orange?style=for-the-badge" alt="RAG">
  <img src="https://img.shields.io/badge/OKF-Open%20Knowledge%20Format-green?style=for-the-badge" alt="OKF">
  <img src="https://img.shields.io/badge/Research-Benchmarking-red?style=for-the-badge" alt="Research">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>How does the way we represent knowledge affect the way LLMs retrieve and use it?</b>
</p>

---

## Overview

**KnowBench** is an experimental benchmarking framework designed to compare different approaches to providing external knowledge to Large Language Models (LLMs).

The project evaluates two fundamentally different knowledge-access strategies:

- **Retrieval-Augmented Generation (RAG)** — retrieving relevant information from an unstructured document corpus.
- **Open Knowledge Format (OKF)** — representing knowledge as structured, explicitly connected concepts.

Rather than building another standalone RAG chatbot, KnowBench focuses on the **experimental comparison of knowledge representation and retrieval strategies** under controlled conditions.

Both systems are evaluated using the **same knowledge domain, questions, LLM, and evaluation methodology**, allowing meaningful comparison across multiple dimensions.

---

## Research Question

> **How does structured knowledge representation compare with conventional retrieval-augmented generation for LLM-based question answering?**

KnowBench investigates whether different knowledge representations influence:

- Answer correctness
- Retrieval effectiveness
- Multi-hop question answering
- Evidence and provenance
- Hallucination resistance
- Latency
- Token consumption
- Knowledge maintenance
- Performance on unanswerable and conflicting questions

---

## Key Idea

```text
                         KNOWLEDGE CORPUS
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          ┌─────────────┐              ┌─────────────┐
          │     RAG     │              │     OKF     │
          └──────┬──────┘              └──────┬──────┘
                 │                             │
        Document Chunking              Structured Concepts
                 │                             │
           Embeddings                    Relationships
                 │                             │
          Vector Retrieval              Knowledge Index
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                         Same LLM Layer
                                │
                                ▼
                       Same Evaluation Set
                                │
                                ▼
                     ┌────────────────────┐
                     │    KnowBench       │
                     │    Evaluation      │
                     └─────────┬──────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
       Correctness         Retrieval           Efficiency
       & Grounding        Performance         & Cost
