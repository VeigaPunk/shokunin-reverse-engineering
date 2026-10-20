# CriticC1Vacuity — can C1 pass on marker text without a real correction?

Seat: author-side advisory critic (not an outside reviewer). Baseline `b563c799d97774aae4351276fe43cb897311e349`.
Read-only. Git objects were read with `git show`/`git grep`. A Python simulation of the contract's rules ran in an eval kernel and wrote no files. No tools installed. No REA/Ghidra run. No W/tools existed when I checked (`W/tools` absent), so every finding targets the contract text, `contract.md:80-96` and `:12-20`, not executor code.
Axes impacted: **calibration** (all findings); depth none.

**Verdict:** Yes. As specified, both counters can reach their declared targets (`claims.json:13`) through marker text or deletion, with no real correction. The temporal sweep also misses real r16 sites. Every defect below can be fixed in the tool. None of them is a tradeoff the judge must reject, provided the corrections land.

## A. temporal-sweep (`contract.md:90-96`)

**A1. The regex and file set miss real r16 sites (OBSERVED).** I applied the contract regex to the five files at baseline. It finds **N=2** sites:
- `.ufo/waves/round-16/verification.json:419` `"pins_unchanged_during_run": true`
- `corpus/lessons/round-16.md:154` "All producer/fixture pins remained unchanged during execution."

It misses these r16 temporal assertions:
- `LOG.md:2012` (round-16 entry, heading `LOG.md:1978`): "Producer/fixture hashes remain unchanged **across** execution." The regex has no `unchanged across`.
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`: "Producer and fixture pins were unchanged during the run." Knowledge files are not in the site file set.
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60`: "Producer/input hashes stayed unchanged during execution." This is the "report" that `corpus/lessons/round-16-verifier-spotcheck.md:183` names. It is in the fleet repo, outside the lane's write scope.

So "N→0" can be reported while 3 of 5 known sites stay uncorrected.

Calibration counterpoint: the lesson at `:183` says the SCORECARD makes this claim. At baseline I found no temporal wording in SCORECARD's r16 section (2280-2348). The only related line is `SCORECARD.md:2299`, "Full producer argv/…/input hashes", and it makes no stability claim. Record "SCORECARD: no site found", and do not write a correction for a site that does not exist.

**A2. The correction predicate is a marker (contract text).** A site counts as "corrected" if any line contains `R16-PROVENANCE` plus the site's repo-relative path.
- One line such as `R16-PROVENANCE: corpus/lessons/round-16.md .ufo/waves/round-16/verification.json` corrects every site in both files.
- The line needs no line anchor and none of the required wording: "map matches committed source-revision blobs; temporal stability not evidenced" (`:183`).
- A correction keyed by path also covers sites added to that file later.

**A3. Deleting a site lowers the count.** The sweep reads a single `--rev`, so a site removed at AFTER disappears instead of counting as unqualified. The r16 controls protect only `LOG.md` as append-only, plus the lessons and knowledge directories (`.ufo/waves/round-16/controls.py:32-33`). `SKILL.md` and `SCORECARD.md` are not append-only-controlled.

**A4. `--extra ABS_FILE` reads the worktree, not REV.** An uncommitted scratch file containing marker lines can drive unqualified sites to 0. The result is unreproducible and has no blob identity.

**A5. Inflation (the opposite failure).** A correct r17 sentence that mentions the phrase gets counted as an unqualified R16 site, for example "carrier pins equal pre/post; not shown unchanged during the run". New r17 lines get mixed into the r16 N.

## B. invocation-audit (`contract.md:80-88`)

Simulated baseline classes. Rows are taken from SKILL.md where cell 2 matches the contract's kind pattern. "Exercised" means any `argv`/`orig_argv` in 12 receipt files: 50 argvs, from r14/r15/r16 `verification.json`, r15 `final-recheck.json` and interactive-r1 `gate-results.json`.

| Row | Class |
|---|---|
| `SKILL.md:447` | exercised_match |
| `SKILL.md:487` | exercised_match |
| `SKILL.md:506` | exercised_match |
| `SKILL.md:507` | exercised_match |
| `SKILL.md:448` citation-drift | unlabelled_variant |
| `SKILL.md:449` custody-pair | unlabelled_variant |
| `SKILL.md:450` quote-fidelity | unlabelled_variant |

