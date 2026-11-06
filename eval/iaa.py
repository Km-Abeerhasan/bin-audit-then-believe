import argparse
import csv
import random
from collections import Counter

LABELS = ["SUPPORTED", "REFUTED", "MISLEADING", "CONFLICTING", "INSUFFICIENT_EVIDENCE"]

def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {r["claim_id"].strip(): r["label"].strip().upper() for r in csv.DictReader(f) if "claim_id" in r and "label" in r}

def compute_cohens_kappa(a, b=None):
    if b is None and isinstance(a, list):
        if len(a) > 0 and isinstance(a[0], (list, tuple)) and len(a[0]) == 2:
            a, b = [row[0] for row in a], [row[1] for row in a]
        elif len(a) == 2:
            a, b = a[0], a[1]
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(a) | set(b)) / (n * n)
    if pe == 1:
        return 1.0 if po == 1 else float("nan")
    return (po - pe) / (1 - pe)

cohen_kappa = compute_cohens_kappa

def compute_krippendorff_alpha_nominal(a, b=None):
    if b is None and isinstance(a, list):
        if len(a) > 0 and isinstance(a[0], (list, tuple)) and len(a[0]) == 2:
            a, b = [row[0] for row in a], [row[1] for row in a]
        elif len(a) == 2:
            a, b = a[0], a[1]
    o = Counter()
    for x, y in zip(a, b):
        o[(x, y)] += 1
        o[(y, x)] += 1
    nc = Counter()
    for (c, _k), v in o.items():
        nc[c] += v
    n = sum(nc.values())
    if n == 0:
        return float("nan")
    d_o = sum(v for (c, k), v in o.items() if c != k)
    d_e = sum(nc[c] * nc[k] for c in nc for k in nc if c != k)
    if d_e == 0:
        return 1.0 if d_o == 0 else float("nan")
    return 1 - (n - 1) * d_o / d_e

krippendorff_alpha_nominal = compute_krippendorff_alpha_nominal

def bootstrap_ci(a, b, fn=None, reps=2000, seed=0):
    if fn is None:
        fn = compute_krippendorff_alpha_nominal
    rng = random.Random(seed)
    n = len(a)
    vals = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        v = fn([a[i] for i in idx], [b[i] for i in idx])
        if v == v:
            vals.append(v)
    vals.sort()
    if not vals:
        return (float("nan"), float("nan"))
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    args = p.parse_args()

    A, B = load(args.a), load(args.b)
    ids = sorted(set(A) & set(B))
    missing = sorted(set(A) ^ set(B))
    ids_l = [i for i in ids if A[i] and B[i]]
    skipped = [i for i in ids if not (A[i] and B[i])]
    a = [A[i] for i in ids_l]
    b = [B[i] for i in ids_l]
    n = len(a)
    if n == 0:
        raise SystemExit("No overlapping labeled claims found.")

    agree = sum(x == y for x, y in zip(a, b)) / n
    kappa = compute_cohens_kappa(a, b)
    alpha = compute_krippendorff_alpha_nominal(a, b)
    lo, hi = bootstrap_ci(a, b, compute_krippendorff_alpha_nominal)

    print(f"\nClaims compared: {n} | Skipped: {len(skipped)} | ID mismatch: {len(missing)}")
    print(f"Observed Agreement: {agree*100:.2f}%")
    print(f"Cohen's Kappa (κ):  {kappa:.4f}")
    print(f"Krippendorff's α:   {alpha:.4f} (95% CI: [{lo:.4f}, {hi:.4f}])\n")

if __name__ == "__main__":
    main()
