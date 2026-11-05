# Verification evidence — seat ScribeKnowledge, round 96 attempt 1

Every check below was run by this seat, in its own scratch clone
(`/fast/scratch/hyaku/kaidoku-r96/ScribeKnowledge/clone`, a `git clone --shared` of
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at HEAD
`3baac2ef4b9b2830d299125b8184ca06d9e6584d`). No lane file outside this seat's
directory was edited; the scratch tree was removed after the receipts were copied out.

## 0. Tool versions (no tool installed or upgraded by this seat)

```
$ upx --version
upx 5.2.0
UCL data compression library 1.03
zlib data compression library 1.3.1.1-motley

$ python3 --version
Python 3.14.8
```

Nothing was installed or upgraded by this seat, so the operator tooling directive in
`/home/vgpnk/.omp/agent/RULES.md` had nothing to record beyond "no install performed".

## 1. The S321 host digest and the published `recheck:` command

```
$ sha256sum /usr/bin/printf
b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf
```

Matches the committed pin (`.ufo/waves/round-96/pins.sha256`, last line) and the
receipt field `source_sha256` in
`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`.

The `recheck:` line published in the knowledge draft was **executed**, not merely
written:

```
$ cd $S/clone
$ python3 -I -B tools/round-96/fresh-source2-check.py --root . --work $S/recheck/work \
    --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --json-out $S/recheck/receipt.json
...
fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
EXIT=0
```

Field-by-field comparison of the recheck receipt against the committed base receipt
`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`:

```
differing top-level keys: ['revision']
  revision | recheck= "3baac2ef4b9b2830d299125b8184ca06d9e6584d" | committed= "0ea695e826f2dca53dd55ac0bafead93de26b173"
```

**Only `revision` differs** (the revision the run was invoked at). Every other field —
`label`, `counts`, `deterministic`, `collides_public_packed`, `intact_identity`,
`blocks`, `packed_sha256`, `source`, `source_sha256`, `exit`, `met_target`, and all
four cell records — is equal. The recheck command in the draft is therefore executable
and reproduces the committed measurement.

## 2. The S321 registry row against the fleet census

The draft row (`.ufo/waves/round-96/w1/ScribeKnowledge/sources-row.md`) was extracted
programmatically and checked for the 11-column shape:

```
cells: 13          # 11 content columns + the two leading/trailing empties from '|'
 1 ' S321 '  2 ' `/usr/bin/printf` — sha256 …'  3 ' tool '  4 ' A '
 5 ' fresh-pack held-out arm source diversity '  6 ' sha256 `b2265abe…`; upx 5.2.0 packable; … '
 7 ' A second, distinct little-endian x86-64 host binary carries … '  8 ' mined '
 9 ' 2026-11-05 '  10 ' on-release '  11 ' corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md '
```

**Arm A — the row appended, the consumer absent** (the landing-order hazard):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file corpus/SOURCES.md --root . --today 2026-11-05
file	E11	S321 missing used-by corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md
EXIT=1
```

**Arm B — the row appended, the consumer present** (the knowledge draft copied into
`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` in the clone):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file corpus/SOURCES.md --root . --today 2026-11-05
VALIDATE_EXIT=0
--- E/W counts ---
     32 	W04
--- S321 lines ---
(none)
```

**No E-code against S321, and no new warning.** The 32 `W04` findings are the
pre-existing duplicate-URL warnings: the lane's own baseline registry (without the row)
produces exactly the same 32 `W04` and no E-code, at exit 0 — so the new row adds
nothing to the finding set.

Census counters, baseline vs with-row:

| metric | lane baseline | with the S321 row |
|---|---|---|
| rows | 225 | **226** |
| tier.A | 205 | **206** |
| tier.B | 11 | 11 |
| tier.C | 9 | 9 |
| status.mined | 201 | **202** |
| status.rejected | 24 | 24 |
| status.invalid | 0 | 0 |

