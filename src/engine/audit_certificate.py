#!/usr/bin/env python3
"""
BiNPipeline: Cryptographic Fact-Check Dossier Generator
Author: Khan Muhammad Abeer Hasan (Jahangirnagar University)
Paper: BiN_Audit_Then_Believe
Conforms to:
- W3C Semantic Web Standards
- Schema.org ClaimReview JSON-LD Specification
- NIST SHA-256 Tamper-Evident Digital Fingerprinting
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

def compute_sha256_digest(data: Dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 hash over canonical JSON bytes."""
    canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(canonical_json).hexdigest()

class AuditCertificateEngine:
    def __init__(self, registry_path: str = "data/tier1_publishers.json"):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"publishers": {}}

    def generate_dossier(
        self,
        claim_id: str,
        claim_text: str,
        claim_author: Optional[str],
        verdict: str,
        confidence: float,
        gate_triggered: str,
        rationale: str,
        supporting_evidence: List[Dict[str, Any]],
        abstention_status: bool = False
    ) -> Dict[str, Any]:
        """
        Generates a W3C Schema.org compliant ClaimReview certificate 
        anchored with a cryptographic SHA-256 tamper-evident fingerprint.
        """
        now_utc = datetime.now(timezone.utc).isoformat()
        
        immutable_payload = {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "verdict": verdict,
            "confidence": round(confidence, 4),
            "gate_triggered": gate_triggered,
            "rationale": rationale,
            "evidence_count": len(supporting_evidence),
            "abstention_status": abstention_status,
            "timestamp": now_utc
        }
        
        digital_fingerprint = compute_sha256_digest(immutable_payload)
        
        claim_review = {
            "@context": "https://schema.org",
            "@type": "ClaimReview",
            "url": f"https://github.com/Km-Abeerhasan/bin-audit-then-believe/audit/{digital_fingerprint[:16]}",
            "datePublished": now_utc,
            "claimReviewed": claim_text,
            "itemReviewed": {
                "@type": "CreativeWork",
                "author": {
                    "@type": "Person" if claim_author else "Organization",
                    "name": claim_author if claim_author else "Unknown Social Media Post"
                },
                "datePublished": now_utc
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": verdict,
                "bestRating": "SUPPORTED",
                "worstRating": "REFUTED",
                "alternateName": gate_triggered,
                "ratingExplanation": rationale
            },
            "auditMetadata": {
                "algorithm": "BiNPipeline-Stage6-DeterministicEngine",
                "confidence_score": round(confidence, 4),
                "cryptographic_fingerprint_sha256": digital_fingerprint,
                "verification_status": "CERTIFIED_AUDITABLE",
                "registry_referenced": os.path.basename(self.registry_path)
            },
            "evidentiaryTrace": supporting_evidence
        }
        return claim_review

    def export_certificate(self, dossier: Dict[str, Any], output_path: str):
        """Exports the certificate as formatted JSON-LD."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dossier, f, indent=2, ensure_ascii=False)
        print(f"[✓] Tamper-evident Audit Certificate saved to: {output_path}")
        print(f"    SHA-256 Fingerprint: {dossier['auditMetadata']['cryptographic_fingerprint_sha256']}")

if __name__ == "__main__":
    engine = AuditCertificateEngine()
    sample_dossier = engine.generate_dossier(
        claim_id="CLM-042",
        claim_text="বাংলাদেশ ব্যাংকের ৫০০০ টাকার নতুন নোট ইস্যু করা হয়েছে।",
        claim_author="Viral Facebook Post",
        verdict="REFUTED",
        confidence=0.97,
        gate_triggered="RULE_4B_OFFICIAL_DENIAL",
        rationale="Bangladesh Bank issued a formal press circular refuting the issuance of a 5000-taka note.",
        supporting_evidence=[
            {"source": "pressinform.gov.bd", "tier": 1, "stance": "Contradiction", "score": 0.96}
        ]
    )
    engine.export_certificate(sample_dossier, "eval/results/sample_claim_review.json")
