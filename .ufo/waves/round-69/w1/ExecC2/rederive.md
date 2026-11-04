# ExecC2 — R69-C2 re-derivation with an independent harness

Seat ExecC2, round 69, wave w1. Attack of R69-C2 (queue C2, aa `operability`).
**I did not run `tools/round-69/contract-probe.py`**, per the seat spec. Everything below
comes from `attack.py` (my own fixture builder + invoker) and `rederive.py` (my own A5/A6
re-derivation with my own `readelf -h` parser and my own sha256), both retained in this
directory.

- Instrument: `tools/round-69/packed-elf.py` = `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`
  (on disk and at `git show f1599810:…` — identical).
- Revision used: `f15998102f1ce3569e61faa2ac6f286bc414538e` (operative freeze).
- `git diff f15998102f1ce3569e61faa2ac6f286bc414538e HEAD -- tools/` is **empty**; worktree clean for
  `tools/`. No post-freeze instrument edit observed.
- Route receipt used for the A5/A6/eceipt clauses: my own three-carrier run,
  `receipts/c3-self.json` (sha256 `fa7e07e598205ecd5ded8f753858ccde304d1d44abd983c768219dd52417fb49`),
  rc 0, 72.7 s, `--rev f15998…`.
- Host packer: `/usr/bin/upx` = `upx 5.2.0`, sha256 `cf2f6e7c…c969` (= both pins).

Invocation template (every arm; only `PATH`, `--work`, `--pkg`, the tool path and the
trailing extras vary):

```sh
env PATH=<pathbin|ambient> HOME=$HOME LANG=C TMPDIR=<scratch>/work \
  /usr/bin/python3 -I -B <tool> \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev  f15998102f1ce3569e61faa2ac6f286bc414538e \
  --pkg  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <work> [extras]
```

`<tool>` is `…/tools/round-69/packed-elf.py` unless the row says round-68. Full raw stderr for every
row is in `runs/<id>.stderr`; machine rows in `arm-receipt.json` (sha256 `9a99b39f…be5bb`).

## Fixtures (built by `attack.py`, per the seat spec)

| id | shape |
|---|---|
| a | `pathbin_no_node` — dir with symlinks to `git`, `readelf`, `upx` **and nothing else**; PATH is set to it |
| b | `ro0500` — existing directory `chmod 0500` |
| c | `upx-5.1.0` — `#!/bin/sh` printing `upx 5.1.0` on `--version`, else exit 3 |
| d | `upx-bumped` — byte-copy of `/usr/bin/upx` plus one appended `\0`, mode 0755 (prints `upx 5.2.0`) |
| e | `upx-5.2.0` — `#!/bin/sh` printing `upx 5.2.0`, a different bytes shape than (d) |

Unnamed shapes I added: `upx-enoexec` (exec bit, no valid exec format), `upx-unreadable`
(byte-identical packer, mode 0111), `upx-dir` (a directory), `pathbin_node_nonexec`,
`pathbin_node_broken` (broken symlink), `pathbin_node_badshebang` (`#!` → missing interpreter),
`upx-pinned-copy` (byte-identical copy used as a *passing* seam value), a bogus `--rev`, a
missing `--root`, a missing `--pkg`, a missing `--work`.

## Arms — command, rc, class

