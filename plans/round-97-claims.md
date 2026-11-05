# Round 97 claims — kaidoku (frozen before data)

Lane: kaidoku. Round: 97, attempt 1. Base: `2a54af0785f75d50912e1136443c8e78e62adf27`
(tip at declaration; local=remote per `jj-lane.sh state`). The lane holds the planner
seat (orchestrator ruling 2026-10-19); no `planner` role is dispatched.

Owned axes coverage, depth, calibration, freshness are all 10.0 on their finite proxies
(SCORECARD round-96 section); the claims sit on the tied-lowest axes (calibration,
depth), the same axes every round since 92. No stagnation waiver is needed and none is
claimed: a capability entered in round 96, inside the window. Two claims, causally
separable: each verifies without the other having landed (C1 reads only `tools/` and
`.ufo/waves/round-97/`; C2 reads only `SKILL.md`, `corpus/`, `tools/round-97/`).

## R97-C1 — calibration (measured): the kill rule binds every field it asserts to the
bytes at the revision they name, requires typed booleans, durability, and its own
re-read receipt, and distinguishes a crash from a kill

Round 96 closed with named limits 2–5, 7, 8/16, 17, 18 (lesson `round-96.md`) and the
non-author spot-check §6 concurred on every route: the receipt's `head == revision` is
a commit pointer, not a byte binding (M96-a); `met_target` verifies clean when absent,
null or a string (M96-f); `repair_cmd`, `public_met`/`public_label` and the imported
round-92 pins are unbound, and counts keys outside the label keys are silently ignored
(limit 5/6); the rule itself scores green without `--json-out` and never re-reads its
own receipt (limit 7); the frozen table has no `--rev != HEAD` scenario (M96-e); a
crash is published as a kill (N9/limit 17); the probe's own write escape is outside
every frozen check (M96-h/limit 8); the r95-battery leg is cwd-dependent (M96-j/limit
18). This round lands `tools/round-97/stop-boundary-repair-battery-v7.py` (the v6
verdict, byte-bound pins, typed met, allow-listed counts, bound repair/imported/public
fields, fsync-before-replace and directory-fsync durability) and
`tools/round-97/kill-rule-v3.py` (the successor rule: K-durability ordering check,
K-wlink planted victims, K-probe planted json-out victim, K-bytes blob binding plus
the dirty-clone leg, K-cwd, kill-class discrimination, and the rule's own re-read
receipt).

**Frozen predicate (one sentence, verbatim in `claims.json`, the receipt's `expect`
arithmetic and this file).** Command A — `python3 -I -B tools/round-97/kill-rule-v3.py
--root . --work <scratch> --mutants .ufo/waves/round-97/mutants.json --fixtures
.ufo/waves/round-97/forgery --prefix forge --decl <FREEZE> --json-out
.ufo/waves/round-97/l1/scores/c1-at-<landing>.json` — exits 0 at the landing revision
with label `mutants killed 21 of 21; forgeries refused 17 of 17; negctl refused 3 of 3;
probe consistent 1 of 1; honest accepted 1 of 1; wlink 2 of 2; durability 2 of 2; bytes
5 of 5; dirtyrefuse 1 of 1; ownrec 1 of 1` and `identity_not_killed true`; and command
B — the pinned round-96 rule `python3 -I -B tools/round-96/kill-rule-v2.py --root .
--work <scratch> --mutants .ufo/waves/round-97/mutants-before-noc1.json --fixtures
.ufo/waves/round-97/forgery --prefix forge --decl <BASE> --json-out
.ufo/waves/round-97/pre/c1-v2rule-at-base.json` — exits non-zero at the base revision.

**Do-nothing control (built before data).** Command B is the control: the do-nothing
world keeps the round-96 rule, which on the round-97 table (a) refuses only part of the
13-forgery set (the seven new-class fixtures are accepted or reason-mismatched by the
v6 verifier), (b) leaves the byte-binding, revold, durability, planted-link and
rule-kind mutants unexpressed or surviving. If command B exits 0, the counter or the
target is wrong and nothing is scored. Second control: the dirty-clone leg inside
command A requires `v6_admitted` true — if the pinned v6 counter ever refuses the dirty
world, the v7 byte binding adds nothing and the claim stops. Before-side receipts
(measured at the base, committed in the freeze): `pre/c1-v2rule-at-base.json`,
`pre/c1-v2rule-cwdprobe.json` (the M96-j red: the pinned rule's r95-battery leg fails
from a non-root cwd), `pre/c1-dirty-v6-admits.json` (the M96-a red: v6 exits 0 on a
dirty tree under the clean revision name).

