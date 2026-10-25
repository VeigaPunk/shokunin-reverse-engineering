# MutFixtures — fixture strength of the R34-C2 green surface (wave 1, seat MutFixtures)

Claim under attack: **R34-C2** (capability acquisition, axis depth), pre-freeze structure-blind
shortcut-replay gate, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`
(`.ufo/waves/round-34/r34b/claims.json`). Inherited R34-C1 untouched: no GNU version-needs reader,
carrier or fixture was executed or scored.

Axes named before acting (Godspeed): **A1** which registered shortcut class can cross a weakened green
surface; **A2** what each green-surface invariant actually buys (measured, not asserted); **A3** whether
`matched == 8` still means eight distinct decodes. Everything below is a probe on private copies; the
lane instruments were read only.

Window: 2026-10-25T07:20:25Z → 2026-10-25T07:28:53Z. Host python: `/usr/bin/python3` = 3.14.8.
No tool installed or upgraded (nothing needed; pacman is paused host-wide and was not touched).

---

## 1. Isolation, baseline reproduction, restoration evidence

Scratch tree (all writes): `/fast/scratch/hyaku/kaidoku-r34b/w1/MutFixtures/`. Each probe gets its own
root so no two probes share mutable state; `pristine/` is a byte copy of the pinned instruments.

Lane pin audit, after every probe (`python3 -I -B` over `claims.json.pins`, 07:27:50Z):

```
pinned_paths 26  mismatches 0
scratch_pristine_matches_lane True
```

`jj status` (read-only, 07:28Z) shows **no modification under `tools/`** — only other seats' `.ufo` files.
Every mutated artifact is a new file inside my scratch root; no shared copy was overwritten, so
"restoration" is: `pristine/` still hashes to the 26 pins, and `manifest.json` records the
fixtures+expected+counter hash of every surface (`manifest.json`, 11 surfaces).

Baseline on the pristine copy (07:20:25Z):

```
cd /fast/scratch/hyaku/kaidoku-r34b/w1/MutFixtures/pristine
python3 -I -B tools/round-34/replay-gate.py --root . --selftest
  -> exit 0, {"cases": 12, "failures": 0, "mutants_killed": 3, "mutants": 3}
python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-mini.json --json-out gate-green.json
  -> exit 0, REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-
python3 -I -B tools/round-34/replay-gate.py --root . --config tools/round-34/gate-config-naive.json --json-out gate-red.json
  -> exit 2, REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization
