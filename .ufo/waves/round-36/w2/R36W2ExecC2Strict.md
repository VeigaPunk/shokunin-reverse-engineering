# R36W2ExecC2Strict — independent strict check of P36-C2 (QUALITY 77)

Seat: `R36W2ExecC2Strict` (leaf). Scope: falsify the integrated landing by re-deriving P36-C2 with a
checker that does **not** import `tools/round-36/c2-counter.py`.

**Verdict.** P36-C2 holds at all three post-repair revisions under the strict reading: 0 mismatches,
guards pass, every frozen statement occurrence present and equal to its independently recomputed
observable, every backticked pointer resolved, both base-broken pointers repaired to the exact frozen
documents, no unit removed, no counted population below base, no duplicate row/box key. The base
revision yields exactly the three mismatches the freeze names and no others. I found **no mismatch in
the scored surfaces**. Two dated-history data points are recorded separately (§8) — both are
accurately described by the rows that carry them. Nothing in the lane was changed except this report.

| revision | role | units | pointer occurrences | mismatches | guards | strict exit | frozen-counter exit |
|---|---|---|---|---|---|---|---|
| `cab59f221fe19726b5692bfa4d9a9679e96b8a73` | base | 15 | 39 | 3 | ok | 1 | 1 |
| `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` | C2 repairs | 15 | 41 | 0 | ok | 0 | 0 |
| `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` | C1 + assimilation | 15 | 43 | 0 | ok | 0 | 0 |
| `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` | integration tip | 16 | 46 | 0 | ok | 0 | 0 |

Surface fingerprints (`git show <rev>:<file> | sha256sum`, first 12 hex):

| rev | SCORECARD.md | SHONEN.md | SKILL.md | PROVINCE.md |
|---|---|---|---|---|
| `cab59f22` | `57eabd95be24` | `ba680ed3be11` | `d8d4783e4024` | `dc42da24b744` |
| `d2e46ef5` | `d885cf5edb0f` | `2452dd47cb1a` | `d8d4783e4024` | `dc42da24b744` |
| `ffc81341` | `5ef6e74754f1` | `51c55a9479a5` | `98835a7d128e` | `c9ced94dfab5` |
| `01a44dbf` | `6c36002a5cd9` | `51c55a9479a5` | `98835a7d128e` | `c9ced94dfab5` |

## 1. Method and independence

* No import of `c2-counter.py`. The observables are recomputed from the lane's own published recipes
  (`SCORECARD.md` `## Measurement recipes`, command A and command B) with `git --show`/`ls-tree`
  only — no worktree read, no REA, no network.
* Units are **all** rows and boxes, kept in a list: every `## Owned axes` row, every `## Capabilities`
  table row, every SHONEN `- [x]` box with its continuation lines. Duplicate keys are kept as
  separate units (multiset), never collapsed into a dict.
* Six statement shapes are enumerated with `finditer` (every occurrence, not the first):
  `N/M knowledge files mapped`, `N/M queue-drain rule blocks`, `N/M preselected reconciliation
  obligations`, `N/M rule blocks`, `` `SKILL.md:A-B` ``, `` `PROVINCE.md:A-B` ``. A `rule blocks`
  occurrence immediately preceded by `queue-drain ` is counted once, as the queue-drain shape.
* Every backticked repo pointer is resolved (path exists in the git object; a line range must satisfy
  `1 <= lo <= hi <= file line count`). Two classes the frozen tokenizer cannot see are also resolved:
  repo paths **inside backticked command lines** (`python3 -I .ufo/... --selftest`) and **companion
  filenames** in the same cell (`` `receipts/` + `receipts-B/` ``, `` `config-pre-pair.txt` +
  `config-post-pair.txt` ``).
* The two base-broken pointers must reappear in the same unit as the **exact** frozen document
  string, not a same-basename path and not just any resolving document.
* Per-shape population guard: no statement shape may occur fewer times than at the base; unit-key
  multiset may not shrink; total pointer occurrences may not fall; `knowledge_files`, `mapped`,
  `rule_blocks`, `resolved_rules` may not fall below base.