| arm | PATH | extras (beyond template) | rc | ruling | class (`unevaluable` prefix) |
|---|---|---|---|---|---|
| `A1_missing_node` | `pathbin_no_node` | — | 2 | **typed** | `missing_tool: node` |
| `A2_work_unusable` | ambient | `--work fixtures/ro0500` | 2 | **typed** | `work_unusable: not writable (…: PermissionError)` |
| `A3_packer_version` | ambient | `--upx …/upx-5.1.0` | 2 | **typed** | `packer_mismatch: version 'upx 5.1.0' != pin 'upx 5.2.0'` |
| `A4_packer_sha256` | ambient | `--upx …/upx-bumped` | 2 | **typed** | `packer_mismatch: sha256 6ad600e7…0801 != pin cf2f6e7c…c969` |
| e (spec) `A5_packer_sha256_script` | ambient | `--upx …/upx-5.2.0` | 2 | **typed** | `packer_mismatch: sha256 3ccde35c…6185 != pin …` |
| `U1_enoexec` | ambient | `--upx …/upx-enoexec` | 1 | **LEAK** | — (`OSError: [Errno 8] Exec format error`, line 253) |
| `U2_unreadable` | ambient | `--upx …/upx-unreadable` | 1 | **LEAK** | — (`PermissionError: [Errno 13]`, line 257 → 118) |
| `U3_upx_is_dir` | ambient | `--upx …/upx-dir` | 2 | typed | `missing_tool: upx (…)` |
| `U4_node_nonexec` | `pathbin_node_nonexec` | — | 2 | typed | `missing_tool: node` |
| `U5_node_broken` | `pathbin_node_broken` | — | 2 | typed | `missing_tool: node` |
| `U6_pkg_absent` | ambient | `--pkg …/upx-dir` | 2 | typed | `missing_tool: rea package (…)` |
| `U7_work_absent` | ambient | `--work <absent path>` | 2 | typed | `work_unusable: not a directory (…)` |
| `U8_root_absent` | ambient | `--root /nonexistent-lane --skip-run` | 2 | typed | `git log -1 --format=%H -- tools/round-69/packed-elf.py failed: rc=128` (free-form, no class token) |
| `U9_bogus_rev` | ambient | `--rev deadbeef… --skip-run` | 1 | **accepted, unvalidated** | — (receipt records `"rev": "deadbeef…"`) |
| `U10_seam_identical` | ambient | `--upx …/upx-pinned-copy --skip-run` | 1 | accepted (pin holds) | — |
| `U11_node_badshebang` | `pathbin_node_badshebang` | — | 1 | **LEAK** | — (`FileNotFoundError: …/node`, line 354 → 186) |
| `B1_missing_node` (r68) | `pathbin_no_node` | — | 1 | **LEAK** | — `FileNotFoundError: … 'node'` |
| `B2_work_unusable` (r68) | ambient | `--work fixtures/ro0500` | 1 | **LEAK** | — `PermissionError: … packed-…` |
| `B3_packer_version` (r68) | ambient | `--upx …/upx-5.1.0` | 2 | no contract | — `argparse: unrecognized arguments: --upx …` |
| `B4_packer_sha256` (r68) | ambient | `--upx …/upx-bumped` | 2 | no contract | — `argparse: unrecognized arguments: --upx …` |

Rows B1–B4 are the same four fixtures against `tools/round-68/packed-elf.py` (base bytes,
`48ef4c68…`). B1/B2 reproduce exactly the two traceback shapes the frozen `c2-at-base.json`
records (rc 1, `FileNotFoundError: 'node'`; `PermissionError: …/packed-…`). B3/B4 reproduce its
`unrecognized arguments: --upx` shape: the base instrument has no seam at all, so A3/A4 cannot
even be attempted there.

### What the five spec fixtures establish (observation)

(a) → `missing_tool: node`; (b) → `work_unusable: not writable (…: PermissionError)`;
(c) → `packer_mismatch: version`; (d) → `packer_mismatch: sha256`; (e) → `packer_mismatch: sha256`
(version pin holds, byte pin refuses it — the two arms are independently load-bearing: (d) is an ELF
that *passes* the version arm and fails only on bytes; (e) is a script that prints the exact pin and
is refused only on bytes). The message is a single-line JSON envelope on **stderr**
(`{"schema": "kaidoku-r69-packed-elf-v1", "unevaluable": "<class>: <detail>", "claim": "R69"}`),
absent from stdout.

## A5/A6 re-derivation over the route receipt

My checker (`rederive.py`) re-derives, from the receipt's own fields and the **pinned source bytes**:

