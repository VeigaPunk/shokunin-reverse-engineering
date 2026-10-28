# R49-C2 pre-freeze attack — C2CounterMut (wave 1, seat `C2CounterMut`)

## Verdict

**Not freeze-ready as drafted: fold in findings F1–F4 before the freeze, or disclose them as limits.**
The counter behaves as the plan predicts on the green fixture (exit 0, `mismatches 0`, battery 11/11 each turning exactly its own atom red, do-nothing 9/9 red) and at FREEZE (exit 1, `mismatches 9`). But:

- **12 of 56 designed fixture forgeries pass all nine atoms** (exit 0 at REV): an invented dead hash (A2), an empty placeholder report (A4), a re-pinned fabricated snapshot (A6), an inflated `identified` count (A8), a rewritten historical SCORECARD freeze (A1), a rewritten round-48 receipt (A5), a substring-suffixed A9 line, a dropped pointer (A3). Ten of the twelve also pass `--battery`.
- **Source mutants: 56 designed, 51 killed, 5 survive.** The shipped battery and genuine runs kill 13 (one of them, M55, only with a deliberately broken battery); the freeze run kills M42; forgeries alone kill 37. The 5 survivors are M05, M38, M40, M43, M44 — four are equivalent under the rest of the counter, and M05 cannot be exercised by any fixture in the lane's history.
- Doc/counter disagreement: the A8 docstring says "every number is re-derived from the registry"; `identified`/`screened` are not re-derived (F06 accepts an inflated value).

No tool was installed or upgraded. The lane tree, drafts, plan, `SCORECARD.md`, `LOG.md`, `corpus/` and `tools/` were not written; all mutants and forgeries live in a scratch clone (`/fast/scratch/hyaku/kaidoku-r49/C2CounterMut/clone`, a `git clone --shared` of the lane, identity `r49-dev` set in the clone only; toplevel asserted before every commit), removed after copying receipts.

## Setup and baseline (all runs use the draft counter, sha256 `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`, byte-identical to the draft `tools/round-49/c2-mismatch.py`)

| step | command (exact) | exit | result | stdout sha256 |
|---|---|---|---|---|
| dev freeze | `bash .ufo/waves/round-49/draft/mkclone.sh /fast/scratch/hyaku/kaidoku-r49/C2CounterMut/clone` | 0 | `DEV_FREEZE=dc6b13fed334a7f771d10f687ccd5798a80f9c6e` | — |
| green fixture | `python3 .ufo/waves/round-49/draft/c2-after.py <clone>` | 0 | `DEV_AFTER=ed537b258e4439c88e9f596ad8504a4cacd89456` | — |
| at freeze | `python3 -I -B c2-mismatch.py --root <clone> --rev dc6b13fe… --freeze dc6b13fe… --json-out …` | 1 | `mismatches 9`, all nine atoms red | `96fb515752741c88b525745231c9cb01d9dafb7ca193e08daa19749e091816d4` |
| green, no battery | `… --rev ed537b25… --freeze dc6b13fe…` | 0 | `mismatches 0`, `atoms_total 9` | `0b3729e7f309a2b77f3d46b26eaaa8114c2e151e645e668c2e771d38dff6fab2` |
| green, battery | `… --rev ed537b25… --freeze dc6b13fe… --battery` | 0 | `mismatches 0`, `battery.failing []`, 11 mutations each `ok`, do-nothing overlay (5 paths restored) red = A1–A9 | `6d57212392f46bf86bc5f3359b24c61ddac435f4e0e2968532265a7a236b6a7f` |
| base revision | `… --rev e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9 --freeze dc6b13fe…` | 2 | `freeze is not an ancestor of rev` | in `runs/base.ORIG.stdout` |

Consistent with the plan: the do-nothing overlay (5 changed paths restored to FREEZE) is all nine red; the eleven battery overlays are each exactly one red atom, none a no-op.

