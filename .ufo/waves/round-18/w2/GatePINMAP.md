# GatePINMAP — falsify probe of routed-defects.py R17-PINMAP (round 18 wave 2)

BROKEN — the R17-PINMAP "closed" verdict is not sound. A one-byte commit that
re-opens the routed defect (a retained mid-map no longer matches its
receipt-pinned sha256) leaves the gate reporting `open_count 0`, R17-PINMAP
closed, exit 0.

- Lane REV under attack: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (all
  `path:line` anchors below are from `git show REV:path` at that rev).
- Workspace: `git clone --no-local --no-hardlinks` into
  `/tmp/kpinmap.P1GNli/lane`, origin remote removed, detached at REV. The real
  lane was never written except this report file.
- No tools installed or updated; pacman untouched.
- Axes worked: calibration (does "closed" mean the defect is fixed?), depth
  (how much corruption one green check absorbs), operability (cost of attack).

## Root cause (observation, code anchors at REV)

`.ufo/waves/round-18/tools/routed-defects.py`, `_pinmaps_retained_check`:

- `routed-defects.py:340-342` — `checks_list = _pin_checks_of(doc)`; an empty
  `pin_checks` list is rejected (`if not checks_list:` → failure). Credit: the
  vacuous-receipt hole is closed (probe B confirms).
- `routed-defects.py:354-362` — every entry of the qualifying receipt's
  `pin_checks` is resolved via `_map_candidates` (`:294-310`; absolute paths
  are re-rooted through the `.ufo/` suffix slice at `:297-298`) and its blob
  sha256 is compared to the recorded `map_sha256`.
- `routed-defects.py:365-369` — **`if not bad: return _check(..., True, ...)`**:
  the check returns PASS on the FIRST receipt (git `ls-tree` alphabetical
  order) whose every pin_check resolves and digests. It is an existential
  check over all receipts, not a universal one.

[INFERENCE from the code, confirmed by probes A–C] drift in any receipt other
than the first qualifying one is invisible to the gate; the "verified
map_sha256" wording in the passing detail line refers only to whichever
receipt happened to qualify.

## Baseline (observation)

```
$ python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
exit 0; open_count 0; all six defects closed
R17-PINMAP r18-receipt-pinmaps detail:
  ".ufo/waves/round-18/runs/calib-aether/receipt.json: 3 pin_checks each
   carry map_path + verified map_sha256"
```

All 15 receipts' `pin_checks` resolve and digest-verify at REV (audited
directly, sha-recomputed per entry: 15/15 OK).

The defect being attacked (routing doc,
`corpus/lessons/round-17-verifier-spotcheck.md:137-139`): mid-run `pin_checks`
must retain the map or its digest, else the "each pin map is retained" texts
lie. A committed map whose bytes no longer match its receipt-pinned digest is
exactly that defect state, re-opened.

## Probe A — cheapest re-open (observation)

Commit `a08496a0f7bd5d0b9928812f8700fab0c3b35dc7` — 1 file, 1 line, appends a
space inside the trailing JSON whitespace of the mid map of the C3
diagnostic-set carrier `s1246-swiss-nethttp` (its single receipt-recorded
digest goes stale: `e5f3f381…` → `128ac3f6…`, file still valid JSON):

```diff
--- a/.ufo/waves/round-18/runs/s1246-swiss-nethttp/pins/mid-1.json
+++ b/.ufo/waves/round-18/runs/s1246-swiss-nethttp/pins/mid-1.json
@@ -765,2 +765,2 @@
-}
+}
```

```
$ python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev HEAD
exit 0; open_count 0; R17-PINMAP closed (all six closed)
detail unchanged: "calib-aether/receipt.json: 3 pin_checks each carry
map_path + verified map_sha256"
```

The drifted receipt is never inspected: `calib-aether` sorts first and
qualifies, so the scan stops (`:365-366`). Result: defect re-opened in the
rev-scoped world while the gate says closed.

