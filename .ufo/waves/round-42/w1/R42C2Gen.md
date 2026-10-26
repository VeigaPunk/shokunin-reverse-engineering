# R42C2Gen — `heldout-gen-v4.py` (table v4, amendment A1), dev arm end to end

**Verdict: DONE** — the v4 held-out generator is built, self-tested, and run end to end on the dev arm
(seed `sha256('dev42')[:40]` = `e48947bb2a1542206bc6a324257b3500231946e3`): **78/78 carriers reach their
declared tuple**, `combo_unseen_majority` = **22/24** combos observed outside the named declared-tuple union,
and the set **regenerates byte-identically** (manifest, 78 carriers, 78 `tree.json`). R41-CL1 is fixed (one
key, `declared_features`). Two defect findings that changed the generator mid-wave are in §6: the round-41
partial-damage recipe lands `clean` on some seeds, and A1's "two decision factors" must count only
*observable* factors.

Seat `R42C2Gen`, lane `kaidoku-shokunin`, base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`, wave 1 (pre-freeze).
Report: `.ufo/waves/round-42/w1/R42C2Gen.md`; artifacts:
`.ufo/waves/round-42/w1/artifacts/R42C2Gen/` (`heldout-gen-v4.py`, `fixtures.json`, `fixtures/`, `REBUILD.md`,
`wave1-measurements.tsv`, `dev42-manifest.json`, `dev42-runs/`, `dev42-combos.tsv`,
`dev42-label-preview.tsv`, `dev42-verify.log`). Nothing outside that directory and the report was written;
scratch was removed; no tool was installed or upgraded.

## 1. What the generator is

`heldout-gen-v4.py` is `git show c4a38ea:tools/round-41/heldout-gen-v3.py` with the v4 body kept verbatim
(image writer adapter, stdlib SquashFS 4.0 reader, damage recipes, tree material, REA runner, envelope parser)
and these changes:

| area | v3 (round 41) | v4 (this wave) |
| --- | --- | --- |
| declared tuple | `carriers[].declared` + a second copy under `class_expected.features` | **one key** `carriers[].declared_features`; `declared_extras` for `extraction_failed`/`max_depth`; `class_expected` keeps only `{label, action, reported_only}` |
| classes | 20 named + `combo`(12) | 27 named + `combo`(24): + `legacy-clean`, `legacy-dep-missing-be`, `legacy-dep-missing-le`, `legacy-body-failure`, `legacy-partial`, `container-depth-limited`, `unknown-residue` |
| legacy carriers | — | pinned unblob 26.6.4 fixtures (`fixtures.json`, 14 distinct images, MIT), seeded choice, pinned 4-byte damage window |
| combo factors | endian, in-tree, escaping, partial, comp, max_depth | family decisions over `legacy chunk / second v4 chunk / links / residue / container wrap / damage / dependency / max_depth 1`, **≥2 observable decisions per carrier** |
| actions | `interp` vocabulary | `draft42` = the A1 precedence text's own (label, action) pairs, rule 1–15, incl. `legacy-body-failure → cross-read-legacy`, `container-depth-limited → raise-depth`, `unknown-residue → isolate-residue` |
| `--verify` | envelope vs class expectation | + `combo_unseen_majority` scoring + **byte-identical regeneration** of manifest/carriers/tree.json |
| build-time gate | — | `build_set` refuses a set whose declared combos miss the unseen majority (critic P8) |

Seed semantics are unchanged: named carriers use `random.Random(int(seed[:16],16) ^ (class_index*1000 + k))`
with `class_index = list(RECIPES).index(name)` (the 20 round-41 classes keep their indices, so their trees are
the same for the same seed); file contents are a SHA-256 counter stream; the combo factor vector is
`Random(sha256('<seed>:combo:<k>')[:16])`; the legacy fixture choice is `Random(sha256('<seed>:fixture:<name>:<k>')[:16])`.
No clock, no `os.urandom`, no directory order, no measurement at generation time.

### 1.1 Legacy carriers are pinned third-party bytes, not generated images

No writer in the lane emits v1–v3 (`tools/round-39/gen-squashfs.py` writes 4.0 only), so the five legacy
classes are built from the unblob 26.6.4 integration fixtures (MIT, commit
`1fcc7a0a584a70a96c31f5a276c20944d199a089`), pinned by URL + sha256 + size in `fixtures.json`:

| id | runtime handler (measured in a dev envelope) | endian | size | pinned damage window |
| --- | --- | --- | --- | --- |
| `v1-be` / `v1-le` | `squashfs_v1` | be / le | 4096 | `0x48` / `0x44` |
| `v2-be` / `v2-le` | `squashfs_v2` | be / le | 4096 | `0x58` / `0x58` |
| `v2ns-be` / `v2ns-le` | `squashfs_v2_nonstandard` | be / le | 4096 | `0x58` / `0x58` |
| `v3-be` / `v3-le` | `squashfs_v3` | be / le | 4096 | `0x84` / `0x84` |
| `v3adapt-be` / `v3adapt-le` | `squashfs_v3` (not `squashfs_v3_adaptive`) | be / le | 4096 | `0x84` / `0x84` |
| `v3ns-be` / `v3ns-le` | `squashfs_v3_nonstandard` | be / le | 4096 | `0x84` / `0x84` |
| `v3bc-le` | `squashfs_v3_broadcom` | le | 4096 | `0x84` |
| `v3ddwrt-be` | `squashfs_v3_ddwrt` | be | 320 | `0x90` |

Two further fixture paths are byte-identical to a pinned image and are recorded under
`fixtures.json:duplicate_bytes` rather than pinned twice (`squashfs_v3_broadcom/big_endian/…/squashfs_v3_be.bin`
= `v3-be`; `squashfs_v3_ddwrt/little_endian/…/squashfs_v3_le.bin` = `v3-le`). All **7 reachable** v1–v3
runtime handler names are covered (`squashfs_v1`, `_v2`, `_v2_nonstandard`, `_v3`, `_v3_broadcom`, `_v3_ddwrt`,
`_v3_nonstandard`), matching R42C2ReconLegacy D7 ("per handler" = the runtime name, not the directory).
Copies of the 14 pinned files are in `artifacts/R42C2Gen/fixtures/` as `<id>--<file>`; the L1 can commit them
to `corpus/evidence/round-42/c2/fixtures/` (command in `REBUILD.md` §1). The `<id>--` prefix is required on
disk: `v2-be` and `v2ns-be` share the basename `squashfs_v2.0_be.bin` with **different** bytes.

Damage is not probed at run time: each pin carries a pre-verified 4-byte zero window, so a legacy carrier is a
pure function of (pin, seed). `legacy-partial` is the one two-fixture layout: the clean fixture at 0, the
damaged one at 4096, so the damaged chunk is a **non-root** chunk and is carved and published — a failing
*root* chunk publishes nothing (§4.4).

## 2. What was run (exact commands, exit codes)

```sh
S=/fast/scratch/hyaku/kaidoku-r42/R42C2Gen; cd "$S"; export TMPDIR="$S"
SEED=$(printf dev42 | sha256sum | cut -c1-40)   # e48947bb2a1542206bc6a324257b3500231946e3
```

1. **Selftest** (no REA): `python3 -I -B heldout-gen-v4.py --seed $SEED --selftest --gen
   tools/round-39/gen-squashfs.py --scratch $S/st --fixtures-dir …/fixtures --fixture-pins …/fixtures.json`
   → **exit 0, 17/17 checks pass** (same-seed byte identity; every seed-dependent carrier differs across a
   different seed, 65/65; per-class replicate distinctness; R40-CL4 pin; depth classes; combined traps; one
   declared key; no second spelling; ≥2 decisions; legacy pins; 4096 offsets).
2. **Dev arm end to end**: `python3 -I -B heldout-gen-v4.py --seed $SEED --out $S/dev42 --run --verify
   --gzip --gen tools/round-39/gen-squashfs.py --scratch $S --fixtures-dir …/fixtures --fixture-pins
   …/fixtures.json` → **exit 0**, 78 REA runs, every envelope `ok:true`, every `run.json` `digest_matches_carrier`
   (78/78), then:
   * `78/78 carriers reached their declared tuple`
   * `combo_unseen_majority: observed 22/24 combos outside the named declared-tuple union (declared prediction 22/24) PASS`
   * `regen: manifest bytes identical ba3d73876cbe9536 vs ba3d73876cbe9536` / `78/78` carriers / `78/78` tree.json
3. **60 ad-hoc REA probes** behind the declared rules (`wave1-measurements.tsv`), and ~45 direct
   `sasquatch` / `sasquatch-v4be` invocations to separate "the extractor failed" from "the extractor exited 0"
   (§6.1). Every REA run: `cd "$S"`, `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
   extract-firmware --format json --full-output --max-depth {1,3} <input> <fresh outdir>`, exit 0; the
   dependency arm strips `$HOME/.local/bin` from the child PATH with `REA_UNBLOB_COMMAND` absolute.

Runs were on development inputs only: unblob 26.6.4 test fixtures (MIT) and trees generated by the lane
writer. **No published image and no C1 carrier candidate was read, carved or extracted** by this seat.

## 3. R41-CL1 (the declared-tuple key) — fixed and proven

`manifest.json` now carries **exactly one** tuple key per carrier, for every class including combos:

```
carriers[].declared_features   {handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published}
carriers[].declared_extras     {extraction_failed, max_depth}     # not part of the binding
carriers[].class_expected      {label, action, reported_only}      # no `features` key
```

Checks that make the fix auditable rather than asserted:

* selftest check *"every carrier declares the six binding fields under ONE key"* — 78 carriers, key
  `'declared_features'`;
* selftest check *"R41-CL1: no second spelling of the tuple"* — asserts no `declared` key exists and no
  `class_expected.features` exists on any carrier;
* `--verify` reads the tuple through `entry[DECLARED_KEY]` only, so a second spelling cannot be scored by
  accident;
* `manifest.declared_schema` records `key: "declared_features"`, the six field names, their types and
  `location: carriers[].declared_features -- ONE key for every class, combos included`.

## 4. Measurements that fix the declared tuples

60 probe envelopes are in `wave1-measurements.tsv` (columns `input, depth, H, G, D, BE, SR, P`). The rows that
decide a rule, with the rule they changed:

### 4.1 Legacy family

| probe | H | G | D | BE | P | consequence |
| --- | --- | --- | --- | --- | --- | --- |
| all 14 pinned fixtures, depth 3 | the fixture's handler | ∅ | ∅ | n/a | 2–4 | `legacy-clean` = `clean` (rule 14) |
| all 14 pinned fixtures, depth 1 | same | `depth-limited` | ∅ | n/a | 2–4 | a depth-1 "clean" legacy class is impossible (matches R42C2ReconLegacy) |
| v3 BE with sasquatch unreachable | `squashfs_v3` | `missing-extractor-dependency` | `sasquatch` | n/a | 0 | **rule 4 turns a BE legacy chunk into `dep-missing-le`** (confirmed independently by R42C2ReconCombo CB4 and R42C2ReconLegacy D2) |
| all 14 damaged with the pinned window | the fixture's handler | `extractor-failure` | ∅ | `yes` on BE / `no` on LE | 0 | `legacy-body-failure` (rule 7) is reachable on all 7 handler names, both endiannesses |
| clean fixture + damaged fixture @4096 | both handlers | `extractor-failure` | ∅ | the damaged chunk's | 3+ | `legacy-partial` = `partial-body-failure` (rule 5); a root-only failure would be P=0, so the class is a two-fixture layout |

No pinned fixture holds a symlink or a device (`unpublished_entries` empty everywhere, matching recon), so the
symlink rows are unreachable on a pure legacy chunk — stated as a limit, never implied away.

### 4.2 Container (A1 step 2)

| input | depth | H | G | F | consequence |
| --- | --- | --- | --- | --- | --- |
| `tar(squashfs_v4_le)` | 1 | `tar` | `depth-limited` | ∅ | **step 2 `container-depth-limited`**, P=1 (the member) |
| `tar(squashfs_v3_le)` | 1 | `tar` | `depth-limited` | ∅ | same |
| both | 3 | `tar` + the squashfs handler | ∅ | the handler | `clean` — hence `max_depth` is pinned to 1 for the class |
| `tar(damaged v4)` | 1 | `tar` | `depth-limited` | ∅ | damage is invisible under the cap (P=1) |
| `tar(v4)` + 64 B tail | 1 | `tar` | `depth-limited`, `unknown-chunk-handler` | ∅ | still step 2 — the residue does not pre-empt rule 2 (this is R42C2ReconLegacy D5's real TRX shape) |

### 4.3 Residue (A1 step 9)

| input | depth | H | G | P | consequence |
| --- | --- | --- | --- | --- | --- |
| v4 image + 64 B seeded tail | 3 | `squashfs_v4_le` | `unknown-chunk-handler` | files + the `.unknown` carve | `unknown-residue` (rule 9) |
| same | 1 | `squashfs_v4_le` | `unknown-chunk-handler`, `depth-limited` | idem | rule 9 precedes rule 10 ✓ |
| legacy fixture + tail | 3 | the fixture's handler | `unknown-chunk-handler` | 4–5 | same, on the legacy family |
| damaged image + tail | 3 | `squashfs_v4_le` | `extractor-failure`, `unknown-chunk-handler` | 2 | rule 5 owns it: **the tail's carve makes P>0** |
| unreachable extractor + tail | 3 | the handler | `missing-extractor-dependency`, `unknown-chunk-handler` | 2 | rule 4 precedes 9 ✓ |

The tail must be non-uniform (R42C2ReconLegacy D6: a uniform fill is claimed by unblob's `padding` handler and
the run lands `clean`). This generator's tail is 64 B drawn from an 8-byte alphabet, seeded — non-uniform, and
still a pure function of the seed.

### 4.4 The depth-limited clause (refined)

`depth-limited` is minted only when an extraction actually reached the ceiling:

| carrier | depth | G | measured |
| --- | --- | --- | --- |
| clean single chunk | 1 | `depth-limited` | yes |
| failing single ROOT chunk (damage) | 1 | `extractor-failure` only | **no depth gap** |
| failing single ROOT chunk (dependency) | 1 | `missing-extractor-dependency` only | **no depth gap** |
| damaged root chunk **with a residue** | 1 | `extractor-failure`, `unknown-chunk-handler`, `depth-limited` | yes (the carve reaches the ceiling) |
| clean chunk + damaged chunk @4096 | 1 | `extractor-failure`, `depth-limited` | yes (the sibling extracts) |
| both chunks fail on dependency | 1 | `missing-extractor-dependency` only | **no depth gap** (nothing was written) |
| container wrap | 1 | `depth-limited` | yes (the tar itself) |

This is band 3 of `precedence_observations` in the manifest: A1's step 10 wording ("depth-limited ∈ G") is
correct as a predicate, but a *generator* that declares `depth-limited` whenever `max_depth == 1` is wrong.

## 5. Dev-arm results

### 5.1 Tuples

78/78 carriers match `declared_features` + `declared_extras` (the full table is in `dev42-verify.log`). Named
classes reach 39 distinct tuples; the label spread the generator expects (`class_expected`, a cross-check, never
the scored label) is: clean 6, clean-empty 2, escaping-symlink-removed 2, in-tree-symlink-metadata 2,
mixed-symlinks 2, dep-missing-be 2, dep-missing-le 6, avm-marker-be-dropped 2, body-extractor-failure 4,
partial-body-failure 10, depth-limited 6, legacy-body-failure 2, container-depth-limited 2, unknown-residue 2,
no-squashfs-chunk 2, unclassified 2 — all 16 A1 labels, all 14 action tokens.

An independent preview of A1 over the declared tuples (`dev42-label-preview.tsv`, written from the precedence
text only, `[INFERENCE]` with respect to the frozen evaluator) agrees with the generator's `class_expected` on
**54/54** named carriers. It also gives the L1 the control ceilings:

* **CTL-C2-7** (exact named-tuple lookup, no fallback): at most **2/24** combos carry a named-class tuple
  (C11 = legacy chunk + dependency + depth 1 → the `dep-missing-le` tuple; C24 = container wrap + depth 1 →
  the `container-depth-limited` tuple), so 8.3 % < 50 %.
* **CTL-C2-7b** (lookup + the majority fallback label `partial-body-failure`): **10/24** = 41.7 % < 50 %.
  Reported, not bound, per A1.

Both numbers are counted on *declared* tuples, which §5.1 shows equal the observed ones on all 78 carriers.

### 5.2 Combos: ≥ 2 observable decisions, 22/24 unseen

`dev42-combos.tsv` lists all 24 (id, decisions, layout, H, G, D, BE, SR, P, depth, inside/outside the named
union). Distribution of decision counts: 5 combos with 2, 5 with 3, 10 with 4, 4 with 5. Every decision kind is
drawn at least twice: container wrap, residue, damage, dependency, legacy chunk, second v4 chunk, links,
max_depth 1. Layouts: 10 single-image, 10 single-fixture, 5 legacy+v4(±residue), 9 wrapped, 10 with a residue.

The two combos *inside* the named union are honest and worth keeping: they are exactly the cases where the drawn
decisions collapse onto a tuple a named class also produces. That is why the binding is "at least half", not
"all", and why the generator refuses to build a set below half (§7 P8 gate).

## 6. Defects found (and what the generator does about them)

### 6.1 The round-41 partial-damage recipe can land `clean` — real generator defect, fixed

Round 41's `corruption_partial` zeroed the **last compressed block of the last-extracted file**. On this dev
seed, carrier H30 (big-endian, xz) wrote a corrupt copy, printed `writer: failed to read/uncompress file`, and
exited **0**, so the envelope carried no `extractor-failure` at all and `partial-mixed` declared
`extractor-failure` while the run said `clean` (first dev arm: `66/78`). Direct probing with the exact binary
unblob picks (`sasquatch-v4be -be`) on that carrier showed the exit code depends on **where** the failure lands,
not on the block size:

| damage target on the H30 tree | rc | files written |
| --- | --- | --- |
| file#0 (first) block#1/#2/#3 | 0 | 3 |
| file#1 block#1 (mid-file) | **1** | 5 |
| file#1 block#2 (last block of the second-to-last file) | 0 | 4 |

The recipe is now **multi-block**: every compressed, non-sparse block at or below the 136 B pin of every file
**except the first** is zeroed. The first file is never touched, so P > 0 by construction; at least one
mid-file failure is guaranteed, so the extractor exits nonzero. Verified on all six partial carriers of the dev
seed (`rc=1`, P = 2..8) and end to end (78/78). The per-block ceiling stays at the R40-CL4 pin
(`MAX_DAMAGED_BLOCK = 136`, lowered from 512 because a 140 B zeroed block was absorbed on this seed; blocks
above it are skipped, not claimed).

### 6.2 A1's "two decision factors" must mean two *observable* factors — fixed

R42C2ReconLegacy D8: a container wrap at `--max-depth 1` means the inner image is never carved, so a dependency
or damage factor drawn with it leaves no trace. Counting those as decisions would let a carrier claim two
factors and expose one — precisely the hole `combo_unseen_majority` exists to close. `combo_decisions` now counts
only observable factors (the wrap and the depth cut are themselves observable, so a capped draw still reaches
the minimum). Confirmed by the dev arm: a capped draw's `extraction_failed` is `False` even when the factor
vector says `damage`/`dep` (earlier dev arms C08/C22 mis-declared it).

### 6.3 A dependency failure suppresses the symlink rows — fixed

A dependency failure means the extractor never ran, so no symlink is inspected: SR stays `no` and no
`unpublished-entry` gap exists. Three dev-arm combos (C10, C12, C20) mis-declared `unpublished-entry`/SR=yes
before the fix. `links_active` now requires `not dep_effective`.

### 6.4 The dependency set of a two-chunk carrier is a union — fixed

`dep-missing-be` is about **membership**, not about which chunk failed: a legacy chunk contributes `sasquatch`
and a v4 BE chunk contributes `sasquatch-v4be`, so a legacy + v4 BE carrier reads `D = {sasquatch,
sasquatch-v4be}` and rule 4's first branch answers `dep-missing-be` (dev arm C04/C16; independently measured by
R42C2ReconCombo CB5). The generator now unions the per-chunk dependencies.

### 6.5 Published-file accounting per damage kind — fixed

`published` is not a function of "damaged" alone:

| damage kind | P | why |
| --- | --- | --- |
| v4 `partial` (late blocks) | **> 0** | earlier files are already on disk when the block fails |
| v4 `zero-id-table` | 0 | sasquatch reads the id table before writing |
| pinned legacy window (root chunk) | 0 | the failure is in the metadata, before any file |
| dependency failure, single root chunk | 0 | the extractor never ran, nothing to carve |
| any failure on a NON-root chunk (residue present / two-chunk / wrapped tar member) | **> 0** | the chunk or the member is carved/published |

### 6.6 Not a defect, but a wording risk for the freeze

Rule 4's action token `install-extractor-le` is what a **big-endian v1–v3** chunk gets (its only dependency is
plain `sasquatch`). The label is right and the measurement is now three-way confirmed, but the token name reads
as endianness-specific. Recorded as `precedence_observations[0]` in the manifest; renaming or scoping the token
is an L1 decision, and it changes no carrier byte (rebind with `--actions-set`).

## 7. Limits and risks

* **Pinned bytes do not follow the seed.** 13 of 78 carriers (the legacy classes and `container-depth-limited`
  k=2) are pinned third-party images and are *identical* across seeds; the cross-seed determinism check is
  therefore stated per carrier (`seed_dependent`) instead of globally. Replicate distinctness is checked per
  class/family, and a per-manifest `used` set stops two legacy carriers from being built from the same fixture
  in the same damage state.
* **A1 rows unreachable on legacy chunks.** No pinned v1–v3 fixture holds a symlink or device, so rows 11–13
  cannot appear on a pure legacy carrier; the legacy classes do not pretend otherwise. Symlink factors enter only
  through the generated v4 chunk.
* **`HF` is not a declared field.** The declared tuple carries `handler_set`, not the per-gap handler set, so
  step 7's `HF ∩ L` is only testable where a single chunk fails on extraction — true for every carrier built
  here, and the evaluator sees the real per-gap handlers. The extra fields in `declared_features` deliberately
  did **not** grow: the six-field binding is what the round-42 counter reads.
* **[INFERENCE]** The unseen-majority and lookup-ceiling numbers in §5.1 hold for the dev seed; a different
  freeze seed redraws factors and could land below half. That is why the gate is at build time (P8): the freeze
  either gets a compliant set or fails loudly.
* **Residue tail safety.** The tail is 64 B drawn from an 8-byte alphabet chosen to match no handler; a
  different handler being added upstream could claim it. `--verify` would catch it as a tuple mismatch, and the
  tail is one constant in the source.
* **The dev arm is not the freeze arm.** This report proves the generator, its declarations, the unseen
  majority and byte identity on `sha256('dev42')`. The freeze re-runs it on the freeze commit hash; nothing here
  is a claim about the held-out set.

## 8. Files (all under `artifacts/R42C2Gen/`)

| file | sha256 / size |
| --- | --- |
| `heldout-gen-v4.py` | `a054e5cdbf32b54e9ec19711230c67b17f404d5fe79c8a1aa8c579aa32bec051` (= `dev42-manifest.json:generator.sha256`) |
| `fixtures.json` | `9f957663c1f21940ec17e32f98485425145b6c4e7eb265a7b12327b629c3da9b` (= `dev42-manifest.json:generator.fixtures.pins_sha256`) |
| `fixtures/` | 14 files, `<id>--<file>`, 56 KB, MIT |
| `dev42-manifest.json` | the dev-arm manifest (165 KB) |
| `dev42-runs/<id>/{envelope.json.gz,run.json}` | 78 carriers; carriers themselves are regenerable (`REBUILD.md` §3) |
| `dev42-combos.tsv`, `dev42-label-preview.tsv`, `dev42-verify.log` | calibration tables + the full verify log |
| `wave1-measurements.tsv` | 60 probe envelopes' feature tuples |
| `REBUILD.md` | exact commands, PATH arms, fixture resolution order |

Tool ledger: **nothing installed, upgraded, moved or removed.** Existing tools used as found (rea-agents 6.5.0
via `npx -y`, unblob 26.6.4, sasquatch 4.5.1, python3). Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2Gen`
removed after the evidence was copied out.

