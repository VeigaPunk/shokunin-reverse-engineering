# R44Assim — round 44 wave 1, §10 assimilation ledger line + surface verification (kaidoku)

**Verdict: CONFIRMED** — `.ufo/waves/round-44/assimilation/` holds nothing (0 entries on disk,
0 files in the HEAD tree, 0 index entries, 0 status entries), the staged register is unchanged
since round 43 (sha256 `5afe1810…bad833`, 83,621 B, mtime 2026-10-24), the 5-row quarantine slice
re-derives **byte-identically** (sha256 `7383a90e…28e6a`, `diff` empty, exit 0) to the round-43
committed slice, and **no staged row has been adopted since round 43** (`corpus/SOURCES.md` is
blob-identical at the round-43 freeze `eadcbfa5` and at HEAD `f5fb8d59`, 137 rows both; the only
`corpus/knowledge/` addition since that freeze, `5856614a`, cites seven sources that all already
existed at the freeze). `considerthese/` does not exist in this lane.

```
Assimilation: none
```

One sentence on why: the kaidoku package's full 5-row quarantine slice was hand-checked in
round 43 (`R43Quarantine`; 1 fabrication-class refuse, 3 present-with-anchor, 1
unverifiable-not-fabrication) and no staged row has been adopted since, so the §10 path appends
nothing this round.

Seat `R44Assim`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base
`c29360e3ba5381a5ab69e372d0d9577970f85018`. Lane HEAD observed at work
`f5fb8d590f0dd6afc0847e1a63e8a3953bef8717` (detached — `git rev-parse --abbrev-ref HEAD`
returns `HEAD`; the round-44 draft claims are `fc5eb54a`, the wave-1 spec/dispatch commit is
HEAD). Lane writes: this report, `.ufo/waves/round-44/w1/R44Assim/` (receipts and slice
evidence) and `.ufo/waves/round-44/w1/artifacts/R44Assim/` (the receipt runner this seat
authored) only; scratch
writes in `/fast/scratch/hyaku/kaidoku-r44/probe-R44Assim/`. No corpus, plan, tool-registry,
VCS mutation, install, or network call. No install was needed (TMPDIR and `HYAKU_SCRATCH` are
unset; `/fast` scratch used).

## 1. What the ledger line must assert

`plans/round-44-claims.md:193-196` (Frontier step, §10): "`Assimilation: none` this round — the
kaidoku package's full 5-row quarantine slice was hand-checked in round 43
(`.ufo/waves/round-43/w1/R43Quarantine.md`) and no staged row has since been adopted; a fresh
hand-check of the slice is re-derived in wave 1 (R44Quarantine) and the lesson records the
verdict table. `considerthese/`: no such directory — one report line."

The ledger line therefore has two testable halves, both checked here independently of the seat
that re-derives the slice (`R44Quarantine`, whose report this seat's line corroborates but does
not re-use as ground): (a) the round-44 assimilation surface is empty/absent; (b) no staged row
was adopted since round 43. The slice's *content* verdicts are carried from round 43 and are
re-derived by R44Quarantine; this seat did not re-open the five sources live and does not claim
that work.

## 2. Round-44 assimilation surface — empty and untracked (A01, A02)

```
A01  test -d .ufo/waves/round-44/assimilation ...                 exit 0
     dir_exists=yes  entries_mindepth1=0  tracked_files=0
     tracked_top_entries=0  index_entries=0
A02  git status --porcelain --ignored -- .ufo/waves/round-44/assimilation   exit 0
     status_scoped_incl_ignored=0  status_untracked_entries=0
```

The directory exists on disk (created by the wave-1 spec generator at 07:59) but is empty, is
absent from the git object tree (git does not track empty directories), and has nothing staged
in the index. Both readings the contract allows ("empty/absent") hold simultaneously; no
assimilation draft exists anywhere else under `.ufo/waves/round-44/` either — the only path
matching `*assimil*` in that subtree is the empty directory itself (`find` → `d
.ufo/waves/round-44/assimilation`), and `.ufo/waves/round-44/{controls,l1}/` are empty too.

## 3. Slice re-derivation — byte-identical (A04, A05)

Derivation command (register read-only; the form round-38/39/42/43 recorded and proved
equivalent):

```
awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output (5 rows; artifact `R44Assim/slice-rederived.txt`):

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

```
A04  rows=5                                                       exit 0
     7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  slice-now.txt
     diff slice-now.txt .ufo/waves/round-43/assimilation/quarantine-slice
     diff_exit=0_byte_identical
A05  5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  register.md   exit 0
     83621 bytes mtime=2026-10-24 08:37:00 -0300
