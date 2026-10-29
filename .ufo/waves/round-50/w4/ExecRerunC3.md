# ExecRerunC3 — wave-4 FALSIFY re-run of the R50-C3 instrument against the LANDED state

**Verdict: HOLD (the landed C3 numbers reproduce exactly and byte-for-byte) — with one
STOP-worthy disclosure finding (F1) and two depth findings (F2, F3) that the L1 must
either fix or disclose.**

Seat scope: re-run `tools/round-50-c3/sqfs-triage-v5.py` from the **committed tip bytes**
in a fresh scratch, reconcile against the landed receipts, verify the control receipts and
the junk parse-refusal log. No REA was run. The lane tree was treated as read-only.

Scratch: `S=/fast/scratch/hyaku/kaidoku-r50/w4-ExecRerunC3` (removed after receipts were
copied into `.ufo/waves/round-50/w4/ExecRerunC3/`). Artifacts + `receipts.tsv` (exact
command, exit code, artifact sha256, UTC) are in that directory.

## 0. Tip drift observed during the seat (important context for the L1)

The lane tip moved **twice** while this seat ran, and the C3 instrument's bytes changed
with it. Both states were re-run and both reproduce:

| lane state | commit | instrument sha256 | SKILL.md status line cites |
|---|---|---|---|
| dispatched tip | `c67b741e8f6bd8d64adbdb15e059d47fde004c77` | `ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0` | `ef4633c5…` ✔ |
| later tip | `92ec6e6d176467104384d80534fdf47975bad5cc` (HEAD) | `f29eb92073dfff0cae48658985a7df3a34b1558430183dacc9968c2dff71b16e` | `f29eb920…` ✔ |

The tip's instrument sha was verified both ways, as required:

```
$ git show c67b741e8f6bd8d64adbdb15e059d47fde004c77:tools/round-50-c3/sqfs-triage-v5.py | sha256sum
ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0  -
$ sha256sum tools/round-50-c3/sqfs-triage-v5.py          # worktree at dispatch time
ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0  tools/round-50-c3/sqfs-triage-v5.py
```

At HEAD the worktree bytes equal `git show HEAD:tools/round-50-c3/sqfs-triage-v5.py`
(`f29eb920…`), and the landed `c3-after.json` / `c3-before.json` `instrument_sha256`
fields were updated to match. **The receipt-to-instrument binding is currently
self-consistent at every tip observed.** Note the instrument changed at `1a7cc5c3`
("C3 guard fix applied (counting-bullet check binds the bullet; sha f29eb920)").

## 1. Findings table

