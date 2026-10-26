# R40W2C2Rescore — C2 score reproduction (round 40, wave 2)

**CONFIRMED** — R40-C2's landed verdict (MET, `matched 26/26`, all bindings true, exit 0 at
`42c10a58cb2cae3a4a0122af35a0cf95ac718043`) reproduces byte-for-byte, holds at the dispatch tip
`4d62ee5a86b4692a13f682b29ed7975e8d7e5326`, and survives an independent label re-derivation and an
independent carrier regeneration. No falsification of the landing. Four non-claim-touching defects/notes
below (one stale embedded table copy, one unenforced frozen-path clause, one claim-text imprecision, one
effective-sample measurement); none changes `matched`, `n`, `bindings`, `distinct_decisions` or
`met_target`.

I attacked: the counter's own reproducibility, its three selftests, its unevaluable boundaries at the
freeze and at the pre-data control commit, the score at the data commit and at the tip, the L1 receipt's
provenance, the held-out→table decision leg **without the counter**, the generator leg **without the
counter**, and the discrimination of the frozen table against six frozen controls plus five of my own
near-variant mutants on the *held-out* envelopes (the controls were only ever scored on the development
set by the L1). I did not attack C1, did not re-run REA, and state nothing about whether the committed
envelopes faithfully describe real unblob runs beyond their subject digests and recorded operations.

## Scratch and hygiene

```
S=/fast/scratch/hyaku/kaidoku-r40/R40W2C2Rescore
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
```

Sandbox clone for the mutant battery: `D=$(mktemp -d "$S/fx.XXXX") && git clone -q --shared <LANE> "$D/lane"`;
`git -C "$D/lane" rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kaidoku-r40/R40W2C2Rescore/fx.khLW/lane` before any commit; every mutant commit used
`-c user.name=fx -c user.email=fx@fx`. No VCS mutation in the lane or fleet, no writes outside the report
and `artifacts/R40W2C2Rescore/`, no installs (no tool version recorded because none was installed or
upgraded; `python3`, `git`, `jq` only). Scratch removed at the end.

Lane facts at run time: the clone's `HEAD` was `0b15c8b2c593b7954efda92249ef3fa895c79f99` (the lane has
moved past the dispatch tip; `4d62ee5a` is an ancestor and was scored as dispatched).

## 1. Reproduction of the landed score

```
python3 -I -B <LANE>/tools/round-40/c2-counter.py --root <LANE> \
    --rev 42c10a58cb2cae3a4a0122af35a0cf95ac718043 \
    --freeze 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --json-out "$S/c2-42c10a58.json"
```

stdout, exit 0 (real 0m0.62s):

```
{"bindings_false": [], "distinct_decisions": 12, "exit_code": 0,
 "freeze": "7fce308631a8b457d6b7c5a4b39a923c4e9a49de", "matched": 26,
 "met_target": true, "met_target_consistent": true, "n": 26,
 "revision": "42c10a58cb2cae3a4a0122af35a0cf95ac718043"}
```

Diff against the L1 receipt `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`
(`jq -S 'del(.argv)'` on both): **identical**, whole document, including `table`, `interpreter`,
`generator`, `writer`, `per_class`, `decision_pairs`, `met_target_formula`,
`pair_fields_derived_from_row: 0`, `row_index_base: 1`, `replicates_identical_in_class: []`
(`diff` printed nothing but the argv difference: absolute tool path and `--json-out` path).
The receipt `.receipt.json` records `exit_code 0`, `counter_sha256 9bd7924…83dd1` = the counter blob at
both freeze and rev, `stdout_sha256 31179…a02c`, empty stderr, and a 0.558 s UTC window.

Same run at the dispatch tip:

```
--rev 4d62ee5a86b4692a13f682b29ed7975e8d7e5326
→ exit 0, matched 26, n 26, distinct_decisions 12, bindings_false [], met_target true
```
The C2 core projection (`matched, n, distinct_decisions, bindings_*, met_target*, table, interpreter,
generator, writer, manifest_first_add, decision_pairs, label_action_vocabulary, unclassified_*,
replicates_identical_in_class, row_index_base, pair_fields_derived_from_row`) is **bit-identical** to the
L1's 42c10a58 receipt (`diff` of the two projections printed nothing → `TIP_CORE_IDENTICAL`).

