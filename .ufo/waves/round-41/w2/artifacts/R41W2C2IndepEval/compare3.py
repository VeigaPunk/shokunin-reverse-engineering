#!/usr/bin/env python3
"""Compare third_eval.py against frozen C2 counter outputs.

Reference rows come from the committed C2 score receipt
  .ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json
  - carriers[].expected_label/expected_action = frozen evaluator output
  - carriers[].label/action = frozen interpreter output
  - real_receipts.rows.{L1,L2,V1,V2} = both, on round-40 receipts
No evaluator/interpreter source is read.
"""
import json
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
HELDOUT = LANE + "/corpus/evidence/round-41/c2/heldout"
R40 = LANE + "/corpus/evidence/round-40/c1"
SCORE = LANE + "/.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json"
EVAL = LANE + "/.ufo/waves/round-41/w2/artifacts/R41W2C2IndepEval/third_eval.py"

ids = [f"H{i:02d}" for i in range(1, 41)] + [f"C{i:02d}" for i in range(1, 13)]
paths = {i: f"{HELDOUT}/{i}/envelope.json" for i in ids}
r40 = {"V1": f"{R40}/V1/after.json", "V2": f"{R40}/V2/after.json",
       "L1": f"{R40}/L1/after.json", "L2": f"{R40}/L2/after.json"}
score = json.load(open(SCORE))
rows = {c["id"]: c for c in score["carriers"]}
rr = score["real_receipts"]["rows"]


def run_eval(input_paths):
    out = subprocess.run([sys.executable, "-I", "-B", EVAL] + input_paths,
                         capture_output=True, text=True, check=True)
    return [json.loads(line) for line in out.stdout.splitlines()]


def main():
    all_inputs = [paths[i] for i in ids] + [r40[k] for k in ("V1", "V2", "L1", "L2")]
    evaluated = run_eval(all_inputs)
    assert len(evaluated) == 56
    res = {entry["input"].split("/")[-2]: entry for entry in evaluated}
    table = []
    for i in ids:
        r, e = rows[i], res[i]
        table.append({
            "id": i, "class": r["class"], "row": r["row"],
            "mine": [e["label"], e["action"]], "step": e["step"],
            "evaluator": [r["expected_label"], r["expected_action"]],
            "interpreter": [r["label"], r["action"]],
            "mine_vs_evaluator": e["label"] == r["expected_label"] and e["action"] == r["expected_action"],
            "mine_vs_interpreter": e["label"] == r["label"] and e["action"] == r["action"],
            "evaluator_vs_interpreter": r["expected_label"] == r["label"] and r["expected_action"] == r["action"],
        })
    for k in ("V1", "V2", "L1", "L2"):
        r, e = rr[k], res[k]
        table.append({
            "id": k, "class": "round-40-C1", "row": None,
            "mine": [e["label"], e["action"]], "step": e["step"],
            "evaluator": r["evaluator"], "interpreter": r["interpreter"],
            "mine_vs_evaluator": [e["label"], e["action"]] == r["evaluator"],
            "mine_vs_interpreter": [e["label"], e["action"]] == r["interpreter"],
            "evaluator_vs_interpreter": r["evaluator"] == r["interpreter"],
        })
    return table


if __name__ == "__main__":
    t = main()
    json.dump(t, sys.stdout, indent=1)
    n = len(t)
    mve = sum(r["mine_vs_evaluator"] for r in t)
    mvi = sum(r["mine_vs_interpreter"] for r in t)
    evi = sum(r["evaluator_vs_interpreter"] for r in t)
    print(f"\n# rows={n} mine_vs_evaluator={mve} mine_vs_interpreter={mvi} evaluator_vs_interpreter={evi}", file=sys.stderr)
    dis = [r["id"] for r in t if not (r["mine_vs_evaluator"] and r["mine_vs_interpreter"])]
    print(f"# disagreements: {dis}", file=sys.stderr)