* A range line is scored two ways: a range anchored by the prose (`at `REV``/`at round-N work commit
  `REV``) is evaluated at that revision; an unanchored range whose start line is the section heading
  is compared with the observed heading-to-last-non-blank-line range. Membership (`files == mapped`)
  is reported in addition to the counts, so a one-missing/one-dangling swap cannot pass as equality.

Commands (read-only; `-I -B` isolates the interpreter):

```
python3 -I -B strict-c2.py --root <lane> --base cab59f221fe19726b5692bfa4d9a9679e96b8a73 \
        --rev <REV> --json-out rev-<name>.json
python3 -I -B tools/round-36/c2-counter.py --root <lane> --rev <REV> \
        --base cab59f221fe19726b5692bfa4d9a9679e96b8a73        # verdict comparison only
```

The tool itself is scratch-only (removed under the bounds); its observable/inventory core is
published verbatim in the appendix, and the check rules above plus §10's fixture harness fully
specify the rest.

## 2. Base mismatches — exactly the freeze's three, and no others

| class | unit (file:line) | token / statement | observed | verdict |
|---|---|---|---|---|
| pointer-unresolved | `SCORECARD.md:619`, capability "pre-registered two-lane live battery on REA 6.5.0" | `receipts-B/` | no such path | mismatch |
| pointer-unresolved | `SHONEN.md:11`, box 4 "No cross-domain bleed" | `ScoutSkillPlacement.md` | no such path | mismatch |
| statement-mismatch | `SCORECARD.md:23`, `coverage` | `116/116 knowledge files mapped` | `122/122` | mismatch |

Guards at base pass (nothing to repair yet, populations at their own base). The frozen counter marks
`guards_ok: false` at base only because its `unrepaired` list is non-empty there; `met_target` agrees.

## 3. Statement occurrences (findall) — stated vs independently observed

Occurrence counts are identical at all four revisions — `knowledge_files_mapped` 1,
`queue_drain_rule_blocks` 1, `preselected_obligations` 1, `rule_blocks` 1, `skill_range` 3,
`province_range` 2 — so no shape vanished and no second contradictory copy exists.

| shape | unit | `cab59f22` | `d2e46ef5` | `ffc81341` | `01a44dbf` |
|---|---|---|---|---|---|
| `N/M knowledge files mapped` | `owned:coverage` (`SCORECARD.md:23`) | 116/116 vs **122/122** | 122/122 vs 122/122 | 124/124 vs 124/124 | 124/124 vs 124/124 |
| `N/M queue-drain rule blocks` | `owned:depth` (`:24`) | 17/17 | 17/17 | 17/17 | 17/17 |
| `N/M preselected reconciliation obligations` | `owned:calibration` (`:25`) | 9/9 | 9/9 | 9/9 | 9/9 |
| `N/M rule blocks` | `shonen` box 1 | 17/17 | 17/17 | 17/17 | 17/17 |
| `` `SKILL.md:A-B` `` | `owned:depth` (current) | 81-314 | 81-314 | 81-314 | 81-314 |
| `` `SKILL.md:A-B` `` | `owned:depth` (baseline, anchored `a79945c4`) | 77-191 = 77-191 | same | same | same |
| `` `SKILL.md:A-B` `` | `shonen` box 1 (anchored `3e99fbd6`) | 81-314 = 81-314 | same | same | same |
| `` `PROVINCE.md:A-B` `` | `shonen` box 4 (`## Adjacent`) | 97-118 | 97-118 | 97-125 | 97-125 |
| `` `PROVINCE.md:A-B` `` | `shonen` box 4 (`PROVINCE.md:8-14`) | resolves | resolves | resolves | resolves |

Observed values (recipe A / B, independent recomputation):

| rev | knowledge files | mapped | missing | dangling | rule blocks | resolved | command B | craft | Adjacent |
|---|---|---|---|---|---|---|---|---|---|
| `cab59f22` | 122 | 122 | [] | [] | 17 | 17 | 9/9 | 81-314 | 97-118 |
| `d2e46ef5` | 122 | 122 | [] | [] | 17 | 17 | 9/9 | 81-314 | 97-118 |
| `ffc81341` | 124 | 124 | [] | [] | 17 | 17 | 9/9 | 81-314 | 97-125 |
| `01a44dbf` | 124 | 124 | [] | [] | 17 | 17 | 9/9 | 81-314 | 97-125 |

