# The `.jsc` route under a complete closure — round-65 matrix

source: S266 — CPython 3 documentation, Command line and environment, `-B`
(https://docs.python.org/3/using/cmdline.html, h3 `Miscellaneous options`, raw line 474;
snapshot sha256 `96f87232…`) — plus the lane's own re-runnable gate
`tools/round-65/jsc-closure-matrix.py` (pin in the round-65 claims container)
verified-at: round 65, base `c99e907cb5576c13a7b22755d776b356fdfc1752`, operative freeze
`922ed89f42bed28173035f3faaf705e0cb70abb7`; measured at the round-65 landing (the receipt
`.ufo/waves/round-65/w1/ExecMatrix/matrix-run.json`)
recheck: `python3 -I -B tools/round-65/jsc-closure-matrix.py --selftest` (34 cases, exit 0) and
`python3 -I -B tools/round-65/jsc-closure-matrix.py --manifest --probe <probe.jsc>` (exit 0,
30 closure entries, cache-free)

## What changed since round 64

Round 64 reproduced the 18-run outcome matrix but stopped honestly: its clause "every input
and binary sha256 equal to its pin" could not be certified, because the instrument pinned nine
objects (three d8 binaries, three inputs, two D1 companions, `view8.py`) and left the D2/D3
companions, the transitive `View8/` tree, the venv identity and the `node --check` binary
unpinned, and because the View8 subprocess wrote `__pycache__` files into the retained
toolchain. Round 65 closes both gaps and re-runs the same frozen predictions. This entry
records what the closure is and what its receipts establish; it does not claim a source
recovery.

## The closure — 30 pinned entries

Observation (manifest check, exit 0 at the freeze):

| group | entries | what it pins |
|---|---|---|
| d8 builds | 9 | `d8`, `snapshot_blob.bin`, `icudtl.dat` for 14.8.178.14, 14.8.178.1, 14.7.173 |
| View8 tree | 12 | every file under `jsc2js-src/View8/` (the whole import closure: `view8.py`, `Parser/`, `Simplify/`, `Translate/`, `Bin/`, `README.md`) |
| venv identity | 4 | `parse/__init__.py`, `parse/__init__.pyi`, dist-info `METADATA` and `RECORD`, plus `venv/pyvenv.cfg` |
| artifacts | 2 | the Typora code cache and the Electron 42.2.0 probe cache |
| harness | 3 | the resolved `node` binary (v24.21.0) and the resolved venv interpreter, each by sha256 of its real path, and the probe path |

The instrument refuses to run (exit 2) when any entry is absent or differs, and when the
toolchain still holds a `__pycache__` directory or a `*.pyc` file. The refusal was
demonstrated red on a scratch copy: one byte flipped in
`d8-14.8.178.1/snapshot_blob.bin` produced `pin_mismatch: ["d8-14.8.178.1/snapshot_blob.bin"]`
and exit 2; a planted `__pycache__/x.pyc` produced `cache_present` naming both the directory
and the file (receipts `w1/ExecControls/pin-mutation.json`, `cache-present.json`,
`cache-clean.json`).

Why the View8 tree and not only `view8.py`: the entry point imports
`Parser.sfi_file_parser`, `Parser.shared_function_info`, `Simplify.simplify`,
`Translate.translate`, `Translate.translate_table`, `Translate.jump_blocks` and
`Simplify.function_context_stack`; the import chain is the run's real code, and pinning only
the entry point certifies one twelfth of it.

## Bytecode writes

Every subprocess runs with `-B` in its argv and `PYTHONDONTWRITEBYTECODE=1` in its
environment. S266 documents the switch's effect: "If given, Python won't try to write .pyc
files on the import of source modules." The instrument does not take the documentation as a
result: it censuses every regular file under the toolchain root (sha256 per path, excluding
`jsc2js-src/.git/`) immediately before the first run and immediately after the last one, and
the two maps must be equal. At the round-65 dry run and at the wave run the census was equal
with zero added, removed or changed paths.
Observation, bounded by QUALITY #19: the bytes are identical at the two named instants; the
census does not establish continuity between them beyond those two maps. An mtime-preserving
byte-identical rewrite is not detected and is not claimed detected.

## The 18 labels (observation)

The label matrix is unchanged from round 64's frozen predictions; reproducing it under the
closure is the claim, not a new discovery:

| cell | predicted and observed label | count |
|---|---|---|
| probe × D1, probe × D2 | `dump-ok` → `view8-ok` → `node-fail` | 6 |
| probe × D3 | `dump-exit-139` (SIGSEGV) | 3 |
| typora × D1, D2, D3 | `dump-exit-134` (SIGABRT) | 9 |

`dump-ok` means the patched d8 printed Ignition text carrying `[SharedFunctionInfo]`; `view8-ok`
means the reconstruction file is non-empty; `node-fail` means `node --check` rejected it. The
reconstruction output is therefore not parseable JavaScript — an observation from the parser,
not an inference from the mapper's documentation. That distinction is the round-64 correction
(S264 proves the upstream contract, not output correctness); it survives here.

## Limits and unknowns

- A matching d8 version is necessary, not sufficient: every Typora cell aborts inside d8
  (SIGABRT) with the matching build, so no View8 stage runs on the real Typora cache. The
  abort is an observed signal death; its internal cause is unknown and is not asserted.
- The probe artifact is a code cache generated by Electron 42.2.0 run-as-node. It exercises the
  route, not a shipped application's cache.
- `.jsc` → source mapping for Typora remains Frontier. This entry holds the route outcome
  under a complete closure, not a source recovery.
- The census excludes `jsc2js-src/.git/` (git metadata, not a run input; a read-only `git`
  invocation can refresh it). No other exclusion exists.