Limits of this seat's evidence: per-run UTC times were not captured by the driver; the final batch (56 forgeries, 58 counter variants × states) started `2026-10-28T21:21:09Z` (`batch2.utc`). An earlier batch with 54 forgeries was superseded by this one before any result was cited; its receipts were overwritten and are not cited. All counter runs used `python3 -I -B`, the clone as `--root`, and a `--json-out` under the scratch dir.

## Findings (ordered; exact evidence in `w1/C2CounterMut/`)

### F1 — the record is not pinned: accepted forgeries of round-48 inputs (must fold in or disclose)

| forgery | what changed (right strings, wrong facts) | ORIG exit | ORIG red | battery exit |
|---|---|---|---|---|
| F08 | SCORECARD `## Round 48` `**Declared freeze:**` rewritten `b6f7ca2a…` → `61b87d74…`; A1 line restated to match | 0 | none | 0 |
| F09 | `.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json` rewritten (a space added before the final newline); A5 digests re-derived and restated | 0 | none | 0 |
| F07 | A9 line `… calibration=harmed (superseded: calibration=improved)` | 0 | none | 0 |
| F01 / F10 | A3 pointer `log_33f65a91` dropped / unnamed list drops `8847042a` | 0 | none | 0 |

Cause: the round-48 closure, the round-48 receipts and SCORECARD's Round-48 section are read at REV with no check that they equal their base content (A1 checks only the lesson header; A5 derives digests from whatever bytes sit at REV; A9 is a substring match). Fix: compare the round-48 inputs to base blobs (or to the base section text) and require the A9 line to match exactly, not as a substring.

### F2 — "right strings, wrong facts" in the snapshots and the teaches cells