| # | Kind | Claim attacked | Command (exact) | Exit | Result | Verdict |
|---|---|---|---|---|---|---|
| F-A | re-run | selftest green, 18 cases, at dispatched tip | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/st` (tool bytes = `ef4633c5…`) | 0 | `selftest: 18 cases, pass 18, fail 0` | **HELD** |
| F-B | re-run | selftest green, 18 cases, at HEAD | same, tool bytes = `f29eb920…` | 0 | `selftest: 18 cases, pass 18, fail 0` | **HELD** |
| F-C | re-run | before at base `f890bbea` = exit 1, 19 mismatches | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root . --rev f890bbead20ca2c549487167f56876ae47f1e1a4 --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out $S/repro-before-head.json` | 1 | `pair_mismatch_count 19`, `verdict "not met"`, all 19 are `*_ddefault` with table label `clean`/`none`; families 4 × `squashfs_v2_nonstandard`, 7 × `squashfs_v3_broadcom`, 8 × `squashfs_v3_nonstandard` — exactly the landed `4 v2ns + 7 v3_broadcom + 8 v3_nonstandard` | **HELD** |
| F-D | re-run | after at `1439dfe9` = exit 0, 0 mismatches | same command with `--rev 1439dfe9dadb5c3cbc525658b300c23f3013cf87` | 0 | `pair_mismatch_count 0`, `evaluator_missing []`, 126/126 labels equal | **HELD** |
| F-E | re-run | the landed receipt is what the committed tool produces | re-ran the **dispatched-tip** tool (`ef4633c5…`) against `--rev 1439dfe9` | 0 | output sha256 `e5df9be1ed42d718d812df345d5c2b230fea7a231890342763b967c66d12cbd1` == landed `git show c67b741e:.ufo/waves/round-50/c3/c3-after.json` **byte-identical** | **HELD** |
| F-F | re-run | ditto at HEAD | re-ran the HEAD tool against `--rev 1439dfe9` | 0 | output sha256 `bcb858d8c782cd7f9d0285cc5c15ecad242901816f8cf985d88d0a4593427315` == landed HEAD `.ufo/waves/round-50/c3/c3-after.json` **byte-identical**; the before receipt likewise byte-identical (`75b9846828aa81e0…`) | **HELD** |
| F-G | re-run | controls are semantic reds 19/126/26/51 | `--controls` at HEAD and at the frozen `1439dfe9` tool | 0 (0) | 9/9 committed controls red in some scope; do-nothing red on the corpus, names the four v2ns `_ddefault` | **HELD** |
| F-H | re-run | each landed control receipt reproduces | `--skill …/w3/ExecTriageControls/ctl-{do-nothing,guard-deleted,action-swapped}.skill.md` | 1 / 1 / 1 | 19 / 26 / 51 mismatches — identical to the landed `ctl-*.json` | **HELD (numbers)** — but see **F1** |
| F-I | re-run | junk control is a semantic red (exit 1, 126) | `--skill .ufo/waves/round-50/c3/ctl-junk.skill.md` | 1 | 126 mismatches | **HELD** |
| F-J | re-run | the literal all-`clean` junk variant is a parse refusal | `--skill .ufo/waves/round-50/w3/ExecTriageControls/ctl-junk.skill.md` | 2 | stderr `sqfs-triage-v5: table error: line 531: duplicate label 'clean' (first on line 530)` — **byte-identical** to the landed `.ufo/waves/round-50/c3/ctl-junk-parse-refusal.log` | **HELD** |
| F-K | depth | predicate is pinned and reaches the receipt | compared HEAD `PREDICATE` constant against the receipts and the claims file | 0 | `c3-before.json.predicate == c3-after.json.predicate == HEAD PREDICATE` (byte-equal); the flattened sentence is present verbatim in `plans/round-50-attempt2-claims.md` | **HELD** |
| F-L | depth | the ddwrt what-if ("moving ddwrt into the no-reader set would move exactly 8 labels and leave `pair_mismatches 0`") | patched a scratch copy of the tool (`NO_READER_FAMILIES` += `squashfs_v3_ddwrt`, `READER_BACKED_V1V3` -= it) **and** the scratch SKILL.md v5 rows to match | 0 | exactly **8** labels moved (1 `legacy-body-failure`→`no-reader-failure` + 7 `clean`→`clean-unverified`), `pair_mismatches 0` | **HELD** — with a caveat in **F3** |
| F-M | depth | the v5 table landed in SKILL.md is what the instrument scores | parsed the v5 block from `git show 1439dfe9:SKILL.md` and from the tool's embedded `V5_BLOCK` | 0 | 17 rules both sides, identical label order, and all 10 decision fields identical for every row. One prose-only divergence: the `no-reader-failure` **cause** cell says "no independent second reader" in SKILL.md vs "no validated complete independent oracle" in the embedded copy (semantics unchanged; the embedded copy carries the newer wording) | **HELD** (decision-equivalent) |
| F-N | depth | instrument refuses the graded/frozen surfaces and temp partitions | `--json-out tools/…`, `--json-out corpus/…`, `--json-out /tmp/…`, `--work /tmp/…`, `--freeze` not an ancestor | 2 ×5 | every refusal fires with a specific message | **HELD** |

**No drift from the landed numbers was found. Every landed C3 count reproduced exactly,
and both landed receipts reproduce byte-for-byte from the committed tool bytes.**

## 2. Findings that survive the attack

### F1 (STOP-worthy, calibration/coverage) — the four landed control receipts carry no `predicate` and no `instrument_sha256`

The task asked me to verify that each landed control receipt
(`.ufo/waves/round-50/c3/ctl-*.json`) carries `instrument_sha256` and `predicate`.
**They do not.** Measured on all four:

```
.ufo/waves/round-50/c3/ctl-action-swapped.json  top keys: [... 'instrument', 'label_distribution', ...]   predicate: NOT PRESENT   instrument_sha256: NOT PRESENT
.ufo/waves/round-50/c3/ctl-do-nothing.json      predicate: NOT PRESENT   instrument_sha256: NOT PRESENT
.ufo/waves/round-50/c3/ctl-guard-deleted.json   predicate: NOT PRESENT   instrument_sha256: NOT PRESENT
.ufo/waves/round-50/c3/ctl-junk.json            predicate: NOT PRESENT   instrument_sha256: NOT PRESENT
```