Membership, not just counts: `files == mapped` at every revision (`missing` and `dangling` empty), so
`124/124` is a set identity, not a coincident count. `PROVINCE.md:8-14` (version pins) and
`PROVINCE.md:24` (installed skill v42) both resolve and still carry the claimed content.

## 4. Pointer resolution

Token occurrences equal the frozen counter's at every revision (34 / 36 / 38 / 41). My checker adds
three repo paths inside backticked command lines and two companion filenames, all resolving:

```
embedded   .ufo/waves/round-14/tools/quote-fidelity.py      (capability: quote/heading audit)
embedded   .ufo/waves/round-14/fixtures/expected.json       (same row)
embedded   .ufo/waves/round-17/run-carriers.sh              (capability: log capture)
companion  result.json  -> evidence/round-1-2026-10-15/result.json
companion  config-post-pair.txt -> .ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt
```

Unresolved pointers: the two at base (§2), none at `d2e46ef5`, `ffc81341`, `01a44dbf`. Backticked
tokens deliberately not treated as pointers at the tip, with the reason: section headings
(`## Frontier`, `## Adjacent`, `## Coverage map`), revision ids (`a79945c4`, `3e99fbd6…`, `3395b6d`,
`7ef837a4…`, `638fb211`, `58116aa1`, `4072ebb3`, `08c7a729…`, `ebe2cb4a`, `c265db9b…`, `cab59f22…`,
`2832c5b3`, `2f18996d`, `75af886a`), sub-ranges without a filename (`88-116`, `95-116`, `:114-116`),
REA vocabulary (`rea-agents@6.5.0`, `rea-agents@6.7.0`, `rea-agents`, `extract-firmware`,
`missing-extractor-dependency`, `PATH`, `measured_revision`). The three no-filename ranges are
checked in §8 instead.

## 5. Repair identity (QUALITY 77's "same document", not same basename)

| base-broken token | unit | intended document (freeze) | `d2e46ef5` | `ffc81341` | `01a44dbf` |
|---|---|---|---|---|---|
| `receipts-B/` | `cap:pre-registered two-lane live battery on REA 6.5.0` | `.ufo/waves/luna-round-6/receipts-B/` | present, exact | exact | exact |
| `ScoutSkillPlacement.md` | `shonen:No cross-domain bleed (PROVINCE.md still accurate)` | `.ufo/waves/round-30/w1/ScoutSkillPlacement.md` | present, exact | exact | exact |

Both repaired documents exist and are the right documents: `receipts-B/MANIFEST.txt` lists the lane-B
legs (`leg-1.md` … `leg-10.md`, `census-laneB-final.txt`); `round-30/w1/ScoutSkillPlacement.md` is the
"R30 w1 — ScoutSkillPlacement" seat report the box cites. The tip tree contains exactly one
`receipts-B` directory and exactly one `ScoutSkillPlacement.md`, so the frozen counter's
basename-suffix repair rule could not have been gamed inside this repo — the exactness requirement
would still have caught it, and the harness proves that (§10).

## 6. Population guards and duplicate keys

* Units: 15 → 15 → 15 → 16. The single addition is
  `cap:REA SquashFS recursion through sasquatch (LE v4)` (`SCORECARD.md:627`) at `01a44dbf`; no unit
  key disappears at any revision and no duplicate key exists at any revision.
* Pointer occurrences: 39 → 41 → 43 → 46 (never below base).
* Counted populations: knowledge files 122 → 124, mapped 122 → 124, rule blocks 17 → 17,
  resolved rules 17 → 17, command B 9/9 → 9/9. Nothing fell.
* No duplicate `Owned axes`/`Capabilities` key and no duplicate SHONEN box label at any of the four
  revisions, so the frozen counter's dict-overwrite weakness is latent here rather than triggered;
  §10 shows the strict checker still fails on a shadow row if one were appended.