| forgery | change | ORIG exit | ORIG red |
|---|---|---|---|
| F04 | `corpus/evidence/round-49/c2/popper.html` gets an unverified paragraph; S147 sha256 pin re-written to match | 0 | none |
| F05 | S148 teaches `supersedes S146 — EX_USAGE is 2, not 64` | 0 | none (battery exit 1: "mutation set incomplete: 10 of 11" — the battery's A7 mutation is keyed to the exact prose `EX_USAGE is 64`; the battery fails closed for a reason unrelated to the atom) |
| F06 | round-49 search-log `identified 2` → `identified 200` | 0 | none |
| F03 | empty `w1/C1Meaning.md` written; A4 restated `reports=73 missing=C1Battery,ScribeReportNumbers` | 0 | none |
| F51 | a `notes.txt` placed under `w1/C1Meaning/` (non-`.md`; accepted by the stated predicate, listed for completeness) | 0 | none |
| F02 | A2 `dead=663f30ee` + 32 invented hex (non-commit, same 8-hex prefix) | 0 | none |

Cause: the snapshot is self-attested (sha256 pin in the row, no origin binding; the atom binds row↔snapshot, not snapshot↔SEP/man7). `teaches` is checked for tokens only, not for the claim. `identified`/`screened` are unverified although the docstring says "every number is re-derived". The dead-hash atom never reads the fleet report that cited it (the report lives outside the lane, so the atom cannot check it; the plan should say so). Fix (L1 decision): state in the plan's disclosed limits that snapshot bytes are self-attested and pin source URL and fetch date into the row; require `teaches` to contain the exact sentence `EX_USAGE is 64`; split the A8 claim into "rows and included/excluded are derived; identified/screened are reported, not verified"; require non-empty report artifacts.

### F3 — duplicate lesson lines: last line wins, so a wrong line hides behind a right one

F26: a wrong `- A2 dead=663f30ee… actual=663f30ee<c×32>` placed before the real line. `lesson_lines` overwrites on each duplicate (`out[m.group(1)] = kv`); ORIG exit 0, no red. The battery goes red only because its A2 mutation reads the first (wrong) line, so it turns no atom red (`red []`). Mutant M49 (first-wins) kills F26. Fix: reject a duplicate `- A<n>` key in the correction section.

### F4 — the shipped battery and freeze run cover a small part of the counter; the rest is reached only by forgeries the battery lacks

- Shipped battery + genuine kill: M09, M14, M15, M16, M19, M23, M27, M34, M35, M45, M46, M50, and M55 (M55 is M43 applied to a broken-battery copy). Freeze run kills M42.
- Forgeries alone kill 37 more (`matrix.txt`).
- The battery's snapshot mutations (A6 `empirical→empirica1`, A7 `EX_USAGE→EX_USAGF`) change bytes without re-pinning, so they are caught by the pin, not the content checks: removing the pin check (M21) is invisible to the battery and only F11 kills it; removing the `EX_USAGE 64` check (M26) only F14 kills it.
- No battery overlay for: A2 prefix/ancestor (M06, M07), A3 completeness/unnamed/first-line-only (M08, M10, M11), A4 seats/missing/reports (M12, M13, M50 only via battery), A5 raw/report prefix (M17, M18), A6 word limit / used-by / status / teaches prefix (M20, M22, M53, M54), A8 rows / included-excluded / duplicates / identified-vs-screened (M30–M33, M52), A9 source row / rejected token (M36, M37), S145 append-only (M51), S147 word limit A7 (M22b), S148 quote presence (M24b).
- The battery's A7 mutation keys on exact prose and fails with "mutation set incomplete" when the prose differs (F05); the battery should fail with a structured reason per missing mutation rather than shrinking the set.

Fix (before the freeze, since the battery is frozen with the counter): add one overlay per sub-check listed above, with re-pinned snapshot variants for A6/A7, and make a missing mutation target a red with its own reason.

### F5 — A8 round-48 reads zero rows silently if a revision is unreadable (code reading; NOT RUN)

`_derived` treats `r.show(rev, 'corpus/SOURCES.md') is None` as an empty registry (`registry_rows('')` → 0). If the base or tip commit were absent in a clone, the round-48 check would accept `rows 0 -> 0 … included 0 excluded 0`. Not executed (every revision exists in the lane). Fix: exit 2 when a registry blob is unreadable.

### F6 — docstring over-claims (plan/counter disagreement)

- A8 docstring: "every number is re-derived from the registry" — `identified` and `screened` are not derived (F06 accepted).
- A3 docstring: the pointer line "states, per hash, the full set of LOG.md line numbers … and the hashes the round-48 entry never named" — the counter checks only the stated hashes; an incomplete pointer set is accepted (F01).
- Plan A5 says the atom checks "which of them the round-48 report quoted"; the counter never reads a report (the report is in the fleet repo). Say so.

## Mutation results (56 source mutants; full table with file sha256 in `w1/C2CounterMut/tables.md`)

Each mutant is a single-point edit of the draft counter source (the exact old/new strings are in `w1/C2CounterMut/drive.py`, `MUT` list; each applied exactly once, verified by `compile()` and non-noop). Kill = the mutant's exit, mismatches, red set or battery differs from ORIG on at least one of: green run, green+battery, freeze run, or any forgery.

| class | count | killed by |
|---|---|---|
| all killed | 51 | shipped battery + genuine 13 (M55 via broken-battery pair); freeze run adds M42; forgeries alone 37 |
| survived | 5 | M05, M38, M40, M43, M44 (below) |

Survivors and why (exact diffs):

- **M05** (A2) `if r.is_commit(dead):` → `if False:`. Killable only by a *dead* 40-hex that resolves to a commit and shares its 8-hex prefix with the real commit. The lane's history has no duplicate 8-hex prefixes (537 commits in the clone and 1706 in the lane repo under `rev-list --all`; `uniq -d` empty in both), and constructing one needs ~2^32 commit hashes. **Survivor by construction**; disclose.
- **M38** (freeze) `if not r.ancestor(freeze, rev):` → `if False:`. At `rev = e4f2cfa5` (not a descendant) ORIG returns `freeze is not an ancestor of rev`; M38 returns `frozen_path_changed` (`blob changed: tools/round-49/c1-controls.py`). Exit 2 in both, so the exit contract is unchanged and only the reason text differs. Equivalent under the walk+blob backstop: a non-descendant revision carrying the frozen files must have a commit in `FREEZE..REV` that touches them.
- **M40** (freeze) `if p and r.show(freeze, p) != r.show(rev, p):` → `if False:`. Equivalent under the path walk: a frozen blob cannot differ between FREEZE and REV without a commit in `FREEZE..REV` touching the path (F25, a touched-and-not-restored tools file, gives exit 2 under M40 as under ORIG).
- **M43** (exit) `if b['failing']:` → `if False:`. Observable only when the battery is red; on the green fixture and on every forgery the battery result is not changed by M43. Killed only by the broken-battery pair (ORIG_BB exit 1 vs M55 exit 0). Disclose: the battery exit gate is untested by the shipped battery.
- **M44** (battery) `if red != sorted(ATOM_IDS):` → `if False:`. Equivalent in practice: every atom returns red when its round-49 line is absent, and at FREEZE every line is absent, so the do-nothing overlay cannot be green on any fixture of this round.

## Forgeries (56 designed, 12 accepted by ORIG)

Accepted by ORIG (atoms), with `--battery` exit: F01 0, F02 0, F03 0, F04 0, F06 0, F07 0, F08 0, F09 0, F10 0, F51 0; F05 1 and F26 1 (battery red only for the incidental reasons in F2/F3). The other 44 are rejected with the expected atom (A1–A9) or exit 2 `frozen_path_changed` (F23–F25: touched-and-restored and touched-not-restored frozen paths). Full list with reasons and stdout sha256 prefixes: `w1/C2CounterMut/tables.md`; raw receipts `w1/C2CounterMut/results-raw.json`; forgery definitions `drive.py` (`build_forgeries`).

## Recommended folds before the single freeze (each is a decision for L1)

1. A8: say the counter does not verify `identified`/`screened`; remove "every number is re-derived" from the docstring and the plan; or stop counting them.
2. Pin the round-48 inputs (receipts, closure file, SCORECARD round-48 section) to base content; make A9 an exact-line match.
3. Reject duplicate `- A<n>` keys (F26).
4. Snapshot self-attestation (F04): state it as a disclosed limit, and pin source URL + fetch date in the row.
5. Teaches cells: require the exact sentence `EX_USAGE is 64` (F05).
6. Non-empty report artifacts for A4 (F03), or disclose that placeholders count.
7. Battery: add the missing overlays listed in F4 and re-pinned snapshot variants; a missing mutation becomes a structured red.
8. A8/`_derived`: exit 2 on an unreadable revision (F5, not run).

Not run: the C1 counter, C1 controls, any data run, the landing text, and any check outside the two C2 drafts. No network access was used (the snapshots were read from the draft directory and pinned by sha256).

## Artifacts (`.ufo/waves/round-49/w1/C2CounterMut/`)

`drive.py` (mutant + forgery builder and runner), `analyze.py`, `analyze2.py`, `analyze.out`, `matrix.txt`, `tables.md`, `results-raw.json` (per run: exit, stdout/json sha256, red atoms, battery failing, runtime), `forgeries.json` (56 forgeries with commit hashes in the scratch clone and expectations), `kill.json`, `drive.err`, `batch2.utc`, `c2-mismatch.orig.py` (copy of the draft, sha256 `90fa4722…`), `mut/*.py` (56 mutant counters + ORIG_BB), `runs/` (base-revision ORIG and M38 receipts, freeze/green receipts).

Tooling: none installed, upgraded or removed on the host. The scratch clone and `$S` are removed after the receipts are copied.
