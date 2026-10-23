# A2NoHarmBaseline — no-harm baseline review 283aad7f → f382e3b7

Seat: `KaidokuR32A2.A2NoHarmBaseline` · written 2026-10-23T06:59Z · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
All checks were exercised (not inferred) in a fresh sandbox clone — never in the lane — at
`/fast/scratch/hyaku/kaidoku-r32/a2audit/A2NoHarmBaseline/clone`, `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE`
unset for every invocation. Clone HEAD = lane HEAD = `f382e3b7978e6091a19ca93277c15a75c0016b43`.
Held item `U064N008Hf47eb933` was not opened, reproduced, retried or rephrased; only files that
*name* the id were read for their hold statements. Tools used (host, nothing installed): git
2.56.0, sha256sum/diff (uutils 0.8.0 / pi-uu-diff 0.8.0), python3 3.14.8, `env -u`.

## What was measured (exact argv → observed result)

| # | Command (sandbox, `git -C <clone>`) | Exit | Observed |
|---|-------------------------------------|------|----------|
| 1 | `git clone --quiet --no-hardlinks <lane> <clone>` then `git rev-parse HEAD 283aad7f^{commit} f382e3b7^{commit} 9a73680a^{commit} 9d54070b^{commit}` | 0 | HEAD=`f382e3b7…43`; base `283aad7f…25`; freezes `9a73680a…1b`, `9d54070b…67` all resolve |
| 2 | `git log --oneline --no-decorate 283aad7f..f382e3b7` | 0 | exactly 3 commits: `9a73680a`, `9d54070b`, `f382e3b7` (the three freezes) |
| 3 | `git diff --name-status 283aad7f f382e3b7` | 0 | **33 files, every row status `A`** — zero M/D/R |
| 4 | `git diff --stat 283aad7f f382e3b7 -- PROVINCE.md SKILL.md SCORECARD.md SHONEN.md LOG.md` | 0 | empty output — all five byte-identical |
| 5 | `git rev-parse <rev>:<file>` for the three claims files at 9a73680a, 9d54070b, f382e3b7, HEAD | 0 | blob ids below — unchanged since each first-add |
| 6 | `git show f382e3b7:<path> \| sha256sum` for 7 instruments + 4 frozen inputs | 0 | every sha256 equals the pin in its claims file (table below) |
| 7 | `sha256sum` of lane working-tree files vs `git show f382e3b7:` | — | all committed frozen bytes intact; 7 working-tree edits + 4 deletions (Finding 3, 6) |
| 8 | `lsattr`/`sha256sum` on `/fast/scratch/hyaku/kaidoku-r32/carriers/` | — | 12 DLLs, `----i---` immutable flag set, sha256+size match `carriers.tsv` row-for-row |

### The 33 added files, classified

- **Freezes (3):** `.ufo/waves/round-32/claims.json` (blob `59ff7d70…7c1`, added 9a73680a), `claims-v2.json` (`01c52260…d25`, 9d54070b), `claims-v3.json` (`7d38b604…0ad`, f382e3b7). Each blob id identical at its own freeze commit, at f382e3b7, and at HEAD — **zero post-freeze mutation**. `claims.json` was untouched by the two supersessions.
- **Instruments (7), all sha256-verified at f382e3b7:** `tools/round-32/c1-arm64x-positive.py` `7a534be6…f1a`, `arm64x_oracle.py` `17eea1f9…686`, `c2-capability-calibration.py` `c3412b04…446`, `c2-capability-calibration-v2.py` `82434cba…36a` (pin per claims-v2.json), `c2-capability-calibration-v3.py` `5955e8ac…d9f`, `freeze-integrity.py` `6b5aa1df…04cd`, `build-arm64x-carriers.sh` `7da284da…ba3`.
- **Frozen inputs (4):** `corpus/evidence/round-32/c1/{carriers.tsv 8cf97b37, predictions.tsv fd804949, inputs/loadconfig-arm64.s 7c29f128, inputs/loadconfig-arm64ec.s c043b748}`.
- **Before/control receipts (19), in-repo receipts only — never executed by me:** `before/`×17 (counter runs at base, selftests, `carrier-build-receipt.txt`, `sources-census-start.txt`, `unmoved-and-novelty-at-283aad7f.txt`, probe artifacts `probe/{a.c,an.json,ia.json,insp.json,insp2.json,x.dll.sha256}`) and `controls/l1-c2-v1-allin1-receipt.txt`, `l1-c2-v2-irrelevant-path-receipt.txt`.
- **No other file** anywhere in the tree was added, modified, renamed or deleted. No production prose, no corpus knowledge, no data content landed in the committed range.

