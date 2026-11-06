# Empirical Pilot Annotation & Agreement Report

## 1. Dataset Overview
- **Domain**: Bengali digital misinformation and public safety claims.
- **Source**: Published fact-check archives (Rumor Scanner Bangladesh).
- **Sample Size**: $N = 50$ real-world claims.
- **Protocol**: 6-question decision tree protocol (`docs/annotation_guidelines.md`).

## 2. Label Distribution (Adjudicated Ground Truth)
- **REFUTED**: 23 (46.0%)
- **MISLEADING**: 18 (36.0%)
- **INSUFFICIENT_EVIDENCE**: 8 (16.0%)
- **SUPPORTED**: 1 (2.0%)
- **CONFLICTING**: 0 (0.0%)

## 3. Inter-Annotator Agreement (IAA) Metrics
- **Observed Agreement**: 94.00%
- **Cohen's Kappa ($\kappa$)**: 0.9055
- **Krippendorff's Alpha ($\alpha$)**: 0.9063
- **95% Bootstrap Confidence Interval**: $[0.7840, 1.0000]$ (2,000 resamples)

## 4. Key Adjudications & Disagreement Analysis
- `REAL-002` (*Protest framing*): Adjudicated to `MISLEADING` because the video depicts genuine protest activity, but its ideological attribution was falsely asserted.
- `REAL-011` (*Casualty count*): Adjudicated to `MISLEADING` because the traffic collision occurred, but the casualty scale was inflated from 1 to 2.
- `REAL-015` (*Circular debunk*): Adjudicated to `REFUTED` following direct verification with the issuing body confirming non-issuance.