```

Per-class `matched` (counter-direct, pristine, default seed, 07:25:53Z):

| class | green counter (rename+permute) | naive counter (no transform) |
|---|---|---|
| structural | **8** | 8 |
| all-false | 0 | 0 |
| size-keyed | 1 | 1 |
| fixed-slice | 0 | 0 |
| digest-keyed | 0 | 0 |
| string-scan | 0 | 0 |
| record-order-replay | 0 | 0 |
| label-memorization | 0 | **8** |

This reproduces the production receipt `.../r34b/after/c2-at-instruments.json` exactly (green 7 below,
positive 8; red over = label-memorization only). The claim's six clauses hold at the pinned registry.

---

## 2. The four assigned weakenings (pinned gate, pinned counter, config copies)

Every run below is `tools/round-34/replay-gate.py --root . --config <copy>` executed with
`cwd = <surface root>`; only the fixture bytes / a counter copy differ. Receipts: `receipts.txt`,
per-surface `gate-*.json`.

### (a) eight fixtures with distinct sizes — 07:24:26Z, exit **3**, class crossing: **none**

Sizes 512/544/576/608/640/672/704/736. Result:

```
REPLAY_GATE_UNEVALUABLE finding=counter_receipt_fields shortcuts_below_target=0 shortcuts_over_target=-
```

The counter never scores anything: `mini-counter.py:decode_fixture` starts with
`if len(data) != SIZE or data[0:4] != MAGIC: raise Unevaluable("fixture_shape")` (`SIZE = 512`,
`mini-counter.py:29-31`). Counter stdout on this surface (07:27:50Z, exit 3):

```json
{"finding": "unevaluable:Unevaluable:fixture_shape", "met_target": false, "predicate": "P34-mini-records: ..."}
```

The gate then reports `counter_receipt_fields` because that payload carries no `matched`/`target` int.
So the size equality of the green surface is **enforced by the counter's format assertion, not by the
fixture design**, and a size-varied surface makes the green clause unevaluable with a diagnostic that
does not name size as the cause.

Supplementary, on a probe-only counter copy with that one assertion removed
(`mini-counter-sizefree.py`, sha256 `4b45f143a36ae9117ae6835a38afdc05060758b12138ab0a15ab738c48f86f17`):

- 07:24:27Z, size-free counter, pinned readers: `REPLAY_GATE_CLEAN` exit 0 — structural 8,
  size-keyed 1 (its template knows only 512).
- 07:24:28Z, + a probe-only **trained** size-keyed reader (8 size→payload entries,
  `size_trained.py` sha256 `cdf04af30dc8fb76e7409253df4575f632dfdd55aed7501819434ee52fdae510`):
  `REPLAY_GATE_REFUSED` exit 2, `shortcuts_over_target=size-keyed-trained` **8/8**.

Interpretation (A2): equal sizing is *injective-defeating*. The eight expected payloads are distinct
(verified: 8 fixtures, 8 distinct payloads), so one size can select at most one answer — a size-keyed
reader is capped at 1/8 no matter how it is trained. Distinct sizes lift that cap to 8/8. The green
surface therefore buys size-blindness by forbidding size variance outright; it does not test it.

### (b) shortened / aligned names — 07:24:29Z and 07:24:30Z, exits **0**, class crossing: **none**

- b1 (`names_off` forced to 64, names packed, no padding): `REPLAY_GATE_CLEAN` exit 0, fixed-slice 0.
  Post-permutation slice at `data[64:96]` is empty for all 8 fixtures — the pool is reshuffled, so 64
  is not a name start.
- b2 (name strings normalised to exactly 31 chars so every pool slot is 32 bytes = the reader's stride):
  `REPLAY_GATE_CLEAN` exit 0, fixed-slice 0, size-keyed 0. Audit of the permuted bytes: `data[64:96]`
  begins with NUL runs, then a name — i.e. the grid does not survive.

Mechanism (`mini-counter.py:permute`): the transformation splits the **whole** pool region at every
NUL, so the zero padding of a 512-byte fixture becomes hundreds of empty strings that are shuffled with
the names. Any layout with padding is therefore destroyed, and shortening names does not help.

Controlled pair — the same fixture bytes, two counters (07:27:37Z):

```
surf-b3 (grid names_off=64, 32-byte slots, values = name offsets; 512 B, count 1..6)
  python3 -I -B tools/round-34/mini-fix/naive-counter.py --root . --control-reader .../fixed_slice.py
    -> exit 0, fixed-slice matched 8/8
  python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader .../fixed_slice.py
    -> exit 1, fixed-slice matched 0/8
  gate --config tools/round-34/gate-config-mini.json -> exit 0, REPLAY_GATE_CLEAN
