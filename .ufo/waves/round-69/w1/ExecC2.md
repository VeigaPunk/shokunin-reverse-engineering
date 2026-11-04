# ExecC2 — R69-C2 attack report (round 69, wave w1)

Seat: executor, attack lane. Claim attacked: **R69-C2** (operability: typed exit-2 contract,
enforced UPX pin, per-carrier format/mode records). Method: an **independent harness**
(`attack.py`, `rederive.py` in this directory) — I did **not** run
`tools/round-69/contract-probe.py`, per the seat spec. Instrument under test:
`tools/round-69/packed-elf.py`, sha256 `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`,
on disk and at `git show f1599810:…` (identical). Revision used:
`f15998102f1ce3569e61faa2ac6f286bc414538e`. `git diff <freeze> HEAD -- tools/` is empty; no
post-freeze instrument edit (observation).

## Verification summary

Probe arm expressions below are read from `contract-probe.py` (lines 197–212 for A1–A4,
`arms_from_receipt` 100–156 for A5/A6). My observation is from my own fixtures and my own
re-derivation (`rederive.md`, `arm-receipt.json`, `rederive.json`).

| arm | probe's own predicate (read) | my observation | both sides |
|---|---|---|---|
| A1_missing_node | rc 2 and `"node"` in `unevaluable` | rc 2, `missing_tool: node`, JSON envelope, no traceback | after **true**; base **false** (rc 1 `FileNotFoundError: 'node'` traceback) |
| A2_work_unusable | rc 2 and `"work"` in `unevaluable` | rc 2, `work_unusable: not writable (…: PermissionError)` | after **true**; base **false** (rc 1 `PermissionError` traceback) |
| A3_packer_version | rc 2, `"packer"` and `"version"` in `unevaluable` | rc 2, `packer_mismatch: version 'upx 5.1.0' != pin 'upx 5.2.0'` | after **true**; base **false** (argparse: `unrecognized arguments: --upx …`; no seam) |
| A4_packer_sha256 | rc 2, `"packer"` and `"sha256"` in `unevaluable` | rc 2, `packer_mismatch: sha256 6ad600e7…0801 != pin cf2f6e7c…c969` | after **true**; base **false** (argparse: `unrecognized arguments: --upx …`) |
| A5_carrier_record | every carrier names `name/format/packing_mode/pin/source/runs`; `format` = checker's own `readelf -h` of `source`; `pin` = checker's sha256 of `source`; `packing_mode` = `upx --best` and `--best` in pack argv; `ok` and all arms true | all three carriers clean under my own parser and sha256; libz format `DYN (Shared object file)` | after **true**; base **false** (r68 receipt: `jq/xxd` miss `name/format/packing_mode`) |
| A6_packer_pin | `packer.{version_pin,sha256_pin,pin_enforced,sha256,version}` present; `pin_enforced` true; sha/version equal the host packer | present and equal: `cf2f6e7c…c969` / `upx 5.2.0`, `pin_enforced: true` | after **true**; base **false** (r68 receipt: three keys absent, sha/version pin `None`) |

After side: `arms_passed 6 of 6` (my re-derivation of the probe's own expressions; I did not execute
the probe). Before side: **0 of 6, all six named**. My independent before-arm reproduces the
committed `.ufo/waves/round-69/l1/pre/c2-at-base.json` shape exactly (same tracebacks for A1/A2, same
`unrecognized arguments: --upx` for A3/A4, same two A5 failures and six A6 failures).

The A3/A4 arms are independently load-bearing, not one arm measured twice: fixture (d) is a real ELF
that **passes** the version check and is refused only on bytes; fixture (e) is a script that prints
the exact pin and is refused only on bytes. Fixture (c) changes the version alone.

A2 also carries the exception class in the detail (`…: PermissionError`), so the typed message is
diagnostic, not just a classification.

## Findings (outside the six named arms — none of these falsifies the frozen predicate)

