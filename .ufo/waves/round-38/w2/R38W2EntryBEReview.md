# R38W2EntryBEReview — QUALITY review of the landed BE-v4 entry

Seat: `R38W2EntryBEReview` (leaf, wave 2, attempt 2). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Target:
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` as landed at
`3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`. Reviewed against `corpus/QUALITY.md` (attempt-2
rule = first freeze `e059ca93`) and the committed receipts
`corpus/evidence/round-38/c1/K{1..4}/{before,after}.json`.

**Verdict: CONFIRMED — no falsifying defect. Every assigned check passes; 3 minor,
non-blocking findings (M1–M3) with line numbers below.**

Worktree-vs-landing identity: `git diff --stat 3b960fe5 -- <entry>` is empty (exit 0), so the
bytes reviewed are the landed bytes. Entry has 47 numbered lines.

## 1. Provenance header — PASS

- L3–L5: sources S112/S113/S114 with resolvable URLs, roles and as-read date. `corpus/SOURCES.md`
  rows exist at lines 118–120, status `mined`, used-by names this entry.
- L6: `verified-at: 2026-10-26`.
- L7: recheck 180d, command `curl -s …/squashfs.py | grep -c 'V4BE_EXECUTABLE = "sasquatch-v4be"'`.
  **Re-run 2026-10-26: stdout `1`, exit 0.** Reproduces.
- L21–L22 correctly characterize S115 (`corpus/SOURCES.md:121`, status `rejected`) as a recorded
  rejection, not a source.

## 2. Every number traced to a committed receipt — PASS (one placement note, M2)

Pure-jq re-derivation over the eight receipts (verbatim):

```
K1 before: 0 missing-extractor-dependency 0 partial
K1 after: 5  (no gaps)                 9656 partial
K2 before: 0 missing-extractor-dependency 0 partial
K2 after: 3 unpublished-entry          10283 partial
K3 before: 0 missing-extractor-dependency 0 partial
K3 after: 4  (no gaps)                    28 complete
K4 before: 0 missing-extractor-dependency 0 partial
K4 after: 4  (no gaps)                    28 complete
```

- Oracle-match recomputation (path-suffix + sha256 + size against
  `corpus/evidence/round-37/c1/K*/oracle.tsv`): K1 5/5, K2 3/3, K3 4/4, K4 4/4; before arms 0/5,
  0/3, 0/4, 0/4. Matches the arms table (L16–L17) cell-for-cell. K2 after
  `unpublished_entries = [{firmware.bin_extract/var/lib/run-link, symlink}]` — matches L17/L37.
- L12 "Every run names the `squashfs_v4_be` handler": verified in all 8 receipts (before gaps
  carry `handler: "squashfs_v4_be"` + diagnostics `stage: squashfs_v4_be`; after runs name it in
  chunks/raw stdout).
- L35–L36: `MaliciousSymlinkRemoved` is present in `K1/after.json` →
  `normalized_result.diagnostics[0].report.__typename__ = "MaliciousSymlinkRemoved"` (WARNING,
  link-to-hello). Confirmed.
- L20 "16/16 oracle regular files": 5+3+4+4 = 16 against the committed oracles; the direct
  `sasquatch-v4be -be` runs are receipted in the committed wave-1 cross-tool reports
  (`.ufo/waves/round-38/w1/R38CrossToolK1.md:74,113,265` — "5/5", "16/16 rows match"). See M2.

## 3. Handler-argv statement vs S112 — PASS

Fetched `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
(590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`; copy in
`.ufo/waves/round-38/w2/artifacts/R38W2EntryBEReview/squashfs-26.6.4.py`):

| entry claim (line) | fetched bytes |
|---|---|
| `SquashFSExtractor` (lines 24-70) (L3, L28) | class at 24, `get_dependencies` return at 68–69 — range accurate |
| argv `sasquatch-v4be [-be] -no-exit-code -f -d {outdir} {inpath}` (L25–L26) | executable pick at 41; `-be` appended at 50; tail at 56–65 — exact |
| drops `-be` when `header.bytes_used == header.mkfs_time` (L26–L27) | lines 48–50 (`is_avm`; `if not is_avm: append("-be")`) — exact |
| `get_dependencies()` returns both `sasquatch` and `sasquatch-v4be` (L28) | lines 68–69 — exact |

## 4. Corrected-premise paragraph — PASS (one labeling note, M1)

- L30 quote `does not reproduce` (3 words) is contiguous in the first freeze:
  `git show e059ca93:plans/round-38-claims.md` — "the round-37 'missing-extractor-dependency'
  before-arm does not reproduce on these carriers".
- Mechanism is committed: freeze v2 `79f69347` (plans/round-38-claims.md) states the L1's v1
  probes "never actually stripped `~/.local/bin` — `grep -v sasquatch` filters PATH component
  names"; wave-1 `.ufo/waves/round-38/w1/R38RevengerPremise.md` §1.6 demonstrates filter A leaves
  `~/.local/bin` (after-arm outcome) while the round-37 harness filter (by directory contents,
  `tools/round-37/c1-run.sh:43`) reproduces the gap on all four carriers. The entry's L30–L31
  compression ("filtered PATH entries by directory name and never removed `~/.local/bin`") is
  faithful to both.
- "A property of the PATH the unblob child process sees, not of the image" (L29–L30): supported —
  both arms measured on identical carrier bytes (same `subject.digest.sha256` in before/after).

## 5. Not-promoted status statement — PASS

- L43 "This is not a Core promotion": no round-38 Core row exists; first-freeze counter score
  `.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` has `province_core_row: false`,
  `province_core_section: false`. The only "Core" token in the entry is this negation — no
  overclaim.
- L43–L45: first-freeze predicate says "carries no extraction gap" (contiguous); counter score:
  `carriers_matched: 3`, `met_target: false`, K2 `matched: false` with
  `after_gaps_empty: false`, K3/K4 matched. "Honest stop (3/4 carriers)" is exactly what the
  first-freeze rule produced at the landing rev (attempt-2 rule = QUALITY 79; the v3 score file is
  explicitly named `NOT-THE-RULE`).
- L45–L46 "stays on the PROVINCE Frontier": `PROVINCE.md:157` — "big-endian/AVM stays here.
  Round 38: standard BE v4 measured … not promoted — R38-C1 honest stop, K2's in-tree symlink
  leaves an `unpublished-entry` gap"; frontier note at `PROVINCE.md:374`. Consistent.
- L41 round-36 precedent: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:86-88,120,188`
  records `unpublished-entry` gaps for symlinks (LE). Confirmed.
- L46–L47 "AVM-BE and vendor-mangled images were not measured. Nothing … about the extracted
  programs": no such receipts exist; consistent with the claims file's "Not claimed" list.

## 6. Quote audit — PASS (all ≤ 25 words, contiguous in committed bytes)

| line | quote | words | located in |
|---|---|---|---|
| 30 | "does not reproduce" | 3 | `e059ca93:plans/round-38-claims.md` (P38-C1 "Not claimed") |
| 40, 43–44 | "no extraction gap" | 3 | same file, predicate "carries no extraction gap" |
| 21 | "Cannot open the file as archive" | 6 | `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt:12,29,46,63` |
| 36 | `MaliciousSymlinkRemoved` | 1 | `K1/after.json` diagnostics `__typename__` |

## Minor findings (non-blocking)

- **M1 — L30–L31, unlabeled historical inference.** The causal clause "because its probes
  filtered PATH entries by directory name" is stated as fact, but the v1 probe command itself was
  never committed; the `grep -v sasquatch` shape is the L1's own v2-note assertion
  (`79f69347`) and is marked [INFERENCE] (medium confidence) in `R38RevengerPremise.md` §5. The
  outcome it explains is fully evidenced; the literal command history is not. Suggest labeling or
  citing the v2 note.
- **M2 — L20, citation placement.** The "16/16" number is correct but its producing receipts are
  the committed wave-1 cross-tool reports (`R38CrossToolK1.md:74,113,265`), not the
  `corpus/evidence/round-38/c1/K*` files the L19 "Receipts:" line cites.
- **M3 — L38/L40, universal inferences stated flat.** "on every run" (L38) and "'no extraction
  gap' is unreachable on any carrier with an in-tree symlink" (L40) generalize beyond the
  committed runs (landed K2 receipt + premise-seat fresh run). Mechanism support exists (envelope
  limitation "only regular files are published"; round-36 rows 86–88 show gap count = symlink
  count), but QUALITY #5 labeling would put these under inference.

## Residual risk / verification gaps

- Zoneless dates (`2026-10-26`) in the header are not checkable by the QUALITY-23 strict tool;
  both landing commits are `2026-10-26T03:50:00-03:00`, so no future-dating is possible on these
  bytes. Stated unchecked per row 23.
- The entry's sasquatch-v4be "4.5.1" version pin (L17) is environment attestation from committed
  wave-1 records (`R38RevengerPremise.md` §1.5), not a receipt field; not re-measured here.
- I did not re-run REA or the counters; the counter scores cited are the L1's committed receipts
  (`.ufo/waves/round-38/l1/scores/`).

## Bounds & tooling record

No installs/upgrades; no pacman; REA not invoked (not needed); read-only git only
(`show`, `diff --stat`, `log`); no VCS mutation; no writes outside this report and
`.ufo/waves/round-38/w2/artifacts/R38W2EntryBEReview/` (holds the pinned S112 fetch
`squashfs-26.6.4.py`, sha256 above). No scratch directory was created (nothing to clean; TMPDIR
untouched). Writes: none to corpus/, PROVINCE.md, SCORECARD.md, SHONEN.md, LOG.md, tools/.