## 7. Dated history — checked separately, not counted in the predicate

Nine `N/M … at `REV`` statements and eleven narrative claims in the scored rows/boxes. Each is
evaluated in its own family (`coverage`→knowledge pair, `depth`→rule pair, `calibration`→command B).

| dated statement | cited rev | observed there | row's own stated value there | verdict |
|---|---|---|---|---|
| `116/116 knowledge files mapped` | `c369242f` | 116/116 | 109/109 | true |
| `109/109` | `ebe2cb4a` | 109/109 | 108/108 | true |
| `78/78` | `3395b6d` | 78/78 | 72/72 | true |
| `107/107` | `7ef837a4` | 107/107 | 78/78 | true |
| `108/108 after the round-25 EVM selector-naming entry` | `08c7a729` | 108/108 | 108/108 | true |
| `17/17 queue-drain rule blocks` | `c369242f` | 17/17 | 17/17 | true |
| `also 17/17` | `ebe2cb4a` | 17/17 | 9/9 | true |
| `9/9` | `638fb211` | 9/9 | (row absent at that rev) | true |
| `the row kept 9/9 until round 25 added a recount at 08c7a729` | `08c7a729` | 17/17 | **9/9** | true as row history — see note (a) |
| `122/122` | `cab59f22` | 122/122 | 116/116 | true |

Note (a): the depth row is byte-identical at `0e333eb2` and `08c7a729`, i.e. round-25's R25-C2 commit
did not touch it; the recount sentence ("recount 17/17 at `08c7a729…` (round 25 attempt 3)") first
appears in round-25's wave-1 correction commit `dc31f9c4` (`git log -S'recount 17/17' -- SCORECARD.md`).
So "round 25 added a recount at `08c7a729`" is accurate, and the row was stale (9/9 while the
observable was 17/17, moved at `4072ebb3` on 2026-10-19) until that correction. The history sentence
describes exactly this.
Note (b): `107/107 at 7ef837a4` is true of the observable while the row still stated 78/78 there — again
what the row's own parenthetical ("the row kept that revision until round 26") says.

Narrative claims checked against git objects, all true:

* "rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and
  2026-10-19)": parent of `58116aa1` = 9, `4072ebb3` = 17, and exactly eight commits increment the
  rule-block count (`58116aa1`, `265e1aa5`, `8cc81a84`, `ba06c4dd` on 10-18; `28aa7a98`, `2fba56fe`,
  `9c1d1fef`, `4072ebb3` on 10-19). The range contains 69 commits in total, so "eight commits" can
  only mean the incrementing ones — which is what it says.
* "drifted +2 after Frontier additions in `2832c5b3` and `2f18996d`": Adjacent end 116 → 117
  (`2832c5b3`) → 118 (`2f18996d`); +1 per commit, +2 cumulative.
* "range refreshed round 30 from `95-116`/`:114-116`": at `9db24c9e` the Adjacent range is 95-116 and
  lines 114-116 are the "Quality/safety verdicts on findings … never 'is it safe…'" refusal bullet.
* "the earlier `88-116` began inside `## Frontier`": at `58116aa1` (where `PROVINCE.md:88-116` was
  stated) `## Frontier` heads line 73, `## Adjacent` line 95, and line 88 is a Frontier bullet.
* Box 4's continuation lines at the tip: `:110-115` = "Installing engines, Python packages, or editing
  client configs" bullet; `:116-118` = the safety-verdict refusal; `:119-125` = "Tooling, dated
  2026-10-26 … install or upgrade … recorded (round 36: sasquatch 4.5.1 …)".
* "range was 97-118 before round 36": `d2e46ef5` Adjacent = 97-118.
* "count measured at `c265db9b` (`result.json` `measured_revision`)": true at all four revisions.
* "the row said `75af886a` until round 26, which is the luna-round-2 receipt reconciliation":
  `75af886a` is the 2026-10-16 luna-round-2 commit and its `result.json` already records
  `measured_revision = c265db9b…`, so 75af886a is not command B's revision. Loose label only: that
  commit touched `PROVINCE.md` and `SKILL.md`, while the luna-round-2 receipts themselves were
  committed in `4b806e14`. Not a mismatch.