## 3. The R95-VD-2 counting command, run as published

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ python3 -c "import re,html;s=open('.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html','rb').read().decode('utf-8','replace');print(html.unescape(re.sub(r'<[^>]+>','',s)))" > /tmp/s320-stripped.txt
$ grep -o 'O_NOFOLLOW' /tmp/s320-stripped.txt | wc -l
6
$ grep -o 'O_NOFOLLOW' .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html | wc -l
6
```

**6 both before and after tag-stripping.** The round-95 prose said "five times"; the
count is six. The six occurrences were located individually (byte offsets 3497, 14186,
18048, 18932, 29400, 36595 in the tag-stripped text): the file-creation-flag list, the
`O_NOFOLLOW` description (the only one carrying the rule), the two `O_PATH`
occurrences, the `ERRORS` entry, and — the one the round-95 enumeration missed — the
`HISTORY` section's own `O_NOFOLLOW` / `POSIX.1-2008` entry.

## 4. Facts quoted in the drafts, read from committed bytes

Each number the drafts publish was read out of a committed receipt or instrument, not
from memory:

| published fact | source |
|---|---|
| `r95-rule mutants killed 5 of 10`, `counts {killed: 5, mutants: 10}`, `exit 1`, survivors M2/M3/M4/M6/M10 | `.ufo/waves/round-96/pre/c1-legacy-rule-at-base.json` (each mutant's `killed` flag read individually) |
| `unbound accepted 5 of 6 (1 crash); nojson exit 0`, `typed_refusals 0`, `KeyError: 'fresh_scored'`, nojson `exit 0` / `receipt_written false` | `.ufo/waves/round-96/pre/c1-v5-admits-unbound-at-base.json` |
| before `victim_intact false` / after `victim_intact true` | `.ufo/waves/round-96/pre/c1-probe-writer-unbound-at-base.json` |
| `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`, `exit 0`, `identity_not_killed true` | `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` |
| K-dmain `pos` 0 / `shortrev` 1 / `rewrite` 1 / `notrecomp` 1 / `nojson` 2; K-fsync `fsync_calls 1`; selftests `cases=13 failures=0` and `cases=5 failures=0`; r95 battery regression exit 0 | same receipt, `honest` block |
| the six round-96 forgeries' `exact: true` and their single reasons | same receipt, `honest/K-forgeries/rows` — all six r96 rows `exact True`; the four r95 rows are refusal-only (`exact False`, `ok True`) because the v6 counter additionally binds `head` and the pins, so a round-95 fixture legitimately carries more than one reason |
| honest public run `exit 0`, `selfverify ok=True reasons=0` | `.ufo/waves/round-96/l1/scores/honest-pos.json`, `.stdout`, `.rc`, `.stderr` |
| red evidence `head null`, `selfverify ok=False reasons=1`, stderr `selfverify reason: head-not-bound`, `.rc` = 1 | `.ufo/waves/round-96/l1/scores/honest-pos-red-head-not-bound.{json,stdout,stderr,rc}` |
| probe `verdict "hardened"`, `victim_intact true`, `receipt_valid true`, `tmp_is_symlink true`, `tmp_left true` | `.ufo/waves/round-96/l1/scores/c1-symlink-v6-at-decl.json` |
| S321 label, counts, determinism, no-collision, blocks 5, packed sha256 `95f2bebe…`, and the four cell records (near ±7 repaired rc 0; far ±40 refused rc 2, typed refusal text) | `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json` |
| the four instrument digests (`7d7d559a…` v6, `3b8c7583…` kill-rule-v2, `67b74a4b…` symlink-probe-v2, `124f71f7…` fresh-source2-check) | recomputed with `sha256sum` and matched against `.ufo/waves/round-96/pins.sha256` |
| the six intended forgery reasons | `.ufo/waves/round-96/mutants.json` `forgery_reasons` |
| M0 identity must not be killed; the per-mutant `kills_via` map | `.ufo/waves/round-96/mutants.json` `mutants[]` |
| the **measured** kill attribution per mutant (which check has `ok: false`) | `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` `mutants[]` — read programmatically; see §5 |
| the seven named checks and their semantics | `tools/round-96/kill-rule-v2.py` module docstring + `c_selftest`/`c_verify_forgeries`/`c_agreement_exact`/`c_dmain`/`c_fsync`/`c_probe` |
| the v6 bindings and their typed reasons | `tools/round-96/stop-boundary-repair-battery-v6.py` docstring + `verify_receipt`/`count_problems` — the reasons the code can emit are `label-shape-unparsable`, `label-not-recomputed`, `label-not-frozen`, `met-not-recomputed`, `revision-not-bound`, `head-not-bound`, `receipt-missing-pin:<field>`, `counter-pin-not-bound`, `verdict-pin-not-bound`, `repair-pin-not-bound`, `counts-missing-key:<k>`, `counts-type:<k>`, plus `receipt-required` on the usage path |
| `upx 5.2.0`, Python 3.14.8 | `upx --version`, `python3 --version` on this host |

## 5. Declared vs measured kill attribution (a divergence this seat found and did not smooth over)

The mutant table `.ufo/waves/round-96/mutants.json` declares a `kills_via` string per
mutant. The after receipt `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json`
records which checks actually failed. The two disagree in one place.

```
M0  declared: control: must NOT be killed          measured: killed=false, no failing check
M1  declared: K-selftest planted-tmp case           measured: K-selftest
M2  declared: K-fsync                               measured: K-fsync
M3  declared: K-dmain negctl                        measured: K-dmain (notrecomp, rewrite, shortrev)
M4  declared: K-dmain negctl                        measured: K-dmain (notrecomp, rewrite, shortrev)
M5  declared: K-selftest verify-catches-not-frozen  measured: K-selftest, K-dmain/rewrite
M6  declared: K-dmain shortrev                      measured: K-selftest          <-- DIVERGES
M7  declared: K-agreement F3                        measured: K-agreement, K-selftest
M8  declared: K-agreement F1                        measured: K-agreement, K-selftest
M9  declared: K-agreement pos                       measured: K-agreement, K-selftest
M10 declared: K-probe receipt-content consistency  measured: K-probe
```

**M6 diverges.** The mutant table declares M6 (the removed `revision-not-bound`
branch) to be killed by "K-dmain shortrev"; the measured receipt shows M6 fails
**K-selftest** instead — the v6 counter's selftest carries a `verify-catches-wrong-revision`
case (`tools/round-96/stop-boundary-repair-battery-v6.py`), so the mutant trips the
selftest before the negative control ever reaches the branch. M6 is killed either way,
so the frozen label and the kill rule are unaffected; only the *attribution* differs.

The knowledge draft therefore reports the **measured** attribution, names the
divergence explicitly, and does not edit the frozen mutant table (the table is
frozen; the declaration says predicates, counters, kill rules, manifests, pins,
fixtures and targets are never re-declared or edited). This is a naming/attribution
observation for the round's lesson, not a change to any frozen byte.

The other divergence, M5, is additive rather than conflicting: the mutant table names
K-selftest and the measurement shows K-selftest **and** K-dmain/rewrite failing — the
`label-not-frozen` branch the mutant deletes is exercised by both.

## 6. Checks NOT run by this seat (and why)
- **The frozen counting commands were not re-run.** The seat's item is *drafting*, not
  reproduction; the reproduction seats are `ExecRepro` and `ExecFreshSource` in this
  wave, and the after receipts they produce are the frozen evidence. Nothing in the
  drafts depends on a fresh run of the kill rule, the battery or the probe — every
  number quoted comes from a committed receipt.
- **The C2 after-side was not measured.** Craft block 35, QUALITY 193/194 and the
  SKILL.md registry rows are R96-C2 and belong to the craft-block seat
  (`ScribeBlock35`). This seat's drafts touch only the knowledge entry, the S321 row
  and the lesson's Gate / Corrections sections; the knowledge draft names the craft
  block only as the C2 claim's subject and asserts nothing about its content.
- **No host mutation, no install, no `~/.local/bin` write, no fleet-root write.** The
  only writes this seat made are its own seat directory (four files) and this report's
  scratch, which is removed.
