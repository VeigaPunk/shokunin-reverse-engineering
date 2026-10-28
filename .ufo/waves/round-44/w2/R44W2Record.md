# R44W2Record — the round-44 record audited against its receipts

Seat `R44W2Record` (wave 2, record audit). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Audited revision: `4503fb78` (HEAD at audit time).** The lane moved three times while I worked —
`8bb1090a` → `923fa870` → `4503fb78` — and sibling wave-2 seats corrected parts of the record in
flight; where that matters I name the revision I read. Every number below was re-derived by me from
committed bytes or from an independent re-run, never copied from the record.

Re-run receipts (argv, exit code, stdout sha256, wall, observed values):
`.ufo/waves/round-44/w2/artifacts/R44W2Record/rerun-receipts.json` plus the receipt/stdout copies in
that directory. No tool was installed or upgraded in this seat.

## 1. What I re-ran (independent, read-only w.r.t. the lane)

| run | command | exit | observed |
|---|---|---|---|
| C1 @ `55bcce69` | `python3 -I -B tools/round-44/c1-counter.py --root . --rev 55bcce69… --freeze c48f8a4b… --pkg65 <rea-agents 6.5.0> --work <scratch> --json-out <scratch>` | **1** | `carriers_matched 4`, `met_target false`, `failing []`, `frozen_path_changed []`, `bindings_false ["province_core_section","province_core_row","frontier_note"]`, `run_provenance_ok true` on all four carriers |
| C2 @ `55bcce69` | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 55bcce69… --freeze c48f8a4b… --work <scratch> --json-out <scratch>` | **0** | `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`, `unevaluable 0`, rubric sha `e8cc0ded…` = at-freeze |
| C1 @ HEAD `4503fb78` | same, `--rev 4503fb78` | **2** | `reason frozen_path_changed`, 8 paths |
| C2 @ HEAD `4503fb78` | same, `--rev 4503fb78` | **2** | `entries_evaluated 0`, `frozen_path_changed` 8 paths, `unevaluable 1` |
| preflight @ `c86ea508` / `55bcce69` / `923fa870` / `4503fb78` | `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b… --rev <REV> --pathspec tools/round-44` | **1 / 0 / 1 / 1** | `touched 8, blob_changed 8` / `clean` / `touched 8, blob_changed 8` / `touched 8, blob_changed 8` |
| command A | SCORECARD `## Measurement recipes` A at `c29360e3`, `c48f8a4b`, `55bcce69`, `c86ea508`, HEAD | 0 | `137/137, 21/21, 10.0, 10.0` / `137/137, 21/21` / `138/138, 21/21` / `138/138, 21/21` / `138/138, 21/21` |

## 2. Numbers the record states, checked against the receipt

All of these **reproduce exactly**; no discrepancy.

| record claim | location | receipt value |
|---|---|---|
| `carriers_matched 4`, `met_target false`, exit 1 at `55bcce69` | `LOG.md:3201`, ledger row `LOG.md:3224` | `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`; my re-run exit 1 |
| exit 0 + `carriers_matched 4` at `4cc1ac11` | `LOG.md:3201` | `corpus/evidence/round-44/c1/counter-at-4cc1.json` (`exit_code 0`, `met_target true`, `bindings_false []`) |
| `carriers_matched 0`, exit 1, every doc binding false at the freeze | ledger `LOG.md:3224` | `corpus/evidence/round-44/controls/c0/receipt.json` (`control CTL-C1-0`, `measured.carriers_matched 0`) |
| `entries_evaluated 80`, `mismatches 0`, `frozen_path_changed []`, exit 0 | `LOG.md:3202`, `LOG.md:3225` | `c2-score-at-55bcce69.json`; my re-run |
| base census = 3 mismatches, ids `C2-a1/C2-a2/C2-a4` | `LOG.md:3225` | `w1/artifacts/R44C2Rubric/receipts/{base-census-summary,census-base}.json` (`mismatches 3`, same ids) |
| `frozen_path_changed []` at REV / **8 paths** at the tip | `LOG.md:3201,3203`, `SCORECARD` defect paragraph (at `8bb1090a`) | tip receipts: 8 paths each, **byte-identical lists** (`c1-score-at-tip.json` == `c2-score-at-tip.json`); the 8 are exactly the `M` paths of `c86ea508` |
| `c86ea508` modified 8 files, added none, under `tools/round-44/` | `LOG.md:3203`, lesson `:18` | `git show --name-status c86ea508`: 8 `M` under `tools/round-44/control-fixtures/`, 0 `A` |
| `git log --oneline c48f8a4..main -- tools/round-44/` → only `c86ea508` | lesson `:18` | exactly that one line |
| preflight red at `c86ea508` / green at `55bcce69` | `LOG.md:3203`, `:3229` | my re-run 1 / 0; also red at HEAD (8 paths) |
| wave 1 = **37 seats**, mix `8/8/7/4/3/3/1/1/1/1`, 0 dead | `LOG.md:3204` | `w1-spec.json` has 37 items with exactly that role vector; `r44-w1-results.json` has 37 results, names 1:1 with the spec, no empty output, no failure status (four outputs contain the *word* "failed/error" in prose only) |
| command A `knowledge_files=138, mapped=138, missing [], dangling [], coverage 10.0`, 137/137 before | `LOG.md:3227` | my command-A run at `c86ea508` and at base |
| depth `21/21`, `depth_score 10.0` | `LOG.md:3227` | my command-A run (`citation_resolved_rules 21`, `rule_blocks 21`) |
| `corpus/SOURCES.md` 137 → 139 rows | `LOG.md:3205`, lesson `:47` | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 137 at `c29360e3`, 139 from the freeze on |
| S138 = 10 listings + 22 members, `failures: []` | lesson `:27` | `corpus/evidence/round-44/oracle/manifest.json` `counts{listings 10, files 22, failures 0}` |
| every cited commit hash exists | `LOG.md:3198-3232`, lesson | 12 tokens in the LOG block (10 distinct commits) and 8 in the lesson; every one resolves with `git cat-file -t … = commit` |
| four C1 receipts publish every oracle file, no gaps | `LOG.md:3224` | per-carrier `oracle_hits_ok`, `gap_rule_ok`, `nonregular_*` all true; `failing []` |
| the frozen claim text is **not** literally unsatisfiable, and the counter's red is **not** provenance | lesson `:70-83`, `LOG.md:3201` | see §3 |

