# EX-24 — command A invariance across EX-16's census edit

Seat EX-24 · chain c2 · role executor · wave `arc3-loop1-round2` · 2026-10-19.
Repo HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` at every measurement in this
artifact (no commits landed during the leg; parent integrates). Scratch:
`/var/tmp/ex24r2/` (never `/tmp`). No git mutation, no install, no custody-path
touch; repo reads only.

**Task (seat line):** command A invariance after EX-16's edit (poll) —
`corpus/knowledge` + README + craft section untouched — expect 82/82, 14/14
once C1's rule lands separately (run twice: pre/post C1 landing as available;
state which). Artifact: this file.

## 0. Verdict

**CONFIRMED for EX-16's edit, at every intermediate revision it passed through.**
Command A read 82/82 mapped, 13/13 rules, 10.0/10.0 coverage and depth at the
pre-edit instrument and at all 15 revisions written while the leg was open,
ending at EX-16's declared final `d0772ce8…`; all three command-A surfaces
are byte-identical pre/post; EX-16's
edit is confined to `.ufo/gates/c1-census-v10.py`; and the invariance is
structural — command A's measured read set contains zero paths under
`.ufo/gates/`.

**C1's rule-14 leg is a projection, not a live landing**: at report time the live
`SKILL.md` still carries 13 rules (C1's text is patch-text-only in the wave; only
the parent integrates `SKILL.md`). Applied to scratch copies of the canonical
patch text, command A reads **82/82, 14/14, 10.0/10.0** in every insertion form
tested. One nuance found and measured (the rule-13 seam, §6): only one insertion
form preserves rules 1–13 byte-identically under command A's block split — that
form is recommended to the integrator.

## 1. Method

Command A is run in two forms, both exactly as specified at `SCORECARD.md:92-123`
for the counting logic (`mapped` / `missing` / `dangling` / `citation_resolved_rules`
/ `coverage_score` / `depth_score`):

- **canonical** — the git-object read path verbatim (`git ls-tree` + `git show`
  at a revision). Used at HEAD `14b1682b` for the pre-state; the round's edits
  are uncommitted, so worktree measurement is the operative one for the
  after-states.
- **worktree variant** — identical logic, read path `.read_text()` on the
  worktree files (the only difference). Script: `/var/tmp/ex24r2/commandA.py`;
  archived in this directory's evidence copied from scratch.

Because a deleted knowledge file *normalizes away* in `coverage_score`
(10×81/81 = 10.0), invariance is asserted on the **full tuple**
(`mapped`, `knowledge_files`, `missing`, `dangling`, `citation_resolved_rules`,
`rule_blocks`, `depth_score`), not on the score alone — see the canary in §5.

## 2. Before → after — command A under EX-16's edit

Pre-state (12:01:29Z), canonical command A at HEAD `14b1682b`:

```
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
 "revision": "14b1682b1128d2e41085ebc79c9addeb8786d420", "rule_blocks": 13}
```

Worktree variant at the same instant: identical values. The census instrument at
this instant: sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`.

**The instrument moved 15 times while the leg was open.** Every distinct
revision was captured (15 s watcher, `cmdA-census-<rev>-<hhmmss>.json` in this
directory; consolidated in `revision-table.txt`):

| census revision (sha256[:16]) | first seen (UTC) | command A |
|---|---|---|
| `6f1d19ff4b0878ad` (pre-edit) | 12:01:29 | 82/82, 13/13, 10.0/10.0 |
| `7b5a0e88b0496a5e` … `82fb807e79963f6d` (7 revisions, incl. the one EX-18 and RV-4 name as the interim verified revision) | 12:05:10 – 12:06:55 | 82/82, 13/13, 10.0/10.0 |
| `762bfebe2a913d9c` … `df9ffdf963efa549` (6 revisions, per-file G2 floor merged from EX-14 variant B) | 12:10:10 – 12:11:56 | 82/82, 13/13, 10.0/10.0 |
| `a4c167631269e511` (interim) | 12:15:41 | 82/82, 13/13, 10.0/10.0 |
| `d0772ce892223690` — **EX-16's declared FINAL** (`seats/EX-16.md:15`, 610 lines) | 12:18:26 | 82/82, 13/13, 10.0/10.0 |

All 15 rows: `mapped=82, knowledge_files=82, missing=[], dangling=[],
citation_resolved_rules=13, rule_blocks=13, coverage_score=10.0, depth_score=10.0`.
Distinct tuples across the 15 snapshots: 1. Final re-check 12:21:12Z at the declared
final revision: unchanged; surfaces still identical to pre-state.