Their `freeze` sub-dict also has `instrument_sha256_at_rev: null` and
`instrument_unchanged: null`, whereas `c3-before.json` / `c3-after.json` carry both
fields correctly (`ef4633c5…` / `f29eb920…` at the tips) and a populated freeze block.

**Why this is not a cosmetic gap.** The landed control receipts are the *only* C3 receipts
that were produced by the `1439dfe9` tool (`a2ebb5a4…`, the freeze-era instrument), and
they were committed in `1439dfe9` itself. They are therefore the receipts that cannot
prove which bytes produced them: a control receipt with no `instrument_sha256` and no
`predicate` is indistinguishable from one produced by any tool version. The
`c67b741e` commit ("receipts bind instrument_sha256") patched **only** `c3-before.json`
and `c3-after.json` — one line each, visible as
`+ "instrument_sha256": "ef4633c5…"` — and left the four control receipts unbound. The
SKILL.md status line claims the battery "gates every receipt on re-read with the running
instrument's sha256 bound into it"; that sentence is true for two of the six C3 receipts
and false for the four control receipts.

The numbers themselves are unaffected — I regenerated each control with the tip tool and
got identical 19 / 26 / 51 / 126 (F-H, F-I) — but the *evidence chain* is weaker than
the status line says, and a reader cannot re-derive which tool produced the control
receipts from the receipt itself.

**L1 options (not my call):** re-run the four controls with the tip tool and land the
receipts with the two fields bound (they reproduce 1:1, so this is cheap and
append-only); or amend the SKILL.md sentence to scope the binding claim to the
before/after receipts and say so.

### F2 (depth) — the landed table's zero-coverage rows are not protected by any committed check

