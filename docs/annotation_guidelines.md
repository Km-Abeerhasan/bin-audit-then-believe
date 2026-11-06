# BiN Pilot Annotation Guidelines (v0.1, draft)

Goal: build ~50 REAL claims from published fact-checks, labeled independently by two people.
Freeze these guidelines only after the pilot. Expect to revise them.

## 1. Sampling
- Source: Rumor Scanner, BOOM Bangladesh (check each site's terms first). Record URL and date.
- Domain: Bangladesh public information and safety.
- Take claims in the order you find them within a date range. Do NOT force equal class counts.
  Report the true distribution. Make sure each class appears at least a few times if possible.
- Skip claims whose fact-check you cannot open or read.

## 2. What to record for each claim (see pilot_template.csv)
- `claim_text`: the claim exactly as the fact-checker quotes it (Bengali, unedited).
- `claim_date`: when the claim was posted/circulated, if known. Leave empty if unknown. Do not guess.
- `claim_type`: factual | prediction | opinion | satire.
  Opinion and satire are not verified: leave `label` empty and set `status` = NON_FACTUAL.
  Predictions ARE verified, "as of" the evidence date.
- `fact_check_url`, `fact_check_publisher`, `fact_check_date`.
- `source_rating`: the fact-checker's own rating word, copied verbatim.
- `gold_evidence_urls`: sources the fact-checker cites (semicolon separated).
- `gold_evidence_retrievable`: Y / N / PARTIAL. N if cited sources are social posts, offline documents, or paywalled.
- `is_provenance`: Y if the claim says an authority issued something ("BWDB issued this notice").
- `safety_critical`: Y for floods, evacuation, health emergencies, disasters. Otherwise N.

## 3. Label decision tree (annotator picks ONE)
Work through the questions in order. Stop at the first YES.

1. Is the claim opinion or satire? -> status NON_FACTUAL, no label.
2. Do the cited sources support some parts of the claim and contradict others, or is a number,
   date, scale, or attribution distorted while the underlying event is real? -> MISLEADING
3. Do credible, independent sources support materially incompatible conclusions about the same event and date?
   -> CONFLICTING
4. Do the sources clearly show the claim is false? -> REFUTED
5. Do the sources clearly show the claim is true? -> SUPPORTED
6. Otherwise, the available evidence cannot settle it -> INSUFFICIENT_EVIDENCE

Rules:
- Label from the EVIDENCE the fact-check presents, not from the headline alone.
- "No record found" for an alleged official notice: if the fact-checker confirmed with the issuing body
  that it never issued it, label MISLEADING (false attribution) and add a note. If nobody checked, INSUFFICIENT_EVIDENCE.
- INSUFFICIENT_EVIDENCE means evidence is lacking, not that the claim sounds absurd.
  Absurd claims that the fact-checker rejects with evidence are REFUTED.
- Do not use outside knowledge. If you are unsure between two labels, pick the one the decision tree reaches first and write `notes`.
- `confidence`: 1 (guess) to 3 (certain).

## 4. Independent annotation protocol
- Annotator A and B work separately. Do not discuss labels until both files are saved.
- Annotator B should label from the fact-check article without looking at `source_rating` mapped labels from A.
- Save as `annotator_A.csv` and `annotator_B.csv` with identical `claim_id` values.
- Run `python3 eval/iaa.py --a annotation/pilot/annotator_A.csv --b annotation/pilot/annotator_B.csv`.
- Read the disagreement list, discuss each, and record the adjudicated label in `adjudicated.csv`.
  Update the decision tree where the same confusion repeats.

## 5. What to report in the thesis
- Class counts, Cohen's kappa, Krippendorff's alpha with a bootstrap CI, per-class agreement, confusion matrix.
- With 50 items the CI will be wide. That is expected. Do not claim "perfect agreement" from a small pilot.
- Fraction of claims with retrievable gold evidence. This decides whether H1 is feasible.