**Section identity pre vs post** (hashes of exactly the text command A reads,
built with command A's own split semantics; `section-hash.py`):

| surface | pre-ex16 | post-ex16 (stable `82fb807e`) | post-ex16 rev2 (`df9ffdf9`) |
|---|---|---|---|
| craft section sha256 | `5dff0b655cd4300fc613a1b88b8f33dfbb1b86b370f641d069ddf50eeefbcb87` | same | same |
| coverage-map section sha256 | `875128eef0b453d97c3f3562e34aee84513facb1e27678d1eafdb6382364359e` | same | same |
| 82-file knowledge tree digest | `32fad58e7813b5fde1bfec1cf016dfb05bf7d5bdff4ce42aaac3df9fba2be6ad` | same | same |
| `corpus/README.md` | `6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577` | same | same |
| `SKILL.md` | `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` | same | same |

`ALL_SECTIONS_BYTE_IDENTICAL: True` (json equality check over all seven fields,
including the 13 per-rule block hashes).

**Scope of the edit** — `git status --porcelain` at the post-EX-16 stable state:

```
 M .ufo/gates/c1-census-v10.py
 M .ufo/waves/arc2-loop1-round10/C3.md      <- pre-existing dirty path, carried round-1 debt
?? .ufo/gates/__pycache__/
?? .ufo/gates/custody-pair/                <- C3's EX-31 tool (other chain)
?? .ufo/waves/arc3-loop1-round2/
```

No file command A reads appears in the modified set.

## 3. Read-set closure (why the invariance is structural, measured)

Both read paths were instrumented:

- **worktree variant under `sys.addaudithook`** (`read-set.py`): 20 distinct
  paths opened — `corpus/README.md`, `SKILL.md`, and the 18 cited knowledge
  files; `paths_under_.ufo/gates: []`; top-level roots read: `SKILL.md`,
  `corpus`. Outcome: `read_set_excludes_gates: true`.
- **canonical variant** (recording every `git show <rev>:<path>`):
  `git_show_paths_total=51`, `unique_git_show_paths=20`, distinct roots
  `["SKILL.md", "corpus"]`, `paths_under_.ufo/gates: []`, `ls_tree` scope
  `corpus/knowledge` only.

EX-16's edit target is outside command A's read set by construction; the hash
identity in §2 is the empirical confirmation, not the argument.

## 4. Corroborating instrument health (not this seat's claim; measured anyway)

- Census ordinary run at revision `82fb807e…`: `VERDICT: PASS (stale=0
  ambiguous=0 undeclared=0 unresolved=0)`, exit 0, with the new lines
  `UNREADABLE (could-not-evaluate): []`, `G2 positive-assertion guard: ok
  (current-ok loci=5, total loci=17, floor=1)`, `DECLARED FAIL CLASSES: []`.
- Census ordinary run at revision `df9ffdf9…` (current): same PASS 0/0/0/0,
  exit 0, G2 line now per-file: `(current-ok loci per file: PROVINCE.md=17,
  SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)`.
- Creep audit (CR-5 `scope-diff.py` form, the round-1 tool at
  `claims/c2/EX-21/cr5-tool/scope-diff.py`), HEAD-state vs both revisions:
  `rows before=20 after=20 / ADDED (0) / REMOVED (0) / CHANGED (0) / CREEP
  FLAGS: []`, exit 0. Transcript: `census-and-canonical-transcript.txt`.

## 5. Attacks / refutations attempted

| # | attack | result | verdict |
|---|---|---|---|
| A1 | degenerate check — does the invariance measure anything? Canary on scratch copies: delete one knowledge file | `knowledge_files` 82→81, `dangling=["2026-10-13-crash-evidence"]`, **score stays 10.0** | check is sensitive, but only via `dangling`/`missing`; comparison must use the full tuple (adopted) |
| A2 | canary: push one craft citation out of range (`...r7-01-queue-a-ops.md:84` → `:99999`) | `citation_resolved_rules` 13→12, `depth_score` 10.0→9.23 | sensitive to the depth leg |
| A3 | canary: rename both README map tokens for a deleted file | `dangling=["2026-10-13-xcrash-evidence"]` | sensitive to the coverage leg |
| A4 | spill check — did EX-16's edit touch any command-A surface? | `git status` shows only `.ufo/gates/c1-census-v10.py`; all five surface hashes identical | **refuted** — no spill |
| A5 | does the census edit sneak into command A's read path? | audit-hook read set: 20 paths, none under `.ufo/gates/` | **refuted** |
| A6 | mid-flight instability — measure at every intermediate revision, not just the settled one | 13/13 revisions identical (table §2) | stability holds under churn |
| A7 | C1 patch-text self-identity (EX-01's own claims) | payload re-extracted: 896 B, sha256 `a47dc38d1e12856bb34b3f1310af7109d65c649f8eef17a5feb3c00781623b80` ✓; applied via their `apply-rule14.py`: `SKILL.md` = `19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90` (their claimed value) ✓ | claims verified |
| A8 | naive reading of C1's "prior 13 rules byte-identical" under command A's block split | **fails in both observed insertion forms** — see §6 | refuted (as a block-hash statement); a form that satisfies it was found and measured |

## 6. C1's rule-14 leg (projected) and the rule-13 seam

Live `SKILL.md` still has 13 rules at report time; the canonical patch text
(`.ufo/waves/arc3-loop1-round2/claims/c1/EX-01/rule14.patch.md`) was applied to
scratch roots carrying the real `corpus/knowledge` and `corpus/README.md`.

| scratch form | resulting `SKILL.md` | lines | command A | rules 1–13 block-identical? |
|---|---|---|---|---|
| EX-01 canonical (`apply-rule14.py`) | `19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90` | 385 | 82/82, **14/14**, 10.0/10.0 | no — rule 13 block 484→483 B (`\n\n`→`\n`), sha `542d848531864437`→`428e766ad8b286af` |
| EX-05 `insert-rule.py` variant | `8ad330d4edeea358a0f4d3803017fd1a07ac81736cce39aa7b4ca537c7ec6456` | 385 | 82/82, **14/14**, 10.0/10.0 | no — rule 13 block 484→485 B (`\n\n`→`\n\n\n`), sha →`3b01763115ae8a36` |
| **byte-preserving form** (`anchor + "\n" + payload`, payload after the existing blank line) | `68073d44d54f6e3b3b493af8a426e97b83c8fbf4cb43b97aff925d0ab82e9165` | 385 | 82/82, **14/14**, 10.0/10.0 | **yes** — rule 13 stays `542d848531864437`; rule 14 = `d6014403857e5dc3` |
| same + blank line before the next heading | `04d8e3ce31b296169f671b8131d0fbcbb4038e90146aa8060c5c59e6d8d1af93` | 386 | 82/82, **14/14**, 10.0/10.0 | **yes** — rule 13 stays `542d848531864437`; rule 14 = `c7f524629aaf373a` |

Rule 14 resolves under command A's pattern in all forms:
`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7-7` → valid (file has 33
lines). README coverage map and knowledge tree unchanged in every form.

**Finding (hand to c1/integrator):** command A attaches the newline run between
rules to the *preceding* rule's block. Both candidate insertion forms shift that
run, so the prior-13 "byte-identical" assertion holds as a *content-line*
statement but fails as a *command-A block-hash* statement. If the round report
asserts the latter, land the byte-preserving form (or state the assertion on
lines, not blocks). This is a seam artifact of the instrument, not a content
change — no rule text moves in any form.

## 7. Gaps, blockers, honest limits

- **C1's landing is projected.** The live craft section is untouched (13 rules)
  at the last check (12:21:12Z). No live post-C1 command A exists to measure; the
  14/14 legs are scratch applications of the round's own patch text and the two
  insertion scripts the c1 seats shipped.
- **EX-16's landing is complete and self-declared**: `seats/EX-16.md` landed
  during this leg and names FINAL `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
  (610 lines) — the same revision command A measured at 82/82, 13/13. If a later
  revision appears, re-run `commandA.py` — by §3 the surface values cannot move
  without an edit to `corpus/` or `SKILL.md`, which is itself the falsifier to
  watch.
- **/tmp not used** (standing EDQUOT record honored); all scratch under
  `/var/tmp/ex24r2/`. Note on my own watcher: an early gates-directory hash
  fired on C3's `custody-pair/` appearing (12:03:27Z creation) — the trigger was
  correctly re-pointed at the census sha256; it was never a census change.
- Not run: the commit-time (post-integration) command A — that measurement
  belongs to the parent at the work commit, per the round-1 precedent.