I mutated the **landed** `SKILL.md` v5 table (not the tool's embedded copy) one row at a
time in a scratch clone, committed each mutation, and re-ran the full predicate command
plus `--selftest`:

| landed v5 row mutated | corpus run exit | `pair_mismatches` | `--selftest` |
|---|---|---|---|
| `no-reader-failure` action `preserve-unresolved`→`preserve-failure` | **0** | **0** | 18/18 pass |
| `mixed-symlinks` action `audit-symlinks`→`preserve-failure` | **0** | **0** | 18/18 pass |
| `no-squashfs-chunk` action →`isolate-residue` | **0** | **0** | 18/18 pass |
| `avm-marker-be-dropped` action →`preserve-failure` | **0** | **0** | 18/18 pass |
| `body-extractor-failure` action →`salvage-partial` | **0** | **0** | 18/18 pass |
| `escaping-symlink-removed` action →`count-gap` | **0** | **0** | 18/18 pass |
| `clean-empty` action →`none` | **0** | **0** | 18/18 pass |
| `container-depth-limited` action →`inspect-input` (control) | 1 | 3 | 18/18 pass |
| `clean-unverified` handler cell, drop `squashfs_v3_broadcom` (control) | 1 | 7 | 18/18 pass |

**Why:** seven of the seventeen landed v5 rows have **zero** coverage in the 126-envelope
corpus (measured: `no-squashfs-chunk` 0, `avm-marker-be-dropped` 0, `no-reader-failure` 0,
`body-extractor-failure` 0, `mixed-symlinks` 0, `escaping-symlink-removed` 0,
`clean-empty` 0). The mutation battery in `--selftest` mutates the tool's **embedded**
`V5_BLOCK`/`V5_ROWS` constant, never the table as it landed in `SKILL.md`; the corpus run
reads `SKILL.md` but only the ten covered rows can move its number. So for those seven
rows the landed `SKILL.md` text is protected by **no** committed check: the action cells
of `no-reader-failure`, `mixed-symlinks`, `clean-empty` and four others can be changed
and every committed gate still reports green.

This is a real depth limit, not a falsification of the claim: the claim's own text
already says the corpus has *"ZERO no-reader extractor-failure envelopes"* and that the
`no-reader-failure` row is witnessed by a *synthetic* envelope in the selftest fixtures —
and the synthetic fixture does flip (`no-reader-failure-row-deleted` is RED on fixtures),
so the rule is not unverified in the instrument's own copy. What is unverified is the
**landed** `SKILL.md` text for those rows. Note the tool's embedded block and the landed
block are decision-equivalent today (F-M), so the divergence risk is latent, not live.

**L1 options:** add one selftest case that diffs the landed `SKILL.md` v5 block (read
from the lane) against the embedded `V5_BLOCK` on the ten decision fields, so a landed-row
edit cannot silently diverge from the instrument's own copy; and/or land one committed
synthetic envelope per uncovered row so the corpus stops being the only witness.

### F3 (depth/calibration) — the disclosed ddwrt what-if is under-specified: it needs *three* coordinated edits, not one

The instrument docstring and the claims file both say moving ddwrt into the no-reader set
*"would move exactly 8 labels … and leave `pair_mismatches 0` under both rules, because
the table and this evaluator change together."* Reproducing that requires **three**
coordinated edits, not two:

1. `NO_READER_FAMILIES` += `squashfs_v3_ddwrt` (the evaluator's clean path),
2. `READER_BACKED_V1V3` -= `squashfs_v3_ddwrt` (the evaluator's failure path), **and**
3. the table's `legacy-body-failure` **and** `no-reader-failure` **and** `clean-unverified`
   cells moved with it.

With edits 1+3 only (ddwrt still in `READER_BACKED_V1V3`), the run gives
`pair_mismatches 1` — the failed body `dmg_Z3_v3ddwrt_inode_table` reads
`legacy-body-failure`/`cross-read-legacy` from the evaluator while the table says
`no-reader-failure`/`preserve-unresolved`. With all edits, `pair_mismatches 0` and exactly
8 labels move, as claimed (F-L). So the claim is **true as stated** ("the table and this
evaluator change together"), but "the evaluator" is two separate frozensets, and a reader
who changes only the obvious one gets a red run instead of the described 8-label move.
Worth one clause of wording; not a defect.

### F4 (minor, tooling hygiene) — the `predicates`/sha binding is described as covering "every receipt"

Covered under F1.

## 3. What I did NOT run / cannot attest

- **No REA.** No carrier, no oracle, no gap-rule evaluation was executed (forbidden for
  this seat, and the C3 instrument never invokes REA — verified by reading the tool).
- I did not re-run the C1 counter or the C2 battery (out of seat scope).
- I did not verify the round-49 reader census behind the "no validated complete
  independent oracle" wording (it needs `unsquashfs`/7-Zip over the round-42 fixtures and
  the frozen round-50 carriers are the L1's to materialize); I took it as the claim's
  stated input.
- **Lane-readiness note (not a finding):** `git status --porcelain` in the lane shows
  uncommitted modifications to `.ufo/waves/round-50/w3/ExecTriageV5*` and other w3 files
  while the tip moved. Those are the L1's/other seats' in-flight edits; I did not touch
  them. I did briefly write the lane's `plans/round-50-attempt2-claims.md` while
  attempting a hermetic test and **reverted it immediately**; the file is now
  byte-identical to `HEAD` (sha256 `0cf4047443575a982ae8f0a8ce87ce3c785fe9a7064c151c9258e53f12fe22de`
  == `git show HEAD:plans/round-50-attempt2-claims.md | sha256sum`) and
  `git status --porcelain plans/` is empty. The hermetic rerun of that test was then
  performed in a scratch clone with `LANE` repointed, where it **fails correctly**
  (exit 1, `the Counting command bullet does not name the declared base f890bbea`) — the
  `1a7cc5c3` guard fix is real and works.
- No tool was installed or upgraded for this seat (nothing in the task needed one), so
  there is no tool/version/channel record to report.

## 4. Bottom line for the L1

The landed R50-C3 evidence **survives** the falsify wave: every count reproduces exactly
and both before/after receipts reproduce byte-for-byte from the committed tool bytes at
both tips I could observe; the predicate is pinned to the claims file and reaches the
receipts; the four semantic-red controls and the junk parse-refusal reproduce exactly.

Two things need a decision: **F1** (the four control receipts are not instrument-bound,
contradicting the SKILL.md "every receipt" sentence) and **F2** (seven landed v5 rows —
including the `no-reader-failure` row the claim names — have zero corpus coverage and
zero landed-text protection; the selftest battery exercises the tool's embedded copy,
not the landed `SKILL.md`). F3 is a wording tightening. None of these is a wrong number;
they are evidence-chain and coverage gaps that the status line currently overstates.

Artifacts: `.ufo/waves/round-50/w4/ExecRerunC3/` (`receipts.tsv` + 17 artifacts).