**Boundary finding (observation)** — the sibling validator does not catch this
from the clone either, for a different reason:

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-18/runs/s1246-swiss-nethttp/receipt.json     # exit 0, no findings
```

Receipts record absolute `map_path`s into the original lane
(`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/...`), and
`receipt-validate.py` hashes the LIVE file at that path (`verify_mid_maps`,
receipt-validate.py:453-514). The live original-lane file is untouched, so the
digest matches. When I rewrote only `map_path` to point at the clone's
corrupted blob, the same command returned exit 1 with
`mid_map_sha256_mismatch` (actual `128ac3f6…` vs recorded `e5f3f381…`). So:
the validator is live-tree-scoped, the routed gate is rev-scoped — neither
tool as wired detects committed mid-map drift at an evaluated rev. [INFERENCE]
in the real lane (corruption committed there), an in-lane receipt-validate run
would flag it; the routed gate still would not.

## Probe B — vacuous receipt rejected, drift still whitewashed (observation)

Commit `3a9ba11ca4c3cbbda33ecbc8a05fb13309009778` from REV: adds
`.ufo/waves/round-18/runs/aaa-vacuous/receipt.json` containing
`{"steps":{"analyze":{"pin_checks":[]}}}` (sorts first in `ls-tree`) and
corrupts all three `calib-aether/pins/mid-*.json` maps.

```
$ python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev HEAD
exit 0; open_count 0; R17-PINMAP closed
detail now: "calib-notesmd-cli/receipt.json: 2 pin_checks each carry
map_path + verified map_sha256"
```

`aaa-vacuous` was rejected (`:341`, empty list ≠ missing), `calib-aether` was
correctly found bad — and the scan simply moved on to the next intact receipt.
Two independent failures stayed green.

## Probe C — N−1 calibration extreme (observation)

Commit `da156f0602e581522f9d8e701c1dbdc30d49de18` from REV: corrupts 20 of 21
mid maps (every receipt except `calib-notesmd-cli`), 13 of 14 receipts lying,
20 files changed.

```
$ python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev HEAD
exit 0; open_count 0; R17-PINMAP open: False
detail: "calib-notesmd-cli/receipt.json: 2 pin_checks each carry map_path
+ verified map_sha256"
```

One honest receipt whitewashes the fleet. The check's per-revision assurance
is O(1), not O(receipts). [INFERENCE] C1's "retained evidence" language
(claims.json amendment C1: "r18-receipt-pinmaps"-style substance) is
over-claimed relative to what this check can see.

## Secondary surface (observation, not exercised further)

The other five PINMAP checks are literal-text heuristics (`_line_with`
needle matching at `routed-defects.py:148-155`; `_code_text` token filter at
`:161-184`): e.g. `carrier-run-map-code` passes on the literal `map_sha256`
anywhere in non-comment code, so a carrier-run.py change that computes the
digest over the wrong bytes would keep both `carrier-run-retains-map` and
`carrier-run-map-code` green. Cheapest demonstrated attack did not need it.

## Residual risk

- The wave could argue the routed gate is only a coarse tripwire and the
  retained validator is the real control; but the pair's scopes are disjoint
  (rev vs live tree), so no single artifact at REV proves all receipts still
  digest-verify — probes A–C produce such an artifact with exit 0 from the
  gate.
- I did not test whether `_map_candidates` ordering (`:294-310`) can be
  shadowed by a receipt recording a bare relative `map_path` (repo-root file
  tried first); all current receipts use absolute paths, so it needs receipt
  tampering and was out of scope for "cheapest".

## Verification gaps

- `receipt-validate.py --require-mid-maps` was exercised via a path-rewritten
  receipt copy, not against a corrupted real lane (lane writes forbidden);
  its in-lane detection of probe A is inference from its live-path hashing,
  not a run against the real lane.
- Probes were evaluated with the REV-pinned tool; the gate's behavior on
  later wave-2 revisions may differ.

Clone retained at `/tmp/kpinmap.P1GNli/lane` (branches `probeA`/`a08496a` head,
`probeB`, `probeC`) for reproduction.
