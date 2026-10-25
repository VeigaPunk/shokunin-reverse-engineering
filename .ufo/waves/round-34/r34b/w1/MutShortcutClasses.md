# MutShortcutClasses — R34-C2 shortcut-class hardening (round 34 / run-6, wave 1)

Seat: `L1Kaidoku34-2.MutShortcutClasses` (mutation-tester, leaf).
Claim under attack: **R34-C2**, capability acquisition / axis depth — the pre-freeze
structure-blind shortcut-replay gate frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Assignment: stronger variant of each of the seven registered shortcut classes; score every
variant on `mini-counter.py` (green) and `naive-counter.py` (red); report the maximum matched
on the green surface.

**Maximum matched on the green surface over my variants: 8/8** (five independent readers,
four distinct mechanisms). The green surface is therefore defeatable and the frozen CLEAN
receipt is a statement about the seven *registered* readers only, not about the surface.

Run window (UTC): `2026-10-25T07:18:13Z` … `2026-10-25T07:25:53Z`. All work executed in
`/fast/scratch/hyaku/kaidoku-r34b/w1/MutShortcutClasses/` on a byte-copy of the pinned
instrument tree. Lane VCS read-only: only `git rev-parse HEAD` / `git log -1` were run; no
mutating git/jj verb, no lane file written except this report.

---

## 1. Inputs (pinned, hashed)

`cp -a <lane>/tools/round-34/. /fast/.../MutShortcutClasses/root/tools/round-34/` → 29 files.
sha256 of the lane originals (identical bytes in the scratch copy):

| instrument | sha256 |
|---|---|
| `tools/round-34/replay-gate.py` | `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` |
| `tools/round-34/c2-shortcut-gate-counter.py` | `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` |
| `tools/round-34/gate-config-mini.json` | `4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c` |
| `tools/round-34/gate-config-naive.json` | `72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428` |
| `mini-fix/mini-counter.py` | `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52` |
| `mini-fix/naive-counter.py` | `087c97f77ec15e239a6eaa3717317e19312572967220a8ddb0fb2cb92b9f6894` |
| `mini-fix/build.py` | `c67180515bcb1b777efa8d763917832ee9024b59329b65ef4b2c3b112628e32e` |
| `mini-fix/expected.json` | `5ebb5349fd21eb3e885c775cb0068ece04188b9a9a7fdc414c1c83a2d8828483` |