## 9. A1 delta (what the 2026-10-26 ~22:20Z amendment changed here)

The amendment reached this seat before the generator was written, so v4 is A1-native rather than patched onto
the 15-step draft. Against the ticket as first issued, A1 changed exactly this:

| A1 change | what this seat did |
| --- | --- |
| 15-step precedence, new step 2 (`F=∅` + `depth-limited` → `container-depth-limited`) | new named class `container-depth-limited`: k=1 a generated v4 image inside a USTAR tar, k=2 a pinned legacy fixture inside one, both `--max-depth 1` (measured H=`tar`, F=∅, G={depth-limited}, P=1). The class does **not** carry a residue, so its declared gap set is `{depth-limited}`; the real-world TRX shape (G also carries `unknown-chunk-handler`, recon D5) is covered by the combos that draw `wrap + residue` at depth 1 (dev arm C08/C14/C22) |
| new step 9 (`unknown-chunk-handler` → `unknown-residue`, before the depth row) | new named class `unknown-residue`: k=1 image + 64 B seeded non-uniform tail, k=2 legacy fixture + tail, both at depth 3 (measured H keeps the squashfs handler, G={unknown-chunk-handler}, P includes the `.unknown` carve) |
| step 4 "by membership" | the declared dependency set of a two-chunk carrier is a **union** (`sasquatch` from the legacy chunk, `sasquatch-v4be` from a v4 BE chunk), so rule 4's first branch owns mixed BE carriers (§6.4) |
| step 7 keyed on `HF ∩ L` | legacy carriers carry `handler_set` only; on every carrier built here exactly one chunk fails on extraction, so `HF = F` and the declared tuple determines the step-7 answer. Stated as a limit in §7 |
| combos: **≥2 decision factors**, family factor `legacy chunk / second v4 chunk / links / residue / container wrap / damage / dependency / max_depth` | `combo` is 24 carriers over those eight decisions, ≥2 *observable* decisions each (counts 2..5; every kind drawn ≥2×). The word "observable" is the A1-relevant correction: a wrap at depth 1 swallows a damage or dependency factor (§6.2) |
| bindings `combo_unseen_majority` + `lookup_combo_below_half` | each combo carries `outside_named_union_declared`; the manifest's `combo_unseen` block records the union size (39), its sha256, the per-combo decision counts and the declared count; `--verify` recomputes the count from the **observed** tuples and prints both; `build_set` refuses a set below half (P8). **Dev arm: observed 22/24 = 91.7 % unseen** (declared prediction identical), and the two seen combos (C11, C24) are honestly reported |
| controls `CTL-C2-7b`, `CTL-C2-10` | nothing to build here (controls are another seat's files), but the set's ceilings are measured for them: CTL-C2-7 ≤ 2/24, CTL-C2-7b (majority fallback `partial-body-failure`) = 10/24 — both < 50 % (§5.1) |
| one key `declared_features` (R41-CL1) | unchanged by A1 and fixed as first specified (§3) |
| legacy classes, pinned fixtures, "per runtime handler name" | unchanged by A1; 14 distinct pinned images covering all 7 reachable v1–v3 runtime handler names (§1.1) |

Two A1 consequences worth the L1's attention before the freeze:

1. **`container-depth-limited` and `unknown-residue` are reachable only with a container/tail that some other
   tooling might trim.** Both classes are built from generated containers (tar) and seeded tails, so they are
   reproducible and shippable, but a real-world image that is "just a squashfs" cannot exercise them — they exist
   because REA sees the container, not because a vendor ships one.
2. **The seen fraction is seed-dependent.** The dev seed lands 22/24; a freeze seed that draws mostly
   `container wrap + max_depth 1` combos would land lower. The build-time gate is the answer: the freeze either
   gets a compliant set or fails loudly with the count in the message.
