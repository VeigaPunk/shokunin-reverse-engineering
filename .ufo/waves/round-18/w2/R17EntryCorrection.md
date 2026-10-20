# W2 falsify — Round-18 correction in corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md

HOLDS

Seat: KaidokuR18.R17EntryCorrection (author-side advisory, falsify). REV = b2aad08ceeee8dd125ce0d316056d8bd766c7f94 (= lane HEAD, worktree clean for the target file). Baseline = 9011581d84527ba34c675f9cf912e54d2e72d470. All commands run read-only on the lane; writes confined to /tmp and this report. No installs performed (none needed). Axes: calibration (each correction line true), operability (reproducing commands), depth (byte/blob/commit-graph checks).

## 1. "filed bytes 1-198 unchanged vs 9011581" — HOLDS (stronger: entire prefix)

[Observation] Baseline (15552 bytes, 198 lines) is a strict byte-prefix of REV (17469 bytes, 206 lines); the appended block is lines 199-206.

```
$ cmp /tmp/r17diag_base.md /tmp/r17diag_rev.md
cmp: EOF on /tmp/r17diag_base.md after byte 15552   # exit 0 via pipe; no differing byte before EOF
$ head -c 198 /tmp/r17diag_rev.md | sha256sum; head -c 198 /tmp/r17diag_base.md | sha256sum
fd79691ad253cb15de57ddf8b5d7e80bdaf590b35c7fac6c1e35d3db3071e5cf  (both)   # exit 0
$ cmp corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md /tmp/r17diag_rev.md && echo worktree==REV
worktree==REV   # exit 0
```
(tmp files from `git show {9011581,b2aad08…}:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`.)

## 2. Correction line 204 (R17-PINMAP: verdict-not-map; 29 checks) — HOLDS

- [Observation] Quoted original text is at exactly `2026-10-20-r17-go-carrier-diagnostics.md:30-32`: "each pin map is retained with its UTC instant: pre, every 30 s during / analyze (2–8 checks per run, `steps.analyze.pin_checks`), and post. All / maps are equal." Line 3 is the `recheck:` line containing "exit 0 = digests, pins, log binding and mid-run checks consistent" (lines 1-198 byte-identical to baseline, so anchors hold at both revisions).
- [Observation] Producer code citation exact: `git show 9011581:.ufo/waves/round-17/tools/carrier-run.py` (blob f91bbc76) lines 479-487 are `mid = pins.snapshot(...)` / `cmp_mid = pins.compare(...)` / the `pin_checks` append writing exactly `{taken_at_utc, equal, entries, changed, missing}` — no map payload.
- [Observation] Receipt scan over `.ufo/waves/round-17/runs/*/receipt.json` at REV (byte-identical to `d0ab299` for all 8 receipts — per-label `git rev-parse d0ab299:…/receipt.json` == `git hash-object` worktree, 8/8 SAME):

```
$ python3 -I -B (scan pin_checks)
total pin_checks entries: 29
keysets: {('changed','entries','equal','missing','taken_at_utc'): 29}
equal values: {True: 29}
per receipt: 4,2,3,2,4,4,2,8   # exit 0
```
- [Observation] "only the pre and post maps are retained": receipts embed `pins_pre`/`pins_post` (keys `entries, monotonic_ns, taken_at_utc`, 146 entries); `pre==post` for all 8 receipts (exit 0); no `pins/` directory exists in any round-17 run dir (`ls .ufo/waves/round-17/runs/*/pins/` → all "No such file or directory", exit 0); first-pass receipts at `da64646` have no `pin_checks` key at all (8/8, exit 0).

## 3. Correction line 205 (R17-PINMAP: validator overstated; r18 fix) — HOLDS, both halves reproduced

- [Observation] Old validator `9011581:.ufo/waves/round-17/tools/receipt-validate.py` (blob 2762496c) lines 187-191 test only `chk.get("equal") is True`; `entries` never validated.
- [Observation] Forged-entry acceptance at baseline, reproduced (forged entry `{"equal": true, "entries": 999}` appended to a copy of `pro-op/receipt.json` in /tmp):

```
$ python3 -I -B /tmp/forged/rv_old.py /tmp/forged/runs/pro-op/receipt.json   # rv_old.py = blob 2762496c, with blob 6568a493 pins.py beside it
"invalid": 0, "valid": 1, "findings": []   # old_forged_exit=0
```
(First attempt errored exit 2 "pins.py unavailable" — validator requires its sibling pins.py; retried with it. Control: genuine receipt also exit 0.)

