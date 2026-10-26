# R40W2C1L2FalseNeg — wave-2 falsification of the R40-C1 stop reading

**Verdict: CONFIRMED** — the L1's reading of L2's red `nonregular_unpublished_ok` as a pure
path-suffix false positive is correct, and the converse (a suffix-driven false pass in
`oracle_hits_ok`/`gaps_ok`) does not occur anywhere in the four frozen carriers. No defect found in
the L1 verdict; two counter-design defects noted (structural unreachability of L2; docstring/impl
mismatch) that explain the stop but do not overturn it.

What I attacked: the R40-C1 honest stop at 42c10a58cb2cae3a4a0122af35a0cf95ac718043 — specifically
(a) whether L2's only red binding is genuinely a path-suffix artifact (`usr/bin/busy` vs `bin/busy`)
rather than a materialised symlink, and (b) whether the same `same_rel` suffix logic can produce a
false PASS (a published path that matches an oracle row only by suffix while the true path differs)
in `oracle_hits_ok` or `gaps_ok` on V1, V2, L1, L2.

## Method

From committed bytes only. Re-implemented the counter's exact logic (`same_rel`, `published`,
`oracle_hits`, `nonregular_published`, `gap_check` resolution) from
`tools/round-40/c1-counter.py:331-382,606-703` and applied it to:

- receipts `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json` (working tree verified identical
  to the scored revision: `git diff --stat 42c10a58 -- corpus/evidence/round-40/c1` empty, status clean);
- frozen tables `corpus/evidence/round-40/c1/<ID>/{oracle.tsv,nonregular.tsv}` named by
  `.ufo/waves/round-40/c1/carriers.json`;
- frozen rule `.ufo/waves/round-40/c1/gap-rule.json`;
- cross-checked against the frozen score `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`
  (exit 1, `carriers_matched: 3`, `met_target: false`).

Match classification: a `same_rel` hit is **EXACT-AT-EXTRACT** when the candidate's path minus the
matched row equals the extract root (`firmware.bin_extract` in all four receipts) — i.e. the file
really sits at the row's path; otherwise it is a **SUFFIX-SHADOW** (true path differs).

## Finding 1 (confirms the L1 reading) — L2's red is exactly one suffix-shadow hit

L2 published files (6, all `firmware.bin_extract/*`): `etc/hosts`, `opt/app/config.json`,
`opt/app/data.bin`, `usr/bin/busy` (sha256 `e28f81fc…e70`, 40000 B), `usr/share/doc/README`, `zero`.
L2 nonregular rows (10): 8 `dir`, 2 `symlink` — `bin/busy → /usr/bin/busy`, `usr/bin/ls → busy`.

- (a) **Confirmed: no symlink path of L2 is published as a file.** Neither `firmware.bin_extract/bin/busy`
  nor `firmware.bin_extract/usr/bin/ls` appears in the published set; no published path suffix-matches
  `usr/bin/ls` at all; zero EXACT published×nonregular collisions (no materialised symlink/device).
- (b) **Confirmed: the only `same_rel` hit in all 6×10 pairs is
  `firmware.bin_extract/usr/bin/busy` × `bin/busy` (symlink)** — a SUFFIX-SHADOW: the file's true
  path under the extract root is `usr/bin/busy`, which is itself oracle row 4; `usr/bin/busy`
  matches the symlink row only because `'usr/bin/busy'.endswith('/bin/busy')`. The symlink `bin/busy`
  itself is unpublished and is covered by its own gap
  (`unpublished-entry`, `firmware.bin_extract/bin/busy`), which resolves EXACT-AT-EXTRACT; same for
  `usr/bin/ls`. The frozen score's `nonregular_published` list is exactly
  `["firmware.bin_extract/usr/bin/busy"]` — my hand computation reproduces it 1:1.

## Finding 2 (converse, false PASS) — no false pass exists; both channels are closed on the frozen tables

- **`oracle_hits_ok`**: every oracle row in all four carriers matches exactly one published file,
  EXACT-AT-EXTRACT, same sha256 — V1 697/697, V2 8/8, L1 7/7, L2 6/6. Zero SUFFIX-SHADOW-only rows,
  zero multi-match rows, zero misses. The enabling precondition for a false pass — an oracle row that
  is a component-aligned proper suffix of another oracle row, so a published deeper file could stand
  in for a missing shallower one — is absent: **0 oracle-internal suffix pairs in all four tables**
  (enumerated exhaustively; sha equality additionally forces content identity).
