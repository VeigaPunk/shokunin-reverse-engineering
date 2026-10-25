# ExecRedReproduce — R34-C2 independent red reproduction, green-counter attack, and fix probe

Seat: `L1Kaidoku34-2.ExecRedReproduce` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Instruments measured at lane tip pre-wave (`c79bbe7b`, per prompt) on a **copy** of `tools/` in
`/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/clone` — the lane was never written, never
executed in place, and no VCS command was run. No network. No ELF/fixture executed as a program;
fixtures were read as static bytes only; readers were run as `python3` scripts by the counters.

**VERDICT: RED REPRODUCED (8/8) AND THE GREEN COUNTER DEFEATS MY PATH/DIGEST KEY, BUT THE
PERMUTATION DOES NOT DEFEAT A NAME-SET-KEYED REPLAY (8/8 UNDER `mini-counter.py`, three seeds).**
Consequence: the six frozen clauses are untouched (they read only the two pinned configs and
`label-memorization`), so R34-C2 stays CLEAN on its own text — but the green surface's stated
rationale ("only record-array traversal associates a name with its record") is **falsified as a
measured fact**, and the registered shortcut set is not complete over the class space it claims to
exclude. A validated counter rewrite (`mini-counter-fresh`, per-run unpublished content) defeats
both new classes while keeping the structural control at 8/8.

