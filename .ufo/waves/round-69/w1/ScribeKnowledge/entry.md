# Round 69 — the packed-ELF route's contract: a falsifiable arm seam, a typed exit-2 preflight, and a pinned packed shared object

source: S270 — UPX 5.2.0 packer source at tag `v5.2.0`, `src/help.cpp`
(https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp; 27,279 B, sha256
`0b893ca8299c061a8e1961ddbc1fa85cd8d77f3f043cba9a478a697e5d363c79`) and `src/main.cpp`
(https://raw.githubusercontent.com/upx/upx/v5.2.0/src/main.cpp; 41,889 B, sha256
`a02c7cba2939708e2af4c25119fe20a5a7594b7225b189848196280b03dea82c`). Anchors: `help.cpp:460`
`void show_version(bool one_line) {`; `help.cpp:465` `fprintf(f, "upx %s\n", UPX_VERSION_GIT_DESCRIBE);`;
`help.cpp:467` the `UPX_VERSION_STRING "-git-" UPX_VERSION_GITREV` variant; `help.cpp:469`
`fprintf(f, "upx %s\n", UPX_VERSION_STRING);`; `main.cpp:834` `{"version", 0, N, 'V' + 256},  //
display version number`; `main.cpp:1174` `if (strcmp(argv[i], "--version") == 0)`. The first stdout line
of `upx --version` is this banner, and the route pins exactly that string (observed on this host:
`upx 5.2.0`). The same tag's generated manual page renders the flag at `doc/upx.1:164`
(`\&\fB\-\-version\fR: print the version of \fBUPX\fR`) as a secondary locator; its internal-checksum
sentence at lines 112-114 is about the compressed and uncompressed *files*, not the packer binary. The
packer-binary sha256 pin is route policy (`tools/round-69/packed-elf.py:64-65, 257-259`), not a source
claim. S269's own scope (byte identity after decompression) is unchanged and is cited in Limits, not
as evidence for the pin.
verified-at: 2026-11-03 at the landing revision `5ee94c56ce7490938ee38c2e5c10930a1fd1330a` — under
`.ufo/waves/round-69/l1/scores/`: `c1-at-landing.json` (`survivors []`, five kills each naming its
declared case, `pristine.cases 20`), `c1-before-recheck.json` (five survivors, `pristine.cases 13`),
`c2-at-landing.json` (`arms_passed 6`, `failed []`, instrument sha256 `4ac0d83b…`, scored receipt
`c3-at-landing.json`), `c3-at-landing.json` (`target 3`, `carriers_matched 3`, `control_ok true`,
`met_target true`, `failing []`) and `c3-check-at-landing.json` (`met true`, `kinds ["executable",
"shared-object"]`). Frozen instruments `4ac0d83b…`/`51b64c56…`/`e609d85d…`/`1f8f78c1…`; base receipts
`.ufo/waves/round-69/l1/pre/{c1,c2,c3}-at-base.json`; seat receipts
`.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json`,
`.ufo/waves/round-69/w1/ReviewerGates/attacks.json` (`battery-r69`/`battery-r68`), and
`.ufo/waves/round-69/w1/ScribeKnowledge/contract-probe-exec3.json`.
recheck: `sha256sum tools/round-69/packed-elf.py tools/round-69/mutation-check.py
tools/round-69/contract-probe.py tools/round-69/controls.py` (expect the four pins above, and
`48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` for
`tools/round-68/packed-elf.py`); `python3 -I -B tools/round-69/packed-elf.py --selftest` → exit 0 with
`cases 20`, `failed []`; `python3 -I -B tools/round-69/mutation-check.py --root <LANE> --rev <REV>
--tool tools/round-69/packed-elf.py --patch-set r69 --work <SCRATCH> --json-out <OUT>` → exit 0 with
`survivors []` and `pristine.cases 20`; the same battery with `--tool tools/round-68/packed-elf.py
--patch-set r68 --rev d7d9a62cc70935304e600ed0dee864fc4f1751f7` → the five survivors and
`pristine.cases 13`; `python3 -I -B tools/round-69/contract-probe.py --root <LANE> --rev <REV> --tool
tools/round-69/packed-elf.py --pkg <REA 6.5.0 root> --work <SCRATCH> --receipt <THREE-CARRIER
RECEIPT> --json-out <OUT>` → exit 0 with `arms_passed 6`; `python3 -I -B
tools/round-69/packed-elf.py --check-receipt <THREE-CARRIER RECEIPT>` → exit 0 with `met true`.
Source recheck: `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp -o help.cpp
&& sha256sum help.cpp` (expect `0b893ca8…`; `void show_version` at line 460, banner at 465/467/469), the
same fetch for `src/main.cpp` (`a02c7cba…`; `{"version", 0, N, 'V' + 256}` at line 834, `--version`
at line 1174), and `doc/upx.1` (`09552b3c…`; `--version` at line 164). All carriers are host binaries
pinned by sha256 and are never committed.
status: R69-C1, R69-C2 and R69-C3 — the round-69 route is Core for the gate properties and the three
carriers below iff the frozen counters at the measured revision report `survivors []` with all five
mutants killed, each kill's `failed` list naming its declared arm-false case, and `pristine.cases 20`
with `pristine.ok true` (base: the same battery over `tools/round-68/packed-elf.py` at
`d7d9a62cc70935304e600ed0dee864fc4f1751f7` with patch set `r68` reports the five survivors
`M1_identity`, `M2_recovery`, `M3_detected`, `M4_before`, `M5_control` and `pristine.cases 13`); the
contract probe reports `arms_passed 6` of `target 6` — `A1_missing_node`, `A2_work_unusable`,
`A3_packer_version`, `A4_packer_sha256`, `A5_carrier_record`, `A6_packer_pin` each true (base: 0 of 6
with all six named); and the receipt checker reports `met true` with `target 3`, `carriers_matched 3`,
`control_ok true`, `failing []`, every `before_ceiling_ratio` at or below `0.75`, and one carrier of
`kind` `shared-object` (base: `target 2` and no shared-object carrier). A false clause, a post-freeze
instrument edit, or a receipt whose carrier pins/formats/modes do not equal the probe's own derivation
replaces this line and the PROVINCE row with the honest stop; the miss is reported, never narrowed. At
the landing revision `5ee94c56…` the five receipts above report exactly these values
(`.ufo/waves/round-69/l1/scores/`).

