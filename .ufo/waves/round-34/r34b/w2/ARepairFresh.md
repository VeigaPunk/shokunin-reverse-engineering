# ARepairFresh — attack on the proposed repair `mini-counter-fresh.py` (R34-C2 stop, wave 2)

Seat: `L1Kaidoku34-2.ARepairFresh` · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
UTC window: 2026-10-25T07:29:26Z – 2026-10-25T07:33:45Z · python3 3.14.8 · kernel 7.2.11-arch1-1
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ARepairFresh/` (all copies, receipts, my three readers)
Lane writes: this report only. No lane VCS command, no frozen instrument/claims/stop edit, no score.

## Answer in one paragraph

The repair reproduces its own published sweep (the seven registered shortcut readers plus the
unregistered eighth reader file `label_keyed.py`, the two wave-1 classes, all 0/8; `structural` 8/8) but it does **not** close the class it claims to close.
A structure-blind reader that never reads `name_off` (`mine/poszip.py`) reaches the target
**8/8 on all four named seeds and on ten further independent `os.urandom` seeds**, while scoring
**0/8 on the frozen permuted counter** — the repair lowers the bar by deleting the only transformation (pool permutation)
that forced offset resolution. A reader that reads **zero fixture bytes** and replays the seed
leaked on the counter's own command line (`/proc/<ppid>/cmdline`) also reaches **8/8** on every
explicit seed, which is how every receipt in this round runs the counter; and a table keyed on
the opaque filename digest reaches 8/8 for every already-published seed. The artifact is a **new
instrument, post-freeze, not a correction**: new predicate identity, not in `claims[0].pins` or
`instruments.json`, and its adoption would change the counter and predicate that the kill rule
froze. The stop stands; the repair is inadmissible for R34-C2 and insufficient for a next-round
pre-freeze as written.

## Axes named (Godspeed)

1. **Admissibility** — is the artifact inside the frozen instrument set (correction) or outside it (new instrument)?
2. **Class coverage** — does the fresh surface keep every structure-blind class below target, under both defensible readings of "structure-blind"?
3. **Harness isolation** — is the seed/expected content unavailable to the reader process through any channel other than the fixture bytes?
4. **Evidence reproducibility** — do the stop's and the repair's published numbers reproduce from the bytes on disk?

The moves below each test one axis; none was rejected for harming another.

## Method and compliance

- The repair was copied verbatim from the lane; sha256 **`5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c`**, identical to the pin in `w1/ExecRedReproduce.md:487`. The frozen counter copy is sha256 `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52`, identical to `claims[0].pins`.
- Every reader was executed **only as a python reader through a counter** (`mini-counter-fresh.py` or the frozen `mini-counter.py`), never directly and never as an ELF carrier. No fixture, carrier, production reader or lane tool was executed.
- No install; `pacman` untouched (transactions paused host-wide); no network.

## 1. The repair's own published sweep, reproduced (13 readers × 4 seeds)

Command template (cwd `/fast/scratch/hyaku/kaidoku-r34b/w2/ARepairFresh`), one run per reader/seed:

```
python3 -I -B counter/mini-counter-fresh.py --root . \
  --control-reader /fast/scratch/hyaku/kaidoku-r34b/w2/ARepairFresh/<reader> [--seed <seed>]