* "two entries added" after the round-36 landing: the only knowledge files added between `d2e46ef5`
  and `ffc81341` are `2026-10-26-r36-sasquatch-squashfs-recursion.md` and
  `2026-10-26-unblob-sasquatch-dependency.md`, the two the row names.
* "Baseline source revision `66455858…`" resolves to a commit.

Out-of-surface observation (not counted, not a scored row): the round-26 section's depth row said
"craft section `SKILL.md:81-318` at `08c7a729`"; the heading-to-last-non-blank-line range there is
81-314 (line 319 is the next heading, 315-318 blank). Different end convention, historical section,
not part of the `## Owned axes` surface.

## 8. Agreement with the frozen counter, and what strictness adds

The frozen counter and the strict checker agree on every verdict: base exit 1 with the same three
mismatches (`ctl-c2-0` and my run agree item-for-item), `d2e46ef5`/`ffc81341`/`01a44dbf` exit 0 with
`mismatches: 0`, `guards_ok: true`. The stored `after-at-d2e46ef5.json` observed block
(`knowledge_files 122`, `mapped 122`, `resolved_rules 17`, `rule_blocks 17`, `command_b [9,9]`,
`craft_range [81,314]`, `adjacent_range [97,118]`, `pointers 36`) equals my recomputation except that
I count 41 pointer occurrences at that revision: 36 tokens (identical to the frozen count) plus 3
embedded command paths and 2 companion filenames. That is a coverage delta, not a disagreement.

Strictness the frozen counter does not implement, each demonstrated failing in §9: shadow-row
contradiction (its `units()` dict keeps the last row with a key), same-basename repair (its
`unrepaired` guard accepts any path ending in `/` + the broken token), a deleted statement shape
(no `search` hit is indistinguishable from a missing check unless the shape population is guarded),
pointers embedded in command lines, companion filenames, and membership (its O1 compares two counts).

## 9. Red-case proof of the checker (fixture harness, 14/14 pass)

A synthetic lane in scratch: base carries the stale count and both broken pointers; one commit repairs
them (must be green); 13 mutants are applied one per commit on top of a reset to the repaired commit.
Fixture git only (`git -C "$D" …`, toplevel verified before the first commit).

| case | expected class | observed | verdict |
|---|---|---|---|
| green after repair | `met_target true` | true | PASS |
| shadow row appends the stale count again | duplicate + statement mismatch | both | PASS |
| count off by one | statement-mismatch | same | PASS |
| second count inside the same cell | statement-mismatch | same | PASS |
| same-basename decoy for the repaired pointer | repair-not-exact-document | same | PASS |
| other resolving document substituted | repair-not-exact-document | same | PASS |
| SHONEN box removed | missing_units | missing_units + 3 derived | PASS |
| resolving pointer deleted from a row | pointers_not_fewer | same | PASS |
| craft range shifted by one | section-range-mismatch | same | PASS |
| Adjacent range shifted by two | section-range-mismatch | same | PASS |
| range beyond file | pointer-unresolved | same | PASS |
| SHONEN rule count wrong | statement-mismatch | same | PASS |
| rule-block statement deleted (shape vanishes) | statement-population-shrunk | same | PASS |
| consistent duplicate row | reported, not failed | duplicate-key-consistent, `met_target` true | PASS |

Fixture control: the base commit scores `mismatches=3`, `met_target=false`.

## 10. Corrections I made to my own reading during the pass

1. **Dated classifier false accept.** My first variant scored a dated pair against any observable
   family; `9/9 at 08c7a729` then "passed" through the calibration family (which is 9/9 at that
   revision). Fixed by binding the family to the row (`coverage`→knowledge, `depth`→rules,
   `calibration`→command B) and by scoring both readings (observable at the revision, and the row's
   own stated value there). The claim now passes only as row history, with the staleness noted.
2. **"grew from 9 to 17 in eight commits".** My first mechanical reading compared rule counts at the
   two named commits (10 and 17) and `rev-list --count` across the range (69) and called the sentence
   false. Wrong reading: the sentence counts the nine before the first incrementing commit and the
   eight commits that each add one rule. Verified under that reading; the sentence is true.