## The gate, not the route's scope

[observation] At the base `d7d9a62cc70935304e600ed0dee864fc4f1751f7` the round-69 instrument does not
exist (`git cat-file -e d7d9a62c:tools/round-69/packed-elf.py` exits 128, `exists on disk, but not in
…`), and the round-68 route's selftest has 13 cases, none of which calls the gate code — that code
lives inline in `score()`, outside the helper functions `--selftest` exercises — so each of the five
2026-11-03 mutants runs green at 13 cases with `failed []`
(`.ufo/waves/round-69/l1/pre/c1-at-base.json`). The round-69 instrument first lands at `616a5f2f`, the
claims container at `f1599810`, and the freeze-integrity record shows the four frozen bytes equal to
their pins with an empty `freeze_to_main_diff` for `tools/`
(`.ufo/waves/round-69/w1/ReviewerGates/freeze-integrity.json`; the pins are also `claims.json`
`instrument_pins`).

The route's scope is unchanged: detect a UPX-packed ELF, unpack it with sha256 identity, recover the
original's REA inventory. Round 69 moves the **gate** — which is what decides whether the route's five
arms are measurable at all — and one carrier class. It adds no REA reader key: the route is still a
pre-step that restores bytes outside REA and hands the restored file to `rea analyze`.

[inference] A gate whose own selftest cannot feed its arm expressions a false input is decorative: a
mutation that turns an arm's condition into a constant leaves every selftest case green, which is
exactly what the five round-68 mutants did. The round-69 seam makes each arm's expression a function of
an in-memory model, so a false model per arm is expressible without upx, REA or a carrier.