```

The register hash equals the ring recorded from round 38 through round 43, so the staged state
did not move; the derived slice hash equals the round-43 committed slice
(`.ufo/waves/round-43/assimilation/quarantine-slice`). The trailing stray backtick on the four
no-locator rows is the register's one-fewer-column table form, carried unchanged from prior
rounds; ids are unambiguous.

## 4. Adoption audit since round 43 — no staged row adopted (A06–A10)

```
A06  R43_FREEZE=eadcbfa5                                            exit 0
     sources_rows_at_r43freeze=137   sources_rows_at_head=137
     sources_blob_at_r43freeze=d0e6770a85f4be9a5e09865f4e8cce5934c2b7fe
     sources_blob_at_head     =d0e6770a85f4be9a5e09865f4e8cce5934c2b7fe
     knowledge_commits eadcbfa5..HEAD: 5856614a only
A09  every source cited by 5856614a's entry already existed at the freeze:
     S112/S118/S119/S120/S121/S130/S135 -> freeze_rows=1  head_rows=1   (all seven)
A07  head_sources_S138_S139_rows=0   base_sources_S138_S139_rows=0
     head_sources_row_count=137       head_last_row=| S137
     corpus/knowledge files naming S138/S139: 0
A08  slice-id mentions in corpus/knowledge at HEAD: S150=0, S113=1, S117=1, S136=1, S147=0
     those three files were added at 3b960fe5 (2026-10-26) and eadcbfa5 (2026-10-27, the
     round-43 freeze commit) — nothing added after the freeze cites a slice row
A10  corpus/ + PROVINCE.md changed paths, eadcbfa5..HEAD: 414, all round-43 land
     (evidence trees under corpus/evidence/round-42|43/, PROVINCE.md, corpus/README.md,
     corpus/evidence/local-sources.json) — no SOURCES row, no new source admission