### F1 — contract leak: an executable packer of invalid format escapes as a traceback (observation)

`--upx <file with exec bit and no valid exec format>` (`upx-enoexec`: 21 bytes of garbage, mode 0755)
passes `os.path.isfile` + `os.access(X_OK)` and then `subprocess.run` raises
`OSError: [Errno 8] Exec format error` at `packed-elf.py:253` (`run([upx, "--version"])`); `run()`
(line 186) has no error handling and `main` catches only `Unevaluable`, so the caller sees a
**traceback and rc 1**, never the exit-2 envelope. Raw: `runs/U1_enoexec.stderr` (`arm-receipt.json`
id `U1_enoexec`, rc 1, kind `leak`).

This contradicts the module docstring ("could-not-evaluate (missing node/git/readelf/upx, …)") and
`preflight`'s own docstring ("A refused route must be a named class, never a crash"). It is the same
*shape* as the base defect M68-8/ADV-3 the round claims to repair, moved one step along: a packer
that exists but cannot be spawned still crashes instead of refusing. Severity: medium — a caller that
branches on rc 2 treats this as a generic failure with no class; it is also a way to make the route
exit 1 (a scoreable "not met") from an environment fault.

### F2 — contract leak: an executable-but-unreadable packer escapes as a traceback (observation)

`--upx` a byte-identical copy of the pinned packer with mode `0111` passes `os.access(X_OK)`; the
version pin holds (`upx 5.2.0`), then `sha256_file(upx)` at line 257 raises
`PermissionError: [Errno 13] Permission denied` (line 118), uncaught → traceback, rc 1. Raw:
`runs/U2_unreadable.stderr`. The admission test never asks `os.access(R_OK)` though the very next
step reads the file. Same severity and same class as F1.

### F3 — contract leak: the tool checks are `which`-only, so a present-but-unrunnable tool crashes (observation + one inference)

A `node` on PATH whose shebang names a missing interpreter is found by `shutil.which` (so preflight
passes) and then `run([node, "--version"])` raises
`FileNotFoundError: [Errno 2] No such file or directory: '<path>/node'` at line 354 → traceback,
rc 1. Raw: `runs/U11_node_badshebang.stderr`, `extra-probes.json`. The same construction applies to
`git` and `readelf` (their `run()`/`git()` calls are equally unguarded; `git()` catches only
`CalledProcessError`, not `OSError`) — **inference**, not separately run.

**Inference (untested):** `subprocess.TimeoutExpired` from the 900 s bound in `run()` is likewise
uncaught, so a packer whose `--version` hangs for 900 s would end as a traceback with rc 1, not an
exit-2 class. I did not wait 900 s to observe it.

So the exit-2 contract is total for *absent* prerequisites and for *pin mismatches*, and partial for
*present-but-broken* ones. A1–A6 cannot see this because none of them builds a broken-but-present
tool.

### F4 — the `--upx` seam is checked, never used: work always runs the module constant (observation + inference)

`score()` packs, lists and decompresses with the **module constant** `UPX = "/usr/bin/upx"`
(lines 387 pack, 391 list, 397 unpack, 411/412 control list/decompress); only `preflight()` consumes
the `--upx` value. Empirically: a
byte-identical copy at another path is accepted (`receipts/c3-seam.json`, rc 0, `met true`) and the
receipt records `packer.upx = /…/fixtures/upx-pinned-copy`, while **all three** pack argvs are
`["/usr/bin/upx", "--best", …]`. `rederive.json` label `self-route-run-at-freeze` has
`seam_equals_used: true`; label `seam-run-pinned-copy` has it false, and that run still reports
`met true` with `failing []` — the seam value is nowhere load-bearing. (That receipt's `packer.upx`
names my scratch path, which is deleted before yield; the evidence is its recorded `pack.argv`, not
the path.)

