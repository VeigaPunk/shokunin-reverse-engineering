# R43RevRevenger — round 43 wave 1: the frozen v4 held-out generator, reverse-engineered

**VERDICT: DEFECTS FOUND** — the placement spec is complete and demonstrated end to end (patched port
reproduces the frozen bytes plus one added check, 6 intended manifest deltas and 0 unintended), but the draft
claims file has **two blocking defects** the refusal alone does not fix (D1: the declared-tuple *predictor*
still mispredicts the C02 shape, measured incidence 42.2 % of seeds — so on most seeds the generator would
refuse and the round would have no data; D2: making `--run` mandatory collides with the counter's
`--seed/--out` seed-regeneration arm, which round 42's counter hard-requires to emit a manifest), plus **one
plan sentence that is unsatisfiable by design** (D3), one pre-existing generator defect (D4) and one vacuity
(D5). Details in §6; each has a concrete fix.

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`. Target read at
`git show 6b9e64fe:tools/round-42/heldout-gen-v4.py`, 3419 lines, sha256
`c2b1641ad6beec0d8eead002520174fb596c574efe44220c4a440917be03a5e1` (matches
`corpus/evidence/round-42/c2/heldout/manifest.json` `generator.sha256`, i.e. the committed held-out set was
produced by exactly the bytes analysed here). I read the whole file; every claim below is a line reference,
a run, or explicitly marked `[INFERENCE]`. Nothing was frozen, nothing in the lane was written, no REA/unblob
was run on third-party firmware (only on two carriers I generated myself), no tool was installed.

---

## 1. Q1 — where the DECLARED six-field tuple is computed

### 1.1 The six-field selection (one place, shared by every class)

| item | line | note |
|---|---|---|
| `DECLARED_FIELDS` | 1135-1136 | `('handler_set','gap_kinds','gap_dependencies','be_argv','symlink_removed','published')` — the binding order, and therefore the JSON key order of every `declared_features` |
| `DECLARED_KEY = 'declared_features'` | 1137 | the single spelling (R41-CL1) |
| `DECLARED_EXTRAS_KEY`, `EXTRA_FIELDS` | 1138-1139 | `extraction_failed`, `max_depth` — cross-checked by `--verify`, **not** part of the binding |
| `declared_tuple(features)` | 1142-1144 | projects the 8-field features dict down to the 6 |
| `declared_extras(features)` | 1147-1149 | the other 2 |

### 1.2 Named classes: computed per class from static tables + the drawn endianness

- `expected_features(name, endian, primary=None, secondary=None)` — **1092-1126**. Two branches:
  - `recipe['kind'] == 'legacy'` → `legacy_features()` — **710-768** (handler set / BE / P / G from the two
    pinned fixtures the seed drew and the recipe's `arm`/`damage`/`pair` flags).
  - everything else → `EXPECTATIONS[name]` — table **1006-1078** (27 named classes; the class→recipe table is
    `RECIPES` at **296-505**). `handler == 'k'` resolves to `squashfs_v4_be/le` by the replicate's endianness
    (1105-1112); `be == 'k'` the same (1112-1114).
- Written into each carrier entry at three sites: **1954** (`build_carrier`, named/v4 classes; `features` at
  1931, endian at 1774-1776), **2007+2092** (`build_legacy_carrier`: the tuple comes from the drawn fixtures,
  the endian from `primary['endian']`), **2305** (`_finish_simple`, called from the container builder at 2206
  and the residue builder at 2267). In each builder the declaration and the built bytes take their endianness
  from the same variable, so the two cannot disagree.

### 1.3 Combos: computed from the seeded factor vector, no named-class tuple consulted

- `combo_decisions(factors)` — **793-824** (the "observable decision" accounting).
- `combo_factors(seed, k, pins, variant=0)` — **826-876**: one `random.Random(sha256('<seed>:combo:<k>'))`
  draw in a fixed order, then 5 compatibility rules (855-869).
- `combo_draw(seed, k, pins)` — **878-889**: first variant with ≥ `COMBO_MIN_DECISIONS` (=2) decisions.
- **`combo_declared(factors)` — 891-982. This is the R42-CL1 predictor.** The binding tuple is assembled from
  clauses at 909-982; the faulting clause is **943-947**:

  ```
  943  reached = ((not damage_effective) or bool(factors['residue'])
  944             or bool(factors['two_chunk']))
  ```

  It says "a failing single root chunk mints nothing". The round-42 measurement says otherwise for a generated
  v4 body: REA observed `depth-limited` on C02. **The same function already contradicts itself** — the
  `published` clause at **959-963** returns `'nonzero'` for `factors['body_v4']` damage precisely because the
  v4 damage recipe zeroes a LATE data block, so earlier files are published. If output was written, the
  extraction descended and the depth ceiling was reached. Round-42 evidence (committed, and re-derived by me
  from the envelope, not from `run.json`):

  | | C02 |
  |---|---|
  | manifest `declared_features.gap_kinds` | `["extractor-failure","unpublished-entry"]` |
  | `C02/rea-full.json` → observed `gap_kinds` | `["depth-limited","extractor-failure","unpublished-entry"]` |
  | declared `published` / observed files | `nonzero` / 6 files |

  `corpus/evidence/round-42/c2/heldout/C02/...`, and the round-42 receipt
  `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` has `features_match: false` for **C02 only** (78/78
  carriers checked; `bindings_false: ["observed_features_match_declared"]`, `exit_code: 1`).
- Written at **2474** (carrier entry) and **2490** (tree.json), from `declared = combo_declared(factors)`
  computed at **2344**.

**Consequence for the round (D1, blocking).** Adding the refusal without touching 943 makes the round
*refuse* rather than *misdeclare*. I measured the incidence with the frozen draw itself
(`c02-shape-sim.py`, 500 seeds × 24 combos, `demo-log.txt` §k): **211/500 seeds (42.2 %) contain at least one
C02-shaped combo**, mean 0.578 such combos per 24, max 4. So with the round-43 seed (the freeze commit hash,
not choosable) the generator has ~42 % chance of exiting 3 with no manifest. The fix is one clause (§6 D1).

## 2. Q2 — where `--run` writes envelopes, and where a post-run hook can sit

### 2.1 The envelope writers

| function | line | writes |
|---|---|---|
| `_envelope_parts(full)` | 2539-2579 | pure: `{ok,data,meta}` → `(data, subject_sha256, shape)`; `shape` carries `handlers`, `failed_chunks`, `gap_kinds`, `gap_dependencies`, `be_argv`, `symlink_removed`, `files`, `parameters.max_depth` |
| `_write_envelope(entry, full, gz)` | 2581-2595 | `<OUT_DIR>/<id>/envelope.json` (the `data` object) **and** `<id>/rea-full.json` (the whole envelope); `.json.gz` under `--gzip`, mtime 0 |
| `run_rea(entry, scratch, keep_extraction, gz)` | 2613-2662 | calls `_write_envelope` at **2649**, then writes `<id>/run.json` at **2655** (arm, exit code, digest binding, shape copy) |
| `out_of_domain_run(...)` | 2664-2721 | non-`extract-firmware` op (`inspect-firmware-regions`, provider binwalk); `_write_envelope` at **2703**, `run.json` at **2709** |

`_write_envelope` has exactly two call sites (2649, 2703); both run functions have exactly one caller, the
`--run` loop in `main` at **3379-3401**. A record with `'error'` (no JSON envelope on stdout) is still written
to `run.json` (2630-2634 / 2684-2691) and counted as a failure by the loop (3386-3390).

### 2.2 The exact order in the frozen file — and why there is no hook point

```
build_set(...)            2770      builds carriers, writes <id>/tree.json, THEN writes manifest.json (2942)
main                      3373-3374 calls build_set
main                      3379-3401 the --run loop: run_rea / out_of_domain_run per carrier
main                      3403-3404 return 1 if any record had an error
main                      3405-3410 --verify → verify() + regen_check()
```

**The manifest is finalized (written) at line 2942-2943, i.e. BEFORE the first REA process is spawned.** There
is therefore no point "after the run, before manifest finalization" in the frozen file: the order is inverted
with respect to the claim. The refusal cannot be inserted into v4 as-is; the manifest write must move behind
the run. That is the core of the placement spec (§5).

Proof that this inversion is not cosmetic (`demo-log.txt` §a vs §j): the frozen generator run **without**
`--run` and the frozen generator run **with** `--run --verify` emit the *same* `manifest.json` bytes —
`ee41d057536a99e7c7e7965b360a5f06288428823af38bbcc0600461df84046e` both times (same seed, same
`--classes clean-le`). A manifest therefore carries **no evidence that REA ever ran**, which is exactly the
hole QUALITY 85 / M42-2 is about.

## 3. Q3 — every path that produces a manifest without a full `--run` pass

`manifest.json` is written at exactly **one line** (2942-2943, inside `build_set`), and `build_set` has exactly
three call sites:

| # | path | `--run`? | consequence |
|---|---|---|---|
| 1 | **`main` with no `--run` — the DEFAULT** | no | `--run` is `action='store_true'` (**3274**); there is no `--no-run` flag because no-run *is* the default. `python3 -I -B heldout-gen-v4.py --seed X --out DIR` writes a complete 78-carrier manifest and **zero envelopes**, exit 0. Demonstrated: `demo-log.txt` §a (`manifest present: yes`, `envelopes written: 0`, `EXIT=0`). |
| 2 | `main --classes <subset>` | optional | `parse_classes` (**2724-2735**) accepts any subset, so "a full pass" is only over the selected subset; the manifest's `classes` list records it, and nothing binds it to the 27×2+24 structure (that check lives in the counter). |
| 3 | `regen_check` (**3050-3098**, `build_set` at **3064**) | no | writes a second full manifest into a temp dir to compare bytes — a dev path, but it *is* a manifest-writing path. |
| 4 | `run_selftest` (**3100-3263**, `build_set` at **3112**) | no | three manifests (seeds a/b/c) into temp dirs; requires `--selftest`, ignores `--out`. |

Classes that skip REA: **none** — every carrier in the loop gets `run_rea` or `out_of_domain_run`. But the
`out-of-domain` class (H25/H26) runs `inspect-firmware-regions`, not `extract-firmware`, so its six-field
tuple is observed on a binwalk envelope with `normalized_result.chunks == []` — see D5.

So the answer to "(a `--no-run` mode? a class that skips REA?)" is: **the default mode is the hole; the flags
are fine.** All four paths must be closed or named (§5, §6 D2).

## 4. Q4 — the `generator` block round 42 already writes

From `corpus/evidence/round-42/c2/heldout/manifest.json` (`generator` = **2814-2849** in the source), 8 keys in
this order:

1. `name` — literal `'heldout-gen-v4.py'` (2815)
2. `version` — `VERSION = 'r42-c2-v4'` (146)
3. `sha256` — `sha256_file(os.path.abspath(__file__))`, i.e. the generator's own bytes
4. `carriers_per_class` — `CARRIERS_PER_CLASS = 2`
5. `writer` — `{name: 'gen-squashfs.py', path: <lane-relative or relpath>, sha256, block_encoder}` (2817-2822)
6. `partial_pin` — `{rule: 'R40-CL4', pinned_by: 'compressed-length', fill, max_damaged_block,
   measured_fail_range, measured_absorbed_from, measured_by}` (2823-2832)
7. `fixtures` — `{pins, pins_sha256, project, commit, url_base, license, count, resolution, damage_recipe}`
   (2833-2847)
8. — (nothing else today; `tuple_check` is the new key, appended last, §5)

Top-level manifest keys, in file order: `seed, round, claim, generator, action_vocabulary, action_set,
action_source, label_actions, new_labels, new_label_tokens_binding, precedence_observations, rea,
declared_schema, families, replicate_variation, out_of_domain, combo_unseen, classes, carriers` (2811-2940).

Note `round: 42` and `claim: 'R42-C2'` are literals at **2812-2813** — the port must change them, and
`precedence_observations` (2859-2884; rule 8 at 2874-2880) carries round-42's three MEASURED/TBC statements, including the
rule-8 text that D1 shows is now known to be too strong.

---

## 5. Placement spec (function + line + insertion order)

Original = `tools/round-42/heldout-gen-v4.py` @ `6b9e64fe` (sha `c2b1641a…`). Patched = the frozen port
`heldout-gen-v4r43.py` (sha **`996c16a0cbb1f3d476f7a2009066a896c83685256617954646d4de2db2fcaa6c`**), produced
mechanically: `git show 6b9e64fe:tools/round-42/heldout-gen-v4.py > gen.py && patch -p0 < placement.patch`
(verified: the result's sha equals the one above; `demo-log.txt` head).

### 5.1 New/changed pieces, in insertion order

| step | where (original line) | change |
|---|---|---|
| S1 | 2942-2943 (`build_set` tail) | **DELETE** the manifest write. `build_set` keeps returning `(manifest, carriers)` — identical dict, identical key order, identical per-carrier print loop (2945-2960). |
| S2 | after 2962 (`return manifest, carriers`) | **ADD** `serialize_manifest(manifest, drop_tuple_check=False)` (= `json.dumps(obj, indent=2) + '\n'`, byte-identical to 2942-2943) and `write_manifest(manifest, out_dir)` — the **only** manifest write in the program. |
| S3 | after 2964-2976 (`observed_features`) | **ADD** `read_envelope(out_dir, cid)` (plain or `.json.gz`), `collect_observed(out_dir, carriers)` (re-derives the tuple from `rea-full.json` via `_envelope_parts` → `observed_features`), `refusal_check(out_dir, carriers)` (returns rows + `mismatched` + the `tuple_check` summary), and `run_tuple_check(dir)` (the standalone `--tuple-check DIR` mode). |
| S4 | `main` 3373-3374 | keep `build_set`, then: `--verify` without `--run` → `SystemExit` (moved up from 3411-3412); `--carriers-only` + `--run` → `SystemExit`; **no `--run` and no `--carriers-only` → return 4 BEFORE `build_set`** (no directory is created). |
| S5 | `main` 3379-3401 | the run loop, unchanged. |
| S6 | `main` 3403-3404 | unchanged (`return 1` on any error record) — a second, independent guard for a carrier with no envelope. |
| S7 | **between 3404 and 3405 — the hook** | `refusal = refusal_check(OUT_DIR, carriers)`; on `not ok`: print one `REFUSE <id> <class> <field>: declared … observed …` line per differing field, then `declared_tuple_unobserved: k/n …; no manifest written`, **return 3**. |
| S8 | after S7 | `manifest['generator']['tuple_check'] = refusal['summary']` (appends as the last `generator` key → deterministic position), then `write_manifest(manifest, OUT_DIR)`. |
| S9 | 3405-3410 | `--verify` → `verify()` + `regen_check()`, unchanged in meaning. |
| S10 | `regen_check` 3070-3073 | **CHANGE**: neither side is a file any more. Compare `sha256(serialize_manifest(m, drop_tuple_check=True))` for the in-memory `manifest` and the in-memory `fresh`; rename the check `manifest bytes identical (generator.tuple_check excluded)`. |
| S11 | `run_selftest` 3118 | **CHANGE**: `'manifest': sha256(serialize_manifest(manifest, drop_tuple_check=True))` (in-memory). |
| S12 | argparse 3270-3275 | `--seed` no longer `required=True` (required unless `--tuple-check`); add `--carriers-only`, `--tuple-check DIR`; `--run` help says it is required to write a manifest. |
| S13 | 146, 2812-2815 | `VERSION='r43-c1-v4'`, `round: 43`, `claim: 'R43-C1'`, `name: 'heldout-gen-v4r43.py'`, `replaces: {name, version, sha256 of c2b1641a…}`. |

Exit codes: **3** = `declared_tuple_unobserved` (the claim's own token, CTL-C1-2 red); **4** = no-run refusal;
**2** = `--tuple-check` input unusable (missing manifest/envelope); **1** = a carrier produced no envelope;
**0** = manifest written, every carrier declares what its own envelope shows.

### 5.2 Manifest-byte budget of the whole change

Measured with `manifest-delta.py` on the same seed and the same `--classes clean-le`
(`demo-log.txt` §h): **6 differing JSON paths, 0 unintended** —

```
round                      42            -> 43
claim                      R42-C2        -> R43-C1
generator.name             heldout-gen-v4.py   -> heldout-gen-v4r43.py
generator.version          r42-c2-v4     -> r43-c1-v4
generator.sha256           c2b1641a…     -> 996c16a0…
generator.replaces         <absent>      -> the ported round-42 identity
(+ generator.tuple_check on a --run build; excluded from the comparison)
```

Everything else — every carrier's `declared_features`, `declared_extras`, `sha256`, `chunks`, `factors`,
`combo_unseen`, `rea`, `classes`, and each `tree.json` — is byte-identical, and carrier bytes are identical
between the frozen and patched builds (`demo-log.txt` §a/§c: `2/2` shas equal; §i regen: `2/2` carriers and
`2/2` tree.json identical).

### 5.3 Ordering argument (why this placement and no other)

- The refusal must sit **after the last envelope write and before the only manifest write**; in the patched
  order that is exactly S7→S8. Anything earlier cannot see all envelopes; anything later has already written
  the manifest the claim forbids.
- Delete-and-rewrite (`write_manifest` first, `os.remove` on refusal) is **rejected**: a crash, a signal, or a
  `SIGKILL` between the two leaves the unobserved manifest on disk, and a verifier reading the directory after
  a refusal would see the artefact the claim says cannot exist.
- The check reads `rea-full.json`, *not* `run.json`: `run.json` is the generator's own summary of the same
  in-memory shape, so checking it re-reads the writer's opinion. Reading the envelope also makes the check
  runnable by a counter on a committed directory with no generator state (§5.1 S3, `--tuple-check`).
- `--tuple-check DIR` is what makes CTL-C1-2 executable against **frozen bytes**: run on the committed
  round-42 held-out set it prints `REFUSE C02 combo gap_kinds: declared [...] observed [...]` and exits 3
  (`demo-log.txt` §f), while writing nothing.

---

## 6. Defects in the draft (attack)

### D1 (blocking) — the refusal does not fix the predictor, and the predictor is wrong on 42 % of seeds

The draft's generator-change paragraph describes *only* the refusal. With the predictor untouched, a
C02-shaped draw makes the generator exit 3 and the round produces no data; the claim would then be
unscoreable, not true. The measured incidence is 42.2 % of seeds (211/500, up to 4 carriers per seed;
`c02-shape-sim.py`).

Minimal fix, one clause, no new measurement: derive `reached` from the `published` fact the same function
already computes, i.e. move the `carved`/`published` block (**949-966**) above the depth block (**930-947**)
and replace 943-944 with

```python
reached = (not dep_effective) and published == 'nonzero'
```

which reproduces every currently-measured statement (clean → reached; dependency failure → not reached, even
when carved, as C10/C12/C20 measured; damaged v4 late block → reached, the C02 fix; damaged root legacy
fixture, `published == 'zero'` → not reached) and makes the two clauses incapable of contradicting each
other. The `wrap` branch (936-937) stays as written. The rule-8 text in
`precedence_observations` (2874-2880) and the `combo_declared` docstring (891-908) must say
"a damaged **v4** chunk publishes its earlier files before the late damaged block and therefore does reach the
ceiling; only a damaged root **legacy** fixture publishes nothing", replacing "a FAILING single root chunk
(damaged or dependency-missing) mints nothing".
`[INFERENCE]` the links=`none` variant of the shape is not directly measured (C02 had `links: in-tree`);
the `published`-derived rule predicts `depth-limited` there too, and the refusal is the arbiter — but if the
L1 wants zero inferential content in the predictor, restrict the clause to draws whose `published` clause is
already measured, i.e. keep the derivation (it *is* the measured `published` clause).

### D2 (blocking) — `--run` mandatory collides with the counter's regeneration arm

Round 42's counter regenerates by running the generator with **only** `--seed … --out …`
(`tools/round-42/c2-counter.py:1250-1253`) and then **hard-requires** `manifest.json` to exist —
`if not os.path.exists(rman_path): raise Unevaluable('generator_wrote_no_manifest', …)` (`:1256-1258`) — and
reads `declared_features`, `class`, `arm` and `sha256` out of the regenerated manifest (`:1265-1272`). P43-C1
binds "every carrier regenerates byte-identically from the seed" and "`generator_sha_matches_freeze`"-style
identity. If `--run` becomes mandatory, that arm becomes `Unevaluable` for every round-43 score.

Fix (adopted in the spec): `--carriers-only` — builds carriers + `tree.json`, writes **no manifest**, exit 0 —
and the round-43 `c1-counter.py` must (i) pass `--carriers-only` for its regeneration arm and (ii) compare
carrier bytes / `tree.json` against the **committed** manifest's per-carrier `sha256`, `class`, `arm`, instead
of reading a regenerated manifest. This must be written into `plans/round-43-claims.md` (`## Changes from the
draft`) before the freeze, because P43-C1's counting command and its "regenerates byte-identically" clause
currently presuppose the round-42 counter behaviour. The dev paths (`regen_check`, `run_selftest`) are fixed
in the same patch (S10, S11) so none of them creates a manifest either.

### D3 (plan text unsatisfiable by design) — "Combo C02's round-42 shape must appear among the new seed's combos"

The seed is the freeze commit hash and the factor draw is a pure function of it (`combo_factors` 826-876),
so the L1 cannot choose the seed. Measured: the shape appears in 42.2 % of seeds. In ~58 % of seeds the
sentence is false whatever the data does, and the claim would be killed by its own wording. Reword to a
conditional — "if the seed draws the C02 shape, the manifest declares what was observed, including
`depth-limited`" — and keep the *unconditional* demonstration where it belongs: CTL-C1-2 red on the frozen
round-42 C02 bytes (which is reproducible now: `demo-log.txt` §f).

### D4 (pre-existing, minor) — `--verify` fails on any `--classes` subset without `combo`

`verify()` 3040-3047: `majority = len(unseen_observed) * 2 >= max(combo_observed, 1)`; with no combos that is
`0 >= 1` → FAIL. Confirmed on the **frozen** generator too (`demo-log.txt` §i patched, §j frozen — both exit 1
with `combo_unseen_majority: observed 0/0 … FAIL`). Harmless for the claim's full-set run, but any seat that
develops on a subset and runs `--verify` sees a spurious failure. Fix if touched: skip the binding when
`combo_observed == 0` (say so in the output), or require the combo family in `--verify`.

### D5 (vacuity to disclose) — the tuple check is vacuous for the two `out-of-domain` carriers

H25/H26 run `inspect-firmware-regions` (binwalk); their envelope has `normalized_result.chunks == []`, so
`handlers=[]`, `gaps=[]`, `files=0`, `be_argv='n/a'` — which is exactly the declared tuple
(`EXPECTATIONS['out-of-domain']` at 1074-1075). The check therefore always passes there. Effective n for the
refusal is **76**, not 78. Not a defect, but P43-C1's "every envelope's observed six-field tuple equals its
declared tuple" is weaker than it reads; say so in the disclosed limits.

### D6 (recommendation) — keep the round-42 `manifest_before_envelopes` binding, or say why not

Round 42's counter bound it (`c2-counter.py:1337-1339`, `merge-base --is-ancestor`, which is true for equal
commits, so one commit holding both passes). P43-C1 does not list it. If the round-43 counter drops it, the
manifest and the envelopes may land in the same commit — fine — but then nothing binds that the *manifest* was
produced by the run rather than alongside it. The new `generator.tuple_check` block partly replaces it (it can
only exist if the run happened), and the counter should bind its presence and `all_equal == true` explicitly.

---

## 7. Evidence index (all under `artifacts/R43RevRevenger/`)

| file | sha256 | what it is |
|---|---|---|
| `placement.patch` (21 492 B) | `11060e49938577f4…` | `diff -u` frozen v4 → patched port; applies with `patch -p0` to the blob and reproduces sha `996c16a0…` (verified) |
| `tuple-check-proto.py` | `21a1798971885b65…` | standalone port of `_be_argv`/`_envelope_parts`/`observed_features` + the check; `--dir`, `--declared-from` (control only) |
| `c02-shape-sim.py` | `cfb5a7c9c536c859…` | incidence of the C02 shape using the frozen `combo_draw`/`combo_declared` |
| `manifest-delta.py` | `f6b9450302415074…` | manifest-byte delta with the intended-delta allowlist |
| `demo.sh` | `ce5636fd76055e94…` | reproduces §a-§k of the log |
| `demo-log.txt` (15 589 B) | `36337e2b82133261…` | every cited run, command, exit code and output |
| `ctl-c1-2-green-declared.json` | `71f6120ae447ade1…` | C02's tuple re-derived from `C02/rea-full.json` (the green input) |
| `ctl-c1-2-green.json` (54 023 B) | `16a56e3e29d10fb5…` | 78/78 PASS verdict on the same envelopes |
| `supplementary-log.txt` | `2f5253a25433c429…` | §l the patched full 78-carrier `--selftest` (all 17 checks PASS); §m `--run --gzip` then `--tuple-check` on the `.json.gz` directory (PASS) |

Key numbers, all in the log: frozen no-run manifest `ee41d057…` == frozen `--run --verify` regen manifest
`ee41d057…` (§a, §j) · patched no-run exit **4**, no dir (§b) · `--carriers-only` exit **0**, no manifest,
carriers byte-identical (§c) · patched `--run` on 2 real REA carriers: `tuple check PASS 2/2` (§d) ·
mutation `+extractor-failure` declared → exit **3**, per-carrier diff, no manifest (§e) · `--tuple-check` on
the round-42 held-out set → exit **3**, `REFUSE C02 … depth-limited` (§f) · 78/78 green (§g) · 6 intended /
0 unintended manifest deltas (§h) · `--verify` regen PASS on both restructured comparison sites (§i) ·
42.2 % C02-shape incidence (§k). `--gzip` also exercised (`supplementary-log.txt` §m): `--run --gzip` then
`--tuple-check` on the same directory → PASS. Full-set `--selftest` on the patched port:
`all 17 selftest checks passed`, exit 0 (`supplementary-log.txt` §l).

Rebuild recipe for the scratch inputs (no lane path is written):
`git -C <lane> show 6b9e64fe…:tools/round-42/heldout-gen-v4.py > $S/gen.py`;
`cp <lane>/tools/round-39/gen-squashfs.py $S/writer.py` (sha `f535e60e…` = the manifest's recorded writer);
`cp <lane>/tools/round-42/fixtures.json $S/fixtures.json` (sha `9f957663…` = the manifest's `pins_sha256`);
`patch -p0 < placement.patch`.

## 8. Limits and confidence

- **High confidence** on Q1-Q4 line references, the single manifest write, the three `build_set` call sites,
  the inverted order, and the byte-identity of a no-run and a run manifest (executed, not read).
- **High confidence** on the placement spec: the patched port runs the full 78-carrier `--selftest` (all 17
  checks PASS), a real 2-carrier REA run (PASS + manifest last), a red refusal (exit 3, no manifest), and
  reproduces the frozen bytes otherwise (6 intended deltas, 0 unintended).
- **Measured incidence, not a proof of necessity**: the 42.2 % is over pseudo-random seeds drawn from
  `sha256('probe<i>')`; the real freeze hash is one draw from the same function, so 42.2 % is the correct
  probability statement, not a prediction about the actual round-43 seed.
- `[INFERENCE]` (a) the links=`none` variant of the C02 shape mints `depth-limited` (D1); (b) that no other
  combo clause is wrong — round 42 exercised only 24 draws on one seed, so the refusal is the only real
  arbiter and the data run may still refuse on a clause nobody has measured. Both are exactly what the refusal
  is for; neither can be closed without running the round-43 set, which is the L1's post-freeze step.
- Not done by design: no freeze, no commit, no REA on third-party firmware, no reading of the round-43 counter
  (it does not exist at the base — `tools/round-43/` is absent), no mutation of the lane (read-only `git
  status` on the paths I touched is clean), no tool installs, scratch removed.