## The arm seam and the five mutations it kills

`evaluate_carrier(model)` (`tools/round-69/packed-elf.py:155-174`) computes every arm from a plain
model and performs no I/O. `score()` builds that model from the measured carrier and calls the same
function; `--selftest` builds `_model()` — a green carrier — and then one false model per arm
(`:463-543`). `REGISTERED_CASES` (`:88-109`) lists 20 case names, and the last case,
`case-inventory`, fails if the list of cases actually executed differs from it, so deleting a case is
itself a red selftest.

The battery's five patches (`tools/round-69/mutation-check.py:57-70`) are behavioural: each replaces one
arm's expression in the seam with a constant-true form. The base set (`:43-51`) patches the same five
arms where they were computed inline inside `score()` in the round-68 instrument.

| mutant | base site, patch set `r68` (old → new) | round-69 site, patch set `r69` (old → new) | declared arm-false case (the false model it feeds) | base at `d7d9a62c` | round-69 |
|---|---|---|---|---|---|
| `M1_identity` | `and sha256_file(unpacked) == c["sha256"])` → `and True)` | `identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]` → `identity_ok = True` | `arm-pack-identity-false`: `unpacked_sha256 "bb…"` against pin `"aa…"` | survived, 13 cases, `failed []` | killed, 20 cases, `failed ["arm-pack-identity-false"]` |
| `M2_recovery` | `and rec_counts == orig_counts` → `and rec_counts == rec_counts` | `recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]` → `recovery_ok = bool(model["recovered_counts"])` | `arm-pack-recovery-false`: recovered `166/30/190` against original `167/30/190` | survived, 13 cases, `failed []` | killed, 20 cases, `failed ["arm-pack-recovery-false"]` |
| `M3_detected` | `detected = listing["rc"] == 0 and secs == 0` → `detected = listing["rc"] == 0 and True` | `detected = model["upx_list_rc"] == 0 and model["section_count"] == 0` → `detected = model["upx_list_rc"] == 0` | `arm-pack-detected-false`: `section_count 2` with `upx_list_rc 0` | survived, 13 cases, `failed []` | killed, 20 cases, `failed ["arm-pack-detected-false"]` |
| `M4_before` | `and before_procedures < floor` → `and before_procedures == before_procedures` | `before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]` → `before_ok = model["packed_procedures"] is not None` | `arm-pack-before-false`: packed `150` procedures against ceiling `10` | survived, 13 cases, `failed []` | killed, 20 cases, `failed ["arm-pack-before-false"]` |
| `M5_control` | the `all(control["list_rc"] != 0 and control["decompress_rc"] != 0 …)` fold → `fold(carriers, True, len(CARRIERS))` | `control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0` → `control_ok = True` | `arm-pack-control-false`: `control_list_rc 0` | survived, 13 cases, `failed []` | killed, 20 cases, `failed ["arm-pack-control-false"]` |

The battery also refuses a patch site that matches zero or several times and a kill that fails a case
other than the declared one (`killed_wrong_case []`). Measured at the freeze `f1599810`
(`.ufo/waves/round-69/w1/ReviewerGates/attacks.json`, keys `battery-r69` and `battery-r68`):
round-69 patch set → exit 0, `survivors []`, `killed` all five, each `failed` list exactly its declared
case and nothing else, `pristine {cases 20, failed [], ok true, rc 0}`; base patch set at `d7d9a62c` →
exit 0, the five survivors, `pristine.cases 13`. The base receipt is
`.ufo/waves/round-69/l1/pre/c1-at-base.json`; at the landing revision `5ee94c56…` the same battery
reports `survivors []` with the same five kills and `pristine.cases 20`
(`.ufo/waves/round-69/l1/scores/c1-at-landing.json`), and `c1-before-recheck.json` re-derives the five
survivors and `pristine.cases 13` at `d7d9a62c`.

