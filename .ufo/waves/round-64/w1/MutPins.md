# MutPins — mutation probe of the R64 pin gate (`check_pins`)

Seat: `MutPins`, round 64, wave w1. Canonical copy of this file:
`.ufo/waves/round-64/w1/MutPins/pins.md`; byte-identical mirror written to the
`Report:` trailer path `.ufo/waves/round-64/w1/MutPins.md`.

## Target

| item | value |
|---|---|
| instrument (frozen, never edited) | `kaidoku-shokunin/tools/round-64/jsc-route-matrix.py` |
| instrument sha256 | `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` |
| working copy | `/fast/scratch/hyaku/kaidoku-r64/MutPins/mutants/base.py`, sha256 identical to the instrument |
| function under test | `check_pins(args) -> str \| None`, lines 142–166 (inline `PINS` at 56–68) |
| call convention | `importlib` load of each module; `argparse.Namespace` with `probe, typora, d8_match, d8_neighbour, d8_cross, view8_dir` |
| interpreter | `/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python` |

`check_pins` has five distinct gate families: two inputs (`probe`, `typora`), three
`d8` binaries (`D1`,`D2`,`D3`), two extra files inside the `D1` build dir
(`snapshot_blob.bin`, `icudtl.dat`), and `view8.py`. One mutant targets each.

## Verdict table (required)

Every violated fixture was derived from a tree the unmutated instrument accepts
(`check_pins -> None`), so the unmutated error column is attributable to the single
violation and nothing else.

| mutant | violated fixture | unmutated result | mutant result | survived? |
|---|---|---|---|---|
| P1 — drop `snapshot_blob.bin` from the D1 extra-file loop | `d1/snapshot_blob.bin` = 40 wrong bytes (sha256 `6aea29ba…2460fdac`) | `pin mismatch D1 snapshot_blob.bin` | `None` | **YES** |
| P2 — remove the `view8.py` check | `view8/view8.py` absent | `pin mismatch view8.py: <fixture>/view8/view8.py` | `None` | **YES** |
| P3 — drop `D3` from `builds` in `check_pins` | `d3/d8` absent (dir present, binary missing) | `missing d8 D3: <fixture>/d3/d8` | `None` | **YES** |
| P4 — compare only `[:8]` hex digits at all four comparison sites | `inputs/probe.jsc` = 20 bytes, sha256 `a86f6ea0 02372b5e…` (first 8 hex equal to the probe pin, full digest different) | `pin mismatch probe: <fixture>/inputs/probe.jsc` | `None` | **YES** |
| P5 — drop `typora` from the inputs dict | `inputs/typora.jsc` = 40 wrong bytes | `pin mismatch typora: <fixture>/inputs/typora.jsc` | `None` | **YES** |

Killed: 0. Survived: 5. Inconclusive: 0. No baseline failure occurred: the unmutated
gate rejected all five violated fixtures, each with the message naming the violated
path (so every earlier check had already passed on that fixture).

## Controls (each demonstrates the fixture is not independently broken)

| control | unmutated | mutant |
|---|---|---|
| intact skeleton tree, all pins real (`fixtures-skeleton`) | `None` | — |
| intact tree per mutant (`fixtures-<M>-valid`) | `None` | `None` |
| extra violation of a check the mutant keeps (`fixtures-<M>-extra`) | error | error — mutant still rejects |
| P1 extra: `d1/icudtl.dat` wrong | `pin mismatch D1 icudtl.dat` | `pin mismatch D1 icudtl.dat` |
| P2 extra: `inputs/probe.jsc` wrong | `pin mismatch probe` | `pin mismatch probe` |
| P3 extra: `d2/d8` wrong | `pin mismatch d8 D2` | `pin mismatch d8 D2` |
| P4 extra: `inputs/probe.jsc` wrong (prefix differs) | `pin mismatch probe` | `pin mismatch probe` |
| P5 extra: `inputs/probe.jsc` wrong | `pin mismatch probe` | `pin mismatch probe` |

## Mutants (single textual change each; target occurrence asserted == 1 before substitution)

Each mutant file, its exact diff against `base.py`, and the assertion that the target
text occurred exactly once:

**P1** sha256 `00fc948ea4a27911e4d6047f54367e7dc2ee6edb6d7bc790e4e16230ffc5287c`
```diff
-    for fname, key in (("snapshot_blob.bin", "D1-snapshot"), ("icudtl.dat", "D1-icudtl")):
+    for fname, key in (("icudtl.dat", "D1-icudtl"),):
```
(Note: the naive deletion without the trailing comma yields `for fname, key in (("icudtl.dat", "D1-icudtl")):`,
which raises `ValueError: too many values to unpack`; the trailing-comma form is the
minimal edit that keeps the loop iterating over pairs and removes only the snapshot check.)

**P2** sha256 `eb7d3ece3e5160fc05c6a24d222b3d40b63b6f597d046a794d8a437513c07245`
```diff
-    view8 = Path(args.view8_dir) / "view8.py"
-    if not view8.is_file() or sha256_file(view8) != PINS["view8.py"]:
-        return f"pin mismatch view8.py: {view8}"
     return None
```

**P3** sha256 `27bfd22b229e25010eceeabbf710b3b4ae826a156f477dee5e044409e0366d4a`
```diff
-    builds = {"D1": Path(args.d8_match), "D2": Path(args.d8_neighbour),
-              "D3": Path(args.d8_cross)}
+    builds = {"D1": Path(args.d8_match), "D2": Path(args.d8_neighbour)}
```
(anchored to the `check_pins` occurrence because `run_matrix` carries a textually
identical `builds` literal at line 183, which was left untouched.)