This gives **M=3** (OBSERVED, simulation).

**B1. The "unexercised" label is satisfied by any occurrence of the word.** Appending "unexercised" anywhere in rows 448–450 gives M 3→0, and negated text such as "no unexercised variant remains" also counts. The audit also never checks the second requirement in `claims.json:12`(b), that the citation-drift row is re-exercised and its receipt retained. A labelled row 448 passes without that run.

**B2. Matching without an end anchor gives false provenance (OBSERVED).**
- Every exercised citation-drift argv ends in `--strict`: r14 `commands[8]`, r15 `commands[9]`, r15 final-recheck `commands[1]`, and r16 `verification.json` `commands[17]`. The advertised non-strict probe command has never been exercised.
- I rewrote row 448 as the absolute `-I` form without `--strict`. It matches r16 `commands[17]` under prefix matching and does not match under `$`-anchored equality.
- Probe and strict modes have different exit semantics (`SKILL.md:448`), so a prefix match would certify the wrong mode.

**B3. Interpreter normalization can erase isolation.** "Modulo leading python3/interpreter path" might be implemented to strip `-I`. In that case an isolated row and a non-isolated argv compare equal. This is exactly the R16-INVOCATION difference: `:184` contrasts r16's isolated absolute argv with the variant missing `-I`. Even with no flag stripping, a row aligned to the non-isolated r14/r15 argvs counts as exercised_match. That does not meet the claim's "isolated absolute argv".

**B4. A failed or invalid run counts as exercised.** The audit never checks the receipt's exit code or its file hashes. Two consequences:
- Any committed JSON that has an `argv` key and matches the filename glob counts, including fixture or tampered receipts.
- `retain.py` exits 0 for any child exit (`contract.md:28`), so a citation-drift run that exits 2 (could-not-evaluate) would "re-exercise" row 448.

**B5. Binary classes push toward false labels.**
- Row 450, absolutized, equals r14 `verification.json` `commands[7]` exactly (OBSERVED). It is a relative-path variant of an exercised command, not an unexercised one.
- Custody-pair (row 449) was exercised in arc3 r2. Its receipts are text v2 captures under `.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/receipts/*.v2.json` and carry no argv, so the filename glob cannot see them.
- Labelling either row "unexercised" would be a false statement that still gives M→0.
- Row 449's literal `[--label <L>]` cannot be matched by equality at all.

**B6. Scope escapes.**
- A row whose kind cell is `Tool/kaidoku`, `instrument / kaidoku`, or similar is invisible to the audit.
- Commands in cell 4 (self-invocation) and knowledge `recheck:` lines are not audited. Report them as `unaudited`, not as covered.

## C. pins.py / receipts (`contract.md:13-20`, `:106-108`)

**C1.** `equal` is defined only by sha256/size differences or errors (`:16`). A path present in PRE but absent from POST is not required to make `equal` false.

**C2.** Two empty snapshots compare as equal. `retain.py` with no `--pin` would write a receipt claiming "pins equal" with nothing pinned.

**C3.** `compare S S`, swapped PRE/POST, and POST copied from PRE all pass. Nothing requires `pre.monotonic_ns < post.monotonic_ns`, and nothing requires the child's start/end to fall between the two snapshots.

## D. QUALITY #19