## Findings

**None blocking the committed diff. All findings below are about the *pending working tree* and the *final data commit*, not about 283aad7f→f382e3b7 itself.**

1. **PASS — production unchanged across the diff.** `PROVINCE.md`, `SKILL.md`, `SCORECARD.md` byte-identical at both ends (check 4); so are `SHONEN.md` and `LOG.md`. Every change is an addition under `tools/round-32/`, `corpus/evidence/round-32/c1/`, `.ufo/waves/round-32/`. The strict phrase "only instruments/carriers/freezes added" holds with the named exception: 19 in-repo `before/`+`controls/` receipt files ride the same three freeze commits — consistent with the freeze rule "Control receipts are committed before the data commit" (claims.json `freeze_rule`, ≤25w) — no production content among them.

2. **PASS — freeze immutability exercised three ways.** Blob-id equality (check 5), sha256 equality against every `instruments`/`frozen_inputs` pin in `claims.json`, `claims-v2.json`, `claims-v3.json` (check 6 — `freeze-integrity.py` hash `6b5aa1df…` verified against both the v2 and v3 pins), and the lane's own uncommitted `a2before/freeze-*.txt` receipts (read only) corroborate `CLEAN pins=8/2/2, commits_after_freeze=0` at rev f382e3b7.

3. **MEDIUM — uncommitted production edits already sit in the working tree.** Tracked-file census (`git ls-tree -r` + per-file sha256, 21 731 files) shows: **MODIFIED** `LOG.md` (one appended round-32 entry), `SKILL.md` (one sentence rewritten at line 1038 — the r31 verifier-spotcheck correction naming `m-over-256mib`, `m-wal-over`, `m-journal-hot`), `corpus/QUALITY.md` (rows 57–58 appended), `corpus/claim-freezes.tsv` (+2 rows), `corpus/claim-freezes-v2.tsv` (+4 rows), `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` (appended "Novelty-scope correction"), `corpus/lessons/round-31.md` (appended "Corrections appended — round 32", 7 bullets). Each is append-only or the declared r31-repair rewrite and matches the new LOG.md entry's own description. They are consistent, but **they are production edits the final diff will carry** — the "production unchanged" property ends at the data commit.

4. **MEDIUM — C2v3 is met by wrong controls; the final diff must not carry a Capabilities repair as a success.** `controls/a2-receipts.tsv` records `A2C2False` (a SCORECARD explicitly *denying* all four capabilities) scoring `statements=4 match=4 … exit 0`, and `A2C2Labels` likewise `met_target=yes`; `a2-receipts-meta.json` declares `"c2_disposition": "honest-stop … no re-freeze"`. The new LOG.md entry says the same. A `## Capabilities` edit committed anyway must be reported as a frozen-target miss, never used to satisfy the claim, and must not alter `claims-v3.json`/`c2-capability-calibration-v3.py`/anchors/key list.

