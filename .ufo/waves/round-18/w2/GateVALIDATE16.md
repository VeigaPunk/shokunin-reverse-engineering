# GateVALIDATE16 — falsification of routed-defects.py R17-VALIDATE16 (round-18 wave 2)

BROKEN

Axes: (1) closure integrity of the R17-VALIDATE16 gate under adversarial data-only commits, (2) attack cost (changed lines per successful attack), (3) calibration — what the checks actually verify vs. what C1 claims they verify.

All anchors are `git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:<path>` unless noted. Tool blob sha256 at REV: `034f5ead5af0bb1844f9d71c5460e9684b75f6550e820f8c2bf1d46e4de584b2` — never modified; every attack below is data-only. Clone: `mktemp -d` + `git clone --no-local` + `git remote remove origin` + `git checkout --detach b2aad08…` (exit 0 each).

## Baseline reproduction (observation)

```
python3 -I -B $KS/.ufo/waves/round-18/tools/routed-defects.py --root $KS --rev 9011581d84527ba34c675f9cf912e54d2e72d470   # exit 0, open_count 6
python3 -I -B $KS/.ufo/waves/round-18/tools/routed-defects.py --root $KS --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94   # exit 0, open_count 0
```
Matches claims.json C1 ("open 6 at 9011581 -> 0"). The defect (corpus/lessons/round-17-verifier-spotcheck.md:138): scorecard claimed "all 16 receipts exit 0" while only 8 validator runs were retained.

## Ground truth the gate must rest on (observation)

The 8 `receipt.json` blobs at `da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/runs/<label>/receipt.json` have **no `exit` key at all** (observed keys: bound_sessions, carrier, label, log_capture_limit, orig_argv, pins_compare, pins_post, pins_pre, python, rea_ghidra_env, retained_logs, session_dir_baseline, session_parent, session_parent_leftovers, steps, unbound_sessions). So the "k/8 exit 0" count exists only inside the round-18-authored `summary.json` — and the tool computes its truth fraction from that same self-authored file: `zero_exits = sum(... r.get("exit") == 0)` over `doc.get("receipts")` (tools/routed-defects.py:437-445). It never cross-checks any receipt blob at `da64646`.

## Findings

### F1 HIGH — the gate's substance is self-authored evidence; fabricating it closes without a fix and re-opens invisibly (observation)

`zero_exits` (routed-defects.py:437-445) and `labels` (:446-457) are read from `summary.json` at REV; the only cross-repo anchor is the run-dir *names* at da64646 (:446-452). Every evidentiary field — `exit`, `stdout_sha256`, `checks_performed`, `findings`, `validator_rev`, `remap` — is either unchecked or format-checked (:458-462). Attack C (cheapest close-without-fix, 19 added lines, zero validator work):

Commit `d50e67b` (parent `9011581d…`): adds fabricated `.ufo/waves/round-18/evidence/validate16/summary.json` (+15: 8 receipts `exit:0`, `stdout_sha256` all-zero, `checks_performed:0`, `validator_rev` = 40×`f` (nonexistent), `validator_sha256` all-zero) and appends one line each to SCORECARD.md/LOG.md:
`- R17-VALIDATE16: correction — the 8 da64646 receipts validate 8/8 exit 0 (retained in …summary.json).`

```
python3 -I -B <blob>routed-defects.py --root $KS --rev d50e67b…   # exit 0, open_count 5
# R17-VALIDATE16 open False named_open False substance_open False — all 7 checks True
# others still open: PINMAP, PRODUCER-REV, SUMS-RUNLOG, REGISTRY, S032-DIGEST
```
Note: running the in-tree tool at this rev fails (exit 2, file absent — the tool is round-18 content), so the blob from REV was used; the tool reads git objects of `--root` only, which is the canonical `--root LANE --rev REV` invocation. [INFERENCE] C1's per-defect "open at baseline" leg is therefore closable by fabrication; only cross-seat review of diff content would catch it.

Attack B (re-open while closed, on top of REV): commit `7cb6785` replaces the authentic summary (10 insertions, 78 deletions) with the same fabricated shape — the retained evidence (`stdout_sha256` per carrier, `validator_sha256` 618448…, remap provenance) is destroyed. Tool: exit 0, open_count 0, VALIDATE16 closed, `validator-sha256-pinned :: validator_sha256='000…0'`.

Reproduce: re-apply the diff of `7cb6785`/`d50e67b` in any clone, run the command above at that commit.

### F2 HIGH — the stated-count check is a substring test; a false fraction passes (observation)

The substance check requires a line containing `"R17-VALIDATE16"` and `f"{zero_exits}/8"` (routed-defects.py:477-483) via `_line_with`, whose test is `all(n in line for n in needles)` (:132-140) — plain substring. Attack A: commit `26f7222` (SCORECARD.md, 1 insertion/1 deletion), changing REV's correction line (SCORECARD.md:2439) "…validate 8/8 exit 0…" → "…validate **18/8** exit 0…". The stated fraction is now false — exactly the original defect's shape (misstated k/8) — yet:

```
python3 -I -B …routed-defects.py --root $KS --rev 26f7222…   # exit 0, open_count 0
# substance scorecard-states-true-count True (needle "8/8" matched inside "18/8")
```

### F3 MEDIUM — `validator-sha256-pinned` pins nothing (observation)

routed-defects.py:458-462 accepts any 64-hex string. Attacks B/C pass with all-zeros while `validator_rev` = `ffff…` (a nonexistent commit) and `checks_performed: 0`; the real pin at REV (`618448…`, summary.json) is never recomputed against anything.

### F4 What holds (observation, calibration)

- Named checks correctly reject boolean `exit` (:426-433 excludes `isinstance(exit, bool)`), non-8 receipt counts, and a wrong `rev` pin.
- `summary-labels-are-run-dirs` (:446-457) is tied to the immutable da64646 tree — labels cannot be padded or renamed.
- Absent paths keep the defect open (docstring :17-19); the gate fails closed on deletion.
- Baseline/delivered reproduction is exact (6 → 0).

## Verification gaps

- `--strict` (exit 1) and exit-2 paths were not exercised; only exit-0 runs observed.
- I did not re-run `receipt-validate.py` to audit the *authenticity* of REV's existing summary — out of scope: the finding is that the gate cannot distinguish authentic from fabricated, not that wave 1 fabricated.
- [INFERENCE] The self-authored-evidence pattern (substance trusting round-18-authored blobs) likely recurs in other routed defects' checks; only VALIDATE16 was in scope here.

## Residual risk

A data-only commit (≤19 lines, no tooling change, no carrier execution) flips this leg of C1 closed at baseline, or silently invalidates the retained evidence while the gate reports `open_count 0`. Any consumer of `routed-defects.py open_count` as a closure signal for R17-VALIDATE16 inherits that risk. Minimum hardening (not applied): recompute the fraction from `da64646:…/receipt.json`-derived evidence bound by digest in a blob the tool itself hashes, and make the fraction check token-boundary based.

Report: .ufo/waves/round-18/w2/GateVALIDATE16.md