[inference] The five kills say nothing about the five *other* arms: `refusal_ok` has its own case
(`arm-pack-refusal`, green/false pair) and the helper cases (`sections-*`, `identity-*`, `counts-*`,
`fold-*`, `skip-run-no-claim`) do not feed the seam at all. The seam is the tested surface, not the
whole instrument.

## The typed contract: exit 2 before any run

`preflight()` (`:231-262`) checks every prerequisite before any REA or packer invocation and raises
`Unevaluable`; `main()` turns that into one JSON line on stderr and return code 2:

`{"schema": "kaidoku-r69-packed-elf-v1", "unevaluable": "<class>: <detail>", "claim": "R69"}`

The preflight classes are `missing_tool` (a missing `node`/`git`/`readelf`, an unusable `--upx` path, an
unreadable REA package root), `work_unusable` (the `--work` root is not a directory, or a `mkdtemp`
probe inside it fails), and `packer_mismatch` (the packer's `--version` first line or its sha256 differs
from the pin). `score()` raises the same class, still exit 2, for the run-time prerequisites: `git` on
the root, the REA `package.json` sha256 pin, the REA version, a carrier source that is absent or whose
sha256 differs from its pin, an original inventory below the carrier's floor, and a failed `upx` pack
(`:325-390`).

| arm | fixture | round-69, measured at the freeze | base `d7d9a62c`, round-68 instrument |
|---|---|---|---|
| `A1_missing_node` | `PATH` holding `git`, `readelf`, `upx` but no `node` | rc 2, `missing_tool: node` | rc 1, Python traceback ending `FileNotFoundError: [Errno 2] No such file or directory: 'node'` |
| `A2_work_unusable` | `--work` a `0500` directory | rc 2, `work_unusable: not writable (…/ro: PermissionError)` | rc 1, `PermissionError` traceback at `tempfile.mkdtemp` |
| `A3_packer_version` | `--upx` a script printing `upx 5.1.0` | rc 2, `packer_mismatch: version 'upx 5.1.0' != pin 'upx 5.2.0'` | rc 2 by argparse only: `unrecognized arguments: --upx …/upx-5.1.0` (no seam, no packer class) |
| `A4_packer_sha256` | `--upx` a copy of `/usr/bin/upx` with one byte appended | rc 2, `packer_mismatch: sha256 6ad600e7…0801 != pin cf2f6e7c…a969` | rc 2 by argparse only, same refusal shape |
| `A5_carrier_record` | the run's receipt | each carrier names `name`, `format`, `packing_mode`, `pin`, `source`, `runs`; the probe re-derives the pin from the source's sha256, the format from `readelf -h`, and the packing mode from the recorded pack argv (`--best` present); carrier `ok` true and no false arm | `jq: missing ['name', 'format', 'packing_mode']`, `xxd: missing ['name', 'format', 'packing_mode']`, `carriers []` |
| `A6_packer_pin` | the run's receipt | `packer {version 'upx 5.2.0', version_pin 'upx 5.2.0', sha256 cf2f6e7c…, sha256_pin cf2f6e7c…, pin_enforced true}`; host re-derivation equal on both | `packer.version_pin absent`, `packer.sha256_pin absent`, `packer.pin_enforced absent`, `pin_enforced not true` |

Measured: `arms_passed 6` of `target 6`, `failed []`, exit 0, against the three-carrier receipt
`.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` at `f1599810`
(`.ufo/waves/round-69/w1/ScribeKnowledge/contract-probe-exec3.json`; the probe's own instrument sha256
`4ac0d83b…`). Base: `arms_passed 0` of 6 with all six named
(`.ufo/waves/round-69/l1/pre/c2-at-base.json`; receipt
`.ufo/waves/round-68/l1/scores/c2-at-landing.json`). At the landing revision `5ee94c56…` the same
probe reports `arms_passed 6`, `failed []`, `instrument_sha256 4ac0d83b…`, scored against
`.ufo/waves/round-69/l1/scores/c3-at-landing.json` (`c2-at-landing.json`). The four fixtures are built by the probe, not by
the instrument: a `PATH` symlink farm, a `0500` directory, a three-line `#!/bin/sh` version impostor,
and a byte-appended copy of the real packer.