**P4** sha256 `3c1da95553753e4a7e1c82d3663443865911fda277a8457006ce32f1d7123ec7`
```diff
-        if sha256_file(p) != PINS[name]:
+        if sha256_file(p)[:8] != PINS[name][:8]:
-        if sha256_file(d8) != PINS[name]:
+        if sha256_file(d8)[:8] != PINS[name][:8]:
-        if not f.is_file() or sha256_file(f) != PINS[key]:
+        if not f.is_file() or sha256_file(f)[:8] != PINS[key][:8]:
-    if not view8.is_file() or sha256_file(view8) != PINS["view8.py"]:
+    if not view8.is_file() or sha256_file(view8)[:8] != PINS["view8.py"][:8]:
```
Four comparison sites, each asserted to occur exactly once (that is the whole gate;
truncating fewer leaves a live check). `PINS` values were not touched.

**P5** sha256 `258bad82e4a6a4672a7b7ce0a8b73444938a27a405b116a5f23cf491197f8ad6`
```diff
-    inputs = {"probe": Path(args.probe), "typora": Path(args.typora)}
+    inputs = {"probe": Path(args.probe)}
```
(anchored with the `check_pins` docstring line; `run_matrix` line 185 carries the same
literal and was left untouched.)

## P4 collision construction (why the shaken fixture is real, not hypothetical)

`sha256_file(probe)[:8]` accepts any file whose digest starts `a86f6ea0`. A 32-bit
partial preimage was searched with an OpenSSL/`-march=native` SHA-NI brute forcer
(`collide.c`, 4 threads):

```
message  = b"MutPins-r64-" + (578730735).to_bytes(8, "little")   # 20 bytes
digest   = a86f6ea002372b5e03eeba2e8f5d95d35da665ed21b90a090b94a2a9b7d349b0
pin probe= a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710
prefix8 equal: True    full digest equal: False
```
Re-verified with `hashlib.sha256` (independent of the search program). The file is
20 bytes and is placed at `inputs/probe.jsc` in the P4 fixture tree. So P4's survival
is a genuine truncation defect, not an untested branch: a wrong artifact whose digest
merely collides in 32 bits passes the mutated gate and is rejected by the frozen one.
Cost of the collision: ~5.8e8 evaluations, ~3 s on 4 threads — cheap enough that a
`[:8]` gate is not a practical safeguard either.

## Coverage finding (not a contract change)

`jsc-route-matrix.py --selftest` was run on the frozen copy and on all five mutants
(`TMPDIR` inside the seat scratch):

| module | selftest exit | summary |
|---|---|---|
| base | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| P1 | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| P2 | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| P3 | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| P4 | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| P5 | 0 | `SELFTEST CLEAN cases=22 failures=0` |

The built-in selftest has **zero detection power** over all five pin-gate regressions:
its three pin cases all short-circuit on `probe`, so the `typora`, `D1` extra-file,
`view8.py` and `D3` checks are never exercised, and the prefix-truncation defect is
invisible to it. Consequence for R64-C1 provenance: a green `--selftest` says nothing
about whether pins were actually verified. The pin claim rests on the frozen instrument
text being hash-pinned (`29efef4f…`), and on the gate actually returning `None` over the
pinned tree — not on selftest coverage. This is reported, not fixed; the instrument and
`round-64-claims.md` are frozen and were not edited.

## Method / environment

- Fixture trees (per mutant: `valid`, `viol`, `extra`, plus one `skeleton`) are built
  by `pin_mutants.py` under `/fast/scratch/hyaku/kaidoku-r64/MutPins/`: every pinned
  path is a **symlink** to the real pinned artifact (`probe-electron.jsc`,
  `atom.compiled.dist.jsc`, the three `d8` builds with their `snapshot_blob.bin` /
  `icudtl.dat`, `jsc2js-src/View8/view8.py`); exactly one path is then replaced by a
  regular file of wrong bytes, a 20-byte collision file, or omitted. Symlinks are
  read-only indirection — `check_pins` opens and hashes through them, and nothing was
  ever written through a link into the shared toolchain.
- Baseline gate: the intact skeleton returns `None`, so a `None` from a mutant is not
  an artefact of a malformed fixture layout.
- Repository files: read only. No git/jj mutation, no writes outside
  `.ufo/waves/round-64/w1/MutPins/` and the seat scratch. No package installed
  (host `pacman` untouched); the brute forcer is a local C file linked against the
  already-installed OpenSSL.
- Commands actually run: `pin_mutants.py` (harness; exit 0), `diff -u base.py mutants/P*.py`,
  `sha256sum mutants/*.py`, `mutants/{base,P1..P5}.py --selftest`, `./collide 4`,
  `python -c` hashlib re-check of the collision.

## Evidence surviving scratch deletion

- `mutants/*.py` and `fixtures-*` lived only in scratch and were deleted; the exact
  mutant sources are reproduced by the diffs above from the frozen instrument.
- Structured records copied to `.ufo/waves/round-64/w1/MutPins/results.json`
  (instrument sha, base-copy sha, per-mutant sha, per-fixture unmutated/mutant return
  values, survived flags, extra-violation control results).

## Bottom line

5 mutants, 5 survivors, 0 killed, 0 inconclusive. Each of the five pin-gate families is
individually removable without any detector in the instrument noticing — including the
full `--selftest`. A `verify` from this instrument therefore means "the frozen text
returned `None` for this tree", which is exactly what the R64-C1 predicate asks for, but
the gate's own checks have no runtime corroboration beyond the frozen sha256 of the
instrument. No contract change is implied.