- `format` — my own `readelf -h` parser on `carrier.source` (separate code path from the
  instrument's `elf_format`), compared field-wise;
- `pin` — my own sha256 of `carrier.source`;
- `packing_mode` — `upx --best` and `--best` present in `carrier.runs.pack.argv`, pack rc 0;
- `name/format/packing_mode/pin/source/runs` all non-empty; `ok` true, no false arm;
- A6 — `packer.{version_pin,sha256_pin,pin_enforced,sha256,version}` present, `pin_enforced` true,
  sha and version equal to the **host** `/usr/bin/upx` as I measure it.

Result on `receipts/c3-self.json`: **A5 true, A6 true** (`rederive.json`, label
`self-route-run-at-freeze`). The same rules over `receipts/c3-seam.json` (the run with
`--upx <byte-identical copy>`) also give **A5 true, A6 true** with `met true`, while its
`packer.upx` names the copy and its pack argvs name `/usr/bin/upx` — see F4 in `ExecC2.md`.
Observed values:

| carrier | kind | source sha256 | format (mine = receipt's) | packing_mode / pack argv | ratio |
|---|---|---|---|---|---|
| jq | executable | `e8156675…7806` | ELF64 / 2's complement, little endian / DYN (Position-Independent Executable file) / Advanced Micro Devices X86-64 | `upx --best`; argv `["/usr/bin/upx","--best","-q","-o",…]` rc 0 | 0.0599 (10/167) |
| xxd | executable | `7b1e5d0c…ae65` | same as jq | same | 0.1010 (10/99) |
| libz | shared-object | `6c78c5e5…5ca9` | ELF64 / 2's complement, little endian / **DYN (Shared object file)** / AMD X86-64 | same | 0.6522 (120/184) |

Recorded `before_ceiling_ratio` equals `ceiling/orig_procedures` to 4 dp on all three carriers
(0.0599, 0.101, 0.6522); every ratio ≤ 0.75; `packed_counts.procedure_count` (3, 3, 98) is at or
below its declared ceiling (10, 10, 120). `target 3`, `carriers_matched 3`, `control_ok true`,
`failing []`, `met_target true`.

`packer.upx` = `/usr/bin/upx` and all three pack argvs start with `/usr/bin/upx` — the seam value and
the executed packer coincide in this run (see F4 for the shape where they do not).

## Before arm — the same rules over the round-68 evidence

| arm | observation | verdict |
|---|---|---|
| A1 | `B1` rc 1, `FileNotFoundError: … 'node'` traceback; no envelope | false |
| A2 | `B2` rc 1, `PermissionError: … packed-…` traceback; no envelope | false |
| A3 | `B3` rc 2 from argparse (`unrecognized arguments: --upx`), no envelope; no `--upx` seam exists | false |
| A4 | `B4` same argparse rejection | false |
| A5 | over the committed `.ufo/waves/round-68/l1/scores/c2-at-landing.json`: carriers carry no `name`, `format`, `packing_mode` (2 named failures) | false |
| A6 | same receipt: `packer.version_pin`, `sha256_pin`, `pin_enforced` absent (6 named failures) | false |

So the before side is **0 of 6, all six arms named** on my own re-derivation — the same six names
and the same failure shapes as the committed `pre/c2-at-base.json`.

## Verdict on the frozen predicate

The predicate, verbatim from the declaration, is a six-arm conjunction after the round and its
negation at the base. What I can honestly say:

1. **Observation.** Each of the six after-side arms is true on my own fixtures and my own
   re-derivation, against the instrument whose sha256 is the frozen pin, at the operative freeze:
   A1 `missing_tool: node` rc 2; A2 `work_unusable` rc 2; A3 `packer_mismatch: version` rc 2;
   A4 `packer_mismatch: sha256` rc 2; A5 true; A6 true.
2. **Observation.** The before side is 0 of 6 with all six arms named (B1–B4 + the two receipt arms).
3. **Inference (labelled).** Because I implemented the probe's six arm predicates from its source
   rather than executing it, `arms_passed 6` / `0` are my re-derivations of its result, not its
   output. The seat assignment forbids running it.
4. **Unknown (the residual).** The predicate names "the measured run's receipt" and "the measured
   revision"; the measured revision is the landing commit, which does not exist at this writing
   (`l1/scores/` was empty throughout). My receipt is the frozen instrument's honest output at the
   freeze. Reading the predicate as written — six arms true, all named, with the measured run's
   receipt — the sentence is **satisfiable and every clause I can reach holds**; the L1's own probe
   invocation at the landing revision is the only unexercised step.

No clause of R69-C2's kill rule fires on the honest evidence: no arm false, pins/formats/modes equal
my derivation from the pinned source bytes, the pin is enforced and equal to the host packer, the
before arm shows 0/6 naming all six, and no post-freeze instrument edit exists. The gaps I did find
(F1–F8 in `ExecC2.md`) are **outside the six named arms**: they are contract-shape leaks and
evidentiary boundaries, not predicate falsifiers. They are reported, not used to narrow the claim.