Lane tip at measurement: `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (`git rev-parse HEAD`,
07:18:13Z). Python: `/usr/bin/python3` = 3.14.8. No tool installed or upgraded (nothing was
needed; `python3` + stdlib only). No network used. No ELF, fixture or reader executed as a
program of interest: readers are spawned as `python -I -B <reader> <path>` by the counters,
fixtures were only ever read as static bytes.

## 2. Method

1. Scored the seven registered readers plus `structural.py` on both counters to reproduce the
   frozen numbers (§3.1).
2. Wrote one hardened variant per registered class (`variants/s2_*.py`), plus one or two
   sub-variants where a class has more than one strengthening direction (`s2b_*`, `s2c_*`,
   `s2d_*`). Tables were generated from the pinned `expected.json`, never hand-typed, by
   `gen_variants.py` (`/usr/bin/python3 -I -B gen_variants.py`, rc 0, 07:20:00Z, 13 files).
3. Scored every reader on green and red with the pinned counters, then on a third
   *perturbed-payload* surface I built to test whether the 8/8 hits were memorization
   (`score_all.py`, rc 0, 07:24:23Z → `out/final-score.json`).
4. Gate controls: pinned green and red configs, then a config registering all 12 hardened
   variants, run twice for stability; plus seed randomization and a lying-counter probe.

Counter invocations were exactly the gate's own recipe:
`/usr/bin/python3 -I -B <counter> --root <abs root> --control-reader <abs reader>`, env
`PATH=/usr/bin:/bin HOME=/tmp LANG=C` (the same env `mini-counter.py:116-118` and
`naive-counter.py:48-51` give readers).

## 3. Results

### 3.1 Pinned readers, reproduced (scratch copy, absolute root)

| class (reader) | green | red | gate row |
|---|---|---|---|
| all-false | 0/8 | 0/8 | below |
| size-keyed | 1/8 | 1/8 | below |
| fixed-slice | 0/8 | **0/8** | below |
| digest-keyed | 0/8 | **0/8** | below |
| string-scan | 0/8 | **0/8** | below |
| record-order-replay | 0/8 | **0/8** | below |
| label-memorization | 0/8 | 8/8 | **over** (red) |
| structural (positive control) | 8/8 | 8/8 | — |

Gate reproduction (07:22:24Z / 07:22:25Z):

```
python3 -I -B root/tools/round-34/replay-gate.py --root "$S/root" \
    --config "$S/root/tools/round-34/gate-config-mini.json" --json-out out/gate-pinned-green.json
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-   rc=0
python3 … --config "$S/root/tools/round-34/gate-config-naive.json" …
REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization   rc=2
```

This reproduces `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` exactly
(`green_positive_matched=8`, `shortcuts_below_target=7`, red over `label-memorization`).
Receipts: `out/gate-pinned-green.json`, `out/gate-pinned-red.json`.

### 3.2 Hardened variants — every number is an executed receipt

From `out/final-score.json` (07:24:23Z); columns green / red / perturbed-payload:

| registered class | hardened variant | green | red | perturbed | what the variant keys on |
|---|---|---|---|---|---|
| all-false | `s2_all_false` | 0/8 | 0/8 | 0/8 | nothing (floor) |
| size-keyed | `s2_size_keyed` | **1/8** | 1/8 | 0/8 | size (all eight are 512 B) |
| fixed-slice | `s2_fixed_slice` (8 strides) | **0/8** | 0/8 | 0/8 | fixed offsets only |
| " | `s2d_fixed_slice_offsets_memo` (hybrid) | **8/8** | 7/8 | 0/8 | every offset + memorized payload |
| digest-keyed | `s2_digest_keyed` (all 8 digests) | **0/8** | 8/8 | 0/8 | whole-file digest |
| " | `s2b_digest_replay` | **8/8** | 0/8 | 0/8 | digest of the *permuted* copy, replayed offline |
| string-scan | `s2_string_scan` | **0/8** | 0/8 | 0/8 | printable runs, no payload |
| " | `s2b_string_name_keyed` | **8/8** | 8/8 | 0/8 | name pool + memorized name→(flags,value) |
| " | `s2c_string_pool_noheader` | **8/8** | 8/8 | 0/8 | printable runs only, no header at all |
| record-order | `s2_record_order` (count key) | **6/8** | 6/8 | 0/8 | record count + memorized sequence |
| " | `s2b_record_sig` | **8/8** | 8/8 | 0/8 | (count, ordered (flags,value) pairs) |
| label-memorization | `s2_label` (full + normalized) | **0/8** | 8/8 | 0/8 | basename |
| " | `s2b_label_hash_replay` | **8/8** | 0/8 | 0/8 | basename `opaque-<sha256[:20]>.data`, replayed |

`max_green_over_variants = 8` (`out/final-score.json:max_green`).

Five readers hit 8/8 on green: `s2b_string_name_keyed`, `s2c_string_pool_noheader`,
`s2b_record_sig`, `s2b_digest_replay`, `s2b_label_hash_replay`; the hybrid `s2d` is a sixth.

None of the seven registered readers reaches 8/8 on green, and six of them miss on red as
well — see F2.

### 3.3 Gate control: would the gate catch a strengthened class?

Registering all 12 hardened variants as shortcut classes and re-running the same pinned gate
(07:22:37Z, repeated 07:23:54Z and 07:23:56Z, identical output):

```
REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 \
shortcuts_over_target=s2b_digest_replay,s2b_label_hash_replay,s2b_record_sig,s2b_string_name_keyed,s2c_string_pool_noheader   rc=2
```

Receipts `out/gate-strong.json`, `out/gate-strong-1.json`, `out/gate-strong-2.json`
(`classes_over_target` identical across runs). The gate *mechanism* is sound: it refuses as
soon as one registered shortcut meets target. The frozen CLEAN therefore measures the
registered reader set, not the green surface.

### 3.4 Perturbed-payload control (is the 8/8 real memorization?)

`root2` = the same eight fixtures with record 0 of every fixture rewritten
(`value ^= 0x01010101`, `flags ^= 1`, same 512-byte size, header untouched) and
`expected.json` recomputed from the decoded bytes. Positive control `structural.py` scores
**8/8** on it, which validates the recomputed expectation; every memorizing variant scores
**0/8** (`.ufo`-external artifact `out/final-score.json:perturbed_green`; the run at
07:23:0xZ printed `structural 8/8`, `s2b_record_sig 0/8`, `s2b_string_name_keyed 0/8`,
`s2c 0/8`, `s2b_digest_replay 0/8`, `s2b_label_hash_replay 0/8`, `s2_record_order 0/8`,
`size_keyed 0/8`, `label_replay_full 0/8`).

So the 8/8 hits are memorization of *constant* payloads, not decoding: one value/flag
perturbation per fixture kills all of them while leaving the structural reader at 8/8.

### 3.5 Seed control

The green counter takes `--seed` (default `kaidoku-r34-mini-v1`, `mini-counter.py:139`) and the
gate config never passes one. Re-scoring with `--seed kaidoku-r34-mini-v2` (07:24:48Z,
`out/seed-v2.txt`):

| reader | seed v1 (green) | seed v2 |
|---|---|---|
| structural | 8/8 | **8/8** rc 0 |
| `s2b_digest_replay` | 8/8 | **0/8** rc 1 |
| `s2b_label_hash_replay` | 8/8 | **0/8** rc 1 |
| `s2b_string_name_keyed` | 8/8 | **8/8** rc 0 |
| `s2b_record_sig` | 8/8 | **8/8** rc 0 |

Randomizing the permutation seed defeats the two *replay* routes only. The content-keyed
routes survive any permutation, because the permutation preserves the string multiset and the
payload bytes.

## 4. Findings

**F1 — DEFECT (green surface). Maximum matched = 8/8; the frozen CLEAN does not establish
"only record-traversal can pass".**
Two independent root causes, both evidenced above:

* **F1a fixture/content keying** — the transformation is a re-encoding, not a perturbation.
  `permute()` (`mini-counter.py:57-82`, docstring `:5-6`) preserves: total size, record order,
  every record's `flags`/`value`, the u16 count, and the *multiset* of pool strings; it only
  rewrites `name_off`. The fixture set is memorizable by content:
  25 names, **25 unique**, each name carrying **exactly one** `(flags,value)` in the whole set
  (measured on the scratch copy; `s2b_string_name_keyed` embeds that map).
  Hence a reader that never touches `records_off` reproduces `expected.json` exactly:
  `s2b_string_name_keyed.py` reads only the header's `names_off` (`:14`) and the pool;
  `s2c_string_pool_noheader.py` reads no header, no record array, no `name_off` at all.
  Independently, `(count, ordered (flags,value) pairs)` is a **perfect identity key**:
  all 8 fixtures have distinct payload signatures (`s2b_record_sig.py:13-19` reads the array's
  payload columns only) → 8/8.
* **F1b green-counter identity leak** — the transform is deterministic with a public fixed
  default seed and the copy is named by its own digest
  (`mini-counter.py:114`, `"opaque-" + sha256(transformed)[:20] + ".data"`), and readers run
  unisolated (only `PATH`/`HOME`/`LANG` replaced, `:116-118`; the lane tree is still
  readable). Replaying `permute()` offline reproduces all eight copies' digests
  (verified byte-for-byte against the counter's own `transformed_sha256`,
  07:20:5xZ) → `s2b_digest_replay` (hash only) 8/8 and `s2b_label_hash_replay`
  (basename only) 8/8. The "opaque" name leaks the identity it is supposed to remove.

**F2 — the registered below-target evidence is largely vacuous (4 of 7 classes).**
`fixed-slice`, `digest-keyed`, `string-scan` and `record-order-replay` score **0/8 on the
shape-only red counter too**, i.e. they cannot win even where identity, labels and digests
survive. They are not competitive specimens of their classes, so "they stay below target on
green" carries no information:
* `digest_keyed.py:7-9` keys on `e1c4d1d5`; `sha256(alpha.mrec)[:8] = d1de0e6f` — the memo key
  matches **no** fixture.
* `record_order_replay.py:16-18` treats `name_off` as an index into an 8-name list; real
  `name_off` values are pool offsets (alpha `[0,10,20]`, gamma `[0,14,30,41,54]`), so it drops
  all but one record per file on every surface.
* `fixed_slice.py` guesses `value=offset`; `string_scan.py` guesses `flags=0,value=0` — both
  structurally cannot hit the expected payload.
Only `label-memorization` is a live class (8/8 red), `size-keyed` is capped at 1/8 by design,
and `all-false` is a floor. The red case, and therefore the gate's discrimination, rests on
**one** reader.

**F3 — per-class maxima on the green surface (measured):**

| class | max green | structural reason for the cap |
|---|---|---|
| all-false | 0 | emits nothing |
| size-keyed | 1 | one key → one fixture (all eight are 512 B) |
| fixed-slice (pure) | 0 | offsets cannot supply payload; hybrid with a memo table → 8 |
| digest-keyed | 0 honest / **8** replay | identity is only defeated if the transform is unpredictable |
| string-scan | 0 pure / **8** with name→payload memo | payload is constant per name |
| record-order | 6 (count key) / **8** (payload signature) | count groups `{1: beta,epsilon}`, `{3: alpha,eta}` cap a count-only key at 6 |
| label | 0 honest / **8** replay | the opaque basename is the digest |

So the assignment's rule ("anything below is evidence the green surface defeats identity
keying") holds only for the *strict* identity keys (size, fixed offset, digest-of-input,
label-of-input) and fails the moment the key carries fixture content.

**F4 — gate hardening gap: `met_target` is trusted, never cross-checked.**
`replay-gate.py:93-99` type-checks `matched`/`target`/`met` and `:98` compares `target` to the
config, but never checks `met == (matched >= target)`. Probe (07:25:53Z):
`probe/fake-counter.py` reports the positive control as `matched=3, target=8, met_target=true`
and three shortcuts as `matched=0, met_target=false`; the pinned gate then printed
`REPLAY_GATE_CLEAN finding=no_shortcut_meets_target` rc 0 (`out/gate-fake-counter.json`) — a
CLEAN with the positive control below target, which is exactly the vacuity the gate exists to
refuse. The production receipt is partly protected by
`c2-shortcut-gate-counter.py:118` (`green_positive_matched == 8`, read from `matched`), but the
gate alone fails open on an inconsistent receipt. One-line fix:
`if met != (matched >= config["target"]): raise Unevaluable("counter_receipt_inconsistent")`.
Note also `c2-shortcut-gate-counter.py:109-110` records `shortcuts_below_target` from
`met_target` without asserting it, so the frozen green clause is not independent of the same
field.

**F5 — operational: a relative `--root` silently degrades the gate.**
`resolve()` (`replay-gate.py:71-73`) returns a root-relative path, but the counter runs with
`cwd=root` (`:80`), so `--root root` double-prefixes (`root/root/tools/...`); the counter
answers `reader_absent` and the gate mislabels it `REPLAY_GATE_UNEVALUABLE
finding=counter_receipt_fields` rc 3 (07:23:56Z, `out/gate-relroot.json`) instead of naming the
path problem. The pinned receipt used an absolute `--root`, so the frozen numbers are
unaffected; the instrument should resolve root to absolute before spawning.

**F6 — remedial surface (validated).** A payload-perturbing surface defeats every memorizer:
one `value`/`flags` rewrite per fixture with a recomputed expectation gives
structural 8/8, all memorizers 0/8 (§3.4). Seed randomization alone is insufficient (§3.5).

**F7 — what the gate still does right (do not over-claim in the other direction).** The
gate's selftest/refusal/positive-control machinery is intact: pinned red is REFUSED for the
correct class (rc 2), registering my strong readers is REFUSED (rc 2, stable), and no reader
in the set can reach 8/8 without either walking the record array or embedding a memorized
table. The claim's *mechanism* survives; its *evidence set* and *green surface* do not.

## 5. Remediation (ranked, all fixture-side except R4)

1. **Perturb the payload per run** (R1): rewrite at least one record's `value`/`flags` in each
   transformed copy, shuffle record order, and recompute the expectation from the decoded
   bytes. Kills F1a and `s2d` (§3.4). This is the only change that closes the content-keyed
   routes.
2. **Randomize the transformation per invocation** (R2): drop the fixed default seed / pass
   `--seed` from the gate from a fresh entropy source. Kills the replay routes (F1b) but not
   F1a.
3. **Isolate the reader** (R3): run it in a temp-only view of the filesystem (no lane tree, no
   fixtures directory, no counter source). Removes offline table building for the replay
   routes.
4. **Make the registered set non-vacuous** (R4): require each registered shortcut to meet
   target on the red surface (`met_target` on the naive counter) or mark the class
   `UNEVALUABLE`; and repair or drop `digest_keyed` (`e1c4d1d5` ≠ `d1de0e6f`) and
   `record_order_replay` (index ≠ pool offset) so they are real specimens — otherwise register
   the strengthened `s2_digest_keyed` (8/8 red, 0/8 green) and `s2_record_order` (6/8 both) as
   the class representatives.
5. **Cross-check the receipt** (R5): `met == (matched >= target)`, plus a `>=` vs `==`
   decision made explicit; assert `shortcuts_below_target` in the C2 counter instead of
   recording it.
6. **Absolute root** (R6): `resolve()` → `Path(root).resolve() / path`.
7. If the surface is changed, the frozen claim must be re-frozen: with any one of
   `s2b_string_name_keyed`, `s2b_record_sig`, `s2b_digest_replay`, `s2b_label_hash_replay`,
   `s2c_string_pool_noheader` registered, the gate returns REFUSED, so the current CLEAN
   cannot stand as evidence for a stronger class set.

## 6. Verdict

**Max matched on the green surface over my hardened variants: 8/8 — DEFECT, not a coverage
finding.** The pre-freeze green surface leaves two independent 8/8 routes open: (a) the
permutation preserves the payload bytes and the global uniqueness of names, so a
content-keyed memorizer (`s2b_string_name_keyed`, `s2c_string_pool_noheader`,
`s2b_record_sig`, 8/8 each) never needs to associate a name with its record; and (b) the
transformation is deterministic under a public default seed and leaks the copy's digest into
the file's basename, so identity-keyed replay (`s2b_digest_replay`, `s2b_label_hash_replay`,
8/8 each) survives the "opaque" rename. The registered seven stay below target only because
four of them are non-competitive even on the shape-only red counter and one is a floor. The
gate's refusal/window machinery is sound and refuses a strengthened class set (rc 2, stable),
so the repair is fixture-side (payload perturbation + per-run randomization + reader
isolation) plus registering non-vacuous class specimens; the frozen CLEAN receipt must not be
promoted to "no structure-blind shortcut can pass" until then.
Pinned claim `R34-C2`: **not contradicted by this seat's controls on the gate mechanism**;
**the green-surface evidence supporting it is falsified as stated**.

## 7. Artifacts (scratch, evidence pointers)

| path (under `/fast/scratch/hyaku/kaidoku-r34b/w1/MutShortcutClasses/`) | content |
|---|---|
| `root/` | byte copy of the pinned `tools/round-34` tree (29 files) |
| `root2/` | perturbed-payload control surface (record 0 `value ^= 0x01010101`, `flags ^= 1`, recomputed `expected.json`) |
| `gen_variants.py` | deterministic variant generator (tables from `expected.json`) |
| `variants/` | 13 hardened readers, sha256 per file in `out/final-score.json` |
| `score_all.py`, `out/final-score.json` | green / red / perturbed scores, exits, matched fixture lists, per-variant sha256 |
| `out/gate-pinned-green.json`, `…-red.json` | reproduction of the frozen gate verdicts |
| `out/gate-strong.json`, `…-1.json`, `…-2.json`, `out/gate-config-strong.json` | REFUSED when the hardened variants are registered |
| `out/gate-fake-counter.json`, `probe/` | gate CLEAN with positive control `matched=3, target=8, met_target=true` |
| `out/seed-v2.txt` | seed-2 rerun table |
| `out/gate-relroot.json` | relative-`--root` degradation |
| `out/score-table.json`, `logs/score-2.log` | second pass (post table-shape fix), before the control surfaces |

Mid-run correction disclosed: my first generator emitted the memorized tables as JSON arrays,
which the counters' `canonical()` (`mini-counter.py:85-97`, `naive-counter.py:18-30`) rightly
rejects, so five variants read 0/8 on their first pass; the tables were re-emitted as
`{name,flags,value}` objects and every number above is from the corrected pass (the first
pass' output was terminal-only; `out/score-table.json` and `logs/score-2.log` are the second,
already-corrected pass, and `out/final-score.json` supersedes both). That strictness is a good
property of the counters, not a defect.

Untested by this seat (deliberately): the gate selftest mutants (L1-owned), the production
reader, and the twelve R34-C1 carriers — none executed, per the inherited stop.