- **`gaps_ok`**: all 352 path-resolved gaps (V1 263, V2 85, L1 2, L2 2) resolve EXACT-AT-EXTRACT to
  exactly one nonregular row; plus 4 structural `depth-limited` (1 per carrier) within allowance.
  `gap_check` fails closed on ambiguity (`!= 1` hits → False), and the wrong-entry-credit channel
  would require a symlink/fifo row that is a proper suffix of another nonregular row — the 6
  nonregular-internal suffix pairs that exist (V1: `bin⊂usr/bin`, `lib⊂usr/lib`,
  `lib⊂lib/modules/2.6.39.4/kernel/lib`, `sbin⊂usr/sbin`; L1: `lib⊂usr/lib`; L2: `bin⊂usr/bin`) all
  have a `dir` as the shallow element, and dirs take no path-resolved gaps (`allowed: []`), so the
  channel is structurally closed on these tables.
- **Cross-table (nonregular row suffix-of oracle row)**: exactly one pair lane-wide —
  L2 (`bin/busy`, `usr/bin/busy`) — which is Finding 1. Zero such pairs in V1/V2/L1.

Full machine-readable enumeration: `.ufo/waves/round-40/w2/artifacts/R40W2C1L2FalseNeg/suffix-ambiguity-enumeration.json`.

## Finding 3 (defect, design) — the L2 stop was structurally forced, not receipt-evidence

Given the frozen L2 tables + frozen counter, **no honest receipt can make L2 green**:
`oracle_hits_ok` compels a published file ending in `/usr/bin/busy` with sha `e28f81fc…` (oracle row
4, `usr/bin/busy`, 40000 B, built by `tools/round-40/mk-l-carriers.py` TREES['L2'].files), and any
such path necessarily `endswith('/bin/busy')`, so `nonregular_unpublished_ok` is false in every
admissible receipt; omitting the file instead breaks `oracle_hits_ok` (5/6). `met_target: 4` was
therefore unreachable at any revision with these frozen inputs — the "honest stop" is correct, the
demotion to measured-not-promoted at 4d62ee5a was the only admissible outcome, and the stop says
nothing about receipt honesty (all other L2 bindings true: oracle 6/6, gaps_ok, handler, chunks,
projection, evidence-id, provenance).

## Finding 4 (defects, low) — counter bookkeeping

1. **Docstring/implementation mismatch**: the binding doc (`c1-counter.py:54-56`) says "no published
   regular file path **equals** a non-regular entry path"; the implementation
   (`nonregular_published`, :643-650) uses component-suffix equality. The documented stricter
   semantics would not have fired on L2. (Note: suffix matching for the ORACLE side is frozen design
   — P40-C1 says "same relative-path suffix, same sha256" — the mismatch is only on the nonregular side.)
2. **Self-test gap**: the 65 red cases exercise `nonregular_unpublished_ok` only via an
   EXACT-AT-EXTRACT published path (`usr/share/demo/escape`, :1783-1787) and `oracle_hits_ok` only
   via deletion (:1788-1790); no test constructs the SUFFIX-SHADOW shape that actually fired, nor the
   shadow false-pass shape (Finding 2 shows it is latent, not active).

## Residual risk and verification gaps

- I re-derived the counter logic by hand from committed bytes and matched the frozen score; I did not
  re-run REA or the counter itself (rerun-vs-receipt is receipt-shape only by design — disclosed limit).
- The false-pass channels are closed on the frozen data but remain latent for any future fixture that
  adds (i) same-content suffix-paired oracle paths, or (ii) a symlink row that is a proper suffix of
  another nonregular row. Unexercised by V1/V2/L1/L2.
- L1's external-carrier patch and c1-extra supplementary gate were not re-audited here (outside this
  seat's item); c1-extra receipt at 42c10a58 shows `oracle_rederived/frontier_content/sourced_new` all true.

## Tooling and bounds record

No tools installed or updated; no pacman transactions; no subagents/background jobs; only read-only
git (`diff --stat`, `status --porcelain`). Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2C1L2FalseNeg`
used transiently, removed at finish. No vendor bytes copied into the lane; no VCS mutation.