Verdict on this shape: **the contract holds for any accepted run**, because the pin is the host
packer's sha256 — a seam value that passes preflight is byte-identical to the constant, so check-time
and use-time bytes coincide. What is *not* enforced is path identity: the receipt's `packer.upx` can
name a file that never executed. Residual gap (**inference**): if `/usr/bin/upx` were replaced
between preflight and the pack calls, the receipt would still record the pre-change pin (TOCTOU);
nothing in the receipt or the probe closes that window.

### F5 — A5/A6 are receipt-shape checks with no binding to the instrument or the revision (observation)

The probe reads the caller's `--receipt` and re-derives fields from the pinned sources; it never asks
whether that receipt was produced by the instrument it just wrote from `git show <rev>:<tool>`, nor
at which revision. Demonstration: I took the committed round-68 landing receipt, added **only** the
three record fields per carrier (`name`, `format` from my own `readelf`, `packing_mode`) and the
three packer keys (`version_pin`, `sha256_pin`, `pin_enforced: true`) — everything else untouched,
including its round-68 provenance — and it passes **A5 and A6** under the probe's own rules
(`forged-r68.json`; `rederive.json` label `forged-r68-retrofit`). It still fails the C3 clauses
(target 2, no shared-object), but R69-C2's counter does not look at those.

Consequence: the predicate's phrase "the measured run's receipt" is a **provenance premise the
counter cannot check**. The honest receipt passes (I ran the route myself, rc 0) and so does a
retrofitted one. This does not falsify R69-C2 as frozen — the kill rule only requires that pins,
formats and modes *equal the probe's derivation*, which a retrofitted receipt satisfies by
construction — but the arm is not attack-resistant to a receipt-producing adversary. Recommend the
L1 cite the receipt's own `instrument.sha256` and `rev` in the LOG entry, and prefer the receipt from
the same run that produced the C3 landing evidence.

### F6 — the exit-2 class vocabulary is inconsistent and one documented class is unimplemented (observation)

Observed prefixes: `missing_tool:`, `work_unusable:`, `packer_mismatch:` — but the `--root` failure
emits `"unevaluable": "git log -1 --format=%H -- tools/round-69/packed-elf.py failed: rc=128"`, a
free-form sentence with no class token (my harness had to treat the whole clause as the class). The
REA package errors (`REA package root unreadable`, `REA package.json pin drift`, `REA version
drift`) are likewise unclassified prose. A consumer cannot key on a stable class for these.

Separately, the module docstring lists "**unknown revision**" among the exit-2 classes, but no code
validates `--rev`: `--rev deadbeef… --skip-run` is accepted and the receipt records
`"rev": "deadbeef…"` with rc 1 (the `--skip-run` verdict), never a typed refusal
(`runs/U9_bogus_rev.stdout`). The promise exceeds the implementation. For this round it is inert —
the L1 passes a real revision — but the docstring overclaims the contract.

### F7 — the probe records the instrument hash but never enforces the frozen pin (observation)

`grep -c 4ac0d83… tools/round-69/contract-probe.py` = 0: `check()` writes the tool from
`git show <rev>:<tool>`, hashes it into `instrument_sha256`, and runs it — no comparison to the
frozen pin anywhere. A drifted instrument at the measured revision would be executed and could still
report `arms_passed 6`; the kill rule's "post-freeze instrument edit → not verified" clause is
therefore **manual**, not counter-enforced. Today the pin holds (disk = `git show f1599810:…` =
`4ac0d83…`; `git diff <freeze> HEAD -- tools/` empty), so nothing is wrong with this round's
evidence — only with what the counter would catch by itself.

### F8 — minor: `pre/c3-at-base.json` is a console transcript, not a JSON document (observation)

It begins with a `+ /usr/bin/python3 -I -B tools/round-69/packed-elf.py --check-receipt …` shell
line before the JSON object, so uniform JSON readers fail on it (`rederive.py` raised
`JSONDecodeError: Expecting value: line 1 column 1`). It is a *pre* control artifact and no C2 clause
reads it; noted only because the round's receipts are otherwise machine-shaped.