5. **PASS — held item `U064N008Hf47eb933` stays a hold.** Every naming file is a hold/exclusion record; zero unhold, release, retry, rephrase or replacement record exists, and `s3-unjoined64/record-result.json` holds no result under the id. Disposition record (`s3-unjoined64/policy-holds.json`, 2026-10-21): `"HOLDoriginalitem/question;retainreportunqualified; no wake/reroute/newidentity/rephrase/retry/replacement/futurecontinuation."` Newest fleet ledger `.ufo/waves/hyaku/PHASE4.md:22` lists it under "Item holds" still held; `:128` "item hold `U064N008Hf47eb933` stays held" at the r30 unblock. Fleet round reports `.ufo/reports/round-{29,30,31}/kaidoku.md` each attest "remains held and untouched"; lane lessons `corpus/lessons/round-{30,31}-verifier-spotcheck.md` say "not touched"; the round-32 a2audit spec/dispatch re-impose "Do not inspect/retry held item". No committed diff file, and no `a2audit/` report, reproduces the item.

6. **LOW — stale tracked fixtures absent from working tree.** 4 deletions pending: `arc3-loop1-round4 …/alias-{1,2}.conf` and two `round-{18,19} …/symlink-loop` scratch fixtures. Pre-existing cleanup unrelated to round 32; harmless, but if the data commit sweeps `git add -A` they ride along.

7. **INFO — custody ledgers self-disclose a FLAGGED row.** Working-tree `claim-freezes-v2.tsv` marks `round-32/claims-v3.json` `FLAGGED INSTRUMENT_UNPINNED` — v3's counter parses historical evidence anchors (`round-14/…/quote-fidelity.py`, `round-17/run-carriers.sh`, `round-27/xpin-attribute.mjs`) that are pointers, not executed instruments; corroborated by `a2before/freeze-ledger-v2-before.txt`. Disclosure, not a violation.

## SHONEN boxes — "unchanged" interpreted

`SHONEN.md` (byte-identical across the diff) holds 4 boxes, all `[~]`. Canonical form, fleet `PROTOCOL.md:432`: marks are confined to the box character plus one indented evidence line per box — `[x] <verifier-id>` or `[~]` with a resolvable pointer; no other prose, no added or removed boxes. **Unchanged therefore means:** all 4 boxes survive, marks stay `[~]` — `[x]` requires a *named non-author verifier* nothing in round 32 supplies — and no box is added or removed. What precedent allows *within* unchanged boxes: the indented pointer refresh (rounds 25/26/30 each refreshed ranges after PROVINCE drift). A C1 Core-table row lands above `## Frontier` (:73), pushing `## Adjacent` (:97) down — box 4's asserted range `PROVINCE.md:97-118` will drift again and legitimately needs the same refresh; that is not a mark change.

## What the final diff must preserve

Byte-identical against f382e3b7/HEAD blobs: the three claims files (`59ff7d70`, `01c52260`, `7d38b604`), all 7 instruments and 4 frozen inputs (hashes above), all 19 before/control receipts; plus `fleet_pin cef00867`, key list, anchors_at_freeze and targets as text. Predicate/label/target edits are forbidden in either direction — the C2 shortcut result is reported, never repaired. `corpus/knowledge/2026-10-13-r4-13-pwntools-persist.md` (the held item's file) untouched; its hold records untouched. 4 SHONEN `[~]` boxes as above. No file may name a Python import in a MARKER/log path; no seat reports may land inside the data commit's production files.

## Residual risk / verification gaps

- Working tree ≠ committed range: 7 MODIFIED + 4 DELETED + uncommitted `a2audit/`, `a2before/`, `controls/c2-negative/`, `w1/swarm-registry.json`, `a2audit-*` spec/dispatch files exist and are **out of committed-diff scope**; reviewed as declared, not certified line-by-line.
- I read receipts; I ran no counter, selftest, REA, build or test (per assignment "No tests"). Counter outputs cited (4/4 met by denial controls) are from retained receipt bytes, not re-executed.
- C2v3 falsification is a pending-commit hazard, not a defect in the reviewed diff; L1's data commit decides whether the claim is honestly reported as unmet.
- Deadline headroom: report written ~06:59Z, inside 07:35Z.

Verdict: **the committed diff 283aad7f→f382e3b7 is clean — production unchanged, freeze immutable, only instruments/carriers/freezes/receipts added; the hold stands; the real no-harm risk is what the still-uncommitted production edits and the C2v3-falsified counter imply for the final data commit.**