```

Seeds `seed-a`, `seed-b`, `seed-c` and a no-`--seed` run (`os.urandom`). All 52 runs 07:30:18Z–07:30:21Z;
per-run JSON in `out/sweep/`, table in `out/sweep.json`.

| reader | class | matched/8 (seed-a, seed-b, seed-c, urandom) | exits |
|---|---|---|---|
| `readers/structural.py` | structural positive control | **8, 8, 8, 8** | 0,0,0,0 |
| `readers/all_false.py` | all-false | 0,0,0,0 | 1,1,1,1 |
| `readers/digest_keyed.py` | digest-keyed | 0,0,0,0 | 1,1,1,1 |
| `readers/fixed_slice.py` | fixed-slice | 0,0,0,0 | 1,1,1,1 |
| `readers/label_keyed.py` | label-keyed | 0,0,0,0 | 1,1,1,1 |
| `readers/label_replay_full.py` | label-memorization | 0,0,0,0 | 1,1,1,1 |
| `readers/record_order_replay.py` | record-order-replay | 0,0,0,0 | 1,1,1,1 |
| `readers/size_keyed.py` | size-keyed | 0,0,0,0 | 1,1,1,1 |
| `readers/string_scan.py` | string-scan | 0,0,0,0 | 1,1,1,1 |
| `readers/nameset.py` | nameset-replay (wave 1) | 0,0,0,0 | 1,1,1,1 |
| `readers/pathkey.py` | path-digest-replay (wave 1) | 0,0,0,0 | 1,1,1,1 |

So the repaired surface does defeat the **registered** classes and the two wave-1 classes, and its
structural positive control meets the target. That part of the wave-1 claim reproduces exactly.
The rest of this report attacks the unregistered breadth, which is the same axis that produced the stop.

## 2. My own shortcuts against the repair

### R-A `mine/poszip.py` — positional row/pool pairing (never reads `name_off`)

Sha256 `710738ec682fc2471ea5497ad7d4e7bfa1e704f328cb434c76274c2bd4141c82`. It reads the header
only for `count` (`<H` at 6) and `records_off` (`<I` at 8); it **never reads bytes 12..16** (the
`names_off` field) and never resolves a `name_off`: it unpacks each row as `struct.unpack_from("<HI", data, base + 2)`
and takes the i-th NUL-terminated pool string in *file order* for the i-th row, with
`pool_start = records_off + 8 * count` computed arithmetically.

Why it is a shortcut, not structural work: the fresh generator builds the pool by iterating the
record list in order (`mini-counter-fresh.py:64-68`) and writes the rows in that same order
(`:78`), so pool order ≡ row order and the association is the identity map; `names_off` is
redundant because the generator sets it to `records_off + 8*count` (`:70`). Nothing in the fresh counter
permutes the pool or the rows — `def permute` and `--selftest` are absent from the file
(verified: `has_permute False`, `has_selftest False`, `size 6221`).

| seed | matched/8 | met_target | exit | UTC |
|---|---|---|---|---|
| `seed-a` | **8** | true | 0 | 07:30:20Z |
| `seed-b` | **8** | true | 0 | 07:30:20Z |
| `seed-c` | **8** | true | 0 | 07:30:20Z |
| urandom | **8** | true | 0 | 07:30:20Z |

Receipts: `out/poszip-seed-a.json` … `out/poszip-urandom.json`. Replicated on **10 further independent
`os.urandom` seeds** (07:34:41Z–07:34:44Z, `out/urandom-10x.json`): **8/8 on all ten**, exit 0 each;
`structural` 8/8 on the same ten as control. The class is not seed-lucky — it is structural.

### R-B `mine/seedreplay.py` — parent-argv seed replay (reads zero fixture bytes)

Sha256 `812bd37964e2e2754b3400ed464046aab701a8a1ee983922b6c9b3642d83f73c`. The repair runs the
reader as the counter's child and passes the seed on its **own command line** (`--seed`), so
`/proc/<ppid>/cmdline` publishes it. The reader re-runs the public `generate()` for that seed,
hashes the eight generated fixtures, matches the `opaque-<sha256[:20]>.data` basename, and prints
that fixture's expected records. It never opens `argv[1]`.

| seed | matched/8 | met_target | exit | UTC |
|---|---|---|---|---|
| `seed-a` | **8** | true | 0 | 07:30:20Z |
| `seed-b` | **8** | true | 0 | 07:30:21Z |
| `seed-c` | **8** | true | 0 | 07:30:21Z |
| urandom (no `--seed`) | 0 | false | 1 | 07:30:21Z |

Boundary stated precisely: the `env` handed to the child is `{"PATH", "HOME"}` only, so the seed
does **not** leak through the environment; it leaks through argv, and only when `--seed` is passed.
With `os.urandom` the class refuses (all eight reader calls exit 3; receipt `out/sweep/seedreplay-urandom.json`); on the named seeds all eight exit 0. Every receipt in this round
passes `--seed` explicitly, so under the round's own operating practice this class is live.
Not tested (unrun): reading `/proc/<ppid>/mem`; `yama/ptrace_scope` is **1** here, which per its
documented semantics restricts attach to descendants, so I did not pursue the ancestor-memory route.

### R-C `mine/seededtable.py` — published-seed table keyed on the opaque filename

Sha256 `7767babafa6c94c12d9032db3590d813251c0d7ee07cde5c7387967c98126b78`. `score()` returns
`"seed": str(seed)` in its JSON, so any recorded run publishes the material needed to regenerate
its fixtures offline; generation is fully deterministic from the seed. The reader keys on the
filename's content-digest prefix (`sha256(content)[:20]`) and replays a precomputed table for six
already-published seeds. It opens no fixture.

| seed | matched/8 | exit | UTC |
|---|---|---|---|
| `seed-a` | **8** | 0 | 07:32:25Z |
| `seed-b` | **8** | 0 | 07:32:26Z |
| `seed-c` | **8** | 0 | 07:32:26Z |
| `alt-1` | **8** | 0 | 07:32:26Z |
| `alt-2` | **8** | 0 | 07:32:26Z |
| `kaidoku-r34-mini-v1` | **8** | 0 | 07:33:45Z |
| urandom | 0 | 1 | 07:32:26Z |

Receipts: `out/seededtable-*.json`, `out/seededtable-sweep.json`.

## 3. Cross-surface contrast: the repair is weaker than the frozen counter

Same two readers on the **frozen** permuted counter (`frozen/mini-counter.py`, layout
`frozen-root/tools/round-34/mini-fix/`), seeds `kaidoku-r34-mini-v1`, `alt-1`, `alt-2`; runs
07:30:27Z–07:30:30Z, receipt `out/frozen-sweep.json`. Command:

```
python3 -I -B frozen/mini-counter.py --root /fast/scratch/hyaku/kaidoku-r34b/w2/ARepairFresh/frozen-root \
  --control-reader <reader> --seed <seed>