```

`fixed_slice.py` reads only bytes, so the **rename cannot affect it**: the entire 8→0 delta is the
permutation. That is the one measurable thing the permutation buys against a registered class.

The class is also dead by construction. `fixed_slice.py` scans `range(64, len(data), 32)` and emits
`value = offset`; to match, a fixture must (i) put a name start at 64, (ii) encode `value = offset`,
and (iii) tile the whole 512 bytes on a 32-byte grid. (i)+(iii) is arithmetically impossible under the
pinned format: `names_off + 32c = 512` with `16 + 8c <= names_off <= 64` gives `c >= 14` and
`c <= 12.4`. Probe b4 (12 records, `names_off=128`, exact 384-byte pool, offset values, 07:24:32Z)
confirms the collision: `REPLAY_GATE_CLEAN`, fixed-slice 0, and the raw fixture already yields **13**
records (12 names plus one bogus run from the record-array region 64..128).

Interpretation (A2): name length/alignment buys nothing on this instrument. Fixed-slice is defeated by
the format's semantic `value` field and by the 40-byte header arithmetic, not by the permutation; the
permutation merely adds an independent second defeat.

### (c) name pool left unpermuted — 07:24:33Z, exit **0**, class crossing: **none against the registry**

The pool order is fixed by `build.py`, and the permutation is a counter transformation, so the faithful
implementation of "keep the pool unpermuted" is the counter copy with `rng.shuffle(order)` removed
(`mini-counter-nopermute.py`, sha256 `6f09429bde23a71d47be34c764fa7aa724ae0c0c494c4952d50b50a1200b9f92`);
fixture bytes stay pin-identical. Verified identity on all 8 fixtures (`transform == input`: True ×8).

```
REPLAY_GATE_CLEAN exit 0 — structural 8, size-keyed 1, all other pinned classes 0
```

No pinned class moves. In particular label-memorization stays 0 (the counter still renames to
`opaque-<sha20>.data`) and digest-keyed stays 0 (its single template key `e1c4d1d5` matches no fixture
digest — alpha is `d1de0e6f…`). The permutation is therefore **not** what the frozen registry is
sensitive to.

Isolating the rename instead (counter copy keeping the permutation, target file named by the fixture
basename — `mini-counter-renamefree.py`, sha256 `320ba30620fde3cbecaf17a2b3ab0cbc78b8aa15ff8277c48bc4bc485e79bdba`,
07:26:26Z): `REPLAY_GATE_REFUSED` exit 2, `shortcuts_over_target=label-memorization` **8/8**. The
opaque rename, not the permutation, is the load-bearing identity-defeating step for label memorization.

Supplementary (07:24:34Z): a probe-only digest reader trained once over the (now identity) digests,
`digest_trained_identity.py` sha256 `eb5a85301a7afdd60b38a488fbc9a81f3778626bdf69d2fe845d5068e6785714`,
scores **8/8**: `REPLAY_GATE_REFUSED` exit 2, `shortcuts_over_target=digest-keyed-trained`.

### (d) two fixtures byte-identical — 07:24:35Z / 07:24:37Z, exits **0** and **3**

- d1 (consistent: `beta.mrec := alpha.mrec`, beta expected = alpha expected; both sha256
  `d1de0e6f50eca499d70fc619bfa0bba52d9d789e36d2fba31109ffd6a922ad44`, expected.json
  `4c4dc0c2979ab2411543dd9812b8d2a0f80798a2336e2a229cc5cd09e77f7dc4`):
  `REPLAY_GATE_CLEAN` exit 0, structural 8, size-keyed 2, every other pinned class 0.
  The surface now decodes **7 distinct payloads for 8 fixtures** (verified: 8 fixtures, 7 distinct
  payloads), so `matched == 8` no longer implies eight distinct decodes (A3).
  Note the eight *transformed* digests are still distinct (8) because the counter advances one seeded
  RNG across fixtures in sorted order — duplicate content does not collapse the digest channel.
- d1' (+ trained digest over those 8 digests, 07:24:36Z): `REPLAY_GATE_REFUSED` exit 2, 8/8.
- d2 (inconsistent: beta bytes = alpha bytes, beta expected left as beta's own): structural **7** →
  `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target` exit 3. Positive result for the
  gate: its positive control does catch a fixture/expectation mismatch, so the green clause is not
  vacuous in that direction.

---

## 3. Supplementary falsifier of the green clause's class-level reading

The frozen green case scores seven *readers*; `predicate`/claim language speaks of *classes*. On the
**unmodified** fixture surface with the **pinned** counter and gate (07:24:38Z), one probe-only reader
of an already-registered class — digest-keyed, trained once on the counter's own disclosed
`transformed_sha256` values (`digest_trained_pinned.py` sha256
`8c8fa1b32a81eabb8ad7fef73ca966531653d03c014975c0365363b735561c11`) — yields:

```
REPLAY_GATE_REFUSED exit 2  shortcuts_below_target=7  shortcuts_over_target=digest-keyed-trained
rows: digest-keyed-trained matched 8
```

Why it works, and what would stop it:

- `mini-counter.py` seeds `random.Random("kaidoku-r34-mini-v1")` with a constant and prints
  `transformed_sha256` for every row. Two runs give identical digests (07:24:51Z:
  `digests_identical True`), and my independent re-computation of `permute()` matches the counter's
  receipt byte for byte (e.g. alpha `c7adf97ff221d6b3f427e336bb4e78aeb34edd06af753a436634ae6e2ba3e3e8`).
  One prior run is enough to train the map; every later run scores 8/8 without decoding anything.
- Same reader, seed `kaidoku-r34-mini-v2`: **0/8**, exit 1 (`records_mismatch`), while structural stays
  8/8 under that seed. So the attack's precondition is the *fixed* seed, not the permutation itself.

This does not by itself relabel R34-C2: the six clauses are registry-relative and remain true for the
seven registered readers. It does show the green clause is a statement about seven under-trained
witnesses, not about the classes they are named after.

---

## 4. What each invariant buys (the measured answer)

| invariant | measured purchase | evidence |
|---|---|---|
| equal 512-byte size | caps a size-keyed reader at 1/8 because the 8 expected payloads are distinct; on a size-free counter + distinct sizes a trained size key scores 8/8 | a (exit 3), a′ (exit 0, 1/8), a″ (exit 2, 8/8) |
| name-pool permutation | flips fixed-slice 8/8 → 0/8 on identical bytes; defeats only an *untrained* digest reader | b3 naive 8/8 vs b3′ pinned 0/8; e 8/8 |
| opaque rename (not permutation) | flips label-memorization 0/8 ↔ 8/8 | c (0) vs c2 (8/8) |
| name length / 32-byte alignment | nothing: fixed-slice stays 0 with packed or grid-aligned names; needs `value = offset` + impossible exact tiling | b1, b2, b4 |
| eight distinct fixtures | `matched == 8` can be met with 7 distinct decodes; the positive control is what catches an inconsistent duplicate | d1 (7 payloads, 8 matched), d2 (exit 3) |

---

## 5. Findings (draft only — nothing landed, no lane file edited)

**F1 (high, coverage).** `green_clean` is registry-relative and is reachable *against the pinned
instruments* by a trained digest-keyed reader, because the permutation seed is a constant and the
counter publishes `transformed_sha256`. Severity rests on the claim sentence "none meets the target"
being read at class level. Draft wording for L1, not applied: either derive the salt per run from
`os.urandom` (and keep it out of the receipt), or restate the clause as "none of the seven registered
witnesses meets the target" and drop class-level language.

**F2 (high, coverage).** Six of seven registered classes are dead witnesses: on the shape-only counter —
where every identity-defeating step is absent — they still score all-false 0, size-keyed 1, fixed-slice
0, digest-keyed 0, string-scan 0, record-order-replay 0. Mechanisms, from the readers' own stdout on
`alpha.mrec` (07:26:26Z): `fixed_slice` → one fragment `.so.1` with `value 64`; `record_order_replay` →
1 record of 3, indexing an 8-name list with a **byte offset** (`name_off`); `digest_keyed` → `[]`
(template key `e1c4d1d5` matches no fixture, all begin `d1de/a854/79ff/82f0/5bca/ffb5/b1f8/19ff`);
`string_scan` → correct names with `value 0`. The gate has no liveness clause, so a below-target score
on the green counter carries no information for those six. Draft wording: require each registered
shortcut to meet the target on the shape-only counter before its green-counter score counts.

**F3 (medium, diagnosability).** Size variance makes the green surface unevaluable and the gate reports
`counter_receipt_fields` instead of the counter's own `unevaluable:Unevaluable:fixture_shape`; the size
invariant is asserted by `SIZE = 512` in the counter, so it constrains the instrument and does not
transfer to real ELF carriers, whose sizes vary. The counter's `--seed` is likewise unstated in the
predicate.

**F4 (medium, instrument scope).** The permutation's measurable purchase against the frozen registry is
exactly one class (fixed-slice, and only when the fixture is aligned *and* offset-encoded); it buys
nothing against label memorization (rename does that) and nothing against a digest trained once. Draft
wording: describe the permutation as "defeats offset-grid readers", not as "identity-defeating" in
general.

**F5 (low, arithmetic).** Fixed-slice cannot cross any conforming 512-byte fixture: matching needs
`value = offset` (never present; values are semantic version codes) and exact 32-byte tiling, which is
impossible with `16 + 8c <= names_off <= 64` (`c >= 14` vs `c <= 12.4`). Its 0/8 is therefore not
evidence about the counter.

**F6 (positive).** The positive control is load-bearing and works: an inconsistent fixture/expectation
pair (d2) is refused as `positive_control_below_target` (exit 3) rather than passed.

---

## 6. Receipts index (scratch, disposable)

`/fast/scratch/hyaku/kaidoku-r34b/w1/MutFixtures/`
`build_surfaces.py` (driver, builds every surface and runs the gate), `surfaces.json` (full matrix),
`receipts.txt` (per-probe command + exit + verdict line, UTC), `manifest.json` (per-surface
fixtures/expected/counter hashes), `pristine/` (pin-identical copy), and one root per probe:
`surf-a-distinct-sizes/`, `surf-b1-short-names-packed/`, `surf-b2-stride-aligned/`,
`surf-b3-aligned-offset-values/` (also carries the pinned-counter and naive-counter pair),
`surf-b4-exact-tile-permuted/`, `surf-c-unpermuted/`, `surf-c2-permuted-renamed-free/`,
`surf-d1-duplicate-bytes/`, `surf-d2-duplicate-inconsistent/`, `surf-e-trained-on-pinned/`.
Each root holds its `gate-*.json` payloads.

Mutant accounting: **killed** — size invariance (a, once the probe counter lets it be measured: 8/8 for
a trained size key), permutation-as-fixed-slice-defence (b3 vs b3′, 8→0), permutation-as-identity-defence
(e: 8/8 trained digest crosses the pinned surface), label-defeat attribution (c vs c2).
**Survived** — name-length/alignment as a fixed-slice enabler (b1/b2/b4 all stay 0/8).
**Inconclusive at the lane instrument** — (a) under the pinned counter: the surface is refused before
scoring, so the claim neither passes nor fails on it; the observation is a coverage gap (F3), not a
refutation.

VERDICT: none of the four assigned fixture weakenings lets a *pinned* shortcut class cross the target
(a → UNEVALUABLE exit 3; b1/b2 → CLEAN exit 0; c → CLEAN exit 0; d1 → CLEAN exit 0, d2 → UNEVALUABLE
exit 3); the weakenings instead expose that equal sizing is asserted by the counter rather than tested,
that name alignment buys nothing, that the permutation's only measured purchase is fixed-slice on
identical bytes (8/8 → 0/8), and that the rename — not the permutation — defeats label memorization;
a probe-only trained digest reader scores 8/8 on the unmodified green surface with the pinned gate
(REPLAY_GATE_REFUSED exit 2) only because the permutation seed is fixed and disclosed, so R34-C2's
green clause is registry-relative and six of its seven registered shortcut witnesses are dead on the
shape-only counter.