## 3. R44-C1 verdict — confirmed, with two corrections the record now makes and one residual

**Confirmed.** `carriers_matched 4`, `met_target false`, exit 1 at `55bcce69` is exact, and the stop
is *correct for the four receipts as produced*: they carry
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out`, which does not name a
`corpus/evidence/round-44/c1/` path, so the controls-amendment clause (`plans/round-44-claims.md:34`)
is unrealized. No Core row is claimed, and `PROVINCE.md`, `corpus/README.md` and the entry all say
so.

**Correction 1 — provenance is not what failed.** In the receipt *and* in my re-run,
`run_provenance_ok` and `evidence_id_ok` are **true** for all four carriers, `failing` is empty, and
`met_target false` comes only from `province_core_section`, `province_core_row`, `frontier_note`.
Those three are false because `55bcce69` itself renamed `## Round-44 additions to Core` to
`## Round-44 measured, not promoted (R44-C1 honest stop)` and rewrote the frontier note. So the
measured-revision red is a consequence of the honest-stop landing, not a measurement that the claim
cannot be met — at `4cc1ac11` the *same* counter on the *same* four receipts returned exit 0,
`met_target true`, `bindings_false []`. The record at HEAD says this in as many words
(`LOG.md:3201` "the score was withdrawn under the claim text, not rejected by the counter";
lesson `:70-83`). The earlier text at `8bb1090a` did **not**, and any downstream citation of that
revision's sentence is stale.

**Correction 2 — the claim is not unsatisfiable.** `provenance_ok()` is the only provenance
predicate the frozen counter implements (`tools/round-44/c1-counter.py:1176-1182`, `PROV_SEGMENT =
'/kaidoku-r44/'`). A single absolute path satisfies both frozen clauses
(`plans/round-44-claims.md:34` and `:137-138`):

```
$ python3 -c 'import importlib.util as u; s=u.spec_from_file_location("c","tools/round-44/c1-counter.py"); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.provenance_ok("/fast/scratch/hyaku/kaidoku-r44/run/corpus/evidence/round-44/c1"))'
PASS        # exit 0
$ … provenance_ok("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/c1")   → FAIL (lane path has no /kaidoku-r44/)
```

