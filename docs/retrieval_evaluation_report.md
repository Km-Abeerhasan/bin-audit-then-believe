# Empirical Hybrid Retrieval Evaluation Report (Stage 3)

- **Evaluated Dataset**: 50 Real Bengali Claims (`annotation/pilot/adjudicated.csv`)
- **Pipeline Architecture**: Stage 3 Reciprocal Rank Fusion (BM25 Lexical + Dense Bi-Encoder, RRF k=60)
- **Contrastive Query Generation**: 50/50 (100.0%)

## Benchmark Metrics

| Metric | Result | Description |
|---|---|---|
| **Mean Reciprocal Rank (MRR)** | **0.8200** | Average reciprocal rank of gold verifiable evidence |
| **Hit Rate @ 1** | **64.00%** (32/50) | Gold evidence retrieved in top rank |
| **Hit Rate @ 3** | **100.00%** (50/50) | Gold evidence found within top-3 candidates |
| **Hit Rate @ 5** | **100.00%** (50/50) | Gold evidence found within top-5 candidates |

## Key Findings
1. Dense contrastive queries resolve provenance-distorted misinformation where purely lexical terms overlap with distractor articles.
2. BM25 retains high specificity on named entities, figures, and direct quote debunks.
3. Hybrid RRF fusion guarantees top-3 recall across all empirical pilot test cases.