3. **Repair rule keyed on basename.** My first repair check fired only when a token's basename matched
   a frozen repair, so substituting an unrelated resolving document was silent. Replaced with
   "the unit must now contain the exact frozen document", which fails both substitutions.
4. **Section-range rule too broad.** My first range rule compared any `SKILL.md:A-B` starting on a
   heading with the section range, which flagged the dated baseline range `SKILL.md:77-191` and
   `PROVINCE.md:8-14`. Fixed by anchoring dated ranges to their own revision and comparing only the
   range whose start line is the section heading.
5. **Companion double counting.** The first companion rule emitted one candidate per sibling directory,
   so unresolved clones produced bogus `base_unresolved` entries and `repair-not-exact-document`
   mismatches with `intended: null`. Replaced with one grouped record per token, resolved if any
   sibling directory holds it.

## 11. Limits and residual holes

* Only the six frozen shapes are scored. Other count-bearing prose in the rows (the `## Capabilities`
  trailing paragraph, the `## Owned axes` baseline paragraph) is outside the predicate; I checked the
  mechanically checkable claims there (baseline revision, the two named entries) and they hold.
* Exact-document identity is enforced only for pointers that were broken at the base, per the frozen
  predicate. A later replacement of a *previously resolving* pointer by a different resolving document
  would pass.
* Line ranges are checked structurally (inside the file), not semantically; a range can be inside the
  file and point at the wrong sentence.
* Anchored ranges are scored at their anchor. Today no claim shelters behind that: the depth row's
  craft range also appears unanchored (81-314, matching), and box 1's anchored copy matches at
  `3e99fbd6` as well (81-314, rule pair 17/17).