So "no real run can satisfy the whole frozen text" (the `8bb1090a` phrasing and the strength of the
assignment brief) is **false**; what is true is that *this round's four receipts* did not satisfy it.
The record at HEAD already states exactly that ("It is **not literally unsatisfiable** … a naming
loophole, not a provenance", lesson `:72-77`) and cites a wave-2 counterfactual that scored
`met_target true, exit 0`. I confirm that text; I falsify the unqualified version.

## 4. R44-C2 verdict — confirmed, with one note-vs-value edge

`entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`, exit 0 at
`55bcce69` reproduces to the byte (`rubric_sha256 == at_freeze == at_rev = e8cc0ded…`). At base the
rubric fails loudly: exit 1, `mismatches 3`, ids `C2-a1-owned-coverage-count`,
`C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range` — so it is not vacuous in the
"can never fail" sense, and it is `frozen_path_changed`-sensitive (exit 2 at the tip on exactly the
8 paths).

**Edge (instrument, not the counter's stated contract).** For the three repaired entries the
`observed` value the counter records is taken from the appended `c2-correction-value:` note, not
re-derived from the `## Owned axes` row: `tools/round-44/c2-rubric.json` entry
`C2-a1-owned-coverage-count`, embedded script line
`eff=correction(STMT,EID)` → `if eff is not None: stated=eff`, then
`observed = stated if stated==derived`. Consequence: `SCORECARD.md:23` may still read `133/133` and
`SCORECARD.md:24` `20/20` (it does, see D-4) and the counter is green, because the row's value is
overwritten before comparison; the counter would only catch *removal* of the `N/N knowledge files
mapped` pattern (`emit("UNSUPPORTED:pattern-not-found")`). The receipt's `entries[…].observed` for
`C2-a1` is `"137/137"` — the note, not a reading of the row. This is the note-as-observed side of
rule R3 (`tools/round-44/c2-rubric.json` `rules.R3_no_note_is_evidence`) and is disclosed in the
claim as D-17, not a frozen-byte violation.

## 5. Discrepancies (numbered; L1 must act on these)

### D-1 — cited oracle-manifest sha256 matches no committed byte (hard)

- Claim: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12` — "manifest
  `corpus/evidence/round-44/oracle/manifest.json`, sha256
  `4bc53dbba8beee0fbf912771efc0a55fd47a197cca1f56d2aaed790f817c1a13`". Repeated at
  `corpus/lessons/round-44.md:27` (S138 Gate row, `4bc53dbb…c1a13`).
- Command: `sha256sum corpus/evidence/round-44/oracle/manifest.json` → **exit 0**,
  `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`.
- The file has one commit (`c1ff9e89`) and the blob is identical at `c48f8a4b`, `55bcce69`,
  `c86ea508`, `HEAD`; `find . -type f -size -2M | xargs sha256sum | grep '^4bc53dbb'` → **exit 1**
  (no match anywhere in the lane).
- Impact: the only landed knowledge entry and the lesson Gate pin the unblob `__output__` dataset
  provenance to a digest that does not exist. The manifest's own counts (10/22/0) *do* match the
  record, so this is a bad digest citation, not a bad dataset. Smallest safe correction: replace the
  digest with `06a72dd5b660…` in the entry (a text edit — it is not a frozen path) and correct the
  lesson row at next close; do not restate 4bc53dbb anywhere.

### D-2 — `QUALITY 86` and `QUALITY 87` are cited but not registered (hard)

- `LOG.md:3229` — "**Freeze-integrity defect (M44-2; QUALITY 86).**"; commit `923fa870`'s subject
  says "QUALITY 86/87".
- Command: `awk -F'|' '/^\| *[0-9]+ *\|/{…}' corpus/QUALITY.md` → **exit 0**, max row id **85**;
  `git show HEAD:corpus/QUALITY.md | grep -nE '^\| *(84|85|86|87) *\|'` returns rows 84 and 85 only.
- The pre-`923fa870` text of the same sentence said "QUALITY 77", which *does* exist but is the
  round-36 "no shadow units" criterion — so the id moved 77→86 without a row either way.
- Round-36's convention was to land the rows ("See `corpus/QUALITY.md` rows 77 and 78",
  `corpus/lessons/round-36.md:57-59`). Smallest safe correction: land rows 86/87 in
  `corpus/QUALITY.md` (frozen-path-preflight applies — check it is not a frozen path for R44 first),
  or cite no criterion id.

### D-3 — the round-start census count in the lesson is the round-end count (hard)

- Claim: `corpus/lessons/round-44.md:49-50` — round-start
  `…/scripts/sources-census.sh validate --root … kaidoku` "→ `kaidoku ok`, exit 0, **14** W04
  duplicate-URL warnings (pre-existing; S138 is the 14th …)".
- Receipts: `git show HEAD:.ufo/waves/round-44/l1/sources-census-start-replay.txt | grep -c W04` →
  **13**; `…/sources-census-end.txt | grep -c W04` → **14**. S138 cannot warn at round start: it
  enters the registry in the freeze commit, and at base the exact URL appears only in S130
  (`corpus/SOURCES.md:136`; S113's URL is a deeper `…/squashfs_v4_be/__input__` path), so at base
  that URL has no duplicate. Verified: `git show <rev>:corpus/SOURCES.md` + exact-token match → S130
  only at `c29360e3`; S130 and S138 at HEAD.
- Same receipt's first line is `ERROR: config not found:
  /fast/scratch/hyaku/kaidoku-r44/l1/shokunin.conf`, and the file carries no exit code, so the
  record's "exit 0 at round start" is not evidenced by the committed receipt (LOG `:3205` says
  "census exit 0 at round start and end"). The start file is a *replay* landed at `923fa870`, not a
  start-time capture.
- Smallest safe correction: state 13 at round start / 14 at round end, and note the start figure is
  a replay.

### D-4 — the `## Owned axes` rows were not repaired; only a footer note carries the new values (medium, reader-visible)

- `SCORECARD.md:23` still reads `133/133 knowledge files mapped`; `SCORECARD.md:24` still reads
  `20/20 queue-drain rule blocks` … `craft section SKILL.md:81-449`. Corrected values exist only at
  `SCORECARD.md:3511-3517` (`137/137`, `21/21`, `81-543`).
- The footer values are right for the freeze tree: command A at `c48f8a4b` = `137/137`, `21/21`, and
  the craft section's last non-blank line is 543 (next `## ` at 547) — I measured all three.
- But `LOG.md` and the lesson headline say "three self-assessment mismatches repaired", and a reader
  of the rows sees `133/133`/`20/20`/`81-449`. At the *measured revision* command A is `138/138`
  (C1's entry landed), so `137/137` is freeze-tree-scoped — now disclosed by R44-CL9
  (`corpus/lessons/round-44.md:88-95`), but the row/note split is only implied.
- Smallest safe correction: say "repaired by appended correction (rows unchanged, D-17)" in the
  ledger and headline. No frozen byte changes.

### D-5 — wave-1 control taxonomy miscount (low)

- `LOG.md:3204` — "(6 counterfactual reds + 1 positive arm)". The frozen claims classify
  `CTL-C1-0` as the **do-nothing** control (`plans/round-44-claims.md:166`) and make the kill rule
  about *counterfactual* reds only (`:183`). `.ufo/waves/round-44/controls/summary.json` holds
  CTL-C1-0…5 + POS (7 receipts, all `verdict: as_expected`), i.e. 1 do-nothing + 5 counterfactual
  reds + 1 positive arm.
- Smallest safe correction: "1 do-nothing + 5 counterfactual reds + 1 positive arm (7 receipts)".

### D-6 — `r44-w1-results.json` cited without its directory (low)

- `LOG.md:3204` — "(`.ufo/waves/round-44/w1/`, `r44-w1-results.json`)". The file is
  `.ufo/waves/round-44/r44-w1-results.json`; `git cat-file -e
  HEAD:.ufo/waves/round-44/w1/r44-w1-results.json` → **exit 128**.
- Smallest safe correction: give the full path.

### D-7 — stale `SCORECARD.md` `## Round 44` citations inside wave 2 (informational, merge hazard)

- At HEAD there is **no** `## Round 44` section in `SCORECARD.md`: it was landed by `8bb1090a` and
  restored to the frozen-bounded blob at `923fa870`. Verified: `HEAD:SCORECARD.md` = `c48f8a4b`
  blob + a 668-byte / 8-line append, and that append is exactly the rubric's `expected_edits`
  correction block. So its absence is **required**, and `LOG.md:3208-3216` explains it (M44-3).
- Still, several wave-2 reports cite it as live (e.g. `.ufo/waves/round-44/w2/R44W2ConnCross.md:19`
  "`## Round 44` at `:3519-3531`"; `w2/R44W2C2Corrections.md:104`). At HEAD those lines are the
  frozen-bounded footer. Do not merge those citations as current; the ledger is `LOG.md:3218-3229`.
- Consequence for this assignment: the instruction to audit `SCORECARD.md` (`## Round 44`) no longer
  has an object — the round-44 numbers live in `LOG.md`.

## 6. Not verified (out of reach without network)

`corpus/lessons/round-44.md` §Gate re-checks are network claims I did not re-open: the S150
"174,088-byte page" with the absent Japanese heading, S113 "17 locales → 21 + `x-default`", S117
0-byte publisher body / Crossref match. Locally checkable parts of that §Gate (manifest counts,
`failures: []`, quarantine-slice digest `7383a90e7c04…28e6a`) I did verify; the slice digest matches
`.ufo/waves/round-44/w1/artifacts/R44Quarantine/quarantine-slice` exactly.

## 7. Housekeeping

- Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Record/` deleted before this report was finalised;
  the receipts it held are copied under `.ufo/waves/round-44/w2/artifacts/R44W2Record/`.
- No claim, counter, rubric, frozen byte, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state/` or
  production doc was modified by this seat; no git/jj mutation was run anywhere.
- Lane edits observed but not mine (recorded so the L1 can order its own merge): `SCORECARD.md`
  reverted and `LOG.md` rewritten at `923fa870`; `corpus/lessons/round-44.md` gained R44-CL9 and
  R44-CL8 at `923fa870`/`4503fb78`; `HEAD` advanced to `4503fb78` mid-audit.