- [Observation] Round-18 validator rejects the same forged receipt:

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/forged/runs/pro-op/receipt.json
findings: mid_map_missing ×9 + {"code":"mid_entries_mismatch","pins_pre_entries":146,"recorded":999}
# new_exit=1
```
- [Observation] Hardened producer at REV: `b2aad08:.ufo/waves/round-17/tools/carrier-run.py` (blob 37961db5) lines 371-372, 495-511 write `pins/mid-<n>.json` + `map_path`/`map_sha256`; validator (blob bf043886) contains `mid_entries_mismatch` (:485), `mid_map_sha256_mismatch` (:514), `mid_map_compare_mismatch` (:566), `mid_map_missing` (:495,:509), `--require-mid-maps` (:6,:33). End-to-end on a genuine round-18 receipt:

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1246-swiss-nethttp/receipt.json
"invalid": 0, "valid": 1, "findings": []   # r18_validate_exit=0; receipt carries map_path/map_sha256; pins/mid-1.json present
```
- [Observation] Cited w1 evidence exists: `.ufo/waves/round-18/w1/CriticDiscernment.md` documents the same finding (:39, :57 — forged receipt exit 0, findings [] at baseline).

## 4. Correction line 206 (R17-PRODUCER-REV: blobs and revision roles) — HOLDS

```
$ git rev-parse 271167473d87…:.ufo/waves/round-17/tools/carrier-run.py
bc964acdfb0751310ee014799627774c45469f38        # exit 0  → "blob bc964ac"
$ git rev-parse 95e34db62f26…:.ufo/waves/round-17/tools/carrier-run.py
c536e3e4bd0b3091efd43d01448326cec5a63cc8        # exit 0  → "blob c536e3e"
$ git rev-parse d0ab2992149…:.ufo/waves/round-17/tools/carrier-run.py
f91bbc76c73991ba5d74137ca69b115dcee7c12f        # exit 0  → ≠ c536e3e: d0ab299 is not the second-pass producer
$ git merge-base --is-ancestor 27116747… da64646… && echo yes; git merge-base --is-ancestor 95e34db6… d0ab299… && echo yes; git merge-base --is-ancestor d0ab299… b2aad08… && echo yes
yes / yes / yes                                  # exit 0
```
- [Observation] Time windows match after second truncation: first-pass receipt instants at `da64646` span `2026-10-20T13:47:05.97Z` (pins_pre, calib-shfmt) to `14:00:05.29Z` (pins_post, pro-op) — claim "13:47:05–14:00:05Z"; second-pass at `d0ab299` span `14:27:41.94Z` to `14:40:02.31Z` — claim "14:27:41–14:40:02Z" (exit 0). Receipts byte-identical between d0ab299 and REV (8/8).
- [Observation] `d0ab299` (14:47:24Z) postdates the second pass (last pins_post 14:40:02Z); its carrier-run.py blob f91bbc76 matches the 9011581 integrated blob, not the producing c536e3e — "verification revision, not a producer" confirmed. Routing source verified: `corpus/lessons/round-17-verifier-spotcheck.md:137-139` = R17-PINMAP / R17-VALIDATE16 / R17-PRODUCER-REV; w1 reports exist at `.ufo/waves/round-18/w1/` (`CriticDiscernment.md`, `RevProducerRev.md`).

## Findings by severity

None — no defect found. Every tested sentence in the correction block is true at REV.

## Residual risk and verification gaps

- [Observation, no defect] Header (line 200) cites routing `round-17-verifier-spotcheck.md:137-139`, whose range also contains R17-VALIDATE16 (:138); this entry corrects only PINMAP and PRODUCER-REV. "Routed by" is attribution, not a discharge claim — no false statement, but a reader could over-infer coverage. VALIDATE16's correction must live elsewhere (SCORECARD/round-17.md, not falsified here).
- [Observation, no defect] "From round 18 `carrier-run.py` writes…" — the hardened tool is the in-place update of `.ufo/waves/round-17/tools/carrier-run.py` (blob 37961db5 at REV); `.ufo/waves/round-18/tools/` contains no carrier-run.py. Substance true; path implicit.
- [Inference] The claim "filed bytes 1-198 unchanged" is trivially subsumed: all 15552 bytes (lines 1-198) are unchanged. Read charitably as lines, it holds exactly.
- Gaps: my forged-entry fixture uses `entries:999` (CriticDiscernment §5 used `entries:7` plus other mutations) — same defect class, independently reproduced. I validated one representative round-18 receipt (s1246-swiss-nethttp) rather than all 15. No REA/Ghidra runs and no carrier execution (lane bounds); historical receipts accepted as Git objects without re-running producers.

Report: .ufo/waves/round-18/w2/R17EntryCorrection.md
