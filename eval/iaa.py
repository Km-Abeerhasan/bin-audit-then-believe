import argparse
import csv
import random
from collections import Counter

LABELS = ["SUPPORTED", "REFUTED", "MISLEADING", "CONFLICTING", "INSUFFICIENT_EVIDENCE"]

def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {r["claim_id"].strip(): r["label"].strip().upper() for r in csv.DictReader(f) if "claim_id" in r and "label" in r}

def cohen_kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(a) | set(b)) / (n * n)
    if pe == 1:
        return 1.0 if po == 1 else float("nan")
    return (po - pe) / (1 - pe)

def krippendorff_alpha_nominal(a, b):
    o = Counter()
    for x, y in zip(a, b):
        o[(x, y)] += 1
        o[(y, x)] += 1
    nc = Counter()
    for (c, _k), v in o.items():
        nc[c] += v
    n = sum(nc.values())
    d_o = sum(v for (c, k), v in o.items() if c != k)
    d_e = sum(nc[c] * nc[k] for c in nc for k in nc if c != k)
    if d_e == 0:
        return 1.0 if d_o == 0 else float("nan")
    return 1 - (n - 1) * d_o / d_e

def bootstrap_ci(a, b, fn, reps=2000, seed=0):
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

    bad = sorted({x for x in a + b if x not in LABELS})
    if bad:
        print(f"WARNING: unknown labels (check spelling): {bad}")

    agree = sum(x == y for x, y in zip(a, b)) / n
    kappa = cohen_kappa(a, b)
    alpha = krippendorff_alpha_nominal(a, b)
    lo, hi = bootstrap_ci(a, b, krippendorff_alpha_nominal)

    print(f"\n=======================================================")
    print(f"         PILOT INTER-ANNOTATOR AGREEMENT REPORT        ")
    print(f"=======================================================")
    print(f"Claims compared:     {n} | Skipped: {len(skipped)} | ID mismatch: {len(missing)}")
    print(f"Observed Agreement:  {agree*100:.2f}%")
    print(f"Cohen's Kappa (κ):   {kappa:.4f}")
    print(f"Krippendorff's α:    {alpha:.4f} (95% Bootstrap CI: [{lo:.4f}, {hi:.4f}])")

    print("\nPer-class specific agreement (2*both / (countA + countB)):")
    ca, cb = Counter(a), Counter(b)
    for c in LABELS:
        both = sum(1 for x, y in zip(a, b) if x == c and y == c)
        tot = ca[c] + cb[c]
        s = f"{2 * both / tot:.3f}" if tot else "n/a"
        print(f"  {c:<22} A={ca[c]:>3} B={cb[c]:>3}  agreement={s}")

    print("\nConfusion Matrix (Rows: Annotator A, Cols: Annotator B):")
    print(" " * 24 + " ".join(f"{c[:5]:>6}" for c in LABELS))
    for r in LABELS:
        row = [sum(1 for x, y in zip(a, b) if x == r and y == c) for c in LABELS]
        print(f"  {r:<22}" + " ".join(f"{v:>6}" for v in row))

    disagreements = [(i, x, y) for i, x, y in zip(ids_l, a, b) if x != y]
    print(f"\nDisagreements to adjudicate ({len(disagreements)}):")
    for i, x, y in disagreements:
        print(f"  • {i}: Annotator_A={x} | Annotator_B={y}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