```

Reading: the lane's source registry is frozen-identical across the audit window, so zero rows
were admitted since round 43 — the direct test of "no staged row adopted". The single knowledge
addition after the freeze (`corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`, round-43
C1's scored entry) cites only rows that pre-existed at the freeze, and cites none of the five
slice ids. The five slice ids appear nowhere in any entry added after the freeze.

Honest namespace note (not a defect, carried from round 43): three slice ids collide with
pre-existing *lane* SOURCES rows on unrelated subjects —
`S113` = unblob 26.6.4 BE-v4 fixtures, `S117` = unblob README format-count sentences,
`S136` = onekey-sec/sasquatch releases API; `S150` and `S147` have no lane row. The round-43
admission (`corpus/lessons/round-43.md` "### Admission and rejection") normalised its own
`sasquatch-prebuilt-package-inventory` row to lane `S136/S137` after `S135` — a different subject
from the package's `S136` — and recorded that "none was cited by the admitted entry, so no
quarantine row was appended". The A09/A08 counts above are consistent with that: mentions of
`S113`/`S117`/`S136` in knowledge entries refer to lane rows, not to adopted slice rows.

## 5. `considerthese/` — one report line (A03)

`considerthese/` does not exist in the kaidoku lane: `find` over the lane tree returns 0 matches
for `*considerthese*`, there is no lane-root `considerthese` directory, and the campaign root
`/home/vgpnk/Projects/shokuknow` (depth 4) returns 0. For scope honesty, the fleet root has no
`considerthese/` either, while 17 sibling lanes under `/home/vgpnk/Projects/shokunin/` carry
their own `considerthese*` surfaces (`A03 fleet_children=17`: e.g. `audio-shokunin`,
`chousa-shokunin`, `game-dev-2d-shokunin`); those are sibling surfaces, were not read, and are
not kaidoku's to process. The §10 consideration path is therefore not exercised this round — the
same defect the wave-1 debt ledger records as D-26.

## 6. Receipts

Every receipt carries seat `R44Assim`, the exact command, exit code, sha256 of captured stdout,
and wall time; full JSON per receipt plus `receipts.tsv` are artifacts. All checks are read-only
and exited 0 (0 = clean; no claim target is scored here — this is a ledger surface, not a claim).
`stdout_sha256` shown truncated to 16 hex here; the full 64-hex value is in `receipts.tsv` and
each `A*.json`.

| id | exit | stdout_sha256 (16) | wall | check |
|---|---|---|---|---|
| A01 | 0 | `44c704ef1c0b35da` | 7 ms | round-44 `assimilation/` directory/entries/tree/index counts |
| A02 | 0 | `ffb85bd1e331107d` | 15 ms | `git status --porcelain --ignored` scoped to `assimilation/` |
| A03 | 0 | `fdb6b731b6790be8` | 42 ms | `considerthese*`: lane, fleet root, fleet children, campaign root |
| A04 | 0 | `ff52f51bb6dcbeb6` | 5 ms | slice re-derivation (5 rows) + sha256 + `diff` vs round-43 slice |
| A05 | 0 | `348866671bc8dd15` | 2 ms | staged register sha256/size/mtime |
| A06 | 0 | `1d99c0463f8aafe6` | 8 ms | SOURCES blob+row count at `eadcbfa5` vs HEAD; knowledge commits in window |
| A07 | 0 | `6a40f7850b911579` | 9 ms | S138/S139 rows absent at base and HEAD; row count/last row |
| A08 | 0 | `728d444519d8f912` | 15 ms | slice-id mentions in `corpus/knowledge/` + first-add commits |
| A09 | 0 | `6821df469a2b9a4d` | 33 ms | cited-source presence at freeze and HEAD; slice ids as SOURCES rows |
| A10 | 0 | `c858682050a782e3` | 4 ms | 414-path `corpus/`+`PROVINCE.md` diff, `eadcbfa5..HEAD` |
| A11 | 0 | `180affc4c9af8673` | 50 ms | HEAD/branch/`git status` snapshot |

## 7. Findings and limits

- The §10 line is derivable from committed bytes alone: empty assimilation surface + frozen
  registry + a slice hash that matches the round-43 committed file. No network was needed for the
  ledger line, and none was used.
- Limit 1: this seat did **not** re-open the five slice sources; the per-row verdicts
  (S150 refuse / S113, S136, S147 present-with-anchor / S117 unverifiable) are carried from round
  43 and are re-derived live by `R44Quarantine` this wave. The line `Assimilation: none` does not
  depend on their truth, only on their non-adoption — which is what A06/A09 measure.
- Limit 2: "no staged row adopted" is measured as "no SOURCES row added and no new knowledge
  entry citing a slice row after the round-43 freeze". A hypothetical adoption that cited no
  S-id and appended no SOURCES row would evade this test; none is present, and the corpus
  discipline in force (append-only SOURCES + entry citation) makes that shape non-adoptive by
  definition.
- Limit 3: the 17 sibling `considerthese*` directories were located by name only, not read; the
  kaidoku line is about this lane's surface.
- Working-tree observation (verbatim, not a finding of this seat): `git status --porcelain -uno`
  shows one tracked deletion ` D .ufo/waves/round-44/w1.ready.partial` and 15 untracked entries
  (sibling wave-1 reports/artifacts, `corpus/evidence/round-44/`, `.ufo/waves/round-44/w1.ready.dispatched`,
  and this seat's own report/artifacts). This seat created no tracked modification and deleted
  nothing.

## 8. Touched surfaces / out of scope

- Written: this report; `R44Assim/{A01..A11.json, receipts.tsv, slice-rederived.txt,
  slice-sha256.txt}`; `artifacts/R44Assim/receipt.py`; scratch `/fast/scratch/hyaku/kaidoku-r44/probe-R44Assim/slice-now.txt`.
- Read-only: `plans/round-44-claims.md`, `.ufo/waves/round-43/{w1/R43Quarantine.md,
  assimilation/quarantine-slice}`, `corpus/SOURCES.md` (via `git show`), `corpus/knowledge/`,
  `corpus/lessons/round-43.md`, the staged register (read-only, unmodified), git history.
- Out of scope and untouched: C1/C2 tools, counters, receipts, carriers, PROVINCE/README/SOURCES
  text, SCORECARD/SHONEN, `tools/round-44/*`, the register, sibling-lane `considerthese/`
  surfaces. No VCS mutation, no install, no claim score.

## 9. Artifacts

- `.ufo/waves/round-44/w1/R44Assim.md` (this report)
- `.ufo/waves/round-44/w1/R44Assim/receipts.tsv` (full 64-hex stdout sha256 per receipt)
- `.ufo/waves/round-44/w1/R44Assim/A01.json` … `A11.json` (command, exit, stdout/stderr
  sha256 + bytes, wall ms, captured stdout)
- `.ufo/waves/round-44/w1/R44Assim/slice-rederived.txt` (5 rows, sha256 `7383a90e…28e6a`)
- `.ufo/waves/round-44/w1/R44Assim/slice-sha256.txt` (re-derived vs round-43 committed)
- `.ufo/waves/round-44/w1/artifacts/R44Assim/receipt.py` (receipt runner this seat authored;
  the L1 installs tools under `tools/round-44/` — this one is evidence-only and stays in artifacts)
