# R35Audit49 — canonical freeze history audit (w1, mutation-tester seat)

Scope: provenance and integrity of `.ufo/waves/round-35/claims-canonical.json` (the canonical
freeze) and its instruments. Lane read-only except this report; all git use read-only
(`log`/`show`/`ls-tree`/`merge-base --is-ancestor`/`status`); mutation probe ran on a
disposable `/tmp/r35audit49/` copy. No counters executed; no lane production bytes touched.

## Freeze timeline (all 2026-10-25 -03:00, verified via `git log -- <path>` / `git show --stat`)

| commit | time | event |
|---|---|---|
| `aa04633a` | (plan base) | base revision; counters absent from `tools/round-35/` |
| `d2729cba` | 16:05:46 | instruments-first prep; **first ADD of both counters** (c1=`cd4ab7e7…`, c2=`39fe39c5…`); recorded as `instrument_revision` |
| `131eacfa` | 16:05:56 | first add of draft `claims.json` |
| `a5445232` | 16:06:28 | draft claims container completed |
| `13d7a815` | 16:07:04 | "F3": draft `claims.json` removed; `claims-frozen.json` first added |
| `6c2497a2` | 16:07:12 | re-pin of frozen claims |
| `50174048` | 16:07:16 | `claims-frozen.json` removed to re-add |
| `e4ca43dd` | 16:07:45 | `claims-frozen.json` re-added; pins `d49ff16a…`/`c0f37d21…` |
| `f1ea3a6d` | 16:10:02 | pins updated to `018e96d0…`/`3a23f3eb…` — bytes **not yet in any committed tree** |
| `a85ca674` | 16:10:48 | commits counter bytes `018e96d0…`/`3a23f3eb…`; freeze-status gate-failure receipt; `claim-freezes.tsv` row 22 (FLAGGED) |
| `2a51d561` | 16:12:06 | draft pins updated again to `a4be290a…`/`f36fad30…` — pair **never exists in any committed tree** (draft-only) |
| `2323d197` | 16:13:40 | **canonical freeze**: first+only add of `claims-canonical.json`; same commit carries final counter bytes `e28792c7…`/`576c14dd…` (9- and 11-line edits) |
| `ee0c865c` | HEAD | 0 commits after `2323d197` touch `tools/round-35/`, the canonical file, `freeze-status.md`, or `claim-freezes.tsv` |

## Invariants checked

- **INV-1 post-freeze immutability — HOLDS.** `git log --diff-filter=A` → sole ADD `2323d197`;
  `git log 2323d197..HEAD -- <canonical>` → empty; `git status --porcelain` on the file → clean;
  worktree sha256 `1b9855409896d00609174b469a1969167ece856a9dc2a069ecc5347c12627f27` ==
  `git show 2323d197:.ufo/waves/round-35/claims-canonical.json` blob hash.
- **INV-2 pin == committed bytes — HOLDS at the canonical freeze.** All four pins match both the
  `2323d197` tree and the worktree: c1 `e28792c7e54fcfa2…`, c2 `576c14dd95c0a54b…`,
  `plans/round-35-claims.md` `45b644a44851b830…`, `census-start.txt` `b6ce2b1773c60af4…`.
  Ancestry: base `aa04633a`, `instrument_revision` `d2729cba`, supersession commit `a85ca674`
  all ancestors of `2323d197` (`git merge-base --is-ancestor` → ok).
- **INV-3 instruments committed before claims — VIOLATED for the canonical snapshot (strict
  sense), disclosed as setup debt.** The pinned final counter bytes first exist in the *same*
  commit `2323d197` that first adds `claims-canonical.json`; no earlier tree contains them.
  Mitigations present: `freeze-status.md` honest freeze-gate FAIL (`INSTRUMENT_REVISED`),
  tsv row 22 `FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED … not a claim measure or data event`,
  commit message "setup defects disclosed".

## Defects found (advisory)

- **D-A supersession pointer imprecise.** `instrument_supersessions` cites `a85ca674` for both
  counters, reason "finalized freeze-read path and green/red selftest before control/data score",
  but the `a85ca674` tree holds intermediate bytes `018e96d0…`/`3a23f3eb…` ≠ pins. The commit
  whose tree actually carries the pinned bytes (`2323d197`) is named nowhere in the canonical
  record; tsv row 22 independently says "superseded at `f1ea3a6d`" — three different commits
  across record layers, none self-consistent as "the commit with the final bytes".
- **D-B canonical freeze not reflected in record files.** `2323d197` updated neither
  `freeze-status.md` nor `claim-freezes.tsv` (0 touching commits after it); row 22 predates the
  canonical freeze and points at the draft supersession only.
- **C (coverage gap, the challenge target):** no lane instrument validates
  `instrument_supersessions` pointers or that pins exist in a pre-claims tree; a mutant record
  pointing supersession at an arbitrary commit would survive every gate I can see. Draft lineage
  confirms the hazard was real: `claims-frozen.json` pinned `a4be290a…`/`f36fad30…` at
  `2a51d561`, bytes that never existed in any tree.
- Note: `claims-canonical-note.md` is untracked (no commit history); the canonical freeze event
  itself is VCS-evidenced only via commit `2323d197`.

## Mutation probe (role)

Invariant challenged: "post-freeze byte tampering of the canonical freeze is detectable."
Detector (bounded): `sha256(scratch copy) == sha256(git show 2323d197:claims-canonical.json)`.

| state | scratch sha256 | detector |
|---|---|---|
| pristine | `1b9855409896d006…7c12627f27` | MATCH |
| mutant (C1 pin `…28d24220`→`…28d24221`, 1 hex digit) | `ab7e9443aa2e1c89…62df4a1425` | MISMATCH — **KILLED** |
| restored (exact pristine bytes recopied) | `1b9855409896d006…7c12627f27` | MATCH |

Restoration evidence: post-restore hash identical to pristine and to the `2323d197` blob;
scratch dir `/tmp/r35audit49/` (disposable); lane worktree and VCS unmutated throughout.

## Limits

`freeze-integrity.py` not re-run by this seat (freeze-status records its FAIL at `f1ea3a6d`;
no record of a re-run at `2323d197` was found — absence of re-run is an observation, not proof).
Counters' behavioral verdicts (C1/C2 red/green, stops at HEAD `ee0c865c`) belong to other seats.
jj metadata not inspected (git sufficed). Everything above is command output or arithmetic on
hashes; no inference beyond noted coverage gap.