The r16 pattern is presence-only (`.ufo/waves/round-16/measure.py:30,102,141`: `^\|\s*18\s*\|`), so any row 19 passes. Also, `corpus/QUALITY.md:28` (#18) already requires either a matching exercised invocation or an explicitly named unexercised variant. A row 19 that restates #18 adds nothing.

## Red-before cases the L1 must run

Each case runs at BEFORE (or on a fixture) and must show the stated result. Cases RB1, RB3–RB6, RB8–RB13 and RB15 fail the contract-literal tool; RB2 and RB14 are guard cases the contract tool already passes and must keep passing. Run them before trusting N→0 or M→0.

| # | Case | Required result |
|---|---|---|
| RB1 | sweep at `b563c799` | sites include `LOG.md:2012` and `knowledge/2026-10-20-r16-go-selection-preview.md:95`; the fleet report `:60` is listed as `out_of_lane`; N ≥ 4 in-lane, not 2 |
| RB2 | baseline correction leak (guard) | no correction lines at baseline: `git grep R16-PROVENANCE b563c799` hits only `round-16-verifier-spotcheck.md:183-184`, a routing note, not a correction file; 0 corrected sites; the contract tool already passes this — keep it passing |
| RB3 | fixture: AFTER LOG line `R16-PROVENANCE corpus/lessons/round-16.md` without the wording | `corrected=false` |
| RB4 | fixture: one line naming all site paths | corrects at most sites whose `path:line` it names |
| RB5 | fixture: AFTER deletes a BEFORE site from SKILL.md | reported `vanished`, counted unqualified (requires a BEFORE site set) |
| RB6 | `--extra /tmp/x` (uncommitted) | rejected or tagged `not_at_rev` and excluded from counts |
| RB7 | new r17 line with the phrase in negated form | reported as `new_at_rev`, separate from the R16 N |
| RB8 | audit fixture: row 448 + "no unexercised variant remains" | `unlabelled_variant` |
| RB9 | abs `-I` row 448 without `--strict` vs r16 `commands[17]` | no match (anchored equality) |
| RB10 | row with `-I` vs argv without `-I`, and the reverse | no match |
| RB11 | receipt argv equals the row but exit 2, or stdout sha tampered | not exercised_match (require exit in the row's success set + `receipt-validate.py` exit 0) |
| RB12 | `retain.py` receipt: `orig_argv` contains the child argv | wrapper `orig_argv` must not match row 448 |
| RB13 | row with kind cell `Tool/kaidoku` | counted or reported `unaudited` |
| RB14 | pins: mutate content keeping size; restore mtime via `os.utime` | exit 1 (sha), proving no size/mtime short-circuit; the contract-literal tool already passes this — guard against a size/mtime shortcut |
| RB15 | pins: POST missing a PRE path; empty snapshots; `compare S S` | exit 1 for each; empty snapshots and `S S` must not be reported as equal evidence |

## Smallest safe corrections

**Sweep:**
- Widen the phrase class: `unchanged (during|across|throughout)`, `(stayed|remain(ed)?|were) unchanged`.
- Derive the site files from the files touched by r16 commits, including knowledge.
- Add `--before REV` so BEFORE sites are carried forward and deletions are detected.
- Count a site as corrected only if one line contains `R16-PROVENANCE`, the exact `path:line@BEFORE`, and "temporal stability not evidenced".
- Exclude `--extra` from measured runs.
- Report the fleet report as an out-of-lane residual and correct it from the r17 fleet report.

**Audit:**
- Use `$`-anchored token equality and no interpreter-flag stripping.
- Use a structured label (for example `unexercised variant:` in cell 3), not the bare word anywhere in the row.
- Accept a matched receipt only if it passes `receipt-validate.py` and its exit is 0.
- Add an explicit assertion: row 448 is exercised_match against an r17 receipt whose argv contains `-I` and absolute paths, and the mode (probe vs `--strict`) is named.
- Add a `variant_of_exercised` class so rows 449 and 450 are not falsely labelled. Simpler alternative for row 450: absolutize the row so it matches r14 `commands[7]`.

**Pins:** missing or extra keys make `equal` false; require `count > 0`; require strictly increasing `monotonic_ns`; the validator checks pre ≤ child start ≤ child end ≤ post.

**QUALITY #19:** the measure requires the row to cite `corpus/lessons/round-16-verifier-spotcheck.md:183`.

## Searched (bounded)

- `git grep` at baseline over the whole lane for about 15 temporal phrasings: `unchanged during|across|throughout`, `stayed`/`remain(ed)` unchanged, `byte-stable`, `no drift`, `before and after`, and similar. 580 hits; I triaged the r16-scoped ones.
- The contract regex applied to the five site files.
- The full SKILL registry table at baseline.
- All 12 receipt JSONs matching the contract glob, every argv/orig_argv extracted and the contract classification simulated under two normalizations.
- The fleet report `round-16/kaidoku.md`.
- r16 `controls.py` and `measure.py`, and QUALITY rows 17–18.

Not searched: other fleet-repo files beyond the r16 kaidoku report.
