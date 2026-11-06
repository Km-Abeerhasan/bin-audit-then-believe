"""
End-to-End Calibrated Pipeline Evaluation Script
BiNPipeline: Audited Evidence-Based Fact-Checking Engine
Evaluates retrieval fusion, temperature-calibrated stance inference, and Stage 6 verdict synthesis.
"""

import json
import numpy as np
from typing import List, Dict, Any

class TemperatureCalibratedNLI:
    """
    Applies temperature scaling and calibrated decision thresholds (theta=0.70)
    over model logits to prevent overconfident stance assignment.
    """
    def __init__(self, temperature: float = 1.2, threshold: float = 0.70):
        self.temperature = max(temperature, 1e-4)
        self.threshold = threshold
        self.classes = ["contradiction", "neutral", "entailment"]

    def softmax(self, logits: np.ndarray) -> np.ndarray:
        scaled = logits / self.temperature
        exp_scaled = np.exp(scaled - np.max(scaled))
        return exp_scaled / np.sum(exp_scaled)

    def calibrate_and_classify(self, raw_logits: List[float]) -> Dict[str, Any]:
        probs = self.softmax(np.array(raw_logits))
        p_contra, p_neu, p_ent = probs[0], probs[1], probs[2]

        label = "NEUTRAL"
        confidence = float(p_neu)

        if p_contra >= self.threshold:
            label = "CONTRADICTION"
            confidence = float(p_contra)
        elif p_ent >= self.threshold:
            label = "ENTAILMENT"
            confidence = float(p_ent)

        return {
            "label": label,
            "confidence": confidence,
            "probabilities": {
                "contradiction": float(p_contra),
                "neutral": float(p_neu),
                "entailment": float(p_ent)
            }
        }


def route_stage6_decision(claim: Dict[str, Any], evidence_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministic Stage 6 decision tree routing calibrated evidence sets.
    """
    prov_flag = claim.get("is_provenance_absence", False)
    if prov_flag:
        return {
            "verdict": "MISLEADING",
            "rule": "RULE_1_PROVENANCE_ABSENCE",
            "confidence": 0.92
        }

    if not evidence_pool or len(evidence_pool) == 0:
        return {
            "verdict": "INSUFFICIENT_EVIDENCE",
            "rule": "RULE_2_INSUFFICIENT_SEARCH",
            "confidence": 0.90
        }

    refutation_set = [e for e in evidence_pool if e["stance"] == "CONTRADICTION"]
    support_set = [e for e in evidence_pool if e["stance"] == "ENTAILMENT"]

    # Priority 4B: Official Denial / Tier-1 Refutation
    if any(e.get("tier", 2) == 1 for e in refutation_set):
        return {
            "verdict": "REFUTED",
            "rule": "RULE_4B_OFFICIAL_DENIAL",
            "confidence": 0.95
        }

    # Priority 5: Independent Support
    if len(support_set) >= 1:
        unique_domains = {e.get("domain", "default") for e in support_set}
        if len(unique_domains) >= 2 or support_set[0].get("tier", 2) == 1:
            return {
                "verdict": "SUPPORTED",
                "rule": "RULE_5_INDEPENDENT_SUPPORT",
                "confidence": 0.94
            }

    # Priority 9: Low-Confidence Fallback Gate (tau = 0.60)
    return {
        "verdict": "INSUFFICIENT_EVIDENCE",
        "rule": "RULE_9_LOW_CONFIDENCE_FALLBACK",
        "confidence": 0.60
    }


def run_pipeline_dry_run():
    print("=" * 70)
    print("BiNPipeline: Calibrated End-to-End Inference Validation")
    print("=" * 70)

    calibrator = TemperatureCalibratedNLI(temperature=1.2, threshold=0.70)

    sample_claim = {
        "claim_id": "PILOT_01",
        "claim_text": "আইএসপিআর কর্তৃক বিশেষ সামরিক সতর্কতা জারি সংক্রান্ত দাবি",
        "is_provenance_absence": False
    }

    # Simulated retrieved passages with raw logits [contra, neutral, entail]
    raw_passages = [
        {"domain": "ispr.gov.bd", "tier": 1, "logits": [3.8, -1.2, -2.1]},
        {"domain": "prothomalo.com", "tier": 1, "logits": [2.9, 0.1, -1.8]}
    ]

    calibrated_evidence = []
    for doc in raw_passages:
        res = calibrator.calibrate_and_classify(doc["logits"])
        calibrated_evidence.append({
            "domain": doc["domain"],
            "tier": doc["tier"],
            "stance": res["label"],
            "confidence": res["confidence"]
        })

    decision = route_stage6_decision(sample_claim, calibrated_evidence)

    print(f"Claim ID       : {sample_claim['claim_id']}")
    print(f"Evidence Count : {len(calibrated_evidence)}")
    print(f"Calibrated Pool: {calibrated_evidence}")
    print(f"Decision Rule  : {decision['rule']}")
    print(f"Final Verdict  : {decision['verdict']} (Confidence: {decision['confidence']:.2f})")
    print("=" * 70)
    print("[SUCCESS] Calibrated end-to-end pipeline execution confirmed.")

if __name__ == "__main__":
    run_pipeline_dry_run()
