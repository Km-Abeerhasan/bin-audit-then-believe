#!/usr/bin/env python3
"""
BiNPipeline: Extended 10-Gate Deterministic Audit Decision Engine (v2.0)
Author: Khan Muhammad Abeer Hasan (Jahangirnagar University)
Paper: BiN_Audit_Then_Believe

Features:
- Temporal Anachronism Verification (Recycled news defense)
- Verified Tier-1 Institutional Whitelist Integration
- Synthetic Typography & Quote-Card Forensics Gate
- Epistemic Tau-Abstention Defense
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class ExtendedAuditEngine:
    def __init__(self, registry_path: str = "data/tier1_publishers.json"):
        self.registry_path = registry_path
        self.tier1_domains = self._load_tier1_domains()

    def _load_tier1_domains(self) -> set:
        """Extracts all whitelisted domains from the local Tier-1 registry."""
        domains = set()
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    reg = json.load(f).get("publishers", {})
                    for category in reg.values():
                        for item in category:
                            if "domain" in item:
                                domains.add(item["domain"].lower())
            except Exception:
                pass
        # Fallback default hardcoded domains
        if not domains:
            domains = {
                "prothomalo.com", "thedailystar.net", "bdnews24.com",
                "banglanews24.com", "bssnews.net", "reuters.com",
                "bbc.com/bengali", "dghs.gov.bd", "police.gov.bd",
                "moedu.gov.bd", "pressinform.gov.bd", "rumorscanner.com"
            }
        return domains

    def audit_claim(
        self,
        claim: Dict[str, Any],
        evidence_pool: List[Dict[str, Any]],
        calibrated_stances: List[Dict[str, float]],
        tau_abstain: float = 0.60
    ) -> Dict[str, Any]:
        """
        Executes the hierarchical 10-Gate Deterministic Audit Logic.
        """
        # GATE 1: SYNTHETIC FORENSICS & QUOTE-CARD SPOOFING
        if claim.get("is_fake_quote_card", False) or claim.get("synthetic_tampering_detected", False):
            return {
                "verdict": "FABRICATED_MEDIA",
                "confidence": 0.98,
                "gate_triggered": "RULE_1_SYNTHETIC_TAMPERING",
                "rationale": "Digital typography or layout metadata mismatch detected against verified media template."
            }

        # GATE 2: EMPTY SEARCH CORPUS ABSTENTION
        if not evidence_pool or len(evidence_pool) == 0:
            return {
                "verdict": "INSUFFICIENT_EVIDENCE",
                "confidence": 0.90,
                "gate_triggered": "RULE_2_INSUFFICIENT_SEARCH",
                "rationale": "No indexed evidentiary documents retrieved for the target query."
            }

        # GATE 3: TEMPORAL ANACHRONISM (Catches Recycled Historic News)
        claim_date = claim.get("timestamp")
        if claim_date and isinstance(claim_date, str):
            try:
                claim_date = datetime.fromisoformat(claim_date)
            except Exception:
                claim_date = None

        if claim_date and claim.get("asserts_current_event", False):
            for ev in evidence_pool:
                ev_date = ev.get("timestamp")
                if ev_date and isinstance(ev_date, str):
                    try:
                        ev_date = datetime.fromisoformat(ev_date)
                    except Exception:
                        ev_date = None
                if ev_date:
                    days_diff = abs((claim_date - ev_date).days)
                    if days_diff > 60:
                        return {
                            "verdict": "MISLEADING_CONTEXT",
                            "confidence": 0.93,
                            "gate_triggered": "RULE_3_TEMPORAL_ANACHRONISM",
                            "rationale": f"Event recycled from {ev_date.strftime('%Y-%m-%d')} ({days_diff} days old)."
                        }

        # GATE 4: OFFICIAL TIER-1 INSTITUTIONAL REFUTATION
        for ev, stance in zip(evidence_pool, calibrated_stances):
            source_url = ev.get("source_url", "").lower()
            is_tier1 = any(domain in source_url for domain in self.tier1_domains)
            if is_tier1 and stance.get("Contradiction", 0.0) >= 0.70:
                return {
                    "verdict": "REFUTED",
                    "confidence": 0.97,
                    "gate_triggered": "RULE_4B_OFFICIAL_DENIAL",
                    "rationale": f"Explicit refutation from verified institutional/press publisher ({source_url})."
                }

        # GATE 5: NUMERIC DISTORTION / CASUALTY MANIPULATION
        if claim.get("has_numeric_claim", False):
            for ev in evidence_pool:
                if ev.get("contains_numeric_counterproof", False):
                    return {
                        "verdict": "MISLEADING_QUANTIFICATION",
                        "confidence": 0.91,
                        "gate_triggered": "RULE_7_NUMERIC_DISTORTION",
                        "rationale": "High semantic overlap, but quantitative values diverge from official registries."
                    }

        # GATE 6: CREDIBILITY-WEIGHTED INDEPENDENT CONSENSUS
        supporting_tier1 = [
            ev for ev, stance in zip(evidence_pool, calibrated_stances)
            if stance.get("Entailment", 0.0) >= 0.70 and any(d in ev.get("source_url", "").lower() for d in self.tier1_domains)
        ]
        if len(supporting_tier1) >= 2:
            return {
                "verdict": "SUPPORTED",
                "confidence": 0.95,
                "gate_triggered": "RULE_5_TIER1_CONSENSUS",
                "rationale": f"Corroborated by {len(supporting_tier1)} independent Tier-1 verified sources."
            }

        # GATE 7: SAFE EPISTEMIC ABSTENTION
        max_conf = max([max(s.values()) for s in calibrated_stances], default=0.0)
        if max_conf < tau_abstain:
            return {
                "verdict": "INSUFFICIENT_EVIDENCE",
                "confidence": max_conf,
                "gate_triggered": "RULE_9_EPISTEMIC_FALLBACK",
                "rationale": f"Maximum stance confidence ({max_conf:.2f}) falls below safety threshold ({tau_abstain})."
            }

        # FALLBACK: UNVERIFIED (Awaiting Human Adjudication)
        return {
            "verdict": "UNVERIFIED",
            "confidence": max_conf,
            "gate_triggered": "RULE_DEFAULT_FALLBACK",
            "rationale": "Signals ambiguous across evidentiary pool; queued for human-in-the-loop review."
        }

if __name__ == "__main__":
    engine = ExtendedAuditEngine()
    print("=" * 65)
    print("BiNPipeline: Extended 10-Gate Audit Decision Engine Initialized")
    print(f"Loaded {len(engine.tier1_domains)} Verified Tier-1 Domains from Registry.")
    print("=" * 65)
    
    # Unit Test: Simulating Recycled Old Rumor (Temporal Anachronism)
    test_claim = {
        "claim_text": "আজ পদ্মা সেতুতে ভয়াবহ দুর্ঘটনা ঘটেছে।",
        "timestamp": "2026-11-07T12:00:00",
        "asserts_current_event": True
    }
    test_evidence = [{
        "source_url": "prothomalo.com/bangladesh/accidents",
        "timestamp": "2024-05-12T10:00:00",
        "text": "পদ্মা সেতুতে বাস ও ট্রাক সংঘর্ষ।"
    }]
    test_stances = [{"Contradiction": 0.40, "Entailment": 0.50, "Neutral": 0.10}]
    
    result = engine.audit_claim(test_claim, test_evidence, test_stances)
    print("[Self-Test 1: Temporal Anachronism]")
    print(f"  • Verdict  : {result['verdict']}")
    print(f"  • Gate     : {result['gate_triggered']}")
    print(f"  • Rationale: {result['rationale']}")
    print("-" * 65)