Twenty-five bindings, all `true`: `arms_valid, carrier_paths_unique, carriers_committed,
carriers_regenerated, classes_two_each, classes_unique, decisions_reported, envelope_paths_unique,
envelopes_valid, generator_sha_matches_freeze, ids_unique, interpreter_present_at_freeze,
manifest_after_freeze, manifest_before_envelopes, manifest_generator_path, n_equals_twice_classes,
regenerated_seed_matches_freeze, row_decisions_consistent, seed_matches_freeze, v1_table_identical,
v1_table_present, v2_table_columns, v2_table_identical, v2_table_present, writer_matches_manifest`.
`met_target_formula = {matched_equals_n: true, all_bindings_true: true}`; `met_target_consistent: true`.

## 2. Selftests and unevaluable boundaries

| run | command tail | result |
|---|---|---|
| counter | `c2-counter.py --selftest` | `{"cases": 42, "green": 11, "red": 31, "pass": 42, "fail": 0}`, exit 0, 8.48 s |
| interpreter | `sqfs-triage-v2.py --selftest` | `cases=45 pass=45 fail=0`, exit 0 (`ok json-shape / first-table-wins / print-table / real-skill`) |
| generator | `heldout-gen-v2.py --seed 7fce3086… --selftest` | `all 6 selftest checks passed`, exit 0 (same seed → identical manifest bytes `232a3bf6…` and 26/26 identical carrier sha256; different seed → 26/26 differ; no class has two identical carriers) |

Hand wave: the generator's `--seed` is `required=True`, so bare `--selftest` is rejected by argparse with
exit 2 and a usage dump. `SKILL.md:1402` documents `--seed <hex> --selftest`, so this matches the tool's
own contract; recorded only because it differs from the other two tools' bare `--selftest`.

Unevaluable boundaries (JSON receipts written, `exit_code` recorded):

| rev | result |
|---|---|
| `7fce3086…` (freeze, `--rev`=`--freeze`) | **exit 2**, `unevaluable: no_manifest_at_rev` (`c2-freeze.json`, 935 B) |
| `45e89864…` (pre-data control receipts commit) | **exit 2**, `unevaluable: no_manifest_at_rev` |
| `2d1ac5bc…` (held-out data commit) | **exit 0**, matched 26/26, `distinct_decisions 12`, `bindings_false []` |
| `42c10a58…` (measured) | exit 0, 26/26 |
| `4d62ee5a…` (tip) | exit 0, 26/26 |