## 1. Axes named (cheap, independent)
1. **Red reachability** — can an independently written, structure-blind reader hit `matched=8/target=8`
   on the naive counter? (memorise answers keyed on something invariant about the naive counter's inputs)
2. **Key invariance** — does the green transformation destroy the key that the red shortcut uses?
3. **Gate consequence** — what does `replay-gate.py` say when such a class is registered?
4. **Fix direction** — is there a counter shape that defeats even a key-invariant memoriser while the
   structural positive control still meets target?

## 2. Instrument pin verification (`date -u` 2026-10-25T07:18:33Z, exit 0)
All seven hashed files match the `claims.json` pins exactly (`sha256sum`, exit 0):

| file | observed sha256 | pin |
|---|---|---|
| `replay-gate.py` | `8fa94b23…c1c7558` | match |
| `c2-shortcut-gate-counter.py` | `41d59703…9a5a72` | match |
| `gate-config-mini.json` | `4483f385…12ac9c` | match |
| `gate-config-naive.json` | `72b12941…6b1428` | match |
| `mini-fix/naive-counter.py` | `087c97f7…b9f6894` | match |
| `mini-fix/mini-counter.py` | `43ef669f…c47c4b52` | match |
| `mini-fix/expected.json` | `5ebb5349…8828483` | match |

All eight fixture digests in `mini-fix/fixtures/` also match the pins
(`alpha d1de0e6f…`, `beta a8547fcf…`, `delta 79ff7036…`, `epsilon 82f03f99…`, `eta 5bcabeb2…`,
`gamma ffb57ecd…`, `theta b1f87d7c…`, `zeta 19ff4074…`). Runtime: `/usr/bin/python3` = Python 3.14.8.

## 3. Red reproduced — my own reader, own shortcut class (naive counter)
Command (cwd = scratch clone; identical to the assignment's shape, `--root .` on the copy):

```
/usr/bin/python3 -I -B tools/round-34/mini-fix/naive-counter.py --root . \
  --control-reader /fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/r_pathkey.py
```

**Receipt (2026-10-25T07:18:56Z, exit 0):**
`{"finding": "records_match", "matched": 8, "met_target": true, "target": 8, … all 8 rows ok:true, exit:0}`

- **Shortcut class used: input-identity memorization** — basename stem (`alpha`…`zeta`) as primary key,
  raw-byte SHA-256 as fallback key; the answer table is hard-coded; no header read, no record walk,
  no `name_off` dereference. **matched 8 / target 8.**
- Invariant used: the naive counter hands the reader
  `str(<root>/tools/round-34/mini-fix/fixtures/<name>.mrec)` as argv[1] and leaves those bytes unmodified,
  so both the label and the byte-digest are legible to the reader on every call.
  (Corroboration, not the reproduction: the pinned `readers/label_replay_full.py` also scores 8/8
  on the naive counter, exit 0, same timestamp.)
- Artifact: `r_pathkey.py`, sha256 `28acfe5a79b29977c89de26accc55233d54c08daededf2452893e91043d481a9`.

## 4. Green counter vs. that reader — permutation defeats it
```
/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader /fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/r_pathkey.py
```
**Receipt (07:18:56Z, exit 1): `matched 0`, `met_target false`** — every row `exit:3` (my reader's typed
refusal: opaque basename, permuted bytes ⇒ neither key resolves). Seed sweep `--seed alt-1`, `--seed alt-2`
(07:19:56Z): `matched=0` both. **Yes: the permutation defeats the path/digest class.**

## 5. Second class: the permutation does NOT defeat a name-set key (the depth finding)
`r_nameset.py` — **content-multiset memorization**: scan the file with a SONAME regex
(`[A-Za-z0-9_.+-]+\.so(\.[0-9]+)+`), build the sorted set of names found, and replay a hard-coded
name→(flags,value) table keyed by that set. It reads the pool as text only: no header, no record
array, no `name_off`. The name→record association comes from the table, not the bytes.

| counter | command | receipt | UTC | exit |
|---|---|---|---|---|
| naive | `naive-counter.py --root . --control-reader r_nameset.py` | `matched 8 / target 8, records_match` | 07:19:02Z | 0 |
| green | `mini-counter.py --root . --control-reader r_nameset.py` | **`matched 8 / target 8, met_target true`** | 07:19:02Z | **0** |
| green, `--seed alt-1` | same | `matched=8 met=True` | 07:19:56Z | 0 |
| green, `--seed alt-2` | same | `matched=8 met=True` | 07:19:56Z | 0 |
| green, `--seed alt-3` | same | `matched=8 met=True` | 07:19:56Z | 0 |

**So: the permutation does not defeat this reader — it meets the green counter's own target under its
own predicate.** (First pass was 6/8 solely from my regex omitting `-`; after allowing hyphens in the
token class, epsilon `ld-linux-x86-64.so.2` and zeta `libwayland-client.so.0` resolve. Fixed at 07:19:02Z,
receipts above.) Artifact: `r_nameset.py`, sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`.

### 5.1 Why — measured invariance of the transformation (probe, 07:20:05Z, exit 0)
Ran `mini-counter.permute(data, Random("kaidoku-r34-mini-v1"))` over all eight fixtures and compared:

```
alpha/beta/delta/epsilon/eta/gamma/theta/zeta:
  size_eq=True  digest_changed=True  decoded_eq=True  nameset_invariant=True
```
The transform is *required* to preserve decoded content (the counter compares against the original
`expected.json`), so it can never change the answer; and the SONAME multiset is invariant under a pool
reorder. Therefore:

> **Lemma (invariance limit).** Let T be any input transform with `decode(T(x)) = decode(x)`. For any
> shortcut `S(x) = F(g(x))` with `g` public and `g(T(x)) = g(x)`, `S` meets the target on every
> transformed fixture whenever it meets it on the original. A layout-only transform therefore cannot
> exclude any shortcut keyed on a public layout-invariant of the content. This gate's only transform is
> layout-only (pool order + `name_off` rewrite).

The sentence this falsifies is `mini-counter.PREDICATE` itself — "… only record-array traversal
associates a name with its record." That sentence is the predicate the frozen C2 predicate delegates to
("scored under the counter's own predicate"), and the gate's green clause accepts a shortcut's
`met_target` on exactly that counter, so the delegation chain inherits a false premise even though the
C2 clause *quantifier* ("registered") is still satisfied.

## 6. Gate consequence — a registered class flips the frozen green verdict
Frozen-config calibration in the scratch copy reproduces the production receipt lines exactly:
- `replay-gate.py --root . --config tools/round-34/gate-config-mini.json` → `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-`, exit 0 (07:19:33Z) — identical to `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` `green.line`.
- `… --config tools/round-34/gate-config-naive.json` → `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization`, exit 2 (07:19:33Z) — identical to the receipt's `red.line`.
- `replay-gate.py --selftest` → `{"cases": 12, "failures": 0, "mutants_killed": 3}`, exit 0 (07:19:56Z).

Now register my class as an eighth shortcut (seven pinned + `nameset-replay`; scratch config
`gate-config-gap.json`, same pinned counter):
```
/usr/bin/python3 -I -B tools/round-34/replay-gate.py --root . \
  --config /fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/gate-config-gap.json
```
**Receipt (07:19:45Z, exit 2): `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=nameset-replay`**
→ `gate-gap.json`. The gate's own refusal branch bites the class; the frozen CLEAN holds only because
the class is unregistered. This is a registration-completeness gap, not a clause failure: the C2
counter's `red_refused` clause reads exactly `red["exit"] == 2 and verdict == REFUSED and
"label-memorization" in red_classes` (`c2-shortcut-gate-counter.py:105-116`), and both configs it reads
are the pinned files. **I did not and could not move a clause.**

## 7. Fix validated — per-run unpublished content (`mini-counter-fresh.py`)
Prototype in scratch (`--root` kept for gate argv compatibility; `--seed` defaults to `os.urandom(16)`):
generates eight fresh MREC fixtures per run (2–6 records, random SONAMEs, random flags 0–3, random
values), writes them to opaque `opaque-<sha256[:20]>.data` paths, and computes expected records from the
generation. The association is never published, so no table can be keyed on it.

Reader sweep (07:19:47Z, one random seed per run; `structural` repeated 4× at 07:19:56Z with seeds
`eb37e25c…`, `e6a0ff00…`, `4e140175…`, `24ecb138…`, all 8/8):

| reader | class | matched/8 |
|---|---|---|
| `readers/structural.py` | structural (positive control) | **8** (5 runs) |
| `r_nameset.py` | nameset-replay (mine) | 0 |
| `r_pathkey.py` | path-digest-replay (mine) | 0 |
| `readers/label_replay_full.py` | label-memorization | 0 |
| `readers/size_keyed.py` | size-keyed | 0 |
| `readers/fixed_slice.py` | fixed-slice | 0 |
| `readers/digest_keyed.py` | digest-keyed | 0 |
| `readers/string_scan.py` | string-scan | 0 |
| `readers/record_order_replay.py` | record-order-replay | 0 |
| `readers/all_false.py` | all-false | 0 |

Gate run with that counter and all nine classes registered (scratch `gate-config-fresh.json`):
**`REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=9 shortcuts_over_target=-`,
exit 0 (07:19:47Z)** → `gate-fresh.json`. Artifact `mini-counter-fresh.py`,
sha256 `5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c` (dead helper removed after the
sweep; re-probed 07:22:02Z on seed `05c63bf8…`: structural 8/8, `r_nameset.py` 0/8, `r_pathkey.py` 0/8).

## 8. What I recommend the L1 land (draft text only — I wrote no lane doc)
- **Retain R34-C2 as CLEAN.** No clause moved; the two pinned configs and `label-memorization` are intact.
- **LOG/lesson draft:** "R34 depth finding (ExecRedReproduce, independent): the frozen green surface's
  transform is layout-only, so a structure-blind replay keyed on the SONAME multiset met `mini-counter.py`'s
  own target at 8/8 on three seeds (site: `r_nameset.py`), and the gate refuses when that class is
  registered (`classes_over_target=nameset-replay`). The predicate sentence 'only record-array traversal
  associates a name with its record' is false as written; the clause set is unaffected because it quantifies
  over registered readers. Counter shape that closes it: generate the green fixtures per run from a fresh
  seed (unpublished expected), validated at 8/8 structural and 0/8 for all nine shortcut classes."
- **Next pre-freeze, if the L1 wants the rationale to hold:** replace `mini-counter.py`'s committed-fixture
  surface with `mini-counter-fresh.py`'s generate-per-run surface and register `nameset-replay` +
  `path-digest-replay`. Artifacts are reproduced verbatim in Appendix A–C below with sha256 pins; they
  live in `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/` (ephemeral) — L1 must write them into
  `tools/round-34/` to make them durable, and can verify identity against the pins.

## 9. Risks, limits, blockers
- **Scope of the finding:** strictly a registration-completeness/rationale gap; it does **not** falsify any
  of the six frozen clauses, and under the kill rule ("no target, counter, predicate or label may be changed
  afterwards") it cannot be repaired inside R34-C2 — it is next-round material or an honest LOG entry.
- **My fix is a prototype, not a registered instrument:** it was validated against the eight pinned readers
  plus my two, one seed per reader (plus 5 structural seeds). A 100-seed sweep was not run, and no mutant
  set exists for it; it has no `--selftest`.
- **Guessing attack on fresh content is not excluded, it is made non-deterministic:** a reader that guesses
  `flags/value` for ≤6 records has a vanishing but non-zero hit rate (`target=8` all-eight requirement makes
  that ~0 in practice; not measured).
- `mini-counter-fresh.py` output adds `seed`/`records` fields; gate field mapping unchanged
  (`matched`/`target`/`met_target`), verified by the CLEAN run above.
- **Tooling:** nothing installed or upgraded. `python3` 3.14.8 preexisting; `pacman` untouched (transactions
  paused); no network used.
- Scratch is `/fast/scratch/…` and may be reclaimed; every receipt above is quoted verbatim so the report
  stands alone.

## VERDICT
`RED_REPRODUCED matched=8/target=8 exit=0 (path-digest-keyed memorization); GREEN_DEFEATS_IT matched=0
(vs mini-counter, 3 seeds); GREEN_DOES_NOT_DEFEAT_NAME_SET_KEY matched=8 exit=0 (3 seeds) →
gate refuses with classes_over_target=nameset-replay (exit 2); fresh-content counter CLEAN with 9
shortcut classes and structural 8/8.`

---

## Appendix A — `r_nameset.py` (name-set keyed replay; sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`)

```python
#!/usr/bin/env python3
"""ExecRedReproduce R2: name-set keyed memorization (string-scan + replay).

Shortcut class: content-multiset memorization, composed from the registered
string-scan class plus a stored answer table. It scans the file for NUL-terminated
ASCII tokens that look like SONAMEs, then replays a memorized name -> (flags,
value) table keyed by the *sorted set of names found*.

It never reads the header, never walks the record array, and never reads a
name_off field: the association between a name and its flags/value comes from
the table, not from the bytes. Structure-blind by construction.

Invariant exploited: permuting the name pool changes the pool order and every
name_off, but leaves the set of names in the file unchanged, so a key built from
that set is invariant under the mini counter's only transformation.
"""
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(rb"[A-Za-z0-9_.+-]+\.so(?:\.[0-9]+)+")

TABLE = {
    "libc.so.6|libm.so.6|libz.so.1": [("libc.so.6", 0, 100729359), ("libm.so.6", 1, 2819),
                                      ("libz.so.1", 0, 2912)],
    "libcrypto.so.3": [("libcrypto.so.3", 0, 50332424)],
    "libdl.so.2|libgcc_s.so.1|libpthread.so.0|libresolv.so.2|libutil.so.1": [
        ("libgcc_s.so.1", 2, 2912), ("libpthread.so.0", 0, 0), ("libdl.so.2", 1, 2912),
        ("libutil.so.1", 0, 2912), ("libresolv.so.2", 0, 2912)],
    "libatomic.so.1|libstdc++.so.6": [("libstdc++.so.6", 0, 50531585), ("libatomic.so.1", 0, 2819)],
    "ld-linux-x86-64.so.2": [("ld-linux-x86-64.so.2", 0, 2819)],
    "libGL.so.1|libX11.so.6|libwayland-client.so.0|libxcb.so.1": [
        ("libGL.so.1", 3, 2912), ("libX11.so.6", 0, 2912), ("libxcb.so.1", 0, 2912),
        ("libwayland-client.so.0", 0, 2912)],
    "libcares.so.2|libcurl.so.4|libssl.so.3": [("libssl.so.3", 1, 50332424),
                                               ("libcurl.so.4", 0, 50531585),
                                               ("libcares.so.2", 0, 2819)],
    "libffi.so.8|libgmp.so.10|libisl.so.23|libmpc.so.3|libmpfr.so.6|libzstd.so.1": [
        ("libffi.so.8", 0, 2819), ("libgmp.so.10", 0, 2819), ("libmpfr.so.6", 0, 2819),
        ("libmpc.so.3", 0, 2819), ("libisl.so.23", 0, 2819), ("libzstd.so.1", 0, 2912)],
}


def main():
    if len(sys.argv) != 2:
        return 3
    data = Path(sys.argv[1]).read_bytes()
    names = sorted({token.decode("ascii") for token in TOKEN.findall(data)})
    key = "|".join(names)
    if key not in TABLE:
        return 3  # unrecognised content: typed refusal, no receipt
    records = [{"name": n, "flags": f, "value": v} for n, f, v in TABLE[key]]
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — `r_pathkey.py` (path/digest keyed replay; sha256 `28acfe5a79b29977c89de26accc55233d54c08daededf2452893e91043d481a9`)

```python
#!/usr/bin/env python3
"""ExecRedReproduce R1: basename-or-digest keyed memorization.

Shortcut class: input-identity memorization (path label primary, raw-byte
SHA-256 secondary). Never parses the record chain, never reads a header, never
associates a name with a record: it recognises the *file* and replays a stored
answer. Structure-blind by construction.

Invariant exploited: the naive counter hands the reader the fixture's own path
(basename <key>.mrec) and the fixture's own unmodified bytes, so both keys are
available on every call.
"""
import hashlib
import json
import sys
from pathlib import Path

TABLE = {
    "alpha": [("libc.so.6", 0, 100729359), ("libm.so.6", 1, 2819), ("libz.so.1", 0, 2912)],
    "beta": [("libcrypto.so.3", 0, 50332424)],
    "gamma": [("libgcc_s.so.1", 2, 2912), ("libpthread.so.0", 0, 0), ("libdl.so.2", 1, 2912),
              ("libutil.so.1", 0, 2912), ("libresolv.so.2", 0, 2912)],
    "delta": [("libstdc++.so.6", 0, 50531585), ("libatomic.so.1", 0, 2819)],
    "epsilon": [("ld-linux-x86-64.so.2", 0, 2819)],
    "zeta": [("libGL.so.1", 3, 2912), ("libX11.so.6", 0, 2912), ("libxcb.so.1", 0, 2912),
             ("libwayland-client.so.0", 0, 2912)],
    "eta": [("libssl.so.3", 1, 50332424), ("libcurl.so.4", 0, 50531585), ("libcares.so.2", 0, 2819)],
    "theta": [("libffi.so.8", 0, 2819), ("libgmp.so.10", 0, 2819), ("libmpfr.so.6", 0, 2819),
              ("libmpc.so.3", 0, 2819), ("libisl.so.23", 0, 2819), ("libzstd.so.1", 0, 2912)],
}

DIGESTS = {
    "d1de0e6f50eca499d70fc619bfa0bba52d9d789e36d2fba31109ffd6a922ad44": "alpha",
    "a8547fcf1764611f5aec0b869e4560a14c6f3e995b7b3ee703bba09826d7665d": "beta",
    "79ff7036235a026355c9281ffb845e7d2ffebe7f54982d82f36b49fb0ae4b781": "delta",
    "82f03f991a99b73001f160ae2d8d8f9dd327de2b7d4954dbbdb40a99d148738e": "epsilon",
    "5bcabeb2711ead28066d17db4a79ab2351a23d390c887fc009187f39f6ddbc2e": "eta",
    "ffb57ecdad76f6246e2aa2e8179e1effcfd49bbe9ef4c77b1959435b8937cc0a": "gamma",
    "b1f87d7cb8147c5cb02f2f7f4f3212bfd8147c0025b765e70a8341ee09b274e3": "theta",
    "19ff407420ab8028319b97e4bacc976eba3644b167bf0e235f7db5014078ea09": "zeta",
}


def main():
    if len(sys.argv) != 2:
        return 3
    path = Path(sys.argv[1])
    data = path.read_bytes()
    key = path.stem
    if key not in TABLE:
        key = DIGESTS.get(hashlib.sha256(data).hexdigest())
    if key is None:
        return 3  # unrecognised input: typed refusal, no receipt
    records = [{"name": n, "flags": f, "value": v} for n, f, v in TABLE[key]]
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix C — `mini-counter-fresh.py` (candidate fixed green surface; sha256 `5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c`)

Appendix fidelity check (07:22:05Z, exit 0): all three fenced blocks below are byte-identical to the
scratch artifacts (`verbatim_match=True` for each; block sha == file sha).

```python
#!/usr/bin/env python3
"""ExecRedReproduce: P34-mini-records-fresh counter (candidate fix for the gap).

Same predicate shape and the same reader contract as tools/round-34/mini-fix/
mini-counter.py, but the green surface is GENERATED PER RUN from a fresh seed
instead of being eight committed fixtures. Names, record counts, flags and values
are drawn at run time; expected records are computed from the generation, not read
from a public file, and the fixtures are written to opaque temporary paths.

Consequence: no memorised table can be keyed on the content, because the content
has never been published. Only record-array traversal recovers the association.

Never executes fixtures; static bytes only.
"""
import argparse
import hashlib
import json
import os
import random
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

PREDICATE = "P34-mini-records-fresh: eight synthetic record-chain fixtures generated per run from a fresh seed decode to exactly their generated name/flags/value records on opaque paths; the association is unpublished, so only record-array traversal recovers it."
TARGET = 8
SIZE = 512
MAGIC = b"MREC"


class Unevaluable(Exception):
    pass


def decode_fixture(data):
    if len(data) != SIZE or data[0:4] != MAGIC:
        raise Unevaluable("fixture_shape")
    version, count, records_off = struct.unpack_from("<HHI", data, 4)
    names_off = struct.unpack_from("<I", data, 12)[0]
    if version != 1 or count == 0 or records_off < 16:
        raise Unevaluable("fixture_header")
    records = []
    for index in range(count):
        base = records_off + 8 * index
        if base + 8 > names_off:
            raise Unevaluable("fixture_records_overflow")
        name_off, flags, value = struct.unpack_from("<HHI", data, base)
        records.append((name_off, flags, value))
    return records, names_off


def generate(rng, index):
    """Fresh fixture: random name pool, random flags/values."""
    count = rng.randint(2, 6)
    names = []
    while len(names) < count:
        stem = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(rng.randint(3, 12)))
        candidate = "lib" + stem + ".so." + str(rng.randint(1, 9))
        if candidate not in names:
            names.append(candidate)
    rng.shuffle(names)
    records = [(name, rng.randint(0, 3), rng.choice([0, rng.randint(0, 0xFFFFFFFF)])) for name in names]
    pool = bytearray()
    offsets = {}
    for name, _flags, _value in records:
        offsets[name] = len(pool)
        pool += name.encode("ascii") + b"\x00"
    records_off = 16
    names_off = records_off + 8 * len(records)
    if names_off + len(pool) > SIZE:
        raise Unevaluable("fixture_too_large")
    out = bytearray(SIZE)
    out[0:4] = MAGIC
    struct.pack_into("<HHI", out, 4, 1, len(records), records_off)
    struct.pack_into("<I", out, 12, names_off)
    for position, (name, flags, value) in enumerate(records):
        struct.pack_into("<HHI", out, records_off + 8 * position, offsets[name], flags, value)
    out[names_off:names_off + len(pool)] = pool
    expected = [{"name": name, "flags": flags, "value": value} for name, flags, value in
                sorted(records, key=lambda row: (row[0], row[1], row[2]))]
    return bytes(out), expected, "gen-" + str(index)


def canonical(value):
    if not isinstance(value, dict) or set(value) != {"schema", "records"} or value["schema"] != 1:
        return None
    if not isinstance(value["records"], list):
        return None
    rows = []
    for record in value["records"]:
        if not isinstance(record, dict) or set(record) != {"name", "flags", "value"}:
            return None
        if not isinstance(record["name"], str) or not isinstance(record["flags"], int) or not isinstance(record["value"], int):
            return None
        rows.append({"name": record["name"], "flags": record["flags"], "value": record["value"]})
    return sorted(rows, key=lambda row: (row["name"], row["flags"], row["value"]))


def score(reader, seed):
    if not reader.is_file():
        raise Unevaluable("reader_absent")
    rng = random.Random(seed)
    rows = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-fresh-") as work:
        for index in range(TARGET):
            data, expected, label = generate(rng, index)
            target = Path(work) / ("opaque-" + hashlib.sha256(data).hexdigest()[:20] + ".data")
            target.write_bytes(data)
            run = subprocess.run([sys.executable, "-I", "-B", str(reader), str(target)],
                                 capture_output=True, text=True, timeout=60,
                                 env={"PATH": "/usr/bin:/bin", "HOME": str(work)})
            observed = None
            if run.returncode == 0:
                try:
                    observed = canonical(json.loads(run.stdout))
                except (ValueError, TypeError):
                    observed = None
            rows.append({"fixture": label, "ok": observed == expected, "exit": run.returncode,
                         "input_size": len(data), "records": len(expected)})
    matched = sum(1 for row in rows if row["ok"])
    return {"predicate": PREDICATE, "target": TARGET, "matched": matched,
            "met_target": matched == TARGET, "rows": rows, "seed": str(seed),
            "finding": "records_match" if matched == TARGET else "records_mismatch"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--control-reader", required=True)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else os.urandom(16).hex()
    try:
        result = score(Path(args.control_reader), seed)
    except Exception as error:  # noqa: BLE001 - typed refusal, printed
        print(json.dumps({"predicate": PREDICATE, "met_target": False,
                          "finding": "unevaluable:" + type(error).__name__ + ":" + str(error)},
                         sort_keys=True))
        return 3
    print(json.dumps(result, sort_keys=True))
    return 0 if result["met_target"] else 1


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix D — scratch configs used (sha256)
- `gate-config-gap.json` (frozen mini counter + `nameset-replay` registered): `8a5e4837cb2b084ad7afc2d48c22bbb34fcf05c3ce39e600d1f68d532f243a6d`
- `gate-config-fresh.json` (fresh counter + 7 registered classes + `nameset-replay` + `path-digest-replay`): `9bf8416474048d4eec7e83971d32846002792ac7a6dbd3007d15826d386c44eb`
- receipts: `gate-gap.json` (REFUSED, exit 2), `gate-fresh.json` (CLEAN, exit 0), `b2.txt`, `d2.txt`.