## Predicate verdict (as frozen)

I attack R69-C2 as written and do not narrow, widen or re-freeze it.

- **All six after-side arms are true** on my independent re-derivation against the pinned instrument
  bytes at the freeze, with a receipt the instrument itself produced in a green three-carrier run
  (`receipts/c3-self.json`, rc 0, `met_target true`, `failing []`). A1–A4 reproduce exactly the
  fixtures the probe builds; A5/A6 pass under my own `readelf`-based re-derivation.
- **The before side is 0 of 6 with all six arms named**, re-derived independently against
  `tools/round-68/packed-elf.py` (base bytes `48ef4c68…`) and its committed landing receipt.
- **No kill-rule clause fires on the honest evidence**: every arm true; carrier pins/formats/modes
  equal my derivation from the pinned source bytes; the packer pin is enforced and equal to the host
  packer; the before arm shows 0/6 naming all six; no post-freeze instrument edit.
- **Residual, unexercised by me by assignment**: the L1's own `contract-probe.py` invocation at the
  measured (landing) revision, with the receipt from that landing's run. The measured revision does
  not exist yet — `.ufo/waves/round-69/l1/scores/` was empty for the whole seat.

Verdict I can defend: **R69-C2's predicate is satisfied by every arm I can independently reach, and
its before clause is observed; the claim stands as written.** F1–F3 are real exit-2 leaks that A1–A6
do not cover; F4–F7 bound what the counter proves. None of them is a predicate falsifier, and none is
a reason to alter the claim.

## What the L1 must run (not run here)

1. `python3 -I -B tools/round-69/contract-probe.py --root . --rev <landing> --tool tools/round-69/packed-elf.py --pkg <REA 6.5.0> --work <scratch> --receipt <landing run receipt> --json-out .ufo/waves/round-69/l1/scores/c2-at-landing.json` — expect rc 0, `arms_passed 6`, `target 6`, `failed []`.
2. The same probe with `--tool tools/round-68/packed-elf.py --rev d7d9a62cc70935304e600ed0dee864fc4f1751f7 --receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json` — expect `arms_passed 0`, `failed` naming all six.
3. `sha256sum tools/round-69/packed-elf.py` at landing = `4ac0d83…` (the probe does not check this — F7).

## Evidence in this directory

- `rederive.md` — arm-by-arm re-derivation, fixtures, numbers, verdict.
- `attack.py` (sha256 `5d685644…b45af`), `rederive.py` (`e1610cd…fe1d`) — the harness, verbatim.
- `arm-receipt.json` (`9a99b39f…be5bb`) — 19 arms with rc, kind, class, stderr/stdout paths. Its
  `stderr_file` fields name the scratch paths that are deleted before yield; every one of those
  basenames lives under `runs/` here.
- `rederive.json` — A5/A6/C3-clause results for my receipt, the `--upx` seam run, the round-68
  receipt as-is, and the retrofitted receipt.
- `receipts/c3-self.json` (`fa7e07e5…7fb49`) — the frozen instrument's three-carrier receipt from my
  own run at `f1599810…`; `receipts/c3-seam.json` (`3143a32f…54a9e`) — the `--upx` seam run.
- `forged-r68.json` (`ce1bfbee…7eb50`) — F5's retrofitted receipt.
- `extra-probes.json` — the U11 broken-`node` probe (rc, site, fixture hash, raw stderr).
- `runs/` — raw stderr for every arm, plus the two `--skip-run` stdout payloads.

## Scope and hygiene

- Wrote only `.ufo/waves/round-69/w1/ExecC2/` and scratch `/fast/scratch/hyaku/kaidoku-r69/ExecC2/`.
  No tracked lane file, no other lane, no git index, no commit, no push, no mutating `jj`.
- No tool installs; no pacman transaction. Host packer read only (`--version`, `sha256sum`).
- Scratch deleted before yield; receipts copied here first.
