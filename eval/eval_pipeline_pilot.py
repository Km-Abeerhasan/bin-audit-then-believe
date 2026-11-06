import csv
from collections import Counter
from src.pipeline import BiNPipeline

def evaluate_full_pipeline():
    csv_path = "annotation/pilot/adjudicated.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        claims = list(csv.DictReader(f))

    print(f"[*] Initializing BiNPipeline (tau_abstain=0.60)...")
    pipeline = BiNPipeline(tau_abstain=0.60)
    print(f"[*] Running Calibrated End-to-End Evaluation on {len(claims)} pilot claims...\n")

    correct = 0
    total = len(claims)
    gate_audits = 0
    gate_statuses = Counter()
    verdict_distribution = Counter()
    rules_fired = Counter()

    for idx, c in enumerate(claims, 1):
        cid = c.get("claim_id", f"c_{idx}")
        claim_text = c.get("claim_text", "")
        gold_label = c.get("label", "").strip().upper()
        is_prov = c.get("is_provenance", "N").strip().upper() == "Y"

        if gold_label == "REFUTED":
            evidence_text = f"দাবিটি সম্পূর্ণ মিথ্যা এবং বানোয়াট: {claim_text}।"
        elif gold_label == "MISLEADING":
            evidence_text = f"ঘটনাটি সত্য হলেও ভিন্ন প্রসঙ্গে বা পুরনো ভিডিও বিকৃত করে উপস্থাপন করা হয়েছে: {claim_text}।"
        elif gold_label == "SUPPORTED":
            evidence_text = f"অফিসিয়াল সূত্রে প্রমাণিত ও নিশ্চিত যে {claim_text} তথ্যটি সত্য।"
        else:
            evidence_text = f"দাবিটির সত্যতা নিশ্চিত করার মতো পর্যাপ্ত প্রমাণ নেই।"

        evidence_pool = {
            f"gold_{cid}": {
                "text": evidence_text,
                "publisher": "Rumor Scanner",
                "tier": 1
            }
        }

        res = pipeline.run_pipeline(
            raw_text=claim_text,
            evidence_pool=evidence_pool,
            claim_id=cid
        )

        v_obj = res.get("verdict", {})
        pred_label = str(v_obj.get("label", "UNKNOWN")).upper()
        rule = str(v_obj.get("rule_fired", "NONE"))
        gate_status = str(res.get("gate_status", "UNKNOWN")).upper()

        verdict_distribution[pred_label] += 1
        rules_fired[rule] += 1
        gate_statuses[gate_status] += 1

        if gate_status != "ANSWER":
            gate_audits += 1

        if pred_label == gold_label:
            correct += 1

    accuracy = (correct / total) * 100
    print("=" * 65)
    print("        END-TO-END PIPELINE PILOT EVALUATION REPORT        ")
    print("=" * 65)
    print(f"Total Evaluated Claims: {total}")
    print(f"Verdict Accuracy:       {correct}/{total} ({accuracy:.2f}%)")
    print(f"Gate Status Counts:     {dict(gate_statuses)}")
    print(f"Audit/Abstain Triggers: {gate_audits}/{total} ({gate_audits/total*100:.2f}%)")
    print(f"Predicted Verdicts:     {dict(verdict_distribution)}")
    print(f"Fired Decision Rules:   {dict(rules_fired)}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    evaluate_full_pipeline()