The pin is enforced, not recorded: `UPX_VERSION_PIN = "upx 5.2.0"` and `UPX_SHA256_PIN =
cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` (`:64-65`), and a mismatch raises
before any carrier is copied. `--upx` exists so the probe can hand the route a different packer; it is
also the only way to run the route with a packer other than `/usr/bin/upx`. [inference] The receipt's
packer block is therefore a gate as well as a record: `A6` recomputes the host packer's version and
sha256 and requires both to equal the receipt's values *and* the recorded pins.

A carrier record (`score()`, `:428-443`) carries `id`, `name`, `kind`, `source`, `pin`,
`packed_sha256`, `format {class, data, type, machine}`, `packing_mode`, `orig_counts`, `packed_counts`,
`unpacked_counts`, `section_count`, `upx_list_rc`, `before_ceiling`, `before_ceiling_ratio`, `refusal`,
`control`, `arms`, `ok`, and `runs`. `A5` requires the identity subset (`name`, `format`,
`packing_mode`, `pin`, `source`, `runs`) and re-derives the three values that are checkable from the
host: the source's sha256, its `readelf -h` identity, and the packing mode from the recorded pack argv.
[observation] In the round-68 receipt the records carry `pin`/`source`/`runs` but not `name`, `format`
or `packing_mode`, which is the M68-4 gap the round closes; the probe names exactly those three fields
at the base.

## The three carriers, including a shared object

| carrier | kind | source | pin | `readelf -h` type | orig (proc/seg/str) | packed | recovered | ceiling / original = ratio |
|---|---|---|---|---|---|---|---|---|
| `jq` | `executable` | `/usr/bin/jq` | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | `DYN (Position-Independent Executable file)` | 167 / 30 / 190 | 3 / 3 / 3 | 167 / 30 / 190 | 10 / 167 = 0.0599 |
| `xxd` | `executable` | `/usr/bin/xxd` | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | `DYN (Position-Independent Executable file)` | 99 / 29 / 103 | 3 / 3 / 6 | 99 / 29 / 103 | 10 / 99 = 0.101 |
| `libz` | `shared-object` | `/usr/lib/libz.so.1.3.2` | `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9` | `DYN (Shared object file)` | 184 / 29 / 199 | 98 / 6 / 136 | 184 / 29 / 199 | 120 / 184 = 0.6522 |

All three carriers are ELF64, 2's complement little-endian, `Advanced Micro Devices X86-64` in their
`readelf -h` header. [observation] The counts and ratios above are those of the measured three-carrier
receipt `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` (jq and xxd reproduce the round-68
route receipt `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` exactly); the ceilings themselves are
declared per carrier in `tools/round-69/packed-elf.py:72-86` and `claims.json` atom A8.

