# ConnCorrectionPlacement — append-only placement for the four r17 routed corrections

Seat: `KaidokuR18.ConnCorrectionPlacement` (author-side advisory, leaf). Read-only except this file.
No tools installed. All commands below were run read-only from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; exit codes are the observed ones.

## Verdict

All four corrections are dischargeable by appends. They take **four append units**, and the only
non-append write among them is one restored manifest line:

| # | Site | Append unit | Current EOF / slot |
|---|---|---|---|
| 1 | `LOG.md` | one new `## 2026-10-20 — round-18 …` entry | after line 2123 (last byte `\n`) |
| 2 | `SCORECARD.md` | one new `## Round 18 — …` section; corrections are a `### Routed r17 corrections (append-only)` subsection inside it | after line 2426 (last byte `\n`) |
| 3 | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` | one new `## Round-18 correction …` section | after line 198 (last byte `\n`) |
| 4 | `corpus/QUALITY.md` | one new admission-table row 21 | inserted after line 30, before the blank line 31 |

The single sanctioned non-append is the one restored `carriers.tsv` line in
`.ufo/waves/round-17/predictions/SHA256SUMS` (contract §Shared outputs allows "W17 predictions
identical except the restored SHA256SUMS line"). Nothing else may move.

**Line discipline (the trap):** every mechanical C1 check is *line-scoped* — "has a line containing
`R17-PINMAP` and `comparator verdict`" (contract §C1). The ledger's body prose wraps at ~78 columns,
which would split the tokens across lines and fail every check while reading correctly. Each named
correction must therefore be emitted as **one unwrapped line**, exactly as the r17 R16-PROVENANCE
entries were (`LOG.md:2059-2062`, 100–150 chars each).

## Evidence (observed)

| Fact | Command | Exit | Result |
|---|---|---|---|
| No r18 section exists yet in either ledger | `grep -n 'round-18\|Round 18' LOG.md SCORECARD.md` | 1 | no matches |
| LOG EOF / SCORECARD EOF | `wc -l LOG.md SCORECARD.md` | 0 | `2123`, `2426` |
| Both end in newline | `tail -c1 LOG.md \| od -An -c` (same for SCORECARD) | 0 | `\n` |
| R17 sections | `grep -n '^## Round 17' SCORECARD.md`; `grep -n '^## 2026-10-20 — round-17 measured' LOG.md` | 0 | `2350`, `2069` |
| Knowledge entry EOF / last section | `wc -l corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`; `grep -n '^## ' …` | 0 | `198`; `## Not examined` at `181` |
| Pin sentence span | `grep -n 'each pin map\|maps are equal' …` | 0 | `30`, `32` (sentence runs 30–32) |
| QUALITY table end | `grep -n '^\| 20 \|^## Signals' corpus/QUALITY.md` | 0 | row 20 = line 30; `## Signals` = line 32 |
| SOURCES registry end | `sed -n '38,40p' corpus/SOURCES.md` | 0 | S032 = line 38, blank 39, `## Paths` 40 |
| SUMS lost the carriers line at `95e34db` | `git show 95e34db --unified=0 -- …/SHA256SUMS \| grep carriers`; presence spot-checks at 2711674/da64646/d0ab299 | 0 | diff line `-8ac38afe…  predictions/carriers.tsv`; present at 2711674 and da64646, **ABSENT** at d0ab299 |
| SUMS file history | `git log --oneline -- .ufo/waves/round-17/predictions/SHA256SUMS` | 0 | touched only by `95e34db`, `2711674` |
| carriers.tsv sha at REV | `git show 9011581:.ufo/waves/round-17/predictions/carriers.tsv \| sha256sum`; `sha256sum …/carriers.tsv` | 0 | `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5` both |
| All present SUMS entries resolve | Python read-only rehash of the 17 listed paths | 0 | `entries 17 ok 17 bad []`; `carriers.tsv covered: False` |
| Pass-1 run-log is 7/8, no exit line | `git show da64646:.ufo/waves/round-17/runs/run-log.txt \| cat -n` | 0 | 14 lines = 7 start/end pairs (`calib-shfmt` absent), no final exit line |
| Pass-2 run-log is 8/8 + exit | `cat -n .ufo/waves/round-17/runs/run-log.txt` | 0 | 18 lines, `run-carriers exit=0` |
| Receipt counts | `git ls-tree -r --name-only <rev> -- .ufo/waves/round-17/runs \| grep -c receipt.json` | 0 | `8` at `da64646`, `8` at `9011581` |
| Validator coverage | Python read of `verification.json` `commands[].label` | 0 | exactly 8 `receipt-validate-*` (one per label), all against the receipts committed at `d0ab299` |
| Receipt shapes | Python: `receipt['steps']['analyze']` keys at both revisions | 0 | `da64646`: **no** `pin_checks` (pre/post only); second pass (`d0ab299`): 3 checks of `{equal, entries:146, changed, missing, taken_at_utc}`; no `md5` key at either revision |
| Pin scope excludes the producer | Python: `pins_pre.entries` keys | 0 | 146 paths; includes r16 `selection.py`; no `carrier-run.py` |
| Producer chronology | `git log -1 --format='%H %cI' 95e34db` vs run-log start | 0 | `95e34db` 14:27:35Z, pass-2 run starts 14:27:41Z (6 s later) |
| Pass-2 receipts introduced at `d0ab299` | `git log --oneline -- .ufo/waves/round-17/runs/pro-aether/receipt.json` | 0 | `d0ab299`, `da64646` |
| Additive-correction precedent (knowledge) | `git show --stat 856d193 -- corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` | 0 | `1 file changed, 23 insertions(+)`, **0 deletions**; section at line 108 of 129 (appended at EOF) |
| Ledger-correction precedent | `sed -n '1749,1750p' LOG.md`; `sed -n '2162,2163p' SCORECARD.md` | 0 | `## … post-review correction (append-only)`; `## Post-review correction — arc3-loop1-round13 (append-only, 2026-10-19)` |
| Pointer-table line pins | Python read of `.ufo/gates/citation-drift/pointer-table.json` | 0 | `exact` pins into `SCORECARD.md` at 59/60/68/270/622/699/1338/1419; one `extracted` entry whose target line is `LOG.md:254` |
| Status enum | `grep -n 'status enum\|queued|mined|rejected' scripts/sources-census.sh` | 0 | `queued\|mined\|rejected` only — there is no `superseded` status |

The r17 routing text is `corpus/lessons/round-17-verifier-spotcheck.md:137-143` (defects 1–4 at
137, 138, 139, 140–143). Contract checks that consume the placement: `contract.md` §C1.

## Placement matrix (the deliverable)

`R` = required by a §C1 check; `o` = optional, omit unless wanted.

| Correction | `LOG.md` (round-18 entry) | `SCORECARD.md` (Round 18 §) | r17 knowledge entry | Other |
|---|---|---|---|---|
| R17-PINMAP | — | **R** (`R17-PINMAP` + `comparator verdict`) | **R** (same two tokens) | QUALITY row 21 (**R**, why-cell) |
| R17-VALIDATE16 | **R** | **R** | — | new `W18/evidence/validate16/summary.json` (not a rewrite) |
| R17-PRODUCER-REV | o | **R** (`R17-PRODUCER-REV` + ≥2 distinct 40-hex) | **R** (same) | — |
| R17-SUMS-RUNLOG | **R** (`R17-SUMS-RUNLOG` + `7/8`) | o | — | one restored line in `predictions/SHA256SUMS` |

Rationale for the split: the correction goes where the superseded text lives. The pin-map sentence
lives in `SCORECARD.md:2374` and knowledge lines 30–32; the "16 receipts" claim lives in
`SCORECARD.md:2364` and `corpus/lessons/round-17.md:122` (lesson = never rewritten, so LOG carries
the correction); the producer sentence is the SCORECARD baseline paragraph `2352-2355` plus the
knowledge entry's opening; the SUMS/run-log defect is a LOG/evidence matter. `LOG.md:2106`'s own
"8/8 `receipt-validate` exit 0" was **true** at r17 — do not imply LOG was wrong; target
`SCORECARD.md:2364` / `round-17.md:122` by name.

## Exact append points and text

### 1. `LOG.md` — append after line 2123

One new entry; add a correction block under an `R17 corrections (append-only):` lead. Three
single unwrapped lines (second is the fourth defect):

```text
- R17-VALIDATE16: the r17 claim "all 16 receipts `receipt-validate.py` exit 0" (SCORECARD.md:2364; corpus/lessons/round-17.md:122) is corrected: r17's verification.json holds 8 `receipt-validate-*` runs, one per label, against the 8 receipts committed at d0ab2992149a38794e5ef2474ba5d4ef5ee1e905; the 8 receipts retained at da64646adcb19c1ede7537b799b8c7d283fe43da were not validated in r17 and are validated in round 18, evidence .ufo/waves/round-18/evidence/validate16/summary.json.
- R17-SUMS-RUNLOG: `.ufo/waves/round-17/predictions/SHA256SUMS` lost its `carriers.tsv` line at 95e34db62f2693c455d7ee4dfef24b8f3ebc007d (present at 271167473d87ef710f07ecdd98caf0ce12091686 and da64646); round 18 restores the single line `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv`, after which the manifest resolves 18/18 (17/17 present entries rehashed first). The pass-1 `.ufo/waves/round-17/runs/run-log.txt` at da64646 lists 7/8 carriers (calib-shfmt absent) and has no final exit line; it is retained unedited.
- R17-PRODUCER-REV: pass-1 receipts retained at da64646adcb19c1ede7537b799b8c7d283fe43da record no producing tool revision; pass-2 receipts (14:27:41–14:40:02Z) were produced by 95e34db62f2693c455d7ee4dfef24b8f3ebc007d's `carrier-run.py` and retain no `carrier.md5_pre`/`binding.md5_ok`; d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 is the verification revision (evidence b31975de62de5413a6f2d244f2690eaeb3d18c25), not a receipt producer.
```

(The R17-PRODUCER-REV line is optional per §C1; include it if the round entry is to be the single
producer map. If omitted, `LOG.md:2071`'s "source revision" phrasing stays as-is.)

### 2. `SCORECARD.md` — append after line 2426

New section `## Round 18 — <L1 title>, 2026-10-20`; after its claims table, before
`### Capability addition`:

```text
### Routed r17 corrections (append-only)

- R17-PINMAP: supersedes SCORECARD.md:2374's "pre/mid/post pin maps with instants" and corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32's "each pin map is retained … All maps are equal": each r17 mid-run instant retains the comparator verdict against the retained pre map — {equal, entries, changed, missing, taken_at_utc} — not a per-path map (`runs/pro-aether/receipt.json` `steps.analyze.pin_checks`, 3 instants × 146 entries). QUALITY #19's per-instant map is met from round 18 only by `carrier-run.py` writing `pins/mid-<n>.json` + `map_sha256` (contract C3); that does not retroactively evidence the r17 instants.
- R17-VALIDATE16: supersedes SCORECARD.md:2364's "all 16 receipts `receipt-validate.py` exit 0" and corpus/lessons/round-17.md:122's "All 16 receipts pass the final validator": r17 ran the validator 8 times, against the 8 receipts committed at d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 only; the 8 retained at da64646adcb19c1ede7537b799b8c7d283fe43da were never validated in r17. Round 18 validates those blobs; the observed exits and the run revision live in .ufo/waves/round-18/evidence/validate16/summary.json, which is this correction's evidence.
- R17-PRODUCER-REV: the second-pass receipts (14:27:41–14:40:02Z) were produced by 95e34db62f2693c455d7ee4dfef24b8f3ebc007d's `carrier-run.py`, committed at d0ab2992149a38794e5ef2474ba5d4ef5ee1e905; they lack `carrier.md5_pre`/`binding.md5_ok`, added to the tool before that commit. Pass-1 receipts are retained at da64646adcb19c1ede7537b799b8c7d283fe43da and record no tool revision in their 146-path pin map (r16 `selection.py` is pinned; `carrier-run.py` is not). d0ab299 is the verification revision, not a receipt producer; b31975de62de5413a6f2d244f2690eaeb3d18c25 is its evidence revision.
```

`SCORECARD.md:2374` and `:2364` remain untouched; these lines point at them.

### 3. `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` — append after line 198

Heading in the r14 precedent's form (`856d193`, `## Round-15 advisory-pointer correction`,
+23/−0): `## Round-18 correction — mid-run retention and producer revision (append-only)`, then two
single unwrapped lines: the **R17-PINMAP** and **R17-PRODUCER-REV** lines above, first-person to the
entry ("this entry's meter sentence on lines 30–32 is superseded…"). The entry keeps a line carrying
both `R17-PINMAP` and `comparator verdict`, and a line carrying `R17-PRODUCER-REV` with the four
40-hex hashes. Lines 1–198 stay byte-identical.

### 4. `corpus/QUALITY.md` — append row 21 after line 30

Not a correction entry: it is the *criterion* C1 turns the partial disagreement into. Rows 1–20 are
byte-identical (controls.py's `QUALITY rows 1–20 identical`).

```text
| 21 | A retention claim names the artifact retained, not the act of comparison: "the map is retained" requires the per-path map (or its digest) at each named instant; a comparator verdict `{equal, entries, changed, missing, taken_at_utc}` supports only "the comparator found no change against the retained pre map at instant t", never "the map is retained", and "all maps are equal" requires each map to be individually retained. | `corpus/lessons/round-17-verifier-spotcheck.md:137`, `R17-PINMAP` | sharpens 19 |
```

### 5. The one restored manifest line

`.ufo/waves/round-17/predictions/SHA256SUMS`: insert exactly
`8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv`
at its alphabetical slot (current line 5, between `calib-shfmt.prediction.json` and
`pro-aether.inspect-go.json`). Do **not** regenerate the file: 17/17 present entries already verify;
regeneration can silently reorder or reformat. Verify with a copy: `cd …/round-17 && sha256sum -c
predictions/SHA256SUMS` → 18/18 OK.

## Never rewritten (byte-identical, or old-prefix only where stated)

| Path | Constraint | Reason / anchor |
|---|---|---|
| `LOG.md:1-2123` | old-prefix (append after 2123 only) | `PROTOCOL.md:123-125`, `:463`; `controls.py` old-prefix; `extracted` citation target `LOG.md:254` |
| `SCORECARD.md:1-2426` incl. `:2364`, `:2374` | old-prefix (append after 2426 only) | same; exact pins at SCORECARD 59/60/68/270/622/699/1338/1419 |
| `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1-198` incl. `:30-32` | old-prefix | `CORPUS.md:53-60`; controls.py names this one file as the only appendable knowledge entry; precedent `856d193` |
| `corpus/lessons/round-17-verifier-spotcheck.md` | byte-identical, whole file | verifier/lesson; `CORPUS.md:53-60`; controls.py "prior … verifier files byte-identical"; do not annotate it |
| `corpus/lessons/round-17.md` | byte-identical, whole file (esp. `:122`) | lane lesson; controls.py; the claim is superseded by the new entries, not edited |
| `.ufo/waves/round-17/runs/**` (16 `receipt.json`, logs, `run-log.txt`) | byte-identical | evidence standard; contract non-goals; validator re-runs must materialize `git show` blobs into a new dir |
| `.ufo/waves/round-17/verification.json` | byte-identical | 79-command retained record; r18 validator evidence is a **new** file |
| `.ufo/waves/round-17/final-recheck/**` | byte-identical | retained verdicts |
| `.ufo/waves/round-17/predictions/*.json`, `carriers.tsv` | byte-identical | frozen inputs; only `SHA256SUMS` gets the one restored line |
| `corpus/SOURCES.md` S001–S032 evidence cells | append-only: only `status`, `recheck`, `used-by` change in place, each logged old→new | `CORPUS.md:116-118`; S032's unreproducible digest sits in its `anchor` cell, which therefore cannot be fixed — it takes a new S033 row with `teaches` opening `supersedes S032 —` and `fetch-time` in the anchor (contract §C1 R17-S032-DIGEST), inserted at line 39 |
| fleet root `PROTOCOL.md`, `PROTOCOL-APPENDIX.md`, `CORPUS.md`, `AXES.md`, `MISSION.md`, `ROADMAP.md`, root `SCORECARD.md`/`LOG.md`, `scripts/`, `templates/` | never lane-written | `PROTOCOL.md:465-469`; corrections are named in the lane report |
| `SHONEN.md` | template-regenerated only; no `[x]` | `PROTOCOL.md:432` (canonical form); claims `non_goals` |

Adjacent, out of this assignment's four: `R17-REGISTRY` is the one defect that is **not** an append —
the five `SKILL.md` registry rows are an instrument registry and are repaired in place (round-17
precedent, `LOG.md:2062-2063`), with the skill's round-18 section appended.

## Contradictions stated, not smoothed

1. **Readability vs the check.** Ledger prose wraps; the checks require two tokens on one line.
   Resolution: named correction entries are single lines (`LOG.md:2059-2062` precedent); body prose
   may still wrap.
2. **"All 16 validated" can become true only via round 18.** The lesson offers "correct the count to
   8 **or** retain the validator run"; the contract chooses retention. So the honest text is "8 were
   validated at r17; the other 8 at r18, evidence X", never "all 16 passed at r17". The
   round-17 lesson and the r18 summary must not be merged into one claim.
3. **PRODUCER-REV cannot fully name pass 1.** Its receipts pin `selection.py` but not
   `carrier-run.py`; no tool hash exists in the artifact. Naming `2711674` as pass-1 producer is
   [INFERENCE] from chronology (committed 57 s before the run start) and is not asserted here. The
   correction states the gap; inventing a hash would be a new overclaim.
4. **SCORECARD home underdetermined by the checks.** §C1 passes with the line anywhere. I place it
   inside the Round 18 section because C1 is this round's claim; the r13-style standalone
   `## Post-review correction` (`SCORECARD.md:2162`, `LOG.md:1749`) is the form for a correction
   that arrives *after* the round entry is committed. Do not create both.

## Affected axes

- **calibration (primary).** Three overstatements become named, line-anchored corrections in the
  files that carry them, and each is machine-checkable at REV (`routed-defects.py`), so closure
  cannot silently re-launder them. QUALITY 20→21 adds the criterion the outside partial
  disagreement asked for, with the lesson anchor in the why-cell.
- **operability (secondary).** One append point per file, single-line entries, one manifest-line
  restore with a rehash check, and a validator re-run materialized into a new evidence path. No
  pointer-table line moves, so `citation-drift` stays clean without re-pinning.
- **depth: unchanged.** No carrier is re-analyzed and no r17 mechanism is re-asserted; the
  corrections only bound what the retained artifacts support. Nothing here weakens C3.

## Proposed move (one bounded)

Adopt the placement matrix above as the round's correction contract, and emit **all four named
corrections as single unwrapped lines at the four append units**, with the QUALITY row as the only
table-row insert and the one `carriers.tsv` manifest line as the only non-append write. This satisfies every §C1 line check by construction and keeps every existing byte and every
pointer-table line number fixed.

## Risks

1. **Write-before-measure.** `R17-VALIDATE16` would be false if written before the da64646 validator
   run. Sequence: run → write `summary.json` → write the ledger line.
2. **Restore by regeneration.** Re-running `sha256sum` over the directory can change unrelated lines;
   insert the one verified line only.
3. **Line wrapping.** Any editor reflow that splits a correction line breaks the check while leaving
   the prose correct. Re-run `routed-defects.py` after write.
4. **Second-order, for the L1:** the r18 carrier run pins `swiss-misread.py` and inputs but not the
   producer (`carrier-run.py`, `receipt-validate.py`, `run-carriers.sh`), so the PRODUCER-REV class
   recurs for r18's own receipts. Additive remedy with no contract change: record
   `producer: {path, sha256}` in each receipt (or in `run-log.txt`'s argv line). Advisory only.
5. **S032 status.** The census enum is `queued|mined|rejected`; do not write `superseded`. The S033
   row's `teaches` prefix carries the supersession.

## Verification for the L1 (once, after all writes)

```sh
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev <REV> --strict   # 0, open_count 0
python3 -I -B .ufo/waves/round-18/tools/controls.py <BEFORE> <AFTER>                      # no-harm
git show <BEFORE>:LOG.md > /tmp/pre-log && cmp -n "$(stat -c%s /tmp/pre-log)" /tmp/pre-log LOG.md
git show <BEFORE>:SCORECARD.md > /tmp/pre-sc && cmp -n "$(stat -c%s /tmp/pre-sc)" /tmp/pre-sc SCORECARD.md
git show <BEFORE>:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md > /tmp/pre-kn \
  && cmp -n "$(stat -c%s /tmp/pre-kn)" /tmp/pre-kn corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
(cd .ufo/waves/round-17 && sha256sum -c predictions/SHA256SUMS)                            # 18/18 OK
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV>       # 0 (pins unmoved)
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku  # ok
```