So the claim's "command that shows it unmoved" (counter exits 2 at the freeze) and its independence from
the C1 landing (26/26 already at the pure C2 data commit `2d1ac5bc`, before any C1 evidence lands) both
hold as stated. Also verified as claimed: the frozen v2 interpreter on the base `SKILL.md` exits 2 —
tested on both `fa6a8a3f…` (claim base) and `2b0b6a295…` (the counter's derived base):
`exit=2  stderr=sqfs-triage-v2: marker '<!-- sqfs-triage-table v2 -->' absent from the craft section`.

## 3. Independent label re-derivation (no counter code)

`$S/indep.py` (copied to artifacts): `git show` the SKILL at rev and the interpreter at freeze, run
`interp.py --skill SKILL.md --json` over all 26 committed `envelope.json`, compare `(label, action)` to the
manifest's `label`/`action`, and read the chosen row off each result's `rule` index.

```
interp exit 0  stdout bytes 29465   rules in table 11  envelopes parsed 26
H01 clean-be  want=clean/none  got=clean/none  rule=10  OK   … (26 × OK)
H25 out-of-domain want=unclassified/none got=unclassified/none rule=None OK
MATCHED 26/26
distinct pairs 12  distinct rules 12  one-rule-per-pair True
```

Every pair maps to exactly one row and different pairs to different rows; the no-match pair
(`unclassified/none`) maps to **no** row (`rule=None`), exactly the claim's "the no-match pair to none".
Per-envelope features confirm the decisions are feature-derived, not label-derived: no committed
`envelope.json` contains a class name or `expected_label`/`expected_action` (grep over 26 files: 0 hits);
the out-of-domain pair is `operation inspect_firmware_regions` + `provider binwalk` on both H25 and H26.

Table shape at rev: 11 body rows, 11 unique labels, 11 action tokens in the vocabulary line, actions a
bijection onto labels, all action cells inside the vocabulary; v2 block 6603 B at freeze **and** at rev
(`v2.identical true`), v1 block 3086 B at base and at rev (`v1.identical true`).

## 4. Independent regeneration (no counter code)

`$S/regen.py`: materialise `tools/round-40` + `tools/round-39` from the **freeze** blobs into a fresh tree,
run `heldout-gen-v2.py --seed 7fce3086… --out …` with `KAIDOKU_GEN_SQUASHFS` pointing at the materialised
writer, no `--run`, no `--actions-file`.

```
materialised 26 freeze blobs
generator exit 0
regen seed 7fce308631a8b457d6b7c5a4b39a923c4e9a49de
regen carriers 26 committed 26
sha/label/action mismatches: 0
all 26 regenerated identical: True
```

This is the same conclusion the sibling `R40W2C2RegenA` reached by a different route (it also diffed the
whole regenerated tree and varied seeds/locales); I re-ran it because the score's `carriers_regenerated`
binding is the one leg that could be faked by a cached regen directory, and a fresh tree with no cache
produces the same 26 pins.

## 5. Controls re-scored on the held-out set (discrimination)

The L1's kill rule scored the six controls only on the 26 **development** envelopes
(`.ufo/waves/round-40/controls/c2-dev-scores.json`: 0/4/18/2/24/24/24). The held-out claim has never been
tested against them. I substituted each frozen control table (marker line → last row) into the measured
`SKILL.md` inside the sandbox clone, committed, and re-ran the frozen counter against that commit
(`--freeze 7fce3086…`):

| case | matched | missed classes | exit | false bindings beyond `v2_table_identical` |
|---|---|---|---|---|
| CTL-C2-1 catch-all | **4/26** | 11 | 1 | `row_decisions_consistent` |
| CTL-C2-2 v1 transcribed | **18/26** | clean-empty, mixed, partial, out-of-domain | 1 | `row_decisions_consistent` |
| CTL-C2-3 actions rotated | **2/26** | 12 | 1 | — |
| CTL-C2-4 no domain guard | **24/26** | out-of-domain | 1 | `row_decisions_consistent` |
| CTL-C2-5 no mixed row | **24/26** | mixed-symlinks | 1 | `row_decisions_consistent` |
| CTL-C2-6 final `*` default row | **24/26** | out-of-domain | 1 | — |

Every held-out count equals the corresponding development count to the unit, and the missed classes are
the same ones. Independent cross-check: the sibling `R40W2C2IndepEval` evaluated the same six controls
with its own evaluator against the same held-out envelopes and got 4/18/2/24/24/24 as well. The held-out
set is therefore exactly as discriminating as the development set — no easier, no harder — and no control
reaches 26/26 on it.

## 6. Near-variant mutants: five of mine

Each is a single-cell edit of the landed block (or a two-cell swap), committed in the sandbox:

| mutant | matched | missed | interpretation |
|---|---|---|---|
| `clean-empty` action `confirm-empty`→`count-gap` | 24/26 | clean-empty | one action cell is load-bearing |
| swap `published files` between `clean` and `clean-empty` | 20/26 | clean-be, clean-le, clean-empty | the `0` vs `>0` cell separates three classes |
| `avm-marker` `-be in child argv` `no`→`yes` | 20/26 | avm, body-failure, partial | BE handshake column is load-bearing and order-sensitive |
| swap actions of `avm-marker` ↔ `body-extractor-failure` | 22/26 | avm, body-failure | labels and actions are coupled |
| `partial-body-failure` `published files` `>0`→`*` | **26/26** | **none** | **not caught by the decision test** |

The last one is the only mutant that still scores 26/26. Its only false binding is `v2_table_identical`
(the landed table's bytes are the target, so the counter still exits 1 and `met_target` is false). The
held-out set cannot see the degradation because `body-extractor-failure` (files `0`) precedes the widened
`partial-body-failure` row, so the widened row only loses discrimination on envelopes outside the closed
class set (a 0-file extractor failure with a non-`none` dependency set would now be read as
`salvage-partial`). This is a concrete instance of the claim's disclosed limit ("a table with one
load-bearing cell per label can also score a closed class set"), now measured at the cell level. It does
not falsify the predicate, which is explicitly "the frozen table bytes decide these 26", but it does mean
the 26/26 carries no information about cells that row order renders unreachable.

## 7. Freeze / ordering audit

- No commit in `FREEZE..42c10a58` and none in `FREEZE..tip` touches `tools/round-40/sqfs-triage-v2.py`,
  `tools/round-40/heldout-gen-v2.py`, `tools/round-40/c2-counter.py`, `plans/round-40-claims.md` or
  `tools/round-39/gen-squashfs.py` (`git log … --` over all five: empty). Blob sha256 at freeze = at rev
  for all four C2 tool paths and the writer; the receipt's `counter_sha256` equals the blob.
- `SKILL.md` has **no** commit after the freeze through the measured revision (`git log FREEZE..42c10a58 --
  SKILL.md`: empty), so the v2 block cannot have drifted between freeze and measurement; the counter's
  `v2.identical` binding confirms byte equality anyway.
- The four post-freeze commits are: `45e89864` control receipts, `2d1ac5bc` held-out data (26 carriers +
  envelopes + manifest, 131 files), `73c7bf9c` C1 receipts, `42c10a58` C1 landing (PROVINCE, README,
  SOURCES, two knowledge entries — no SKILL, no C2 data).
- Ordering: `seed == freeze` (`seed_matches_freeze`, `regenerated_seed_matches_freeze`), manifest
  `first_add = 2d1ac5bc` and every envelope's `first_add = 2d1ac5bc` (same commit, so "no later than its
  envelopes" holds by `is_ancestor`); both are after the freeze.
- Tamper hole closed: the manifest carries `label`/`action` (not `expected_label`/`expected_action`) per
  carrier, and the counter's fallback reads those; but `regen_ok` requires the *regenerated* manifest's
  pair to equal the committed pair, so hand-editing the expected pair breaks the score (mutant `regen` leg
  re-verified independently in §4).
- Worktree note (not mine): during this wave the lane worktree's `SKILL.md` was dirty — an uncommitted
  19-line append after line 1384 (`### Round-40 instrument registry`, mtime 16:24:08, i.e. before this seat
  started), entirely outside `## Queue-drain craft`. Every measurement here reads committed blobs
  (`git show <rev>:…` and the counter's own `show`), so the dirty worktree cannot have influenced any
  number in this report; rule block 19 (lines 361-375) is untouched by that append.
- `envelope_inferred: true` for all 26: the manifest names `Hxx/carrier.sqsh`, not the envelope path, so
  the counter infers `Hxx/envelope.json`, checks presence at rev, and then the subject digest. The digest
  leg (`envelopes_valid`) passes on every one, so the inference resolves correctly here; noted because the
  predicate says "every envelope's subject digest" and the manifest itself never enumerates envelopes.

## 8. Defects and notes (none claim-touching)

**D1 — the frozen interpreter embeds a stale copy of the table prose.** `--print-table` prints
`TABLE_BLOCK`, and the interpreter's own selftest asserts `print-table == TABLE_BLOCK` described as "the
frozen v2 table block". Compared with the landed block at rev: **2 differing cells, both unscored** — row 6
(`avm-marker-be-dropped`) `cause` (landed cites the genuine-AVM little-endian metadata case; embedded copy
is the older round-39 wording) and `source` (landed cites
`knowledge 2026-10-26-r40-sqfs-triage-v2.md :37-45`; embedded cites
`knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40`). All ten scored cells (`label`…`action`) are
identical in every row, so `matched` is unaffected; the counter reads `SKILL.md`, not `TABLE_BLOCK`, and
the interpreter reads `--skill`. Severity: documentation/hygiene — a reader who trusts `--print-table` as
"the frozen table" gets a stale `cause`/`source` for the one row the wave-2 AVM discussion turns on.

**D2 — one frozen path the counter's `frozen_path_changed` guard does not cover.**
`FROZEN = (INTERP, GEN, COUNTER, CLAIMS)`; the claims' frozen-path list for C2 also names "the SKILL v2 table
block" and `tools/round-39/gen-squashfs.py`. The v2 block is covered instead by the
`v2_table_identical` byte binding; the writer is covered only by `writer_matches_manifest`, which compares
the manifest's declared sha to the **freeze** blob, so a post-freeze edit to
`tools/round-39/gen-squashfs.py` would not raise `frozen_path_changed` (regeneration materialises the
freeze blob, so the edit could not buy a score anyway). **No actual breach:** `git log FREEZE..tip` over
that path is empty. Severity: predicate-guard gap, unexercised.

**D3 — claim text vs table header.** The claims say block 19 has "columns `operation` and `provider`
first"; the landed header is `label | operation | provider | handler | …`. Read as "the guard columns come
before the outcome columns" it is true; read literally (first two columns) it is not, and the counter only
checks column *presence* (`v2_table_columns`), not order. Severity: wording; no predicate clause depends on
it.

**D4 — effective sample size.** For 26 carriers there are **20 distinct feature tuples**; six classes have
feature-identical replicates (`dep-missing-be`, `dep-missing-le`, `avm-marker-be-dropped`,
`body-extractor-failure`, `no-squashfs-chunk`, `out-of-domain` — features include OP, PV, handler set, gap
set, dependency set, BE token, symlink-removed token, published-file count). The other seven classes differ
between their two carriers (file counts, handler flavour). So "26/26" is 20 independent decisions plus 6
duplicated ones; calibration should be read against 20 distinct tests, and against the closed class set
(§6) rather than as 26 independent draws.

## 9. Limits of this attack / what I did not establish

- I did not determine which process wrote the committed envelopes, nor re-run REA; I verified only their
  subject digests, recorded operations/providers, and the generator's determinism.
- The interpreter, generator, table and counter share one authoring seat, so "the table decides these 26"
  is circular to the extent the class set was designed around the table; my mutant battery bounds that
  circularity from below (single-cell edits are caught except where row order masks them) but cannot
  remove it.
- I did not test the seven undeclared rows/columns the claim leaves unscored (`cause`, `source`) beyond
  noting D1.
- The counter's `--selftest` red cases (31 of 42) were run but not individually audited; I audited their
  effect only through the measured runs and my own mutants.

## Artifacts (`<LANE>/.ufo/waves/round-40/w2/artifacts/R40W2C2Rescore/`)

| file | sha256 | content |
|---|---|---|
| `c2-42c10a58.json` | `602e8ab1…a5b4c3` | full counter receipt at the measured revision (identical to the L1's but `argv`) |
| `c2-tip.json` | `afb04af1…bf3a8a` | full receipt at `4d62ee5a` |
| `c2-2d1ac5bc.json` | `be66dd41…60e90c` | full receipt at the C2 data commit |
| `c2-freeze.json` | `faad8fb3…d873fc` | unevaluable receipt, exit 2, `no_manifest_at_rev` |
| `c2-45e89864.json` | `d21ece40…6d6bd6` | unevaluable receipt at the pre-data control commit |
| `indep-run.txt` | `1ec2d26f…41888f` | independent label re-derivation output (26/26, 12 pairs → 12 rules) |
| `indep.py` | `52ee91d6…6ef06` | the re-derivation script (git blobs + frozen interpreter only) |
| `regen-run.txt` | `cd192880…a52ae` | independent regeneration output |
| `regen.py` | `bbed9d88…a44a` | the regeneration script (freeze blobs, fresh tree) |
| `mutants-run.txt` | `ab6ae60e…25e` | the 11-case sandbox battery log |
| `mutant-battery.json` | `3dc55631…8ca` | per-case matched/missed/bindings/exit |
| `mutants.py` | `4febd528…b48` | the battery harness (sandbox clone, fixture identity) |
| `print-table.txt` | `5122a03e…da6c` | frozen interpreter `--print-table` output (D1 evidence) |