```

| reader | frozen surface (3 seeds) | fresh surface (4 seeds) |
|---|---|---|
| `mine/poszip.py` | **0, 0, 0** (exit 1) | **8, 8, 8, 8** (exit 0) |
| `readers/structural.py` | 8, 8, 8 (exit 0) | 8, 8, 8, 8 (exit 0) |
| `mine/seedreplay.py` | 0, 0, 0 (exit 1) | 8 on explicit seeds |

This is the decisive instrument defect: the fresh surface **admits a reader the frozen surface
rejects**, so substituting it is not an equal-strength repair — it converts a counter that forced
`name_off` resolution into one that accepts positional ordering. The fresh predicate's sentence
("the association is unpublished, so only record-array traversal recovers it") is false in the
sense that matters: the association is *published by construction* (order identity), and
`names_off` is redundant because it equals `records_off + 8*count` in every generated fixture.

## 4. Reading matrix: is "every structure-blind class below target" true?

The phrase has two defensible readings and the repair fails both:

| reading of "structure-blind" | who meets the fresh target | verdict |
|---|---|---|
| **D1 (stop's gloss):** "meets the target without walking records" | `seedreplay` 8/8 on every explicit seed; `seededtable` 8/8 on every published seed (`poszip` walks rows, so it is excluded here) | **false** whenever the seed is on argv or already published — both true of every receipt in this round |
| **D2 (capability):** does not recover the name→record association from the file / never reads `name_off` | `poszip` 8/8 on **all** seeds including urandom | **false unconditionally** |

So the answer to the assignment's question is **no**: the seven registered readers, the eighth
reader file `label_keyed.py`, and the two wave-1 classes stay at 0/8 and `structural` meets 8/8, but three of my structure-blind classes meet
8/8 (`poszip` on 14/14 seeds — 4 named + 10 urandom; `seedreplay` on 3/3 explicit seeds; `seededtable` on 6/6 published seeds).

## 5. The repair as an instrument: defects found in the artifact itself

Line references are to the copied artifact (`counter/mini-counter-fresh.py`, 6221 bytes, sha `5181330d…`).

1. **Permutation deleted.** No `permute()`; the pool is built in record order (`generate`, lines 64-78). This is the root cause of R-A and the reason the repair is weaker than the frozen surface. A repair that keeps the frozen predicate shape must keep a transform that breaks positional correspondence.
2. **`--root` is dead.** The parser declares it (`parser.add_argument("--root", default=".")`), but `args.root` is referenced **zero** times; the counter scores only `--control-reader`. A gate that passes `--root` gets no validation that the lane/root is the expected one.
3. **No `--selftest`, no red arm.** The frozen counter has `--selftest` (structural positive control) and the gate supplies the red/refused arm from `gate-config-naive.json`. The fresh counter has neither, so its own "8/8 structural" number exists only as a one-off report line, not as an assertion the instrument can re-run.
4. **Seed published in output.** `score()` emits `"seed": str(seed)`. Combined with the practice of passing `--seed` on argv (both in the report's sweep and in the round's receipts), the "unpublished expected" premise is contradicted by the instrument's own I/O.
5. **No pinned-class assertion (F3 unaddressed).** Nothing asserts that the registered class set equals a pinned set; the same drop-to-floor blindness survives, and the fresh counter has no shortcut list at all.
6. **No red-last/row-count assertion (F4 unaddressed).** There is no selftest case or row-count check in the artifact; the gate's M3-style mutant surface is untouched by this repair.
7. **Predicate identity worsens (F2).** The artifact introduces a **fourth** predicate sentence, `P34-mini-records-fresh…` (sha256 `4426c1f9bbcc7e97904e06926101bf7c003e9e4886668cc2192c58e6291cf1e3`), in addition to A (`7c6c17f0…`, governing), B (`8340aea5…`) and the mini-counter's C (`09988625…`). Its `P34-mini-records-fresh:` label is a different predicate, not a rebinding of A.
8. **Carried over unchanged:** exit-code conflation (0 = target met, 1 = below, 3 = unevaluable), `canonical()` strictness, `timeout=60`, opaque content-hash filenames, `SIZE=512` for all fixtures.

## 6. The stop's evidence checked (the arm I did not attack)

Reproduction of the decisive counterexample on the **frozen** counter, exactly as recorded in
`claim-stop.json` (seeds `alt-1`, `alt-2`, `kaidoku-r34-mini-v1`, runs 07:32:44Z–07:32:47Z,
receipt `out/frozen-stop-counterexample.json`):

| reader | matched/8 (alt-1, alt-2, kaidoku-r34-mini-v1) | exits |
|---|---|---|
| `nameset.py` | **8, 8, 8** | 0,0,0 |
| `pathkey.py` | 0,0,0 | 1,1,1 |
| `label_replay_full.py` | 0,0,0 | 1,1,1 |
| `digest_keyed.py` | 0,0,0 | 1,1,1 |

The stop's decisive counterexample is sound: `nameset` never reads the header, a record row or a
`name_off`; it keys on the sorted SONAME multiset (invariant under the frozen counter's only
transform) and replays a table. The identity-keyed classes are correctly defeated. Nothing in this
wave falsifies the stop's measurement; my findings falsify only the *proposed repair*.

Record-defect spot checks (bounded, read-only):
- F1's repair container exists: `instruments.json` carries the 26-pin map, and all 26 digests are
  byte-identical to `claims[0].pins` (verified programmatically: `inst==claims` is true). `freeze-integrity.py` itself
  was **not run** here (unrun) — it needs the lane VCS and is another seat's surface.
- F2 is confirmed as disclosed: `predicate-reconciliation.json` records A/B/C as three distinct
  sentences with distinct hashes, and the governing sentence is A.
- F3/F4 are **not** repaired by the fresh counter (items 5 and 6 above).

## 7. New instrument or correction of one?

**New instrument. Post-freeze. Not a correction.**

Evidence:
- It is not in the frozen instrument set: absent from `claims[0].pins` and from
  `instruments.json`; `grep -rn "mini-counter-fresh" tools/ *.json` over `tools/` and the two
  r34b pin files returns nothing. It lives only under `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/`.
- It changes the counter **and** the predicate: a new `PREDICATE` constant (sentence D), a new
  fixture source (generated per run vs the eight committed fixtures), and a different transform
  set (permutation removed). `claims[0].kill_rule`: "no target, counter, predicate or label may be
  changed afterwards". A correction preserves predicate identity and pin semantics; this changes both.
- Its CLEAN run in wave 1 used a scratch `gate-config-fresh.json`, not either pinned config, so no
  frozen clause ever evaluated it.

Consequence: the artifact cannot validate R34-C2, cannot be used to "restore" the claim, and its
8/8-structural / 0/8-shortcut numbers are **not evidence about the frozen claim**. The stop's
verdict (`falsified measure; honest stop`) is unaffected. Nothing here awards or restores a score.

If the L1 wants a next-round pre-freeze (new claim, new freeze, new predicate identity), the minimum
conditions this seat's evidence imposes are:
1. keep a transform that breaks positional correspondence — permute the pool and rewrite `name_off`
   (as the frozen counter does), and vary record order independently of pool order;
2. isolate the harness — never put the seed on the child-visible argv, do not print it before the
   run is scored, and do not reuse seeds across receipts (otherwise R-B/R-C stay live);
3. assert the registered class set equals the pinned set before CLEAN (F3) and add the red-last
   case plus a row-count assertion (F4);
4. register an order-pairing class (`poszip`-shaped) and a harness-leak class alongside the
   multiset class, so the bar is set by the strongest known blind reader;
5. pin the artifact under `tools/` and hash it before any data run, with one predicate sentence
   bound in claims, config and counter (and read from claims, not echoed).

## 8. Exact commands and exits

All runs below use absolute scratch paths; `cwd` is `/fast/scratch/hyaku/kaidoku-r34b/w2/ARepairFresh`.

```
# fresh counter, 13 readers x 4 seeds (52 runs, 07:30:18Z-07:30:21Z)
python3 -I -B counter/mini-counter-fresh.py --root . --control-reader <ABS>/readers/<r>.py --seed {seed-a|seed-b|seed-c}
python3 -I -B counter/mini-counter-fresh.py --root . --control-reader <ABS>/readers/<r>.py
# frozen counter, poszip/structural/seedreplay x 3 seeds (07:30:27Z-07:30:30Z)
python3 -I -B frozen/mini-counter.py --root <ABS>/frozen-root --control-reader <ABS>/mine/poszip.py --seed {kaidoku-r34-mini-v1|alt-1|alt-2}
# frozen counter, stop counterexample (07:32:44Z-07:32:47Z)
python3 -I -B frozen/mini-counter.py --root <ABS>/frozen-root --control-reader <ABS>/readers/nameset.py --seed {alt-1|alt-2|kaidoku-r34-mini-v1}
# seeded table (07:32:25Z-07:33:45Z), seeds seed-a|seed-b|seed-c|alt-1|alt-2|kaidoku-r34-mini-v1 (8), urandom (0)
python3 -I -B counter/mini-counter-fresh.py --root . --control-reader <ABS>/mine/seededtable.py --seed <seed>
```

Exit codes: fresh counter 0 = target met, 1 = below target, 3 = unevaluable. Observed exits are
stated per run in sections 1–3 and 6; every nonzero is the counter's own "below target" (1), never 3.
Copies and digests: repair `5181330d…`, frozen counter `43ef669f…`, poszip `710738ec…`,
seedreplay `812bd379…`, seededtable `7767baba…`.

Unrun (not passed, therefore not claimed): the 100-seed sweep; `/proc/<ppid>/mem` ancestry route
under yama scope 1; `freeze-integrity.py` execution; a full `replay-gate.py --selftest` run over a
fresh-counter config.

## VERDICT

`REPAIR_IS_NEW_INSTRUMENT_POST_FREEZE_NOT_A_CORRECTION — fresh sweep reproduces (7 registered + label_keyed +
nameset + pathkey = 0/8; structural 8/8 x14), but structure-blind classes still meet target:
poszip 8/8 on 14/14 seeds incl. 10 independent urandom seeds (frozen surface 0/8 x3), seedreplay
8/8 on 3/3 explicit seeds / 0 on urandom, published-seed table 8/8 on 6/6 published seeds / 0 on
urandom. The fresh surface is strictly weaker than the frozen one (permutation removed; name_off
never needed), so substituting it cannot restore R34-C2; the stop stands and no score moves.`
