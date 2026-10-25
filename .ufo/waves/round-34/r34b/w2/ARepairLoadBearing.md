# ARepairLoadBearing — mutation probe of the fresh-content repair (R34-C2, wave 2)

Seat: `L1Kaidoku34-2.ARepairLoadBearing` (mutation-tester, leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Probe window: 2026-10-25T07:29:38Z … 2026-10-25T07:36:22Z. Scratch (disposable): `/fast/scratch/hyaku/kaidoku-r34b/w2/ARepairLoadBearing/`.
Nothing was written outside that scratch and this report. The lane repo was read-only; no VCS command was run.
No ELF, fixture or reader was executed as a program: readers ran only as `python3` through a counter
(`subprocess` inside the counters). The R34-C1 production reader and its twelve carriers were not run.
No tool was installed or upgraded.

Assignment executed: mutate the **fresh-content repair** (`mini-counter-fresh.py`, w1
`CtlMultiset-files/`, sha256 `5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c`,
byte-identical to the wave-1 pin) on copies in four ways — (a) one fixed generated content set reused for
all runs, (b) names invariant, (c) payload invariant, (d) per-run regeneration dropped — and measure
whether a **structure-blind** reader regains the counter's target (`matched = 8 / 8`) on each mutant.

**Verdict in one line:** the repair is load-bearing in three separately testable places — content
unpredictability (A: a structure-blind replay regains 8/8), payload unpredictability (C: a string-scan +
constant-payload reader regains 8/8) and content non-publication (D: `nameset` **and** `pathkey` regain
8/8) — while name unpredictability alone is **not** load-bearing (B: structure-blind readers stay 0/8 on
independent runs). One boundary reader that walks the record array by ordinal and never reads `name_off`
meets 8/8 on the pristine repair; it is **not** structure-blind under the stop's own definition and does
not change the four mutant verdicts.

---

## 1. Subject and detector (fixed before any mutation)

The repair's green surface generates eight 512-byte `MREC` fixtures per run from a seed
(`os.urandom(16).hex()` when `--seed` is absent), writes them to opaque `opaque-<sha256[:20]>.data`
paths, runs the reader once per fixture, and compares against records computed from the generation.
Read counters (unchanged wave-1/repair plumbing) are `decode_fixture`/`permute`/`canonical`.

Bounded detector: `tools/sweep.py` runs a counter once per (reader, seed) and records argv, exit,
`matched`, `target`, `met_target`, `finding`, counter sha256 and start UTC.

```
/usr/bin/python3 tools/sweep.py --counter <COUNTER> --root root \
  --reader readers/structural.py --reader readers/nameset.py --reader readers/pathkey.py \
  --reader readers/scan_const_payload.py --reader readers/adaptive_fixed.py \
  --reader readers/name_table_replay.py --reader readers/positional_pairing.py \
  --seed <S1> [--seed <S2> ...] --out receipts/<NAME>.json
```

Per-row argv is reproduced verbatim in each receipt, e.g.
`/usr/bin/python3 -I -B mutants/ma.py --root root --control-reader readers/structural.py --seed a1`.

Reader classes (classification fixed before measurement):

| reader | sha256 | class | reads header | walks records | reads `name_off` |
|---|---|---|---|---|---|
| `structural.py` | `2f399cab…b4b6` | positive control | yes | yes | yes |
| `nameset.py` | `2e8feaea…8b97` | structure-blind (content-multiset replay) | no | no | no |
| `pathkey.py` | `28acfe5a…81a9` | structure-blind (path/digest replay) | no | no | no |
| `scan_const_payload.py` | `eaa6f85c…af9a` | structure-blind (SONAME scan + constant payload) | no | no | no |
| `adaptive_fixed.py` | `f6605d26…542a` | structure-blind (SONAME scan + offline-derived table) | no | no | no |
| `name_table_replay.py` | `6cf5c8e9…e664` | structure-blind (name-set table from one observed run) | no | no | no |
| `positional_pairing.py` | `020f01c6…4ac1` | **boundary** (ordinal pairing, `name_off` decoded but unused) | yes | **yes** | no |

The three carrying tables were derived offline by `tools/derive_tables.py` from the **public mutant
source**, applying the same whole-file `lib…so.N` scan the reader uses (so the key is exact for the
content it was derived from). This models an attacker with the counter source and either a fixed seed
(A) or one observed run's generator (B). No MREC byte is decoded structurally to build a table.

---

## 2. Baseline — pristine repair (unmutated bytes)

`pristine/mini-counter-fresh.py` sha256 `5181330d…ff5c`; receipt `receipts/pristine-sweep.json`
(21 rows, 2026-10-25T07:34:20Z–07:34:23Z).

| reader | seeds k1/k2/k3 | result |
|---|---|---|
| structural (control) | 8/8, 8/8, 8/8 | `records_match`, exit 0 |
| nameset | 0/8 ×3 | `records_mismatch`, exit 1 |
| pathkey | 0/8 ×3 | `records_mismatch`, exit 1 |
| scan_const_payload | 0/8 ×3 | `records_mismatch`, exit 1 |
| adaptive_fixed | 0/8 ×3 | `records_mismatch`, exit 1 |
| name_table_replay | 0/8 ×3 | `records_mismatch`, exit 1 |
| **positional_pairing (boundary)** | **8/8 ×3** | `records_match`, exit 0 |

Baseline is clean for the **structure-blind** set (0/8) with the control at target. The boundary
reader's 8/8 is analysed in §5; it is excluded from every regain verdict below because it already
passes on pristine and therefore cannot discriminate a mutant.

Content-freshness control (`receipts/pristine-inputs-p1.log` vs `…-p2.log`, 8 digests each): seed `p1`
vs `p2` **DIFFER** — the pristine repair really does deliver different bytes on different runs.

---

## 3. Mutants

All mutants are copies of the pristine repair; the pristine file was never edited.
Mutant hashes: A `f10e14f5…49f7`, B `3108cd80…e0ab`, C `6e7046ba…254e`, D `7e284fa5…d846`.

### (a) Reuse one fixed generated content set for all runs — **REGAINED ⇒ LOAD-BEARING**

Mutation point: `main()` seed selection — `seed = args.seed if … else os.urandom(16).hex()` →
`seed = FIXED_SEED` with `FIXED_SEED = "r34-fixed-content-v1"`; `--seed` is ignored. Every counter
invocation therefore generates the same eight fixtures. (Interpretation: identical content *across
counter runs*; reusing one set across the eight reader invocations inside a run is already pristine
behaviour.)

Invariant proof (`receipts/mutant-invariants.txt`): `A content-identical across --seed a1/a2: True`.
Direct byte evidence (`receipts/mA-inputs-a1.log` vs `…-a2.log`, 8 digests each): **IDENTICAL**, and
`a1` differs from pristine `p1`.

Receipt `receipts/mA-sweep.json` (28 rows, 07:34:20Z–07:34:24Z), seeds `a1,a2,a3,r34-fixed-content-v1`:

| reader | result on all four seeds |
|---|---|
| structural | 8/8 `records_match` exit 0 |
| nameset / pathkey / scan_const_payload / name_table_replay | 0/8 `records_mismatch` exit 1 |
| **adaptive_fixed** | **8/8 `records_match` exit 0** |
| positional_pairing (boundary) | 8/8 |

`adaptive_fixed.py` reads no header, no record array and no `name_off`: it scans the pool for SONAME
tokens and replays the table derived from the public source under the module's fixed seed. Because the
content is fixed, every run is the memorisation target. **A structure-blind reader regains the target
when the generated content is reused; the per-run *unpredictability* of the content is load-bearing.**

### (b) Keep names invariant — **NOT REGAINED on independent runs ⇒ NOT LOAD-BEARING ALONE**

Mutation point: `generate()` — the random name-pool loop and `rng.shuffle(names)` replaced by
`names = list(FIXED_NAMES[index])` (`FIXED_NAMES` = the eight committed name lists, fixed order).
Flags/value still drawn from the run seed.

Invariant proof (`receipts/mutant-invariants.txt`): `B names identical across independent seeds: True`;
`B payload identical …: False`; `B content identical …: False`. Recorder digests
(`mB-inputs-b-run.log` vs `mB-inputs-b-run2.log`): **DIFFER**.

Receipt `receipts/mB-sweep.json` (21 rows, 07:34:20Z–07:34:23Z), seeds `b-probe,b-run,b-run2`:

| reader | b-probe | b-run | b-run2 |
|---|---|---|---|
| structural | 8/8 | 8/8 | 8/8 |
| nameset | 0/8 | 0/8 | 0/8 |
| pathkey | 0/8 | 0/8 | 0/8 |
| scan_const_payload | 0/8 | 0/8 | 0/8 |
| adaptive_fixed | 0/8 | 0/8 | 0/8 |
| name_table_replay | **8/8** | 0/8 | 0/8 |
| positional_pairing (boundary) | 8/8 | 8/8 | 8/8 |

`name_table_replay`'s table was derived from the `b-probe` generation; the 8/8 at `b-probe` is that
reader seeing exactly the run it memorised — the mutant-A failure mode leaking into the probe, not
evidence about name invariance. On **independent** seeds (`b-run`, `b-run2`) it is 0/8, and every
other structure-blind reader is 0/8. `nameset` even gets the committed name-set key right and still
scores 0/8 because the payload is fresh. **Knowing the name set without the payload buys no target:
randomising names is not, by itself, the load-bearing part of the repair.**

### (c) Keep payload invariant — **REGAINED ⇒ LOAD-BEARING**

Mutation point: `generate()` — `records = [(name, 0, 2819) for name in names]` (flags/value constant
on every record); names remain run-random.

Invariant proof (`receipts/mutant-invariants.txt`): `C payload all (0,2819): True`;
`C names identical across independent seeds: False`.

Receipt `receipts/mC-sweep.json` (21 rows, 07:34:20Z–07:34:23Z), seeds `c1,c2,c3`:

| reader | result ×3 |
|---|---|
| structural | 8/8 `records_match` |
| **scan_const_payload** | **8/8 `records_match` exit 0** |
| nameset / pathkey / adaptive_fixed / name_table_replay | 0/8 |
| positional_pairing (boundary) | 8/8 |

`scan_const_payload.py` scans the pool for SONAME tokens and emits `flags=0, value=2819` for every name:
it reads no header, no record array, no `name_off`, yet meets the target on all three seeds.
**Payload unpredictability is load-bearing.** (Generalisation: any payload that is a public function of
the name — constant, name-derived hash, per-name table — is equally recoverable by a string scan.)

### (d) Drop the per-run regeneration — **REGAINED ⇒ LOAD-BEARING**

Mutation point: `score(reader, seed, root)` no longer calls `generate`; it reads the committed
`root/tools/round-34/mini-fix/fixtures/*.mrec` and `expected.json` and writes those bytes to the same
opaque paths. (`--root` is now load-bearing; `main` passes it through.) This is the pre-repair
committed-fixture surface, kept at the repair's opaque-path/reader shape.

Invariant proof: the eight inputs delivered by mutant D
(`receipts/mD-inputs-d1.log`) are byte-identical to the committed fixtures
(`alpha d1de0e6f…`, `beta a8547fcf…`, `delta 79ff7036…`, `epsilon 82f03f99…`, `eta 5bcabeb2…`,
`gamma ffb57ecd…`, `theta b1f87d7c…`, `zeta 19ff4074…`).

Receipt `receipts/mD-sweep.json` (14 rows, 07:34:20Z–07:34:22Z), seeds `d1,d2`:

| reader | result ×2 |
|---|---|
| structural | 8/8 |
| **nameset** | **8/8 `records_match` exit 0** |
| **pathkey** | **8/8 `records_match` exit 0** |
| scan_const_payload / adaptive_fixed / name_table_replay | 0/8 |
| positional_pairing (boundary) | 8/8 |

Two registered, structure-blind classes — the wave-1 content-multiset replay *and* the path/digest
replay (whose digest fallback still recognises the committed bytes at opaque paths) — regain the
target as soon as the content is the published set. **Non-publication of the per-run content is
load-bearing**; this is the direct mutation of the repair's central change.

---

## 4. Decomposition: which properties the repair actually rests on

| mutated property | structure-blind regain | verdict |
|---|---|---|
| (a) content reused across runs (fixed seed) | `adaptive_fixed` 8/8 | **load-bearing (unpredictability)** |
| (b) names invariant, payload fresh | 0/8 on independent seeds | **not load-bearing alone** |
| (c) payload invariant, names fresh | `scan_const_payload` 8/8 | **load-bearing (payload unpredictability)** |
| (d) committed content, no generation | `nameset` 8/8, `pathkey` 8/8 | **load-bearing (non-publication)** |

Freshness is not one property. The repair closes the wave-1 counterexample because the *content* is
unpublished (D) **and** unpredictable (A) **and** its *payload* is fresh (C). Randomising the names
alone (B) does not close it — a name-set key is obtainable by string scan, but without a fresh payload
it cannot produce the records. This also explains why the repairability argument must not be stated as
"fresh names": the load-bearing ingredient in the name dimension is the *payload*, which (c) isolates.

---

## 5. Boundary finding on the pristine repair: ordinal pairing meets the target

`positional_pairing.py` scored **8/8 on the unmutated repair on all three seeds** (§2), and on every
mutant. It reads the header (`count`, `records_off`, `names_off`), reads each record's flags/value by
ordinal, scans the pool in order, and pairs the *i*-th pool string with the *i*-th record. It decodes
`name_off` but never uses it.

Classification: **not structure-blind** under the stop's own definition ("never reads the header, never
walks the record array, and never reads a `name_off` field") — it does read the header and does walk
the record array. It therefore does **not** falsify the stop's structure-blind counterexample and does
not change any of the four mutant verdicts (it passes on pristine, so it cannot discriminate them).

What it does show, as a coverage observation only: the repair generates the pool in record order and
applies **no permutation**, so the association it forces is *ordinal record traversal*, not
`name_off` dereference — unlike the committed `mini-counter.py`, whose name-pool permutation forces
`name_off`. The repair's `PREDICATE` ("only record-array traversal recovers it") is still literally
satisfied by this reader, so this is not a predicate falsification; it is a narrowing of the
discriminator relative to the pre-repair counter, and an unregistered reader class that meets the green
target on the proposed repair. Reported for the L1; not scored, not integrated.

---

## 6. What this probe says about the stop (and what it does not)

- The stop's decisive counterexample is a **published-content** replay: it keys on the committed
  fixture name sets, which are public in `expected.json`. Mutant (d) reproduces exactly that failure,
  and the pristine repair defeats it (nameset 0/8). The repair is therefore load-bearing against the
  class the stop named.
- The repair's guarantee is nevertheless **conditional on per-run generation and per-run payload
  randomness**; mutating either restores a structure-blind class at target (A, C), and mutating both
  the content source and publication restores two registered classes (D).
- These are mutation/coverage findings about the repair. They are not a re-opening of R34-C2, not a
  judgement of the stop, and carry no score. Per the assignment, a surviving mutant is a coverage
  finding, not permission to change the contract.

---

## 7. Limits of this probe

- **Table model.** The A and B tables were derived offline from the public mutant source, not learned
  inside a run. That is the correct threat model for a fixed seed (A) but it is an *adaptive* attacker:
  an attacker who never sees the source and cannot guess the seed gets nothing. No cross-run online
  learning attack was attempted (a reader has no ground truth, so it cannot learn payloads).
- **B is a negative.** `name_table_replay` 8/8 at `b-probe` is the memorised run, not an independent
  regain; on `b-run`/`b-run2` it is 0/8. No other structure-blind reader exceeds 0/8 on B.
- **Seed count.** 2–4 seeds per counter (A: 4 invocations of one fixed set; B/C: 3; D: 2; pristine:
  3). No 100-seed sweep; guessing attacks (flags 0–3, values random) are not measured. `target=8`
  makes an all-eight guess vanishingly unlikely but unquantified here.
- **Scan-key artifact.** A naive whole-file SONAME scan picks an alphanumeric byte that precedes the
  first pool name (the last record byte at `names_off-1`) into that name. The probes anchor the scan on
  the public `lib…so.N` naming scheme, which recovers the true names; this is a key-construction detail,
  not a defence of the repair. First versions using the unanchored scan measured 6/8 for exactly this
  reason and were discarded (not reported as results).
- **Boundary reader.** §5 is outside the assigned four mutations and outside the structure-blind class;
  it is not evidence for or against the repair's structure-blind guarantee.
- **Durability of the subject.** The repair exists in the lane only as the w1 copy
  `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py` (sha256 `5181330d…`);
  `tools/round-34/mini-fix/mini-counter-fresh.py` does not exist. The pristine bytes probed here are
  that w1 file. Any landing into the instrument tree remains the L1's action; this probe wrote none.

---

## 8. Restoration evidence (scratch disposable; bytes restored/identical)

- Pristine repair sha256 **before** the probe (`07:29:38Z`) and **after** all mutants/runs
  (`07:36:22Z`): `5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c` — unchanged.
- `restored/mini-counter-fresh.py` re-copied from the lane source
  (`.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py`):
  `cmp … exit=0` (identical), sha256 `5181330d…ff5c`.
- Detector re-run on restored bytes (`receipts/restored-sweep.json`, seed `k3`, 07:36:11Z–07:36:12Z):
  structural 8/8, nameset/pathkey/scan_const/adaptive_fixed/name_table 0/8, positional 8/8 — identical
  to the pristine baseline.
- Restored counter sha in the restored receipt rows: `5181330d07ca…` (same as pristine; contrast
  mutant counter shas `f10e14f5…`, `3108cd80…`, `6e7046ba…`, `7e284fa5…`).

---

## 9. Receipts index (absolute paths, all under scratch)

| file | content |
|---|---|
| `receipts/pristine-sweep.json` | baseline, 21 rows, counter `5181330d…` |
| `receipts/mA-sweep.json` | mutant A, 28 rows, counter `f10e14f5…` |
| `receipts/mB-sweep.json` | mutant B, 21 rows, counter `3108cd80…` |
| `receipts/mC-sweep.json` | mutant C, 21 rows, counter `6e7046ba…` |
| `receipts/mD-sweep.json` | mutant D, 14 rows, counter `7e284fa5…` |
| `receipts/restored-sweep.json` | restored bytes, 7 rows, counter `5181330d…` |
| `receipts/derived-tables.json` | A/B tables derived offline (8 keys each) |
| `receipts/mutant-invariants.txt` | per-mutant invariant assertions |
| `receipts/{pristine,mA,mB,mD}-inputs-*.log` | per-input sha256 delivered by each counter |
| `mutants/{ma,mb,mc,md}.py` | mutated counters |
| `readers/*.py` | detector readers (hashes in §1) |
| `tools/{derive_tables,make_readers,sweep}.py` | probe tooling |

Scratch root: `/fast/scratch/hyaku/kaidoku-r34b/w2/ARepairLoadBearing/`.

## VERDICT

`REPAIR_LOAD_BEARING: A(fixed content)=YES — adaptive_fixed 8/8 on 4/4 seeds; B(names invariant)=NO —
structure-blind 0/8 on independent seeds (name_table only 8/8 on the memorised seed); C(payload
invariant)=YES — scan_const_payload 8/8 on 3/3 seeds; D(no regeneration)=YES — nameset 8/8 and pathkey
8/8 on 2/2 seeds. Pristine structure-blind 0/8 (3 seeds); structural control 8/8 throughout; restored
bytes identical (5181330d…, cmp exit 0) and reproduce the pristine result. Boundary: ordinal-pairing
reader 8/8 on pristine but it reads the header and walks the record array, so it is not structure-blind
and does not change the four verdicts.`