[observation] The shared object's packed inventory is not a three-procedure loader stub: `libz` retains
98 procedures, 6 segments and 136 strings on the packed bytes, and its before-arm is a declared ceiling
of 120 procedures (0.6522 of the original 184) rather than a shared bound. [inference] A single global
ceiling would either reject the packed shared object or admit a packed executable whose inventory is
not a stub; the per-class ceiling is the load-bearing relation (QUALITY #107). The 0.75 counter leaves
`libz` 0.0978 of headroom, so a drift in either the ceiling or the original count is visible before the
carrier flips. The recorded `before_ceiling_ratio` is the *declared* ceiling over the original count
(120/184), not the measured packed/original ratio (98/184 = 0.5326); the predicate names the former
and the receipt records the former, and the independent re-derivation notes both
(`.ufo/waves/round-69/w1/ExecC3/verify.md` §4).

The refusal arm exists only where a carrier pins an address: `jq` at `0x103fa0` — the packed bytes exit
1 with `code: invalid_request`, the restored bytes exit 0 with 4,841 code bytes and `FUN_00103fa0`
present. The negative control is on the same three sources: `upx -l` and `upx -d` on each *original*
both exit 2 (`NotPackedException`) and write nothing, and `upx -l` on each *packed* copy exits 0 with
`section_count 0`.

Supersession: the round-68 entry states "packed libraries and static binaries" as Frontier, unmeasured.
This entry measures exactly one packed shared object (`/usr/lib/libz.so.1.3.2`); static binaries and
every other shared object remain unmeasured, and the round-68 frontier clause survives for them.

Measured over the three-carrier receipt: `--check-receipt` → exit 0, `met true`, `target 3`,
`carriers_matched 3`, `kinds ["executable", "shared-object"]`, `failing []`
(`.ufo/waves/round-69/w1/ScribeKnowledge/check-receipt-exec3.json`). Over the round-68 landing receipt
(`.ufo/waves/round-68/l1/scores/c2-at-landing.json`): exit 1, `target 2`, `carriers_matched 2`,
`kinds [null]`, `failing ["target 2 != 3", "carriers_matched 2 != 3", "no shared-object carrier: kinds
[None]", "jq: before_ceiling_ratio None > 0.75", "xxd: before_ceiling_ratio None > 0.75"]`
(`.ufo/waves/round-69/l1/pre/c3-at-base.json`). At the landing revision `5ee94c56…` the three-carrier
receipt `.ufo/waves/round-69/l1/scores/c3-at-landing.json` carries the same counts and ratios, and
`c3-check-at-landing.json` reports `met true`, `target 3`, `kinds ["executable", "shared-object"]`,
`failing []`.

## Limits

- One packer: UPX 5.2.0, `/usr/bin/upx`, sha256
  `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; the pin is enforced, so no other
  version can be measured through this route. `upx --version` also prints a second line (`UCL data
  compression library 1.03`); only the first line is pinned.
- One packing mode: `upx --best` (`PACKING_MODE`), recorded per carrier and re-derived from the pack
  argv. The round-68 route's recorded pack argv also carries `--best`
  (`.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json`), so no comparison between modes exists and no
  other level (`-1`…`-9`, `--brute`, …) was measured.
- One architecture and format: ELF64, little-endian, x86-64 (`linux/amd64`). No 32-bit ELF, no ARM,
  no PE, no Mach-O.
- Three carriers only, all host system files: `/usr/bin/jq`, `/usr/bin/xxd` (a symlink to
  `/usr/bin/tinyxxd`, pinned by the target's bytes), `/usr/lib/libz.so.1.3.2`. Exactly one shared
  object is in the claim; a second (`/usr/lib/liblzma.so.5.8.4`, sha256 `6e4dae5b…`, original
  417/29/227 → packed 175/6/177 → recovered 417/29/227, ratio 175/417 = 0.4197) was probed by an
  executor seat as a generalisation probe, not as claim input, and is not covered here
  (`.ufo/waves/round-69/w1/ExecC3/verify.md` §3).
- One provider: REA 6.5.0 at the npx cache root, `package.json` sha256
  `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`; `package-lock.json` is recorded,
  never pinned (npx rewrites it). Node is required and unbounded in version by the instrument.
- Inventory equality is count equality on procedures, segments and strings, not semantic equality of
  the recovered program; byte identity is measured per carrier against its pin and never assumed from
  the packer's documentation (S269 bounds `--exact` as work in progress for some formats).
- Contract scope: the packer check is `isfile` + `os.access(X_OK)` followed by `upx --version`, and
  `--rev` is recorded without validation. A `--upx` path that passes those file checks but fails to
  execute (a file with the exec bit and no valid exec format, or one that becomes unreadable at exec)
  leaves the typed classes as a Python traceback with rc 1, and a bogus `--rev` is written into the
  receipt; an independent harness measured both shapes
  (`.ufo/waves/round-69/w1/ExecC2/rederive.md`, `arm-receipt.json`). Neither shape touches the six
  named arms.
- The carrier record's `section_count` is the *packed* file's section count (0 for all three); the
  original's section-header and program-header counts are not recorded per carrier. The `detected`
  and `recovery_ok` arms were independently reproduced from bytes
  (`.ufo/waves/round-69/w1/ExecC3/verify.md` §1 and §4).
- [unknown] Whether an anti-UPX stub (altered magic or entry code, `upx -d` refusal by design) is
  handled at all: no such carrier was measured.
- [unknown] Whether the route holds for a packed static binary, a packed PE/Mach-O carrier, or any
  packer other than UPX 5.2.0.
- Counter scope: `--check-receipt` tests `target == 3`, `carriers_matched == 3`, `control_ok true`,
  `met_target true`, `failing []`, at least one `shared-object` kind, and per carrier `ok true`, every
  arm present in that record's `arms` map true, a numeric `before_ceiling_ratio` not greater than
  `0.75`, and counts present. It does not enumerate the arm names a record must carry and does not
  compare a record's identity fields against the instrument's `CARRIERS`; synthetic receipts exercising
  those gaps are recorded in `.ufo/waves/round-69/w1/ReviewerGates/attacks.json` and are not evidence
  about the instrument's own receipt.

## Evidence

- Instruments (frozen bytes): `tools/round-69/packed-elf.py` sha256 `4ac0d83b…`,
  `tools/round-69/mutation-check.py` `51b64c56…`, `tools/round-69/contract-probe.py` `e609d85d…`,
  `tools/round-69/controls.py` `1f8f78c1…`; `tools/round-68/packed-elf.py` `48ef4c68…`, unchanged.
- Base receipts: `.ufo/waves/round-69/l1/pre/c1-at-base.json` (5 survivors, `pristine.cases 13`),
  `c2-at-base.json` (0 of 6, all six named), `c3-at-base.json` (`target 2`, exit 1),
  `controls-at-base.json` (seven arms, `ok true`).
- Battery and probe runs at the freeze `f1599810`:
  `.ufo/waves/round-69/w1/ReviewerGates/attacks.json` (`battery-r69`: `survivors []`, five kills,
  `pristine.cases 20`; `battery-r68`: five survivors, `pristine.cases 13`), and
  `.ufo/waves/round-69/w1/ScribeKnowledge/contract-probe-exec3.json` (`arms_passed 6`, `failed []`).
- Landing receipts at `5ee94c56…` (`.ufo/waves/round-69/l1/scores/`): `c1-at-landing.json` (`survivors
  []`, five kills, `pristine.cases 20`), `c1-before-recheck.json` (five survivors, `pristine.cases 13`),
  `c2-at-landing.json` (`arms_passed 6`, `failed []`), `c3-at-landing.json` (`carriers_matched 3`,
  `control_ok true`, `met_target true`, `failing []`), `c3-check-at-landing.json` (`met true`), and
  `provenance-at-landing.json` (`met true`).
- Three-carrier receipt and its check: `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json`
  (closure `carriers_matched 3`, `control_ok true`, `met_target true`, `failing []`);
  `.ufo/waves/round-69/w1/ScribeKnowledge/check-receipt-exec3.json` (`met true`).
- Source objects opened for this entry: `doc/upx.1` (40,077 B, `09552b3c…`), `src/help.cpp`
  (27,279 B, `0b893ca8…`), `src/main.cpp` (41,889 B, `a02c7cba…`), `doc/upx-doc.txt` (37,208 B,
  `4dc547ed…`), all at tag `v5.2.0`; copies and digests in this wave directory (`upx.1`, `help.cpp`,
  `main.cpp`, `upx-doc.txt`, `SHA256SUMS`).
