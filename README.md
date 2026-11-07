# BiN_Audit_Then_Believe: Evidence-Calibrated Multimodal Fact Verification with Audit Gates

**Department of Computer Science and Engineering | Jahangirnagar University**  
Master of Science in Computer Science & Engineering (PMCS Program, Batch 42)  

* **Candidate:** Khan Muhammad Abeer Hasan (Student ID: CSE2026095)  
* **Project Supervisor:** Dr. Md. Humayun Kabir, Professor, Dept. of CSE, Jahangirnagar University  

---

## 📌 Overview
Automated rumor verification in low-resource linguistic environments (e.g., Bengali digital media) is bottlenecked by:
1. **Sparse and Noisy Evidentiary Corpora:** Digitally latent, unindexed, or cross-lingual press reports.
2. **Generative Hallucinations:** Uncalibrated confidence and synthetic explanations from zero-shot LLMs.
3. **Brittle Stance Aggregation:** Inability of end-to-end classifiers to distinguish authoritative official denials from visual provenance absence and true epistemic ambiguity.

**BiNPipeline** addresses this by decoupling neural retrieval and stance detection from verdict adjudication. The framework couples a dual-path hybrid lexical-dense retrieval module orchestrated via **Reciprocal Rank Fusion (RRF)** with a **Stage-6 Deterministic Verdict Synthesis Engine** governing explicit audit rules.

---

## 🔬 Key Empirical Results ($N = 50$ Adjudicated Benchmark)

Evaluated on an empirical benchmark curated from authenticated investigations by *Rumor Scanner* and *BOOM Bangladesh* with high inter-annotator reliability ($\kappa = 0.9055$):

| Metric | Subsystem | Score | Baseline Comparison |
| :--- | :--- | :---: | :---: |
| **Verdict Accuracy** | Stage-6 Deterministic Rules | **100.0%** (50/50) | vs. Raw Argmax LLM (62.0%) |
| **Mean Reciprocal Rank (MRR)** | Hybrid Fusion (BM25 + Dense RRF) | **0.8200** | vs. BM25 (0.6410), Dense (0.7125) |
| **Hit@3 Retrieval Rate** | Candidate Evidence Coverage | **100.0%** | vs. BM25 (78.0%), Dense (86.0%) |
| **Inter-Annotator Agreement** | Annotation Reliability | **$\kappa = 0.9055$** | Grounded in authenticated fact-checks |
| **Uncertainty Fallback Gate** | Hallucination Guardrail ($\tau_{\text{abstain}}$) | **0.60** | Safe abstention under low evidence |

---

## 🏗️ System Architecture

```text
Claim C ──► [Stage 1-2: Claim Normalization & Metadata Extraction]
                │
                ▼
        [Stage 3: Hybrid Evidence Retrieval]
         ├── BM25 Lexical Matching (Inverted Index)
         └── Dense Bi-Encoder Cosine Retrieval
                │
                ▼ (Reciprocal Rank Fusion, k = 60)
         Top-K Evidence Pool E = {e_1, ..., e_K}
                │
                ▼
        [Stage 4: Calibrated Stance Inference]
         └── Temperature-Scaled NLI Classifier (theta = 0.70)
                │
                ▼
        [Stage 5: Evidence Pool Curation] ──► (S_sup, S_contra)
                │
                ▼
        [Stage 6: Deterministic Audit Gates (RULE_1 to RULE_9)]
                │
                ├── RULE_1: Provenance Absence (Misleading, alpha = 0.92)
                ├── RULE_2: Insufficient Search (Insufficient, alpha = 0.90)
                ├── RULE_4B: Authoritative Tier-1 Denial (Refuted, alpha = 0.95)
                ├── RULE_5: Multi-Source Independent Support (Supported, alpha = 0.94)
                ├── RULE_7: Numeric Mismatch Distortion (Misleading, alpha = 0.88)
                └── RULE_9: Low Confidence Abstention Fallback (Insufficient, alpha = 0.60)
                │
                ▼
          Final Audited Verdict + Justification Trail