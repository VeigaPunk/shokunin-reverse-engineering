# SentinelScope — round 90 (kaidoku), wave r90-w1

Security and cost review of the round-90 instruments. Read-only on the tree: every
artifact below is under this seat dir or `/fast/scratch/hyaku/kaidoku-r90/SentinelScope/`.

**Pins re-verified before any probe** (`receipts/instrument-sha256.txt`):

```
aaf3536ea2226ac8ec498603d50b7b1b4a57c5572c7edef4fcf0e2a91d35590b  tools/round-90/upx-break-repair.py
84664f52afa0c03b38aca23552046fcf5e8e04056a597da7b2b06ef6d5eb8206  tools/round-90/upx-later-block-battery.py
faafc982ca5c7fcf2e787a8f78f81c5eb687c74998d2552ddd8935d01759b826  tools/round-90/control-cheat-repack.py
```

All three equal the pins in `.ufo/waves/round-90/claims.json`. Environment: `bwrap 0.13.1`,
`upx` at `/usr/bin/upx` (5.2.0 pin, checked by the counter's preflight), python 3.14,
`python3 -I -B` for every invocation (the counter's own child form). **No tool was installed
or upgraded** in this seat.

Instruments are pinned; `tools/round-90/upx-break-repair.py --selftest` → `SELFTEST cases=17
failures=0`, rc 0 (`receipts/mkfx.log`).

Fixtures (`receipts/fx.json`, `receipts/mkfx.log`): jq packed 14,036 B / 5 blocks / `ph_off`
14,000 / `u_len` 30,800; xxd 19,560 B; libz 65,580 B; docker-init 357,784 B. The P1 input is
block 1 `sz_cpr` stored − 7; the tool repairs it to the carrier pin.

---

## 1. Hostile inputs to `upx-break-repair.py`

Driver `receipts/hostile.py` + `receipts/hostile2.py`; raw records in `receipts/hostile.json`
and `receipts/hostile2.json`, transcripts `receipts/hostile.log`, `receipts/hostile2.log`.
Every case is `python3 -I -B tools/round-90/upx-break-repair.py --in <X> --out <Y>`, run from
a scratch cwd, wall-clocked.

| case | input/output shape | rc | message (stdout unless noted) | tb |
|---|---|---|---|---|
| H1 | FIFO as `--in` | 2 | `input is not a regular file` | no |
| H2 | directory as `--in` | 2 | `input is not a regular file` | no |
| H3 | `/dev/zero` as `--in` | 2 | `input is not a regular file` | no |
| H4 | 300 MiB sparse file | 2 | `input exceeds 268435456 bytes` | no |
| H4b | 250 MiB, ELF-magic, under cap | 2 | `upstream refusal: no validated PackHeader in the tail window` | no |
| H5 | truncated at 64 / 4096 / half / len−8 | 2 | same as H4b (0.281 s at 250 MiB, 0.04 s at 14 KB) | no |
| H6 | checksum-valid PackHeader, `u_len` 0xFFFFFFFE, `u_file_size` 0x7FFFFFFF | 2 | `round-89 refusal: no l_info candidate carries a derivable first block` | no |
| H7 | `--out` parent is a symlink | **1** | **traceback** — `Refused: --out parent is a symlink: …/outparentlink` | **yes** |
| H8 | `--out` has a symlinked *ancestor*, real parent tail | 0 | repair printed `class break-point`, delta 7 | no |
| H9 | `--out` contains `a/../b/o9` | **1** | **traceback** — `Refused: --out carries a '..' component: …` | **yes** |
| H10 | symlink planted at the final `--out` | 0 | victim sha256 `4a1a2a03…` unchanged; link replaced by a regular file | no |
| H11 | `--out` dir mode 0555 | **1** | **traceback** — `PermissionError: [Errno 13] … .r90-write-ki79ehrz` (tempfile.py:255) | **yes** |
| H12 | `--out` == `--in` | 0 | `overwrote_input: true` (path now holds the packed pin `e8b6c9e7…`) | no |
| H13 | symlink as `--in` | 2 | `input is not a regular file` | no |
| H14 | `--out ""` | 2 | argparse usage error (falsy `--out`) | no |
| H15 | missing `--in` | 2 | `cannot stat input: No such file or directory` | no |
| H16 | `--out` ok, `--info` in a 0555 dir | **1** | **traceback**, and `--out` **was already written** (`out_written: true`) | **yes** |
| H17 | `--info` == `--out` | 0 | final file's first byte is `{` — the repaired binary is gone | no |
| H18 | control: TMPDIR irrelevant | 0 | `mkstemp(dir=out-parent)` — TMPDIR is never consulted | no |
| H19 | existing 0444 file as `--out` | 0 | silently replaced (`replaced_readonly_file: true`) | no |
| H20 | dangling symlink as `--out` | 0 | link replaced; its target was **not** created | no |
| H21 | symlink→directory as `--out` | 0 | link replaced by a regular file; target directory intact | no |
| H22 | `--out` parent missing | **1** | **traceback** — `Refused: --out parent is not a directory` | **yes** |
| H23 | `--out` parent is a file | **1** | **traceback** — same | **yes** |

**Result: 27 cases across the two drivers (22 + 5), 6 uncaught tracebacks (H7, H9, H11, H16, H22, H23), no hangs, no
timeout.** Every input-side hostile shape (FIFO, directory, character device, over-cap,
truncated ELF, checksum-valid bogus PackHeader, symlink) is refused with a typed rc-2 JSON
line and never blocks.

**Why the crashes happen (code anchor).** `main()` at L415 wraps only
`read_input`+`repair` in `except Refused` (L427-431); `write_atomic(args.dst, …)` (L432) and
`write_atomic(args.info, …)` (L434) sit outside it, and `write_atomic` calls
`tempfile.mkstemp` at L118 *outside* its own `try` (the `except OSError` at L119-124 only
covers `fdopen`/`write`/`replace`). So every `Refused` raised by `checked_target` (L100-113)
— including the tool's own `..` and symlinked-parent guards — escapes as an uncaught
exception. The typed-refusal contract that QUALITY 169 is cited for covers the input side
only.

**Input race (not reproduced).** `read_input` does `os.lstat` (L86) and then `open` (L96)
non-atomically; a FIFO swapped in between would block forever (the tool sets no read
deadline). 300 interleavings toggling the `--in` path between a regular file and a FIFO gave
`{"trials": 300, "hangs": 0, "rcs": {"0": 150, "2": 150}, "tracebacks": 0}` in 35.4 s
(`receipts/race.json`, `receipts/race.log`). The window is real in the code but was not won
in 300 attempts; treat as advisory, not demonstrated.

## 2. `--out` / `--info` write scope

- **No `..` escape**: refused (H9) — though via the crash path, not rc 2.
- **Symlinked immediate parent**: refused (H7), again by crashing.
- **Symlinked *ancestor* is not checked** (L108 tests only `os.path.dirname(abspath(path))`).
  H8 gave rc 0 and the bytes landed in the resolved directory `…/realdir/sub/o8` while the
  caller asked for `…/ancestorlink/sub/o8`. The guard's stated purpose ("no `..` component and
  a real, non-symlinked parent") therefore does not survive one extra path level.
- **Final component**: a symlink at `--out` is replaced, never followed (H10, H20, H21) — no
  write-through to a victim, and a dangling target is not created. `os.replace` semantics are
  correctly relied on here.
- **Overwriting the input**: `--out` == `--in` overwrites it (H12, `overwrote_input: true`)
  with no guard; a hardlink alias would not (rename replaces the directory entry), so the only
  exposure is the literal same path — which is exactly what a caller who "repairs in place"
  would pass.
- **`--info` == `--out`** (H17): the repaired artifact is written and then overwritten by the
  JSON record; rc 0 and no warning. The counter never passes `--info` (`invoke()` passes only
  `--in`/`--out`), so no cell is affected.
- **`--out`/`--info` are not a transaction**: when `--info` fails, `--out` is already
  committed and the process dies with rc 1 (H16).
- **Permission semantics**: the result is always mode 0600 (mkstemp), regardless of the
  input's mode; an existing 0444 target is replaced (H19) because only directory write
  permission governs `rename`.
- **No write outside the tree it was given** in the plain case: every successful write landed
  in a directory reachable from the given path. The hazards above are redirection and
  collision, not traversal.

## 3. The carrier-blind sandbox

argv under audit, verbatim (`tools/round-90/upx-later-block-battery.py` L181-183, blind object
built at L279-290):

```
bwrap --dev-bind / / --tmpfs <run_root> --bind <decoy> /usr/bin/jq \
      --bind <decoy> /usr/bin/tinyxxd --bind <decoy> /usr/lib/libz.so.1.3.2 \
      --bind <decoy> /usr/bin/docker-init -- <python> -I -B <cmd> --in <box>/in --out <box>/out
```

Probes `receipts/bwrap_audit.py` (`receipts/bwrap.json`, `receipts/bwrap.log`),
`receipts/procout.json`, `receipts/rwprobe.json`.

**What holds.**
- Mount order is right: later mounts win, and `/proc/self/mountinfo` shows the four file binds
  *after* the tmpfs, with `--dev-bind / /` first (B2). The tmpfs really hides the run root:
  B1 lists `[]` where the host dir holds `packed-original`, and the no-tmpfs control B7 sees
  the file again.
- All four pins read the decoy inside the sandbox (B0: every path prints decoy sha
  `367675832d0a33ea…`).
- Resolved-symlink binds work: xxd's pin resolves to `/usr/bin/tinyxxd`, which is what gets
  bound, and `/usr/bin/xxd` then resolves to the decoy too (B0).
- The child cannot undo the hide: `CapEff 0000000000000000`, `NoNewPrivs 1`, and
  `umount2(hide, MNT_DETACH)` returns `-1/EPERM` (B3, B4).
- The `/proc/<pid>/root` route is closed here: because the tmpfs mount lives in the child's
  own mount namespace, `/proc/<pid>/root<run_root>` resolves through it. One hit (itself,
  empty listing), none for the host parent (`receipts/procout.json`).

**What does not hold.**
- **The boxes tree is not hidden, and the child is handed its own box path in `argv`.**
  `boxes` is created beside `run_root`, not inside it (L264-265, the comment says so
  explicitly), so `--tmpfs run_root` does nothing for it. A repair receives
  `<boxes>/inv-XXXX/in` and can therefore list `<boxes>` and read every sibling `out`.
  The counter's own N3 control (`invoke(repair, pbytes)`, run immediately before each
  carrier's P1 cells) leaves `out == the intact packed bytes` in a sibling box.
  Measurement: `receipts/cheat-sibling-oracle.py` (copies the same-length sibling `out` with
  the fewest differing bytes) scored through the counter's own `invoke`/`score_case` in the
  **blinded** sandbox:

  ```
  {"blind_ok": true, "blinded_recovered": 6, "blinded_cells": 6}   (receipts/leak6.json)
  ```

  All six P1 cells recovered with `repair_rc0/field_only/test_ok/identity/unpack_pin` true,
  i.e. the whole P1 population is satisfiable by a program that derives nothing. The real
  repair scores the same cell 6/6 blinded (`receipts/leak.json`), so the sandbox itself is not
  broken — it simply does not bound provenance. `isolation` stays true for the oracle too
  (`box_after` is `["in","out"]`).
- **Blinding is path-pinned, and the filesystem is full of copies.** A `--dev-bind / /`
  sandbox sees every other copy of the carriers. Bounded sweep (same size *and* same sha256,
  `/usr /opt /var/cache /home /fast`): jq **186**, xxd **110**, libz **83** unpacked copies
  outside their pins, essentially all under `/fast/scratch/hyaku/kaidoku-r90/` — other seats of
  this very round leave `orig`/`*.unpacked` behind (`receipts/copies.log`,
  `receipts/copies-summary.log`). The docker-init section was cut when the sweep hit its 600 s
  cap (`error: interrupted`); no count for it, and none claimed. `tools/round-90/control-cheat-repack.py`
  only tries the four pinned paths, which is why `cheat_killed` passes.
- **The blinding announces itself.** The decoy is 1,280 bytes of `decoy-not-a-carrier\n`
  (L280-281) and reads back verbatim in the sandbox (B5); `mountinfo` names both the decoy's
  host path and the hidden run root (B2). A repair can detect "I am blinded" and branch —
  honest under blinding, repacking when not — defeating the same control from the other side.
- **The scored code has the whole checkout writable.** The root bind is `rw`, and
  `os.access(lane, W_OK)` / `os.access(lane/.ufo/waves/round-90, W_OK)` / `$HOME` are all true
  inside the sandbox (`receipts/rwprobe.json`). A hostile repair can rewrite the instruments or
  the evidence tree it is being scored against. (Nothing was written there by this seat.)

## 4. Cost

`receipts/cost.py`, `receipts/cost.json`, `receipts/cost.log`; `python3 -I -B
tools/round-90/upx-break-repair.py --in <fx> --out <fx>.out`, median of 3 for the real
carriers, per-run timeout 150 s.

**A — real carriers, interior-block tamper (the P1 input shape), all rc 0:**

| carrier | packed bytes | wall (median) | verdict |
|---|---|---|---|
| jq | 14,036 | 0.035 s | `break-point`, delta 7 |
| xxd | 19,560 | 0.039 s | `break-point`, delta 7 |
| libz | 65,580 | 0.058 s | rc 0, `intact` unchanged (declared out-of-class: chain accounts 98,592 of 108,560) |
| docker-init | 357,784 | 0.121 s | `break-point`, delta 7 |

**B — l_info candidates 1 / 801 / 3,201 / 12,801 (the round-88 axis), jq P1 base:**

| candidates | file bytes | wall | rc | label |
|---|---|---|---|---|
| 1 | 14,036 | 0.036 s | 0 | `break-point`, derived 1651 |
| 801 | 52,436 | 0.052 s | 0 | `break-point`, derived 1651 |
| 3,201 | 167,636 | 0.101 s | 0 | `break-point`, derived 1651 |
| 12,801 | 628,436 | 0.291 s | 0 | `break-point`, derived 1651 |

Linear at ≈0.02 s per 1,000 candidates; the added candidates do not change the derived value,
so the loop is a filter, not a rank key. (The `repairs_to_pin` field in the receipt is `false`
for n>0 only because the *input* carries the extra records, so the output cannot hash to the
undecorated pin; the derivation is identical, `derived_sz_cpr 1651` in every row.)

**C — successor density inside the tampered block's own payload** (the `derive_break` scan
window, `sz_unc` 5,408 → at most ~450 effective records at a 12-byte stride):

| planted | wall | rc | label |
|---|---|---|---|
| 0 | 0.035 s | 0 | `break-point` |
| 50 | 0.106 s | 0 | `break-point` |
| 200 | 0.381 s | 0 | `intact` unchanged (no successor accounts the declared `u_len`) |
| 800 | 0.835 s | 0 | `intact` unchanged |

Superlinear: 50→200 planted is ×3.6 for ×4 density; every surviving successor costs a full
`bytearray(d)` copy plus a `find_sentinel` whose own scan is `range(stop+1, ph_off-12)`, i.e.
O(file) per survivor on top of an O(file) outer scan. At the 256 MiB cap (`MAX_INPUT`, L62)
the same shape costs O(size) per survivor with no internal deadline, so a carrier can occupy
the counter's 600 s per-invocation timeout and fail cells by timing out. The 256 MiB figure
itself is **[INFERENCE]** from the measured slope — I did not run a capped-size stress.

A first cost attempt with a wrong insertion point (decoys placed inside the last block's
payload instead of before the PackHeader) ran 1,448 s before I killed it; that run is recorded
here only as a caution about how sensitive this instrument's cost is to where crafted bytes
land, and is not used as a number.

---

## Findings

**F1 — High, control integrity: `carrier_blind` does not bound provenance.**
Exploit path: a repair reads `<dirname(dirname(argv --in)>)/*/out`, i.e. sibling invocation
boxes, which the sandbox does not hide; the counter's own N3 control leaves the intact packed
bytes there immediately before each carrier's P1 cells. Evidence: `receipts/leak6.json`
(`blind_ok true`, `blinded_recovered 6 / 6`), oracle in `receipts/cheat-sibling-oracle.py`.
Impact: P1 6 of 6 is achievable with zero derivation inside the arm that exists to forbid it;
the declared `cheat_live`/`cheat_killed` pair only proves that *one* cheat shape dies.
Smallest remediation: create `boxes` inside `run_root` and, when blinding, add
`--bind <box> <box>` after the tmpfs so only the current box is visible (two lines in
`score()`/`invoke()`); or state in the receipt that the control establishes path blinding only.

**F2 — Medium: the typed-refusal contract is broken on the output side.**
Six of 22 hostile cases die with a traceback (rc 1), including the tool's own guards against
`..` and a symlinked parent, which can therefore never emit the rc-2 JSON the docstring
promises; one of them (H16) leaves `--out` committed. Exploit path: any consumer that reads
rc 2 as "refused, nothing written" mis-reads rc 1 as a crash. Evidence: table §1,
`receipts/hostile.json`, `receipts/hostile2.json`; anchors L118 (mkstemp outside the try) and
L432/L434 (write_atomic outside the Refused handler). Smallest remediation: move the two
`write_atomic` calls inside the existing `try`, and put `mkstemp` inside `write_atomic`'s
`try`.

**F3 — Medium: blinding is path-pinned and self-announcing.**
186/110/83 unpacked carrier copies are reachable through `--dev-bind / /` under
`/fast/scratch/hyaku/kaidoku-r90`; the decoy content is a literal marker; `mountinfo` names
the decoy and the hidden root; and the whole checkout is writable from inside. Impact: a
repair can detect blinding and switch behaviour, and can source the carrier content without
the pins. Evidence: `receipts/copies-summary.log`, `receipts/bwrap.json` (B2/B5),
`receipts/rwprobe.json`. Smallest remediation: replace the marker decoy with carrier-sized
random bytes, add `--clearenv --setenv`, and record in the receipt that the control blinds
*paths*, not content.

**F4 — Low: `--out`/`--info` collide and mutate partially.**
`--info == --out` returns 0 after destroying the repaired artifact (H17); a failing `--info`
leaves `--out` written and exits 1 (H16). Not reachable from the counter (it passes no
`--info`). Remediation: refuse when the two resolve to the same path, and write both or
neither.

**F5 — Low: write-scope guards are one level short.**
A symlinked ancestor of `--out` is not checked (H8, rc 0 into the resolved directory); a
0444 target is replaced (H19); `--out == --in` overwrites the input (H12); results are always
0600. Remediation: resolve the parent with `os.path.realpath` and re-test containment, refuse
`samefile(dst, src)`, and `os.chmod` the temp to the input's mode before `os.replace`.

**F6 — Informational: no internal cost bound.**
Linear on the l_info axis (0.02 s / 1,000 candidates), superlinear on successor density
(0.835 s at ~450 effective records on a 14 KB file). With the 256 MiB cap the quadratic term
is unbounded in wall time; the counter's 600 s child timeout is the only brake.

## What this does not say

No declared cell, arm or control of R90-C1 is falsified here: the repair derives the correct
value from the successor's position, refuses cleanly on every input-side hostile shape, and
the sandbox really does blind the four pins. What F1–F3 say is that `carrier_blind` proves
less than its name claims, and that the instrument's own refusal and write paths are less
disciplined than its parse path. Nothing in this seat edited the tree; no number above is
quoted from a run I did not execute.

## Receipts (absolute)

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/SentinelScope/receipts/`
— `hostile.json`, `hostile2.json`, `bwrap.json`, `procout.json`, `rwprobe.json`, `leak.json`,
`leak6.json`, `cost.json`, `race.json`, `fx.json`, `instrument-sha256.txt`, the matching
`*.log` transcripts, `copies.log`, `copies-summary.log`, and the drivers
(`hostile.py`, `hostile2.py`, `bwrap_audit.py`, `leak.py`, `leak6.py`, `cheat-sibling-oracle.py`,
`cost.py`, `race.py`, `rwprobe.py`). Hashes of everything: `../receipts-sha256.txt`.