**Kill rule.** Before side met (command B non-zero with named survivors recorded); any
forgery accepted or wrongly reasoned at the landing; any honest-arm check red; the
identity mutant killed; any kill_class mismatch; any pin differing; counter-read bytes
changed after the freeze (any `tools/round-97/` or frozen-input diff other than a
disclosed `instrument_supersessions` entry, never silently).

## R97-C2 — depth (measured): craft block 36 names the byte-binding/durability
class, and the depth instruments refuse the three round-96 false-green classes

Round 96's CriticC2 demonstrated with committed receipts that the depth stack (a)
accepts a criterion carrying the opposite rule, (b) accepts a rule-free criterion
(`see (QUALITY 193)`), (c) accepts a row citing an overlapping neighbor row, and (d)
lets a padded decoy table carry the shape floor (`_table_rows` merged every `|` line).
This round lands craft block 36 (marker `receipt-byte-binding v1`) in `SKILL.md`,
QUALITY rows 195 and 196, the knowledge entry
`corpus/knowledge/2026-11-05-r97-receipt-byte-binding.md` (sourced: cites S322,
`fsync(2)`, opened this round), the SOURCES row S322, and the strengthened instruments
`tools/round-97/craft-citation-v2.py` (criterion-cell restatement, citation-number
validation, snippet-carrying-table shape) and `tools/round-97/depth-blocks-v4.py`
(first-table shape floor, `--decoy-proof`).

**Frozen predicate.** Command C — `python3 -I -B tools/round-97/depth-blocks-v4.py
--root . --rev <LANDING> --expect-blocks 36 --shape-from 36 --expect 'blocks 36,
resolved 36, required-shaped 1/1' --json-out .ufo/waves/round-97/l1/scores/c2-depth-v4-at-landing.json`
— exits 0 at the landing; command D — `python3 -I -B tools/round-97/craft-citation-v2.py
--root . --manifest .ufo/waves/round-97/manifests/block36-after.json --block 36 --rev
<LANDING> --json-out .ufo/waves/round-97/l1/scores/c2-block36-at-landing.json` — exits
0; command E — the junk manifest `.ufo/waves/round-97/manifests/block36-junk.json`
under command D exits 1; command F — the discrimination receipts at the landing tree:
`pre/c2-v1-accepts-rulefree.json` shows the round-93 checker exiting 0 where
`l1/scores/c2-v2-refuses-rulefree-at-landing.json` exits 1, likewise wrong-row-overlap,
and `pre/c2-decoy-proof.json` (`control_killed true`) shows depth v3 accepting the
decoy v4 refuses; and at the base commands C and D exit 1 (`pre/c2-depth-v4-at-base.json`,
`pre/c2-depth-v3-at-base.json`, `pre/c2-block36-manifest-at-base.json`).

**Kill rule.** Any after command unmet at the landing revision; junk exit 0; block 36
present at the base; any attack fixture accepted by craft-citation-v2; checker/counter/
manifest pins differing; counter-read bytes changed after the freeze.

## Sources and frontier

S322 (`fsync(2)`, Linux man-pages, man7.org, tier A docs, opened 2026-11-05 by fetch
with sha256 and a located quote) grounds the durability clause of C1's knowledge entry
and block 36; the fetch bytes are `pre/s322-fsync2-fetch.html`. Census before/after via
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
(exit 0 required at round end; start run recorded with W04 warnings unchanged).

## Instruments (frozen at the freeze commit; never changed after scoring)

`tools/round-97/stop-boundary-repair-battery-v7.py`,
`tools/round-97/kill-rule-v3.py`, `tools/round-97/craft-citation-v2.py`,
`tools/round-97/depth-blocks-v4.py`, `tools/round-97/gen-forgery-fixtures.py`,
`.ufo/waves/round-97/mutants.json`, `.ufo/waves/round-97/mutants-before-noc1.json`,
`.ufo/waves/round-97/forgery/forge-*.json`, `.ufo/waves/round-97/manifests/*.json`,
`.ufo/waves/round-97/c2-fixtures/**`, all pinned by sha256 in
`.ufo/waves/round-97/pins.sha256`.