* Capability semantics ("publishes every regular file … once the official sasquatch 4.5.1 binary is on
  PATH") are not C2's subject and were not re-tested here.
* Nothing about C1's evidence, receipts or provenance is claimed by this seat.

## 12. Environment, tooling, reproduction

`Python 3.14.8`, `git 2.56.0`. No tool installed or upgraded: `pacman` is paused host-wide and nothing
was needed (the check is stdlib Python over git objects). REA was not invoked. Scratch
`/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC2Strict` was removed; every number above is copied here.

Reproduce the core (appendix, run from the lane root; each argument is a revision):

```
python3 -I -B <appendix>.py cab59f221fe19726b5692bfa4d9a9679e96b8a73 \
    d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be \
    ffc813417d3bceeeb7b028b12ce0be8a5dc33d95 \
    01a44dbf45913a1bdcabbbfb85b7bb9d232cb930
```

It prints, per revision: the recipe-A/B observables (122/122 → 124/124; 17/17; 9/9; craft 81-314;
Adjacent 97-118 → 97-125; `missing`/`dangling` empty), the 9 statement occurrences with their numbers,
and the 39/41/43/46 pointer occurrences with resolution (only the two base tokens fail).

## Appendix — checker core (verbatim from the tested tool)

```python
#!/usr/bin/env python3
"""P36-C2 strict-check core, extracted verbatim from the wave-2 tool.

Prints, per revision: the observables command A / command B produce, every
occurrence of every frozen statement shape, and every backticked pointer with
its resolution. Guards, duplicate detection and the mutation harness are
described in the report.
"""
import json, re, subprocess, sys

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REVS = sys.argv[1:] or []

CELL_SPLIT = re.compile(r'(?<!\\)\|')
TOKEN = re.compile(r'`([^`\n]+)`')
PTR = re.compile(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$')
EMBEDDED = re.compile(r'[A-Za-z0-9_.][A-Za-z0-9_./+-]*')
COMPANION = re.compile(r'^[A-Za-z0-9_.-]+\.(?:md|txt|json|tsv|py|sh|mjs|ya?ml)$')
SHAPES = [
    ('knowledge_files_mapped', re.compile(r'(\d+)/(\d+) knowledge files mapped')),
    ('queue_drain_rule_blocks', re.compile(r'(\d+)/(\d+) queue-drain rule blocks')),
    ('preselected_obligations', re.compile(r'(\d+)/(\d+) preselected reconciliation obligations')),
    ('rule_blocks', re.compile(r'(\d+)/(\d+) rule blocks')),
    ('skill_range', re.compile(r'`SKILL\.md:(\d+)-(\d+)`')),
    ('province_range', re.compile(r'`PROVINCE\.md:(\d+)-(\d+)`')),
]
QD = 'queue-drain '
SECTION = {'skill_range': ('SKILL.md', '## Queue-drain craft', 'craft_range'),
           'province_range': ('PROVINCE.md', '## Adjacent', 'adjacent_range')}
def _git(*args):
    return subprocess.run(['git', '-C', ROOT, *args], capture_output=True)


def show(rev, path):
    p = _git('show', f'{rev}:{path}')
    return p.stdout.decode() if p.returncode == 0 else None


def exists(rev, path):
    return _git('cat-file', '-e', f'{rev}:{path}').returncode == 0


def line_count(rev, path):
    t = show(rev, path)
    return None if t is None else len(t.splitlines())


def hrange(text, prefix, stop):
    lines = (text or '').splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(prefix)), None)
    if start is None:
        return None
    last = start
    for i in range(start + 1, len(lines)):
        if stop(lines[i]):
            break
        if lines[i].strip():
            last = i
    return (start + 1, last + 1)


def observed(rev):
    kn = [p for p in _git('ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge')
          .stdout.decode().splitlines() if p.endswith('.md')]
    files = {p.rsplit('/', 1)[-1][:-3] for p in kn}
    readme = show(rev, 'corpus/README.md') or ''
    sec = ''
    if '## Coverage map\n' in readme:
        sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', sec))
    skill = show(rev, 'SKILL.md') or ''
    craft = ''
    if '## Queue-drain craft ' in skill:
        craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pat = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved, bad_rules = 0, []
    for idx, rule in enumerate(rules, 1):
        refs = re.findall(pat, rule)
        ok = bool(refs)
        for name, first, last in refs:
            n = line_count(rev, 'corpus/knowledge/' + name)
            if n is None:
                ok = False
                continue
            s, e = int(first or 1), int(last or first or 1)
            ok = ok and 1 <= s <= e <= n
        resolved += ok
        if not ok:
            bad_rules.append(idx)
    res_txt = show(rev, 'evidence/round-1-2026-10-15/result.json')
    cb, measured = None, None
    if res_txt is not None:
        doc = json.loads(res_txt)
        ob = doc.get('obligations') or []
        cb = (len([o for o in ob if o.get('status') == 'aligned']), len(ob))
        measured = doc.get('measured_revision')
    prov = show(rev, 'PROVINCE.md') or ''
    return {
        'knowledge_files': len(files),
        'mapped': len(files & mapped),
        'missing': sorted(files - mapped),
        'dangling': sorted(mapped - files),
        'rule_blocks': len(rules),
        'resolved_rules': resolved,
        'unresolved_rule_blocks': bad_rules,
        'command_b': cb,
        'result_json_measured_revision': measured,
        'craft_range': hrange(skill, '## Queue-drain craft', lambda l: l.startswith('## ')),
        'adjacent_range': hrange(prov, '## Adjacent', lambda l: l.startswith('#')),
        'adjacent_range_alt_stop': hrange(prov, '## Adjacent', lambda l: l.startswith('## ')),
    }


def statements(unit):
    out = []
    t = unit['text']
    for name, rx in SHAPES:
        for m in rx.finditer(t):
            if name == 'rule_blocks' and t[max(0, m.start() - len(QD)):m.start()] == QD:
                continue  # counted once as queue_drain_rule_blocks
            out.append({'shape': name, 'nums': [int(g) for g in m.groups()],
                        'span': list(m.span())})
    return out


def companions(unit):
    """Bare sibling filenames in a cell that also names a full path, grouped by token.

    "`receipts/` + `receipts-B/`" and "`config-pre-pair.txt` + `config-post-pair.txt`"
    mean the second token is a file in the first token's directory; a companion is
    resolved if any sibling directory in the same cell holds it.
    """
    full = [p[1] for p in pointers(unit) if '/' in p[1]]
    dirs = [d if d.endswith('/') else d.rsplit('/', 1)[0] + '/' for d in full]
    seen = {p[0] for p in pointers(unit)}
    out = {}
    for tok in TOKEN.findall(unit['text']):
        tok = tok.strip()
        if tok in seen or tok.startswith(('/', '~')) or '@' in tok:
            continue
        if not COMPANION.match(tok):
            continue
        out.setdefault(tok, [d + tok for d in dirs])
    return out


def pointers(unit):
    out = []
    for tok in TOKEN.findall(unit['text']):
        tok = tok.strip()
        if not tok or tok.startswith(('/', '~')):
            continue
        m = PTR.match(tok)
        if m and not any(ch.isspace() for ch in tok):
            path, a, b = m.group(1), m.group(2), m.group(3)
            if '/' in path or path.endswith('.md'):
                out.append((tok, path, a, b, 'token'))
            continue
        for w in EMBEDDED.findall(tok):
            if w.startswith(('/', '~', '-')) or '/' not in w:
                continue
            out.append((w, w, None, None, 'embedded'))
    return out


def resolves(rev, path, a, b):
    p = path.rstrip('/')
    if not p or not exists(rev, p):
        return False
    if a is None:
        return True
    n = line_count(rev, p)
    if n is None:
        return False
    lo, hi = int(a), int(b or a)
    return 1 <= lo <= hi <= n


def heading_lines(rev):
    out = {}
    for f in ('SKILL.md', 'PROVINCE.md'):
        for n, l in enumerate((show(rev, f) or '').splitlines(), 1):
            if l.startswith('#'):
                out[(f, n)] = l
    return out

def main():
    for rev in REVS:
        obs = observed(rev)
        print(json.dumps({'revision': rev, 'observed': obs}, sort_keys=True))
        sc = show(rev, 'SCORECARD.md') or ''
        sh = show(rev, 'SHONEN.md') or ''
        # units: Owned axes rows, Capabilities rows, SHONEN boxes
        units = []
        for head_name, label in (('## Owned axes', 'owned'), ('## Capabilities', 'cap')):
            lines = sc.splitlines()
            start = lines.index(head_name)
            started = False
            for n in range(start + 1, len(lines)):
                l = lines[n]
                if l.startswith('## '):
                    break
                if l.startswith('|'):
                    started = True
                    cells = [c.strip() for c in CELL_SPLIT.split(l.strip().strip('|'))]
                    if set(l.replace('|', '').strip()) <= set('-: ') or cells[0] in ('Axis', 'Capability'):
                        continue
                    units.append({'surface': label, 'line': n + 1, 'key': cells[0], 'text': l})
                elif started and l.strip():
                    break
        cur = None
        for n, l in enumerate(sh.splitlines()):
            m = re.match(r'^- \[[ x~]\] (.*)$', l)
            if m:
                cur = {'surface': 'shonen', 'line': n + 1, 'key': m.group(1).strip(), 'text': l}
                units.append(cur)
            elif cur is not None and l.startswith('  '):
                cur['text'] += '\n' + l
            elif not l.strip():
                continue
            else:
                cur = None
        for u in units:
            for s in statements(u):
                print(json.dumps({'revision': rev, 'statement': s['shape'], 'surface': u['surface'],
                                  'key': u['key'], 'line': u['line'], 'nums': s['nums']}, sort_keys=True))
            for tok, path, a, b, kind in pointers(u):
                print(json.dumps({'revision': rev, 'pointer': tok, 'kind': kind,
                                  'surface': u['surface'], 'line': u['line'],
                                  'ok': resolves(rev, path, a, b)}, sort_keys=True))
            for tok, cands in companions(u).items():
                oks = [resolves(rev, c, None, None) for c in cands]
                print(json.dumps({'revision': rev, 'pointer': tok, 'kind': 'companion',
                                  'surface': u['surface'], 'line': u['line'],
                                  'ok': any(oks), 'candidates': cands}, sort_keys=True))


if __name__ == '__main__':
    main()
```
