source: S270 — UPX 5.2.0 packer source at tag `v5.2.0`, `src/help.cpp:460-469` and `src/main.cpp:1174`
(https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp, 27 279 B, sha256
`0b893ca8299c061a8e1961ddbc1fa85cd8d77f3f043cba9a478a697e5d363c79`; and
https://raw.githubusercontent.com/upx/upx/v5.2.0/src/main.cpp, 41 889 B, sha256
`a02c7cba2939708e2af4c25119fe20a5a7594b7225b189848196280b03dea82c`; both opened 2026-11-03, HTTP 200;
quote at `help.cpp:465` `fprintf(f, "upx %s\n", UPX_VERSION_GIT_DESCRIBE);`; the flag at
`main.cpp:1174`; the generated manual page `doc/upx.1:164` repeats the flag as a secondary locator)
verified-at: 2026-11-03
recheck: `python3 -I -B tools/round-69/packed-elf.py --selftest` (20 cases, exit 0) and the three
frozen round-69 counters; `curl -fsSL
https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp | sha256sum` must print `0b893ca8…`

# Round 69 — the packed route's gate and contract, and the shared-object carrier

The round-68 route answered "can this artifact be read through the packer?" with four arms. Round
69 asks the next questions: can the route's own gate FAIL when an arm is wired wrong (R69-C1), is a
refusal a named class instead of a traceback (R69-C2), and does the route hold on a class it did not
pick when the carriers were executables (R69-C3)? Instrument:
`tools/round-69/packed-elf.py`; batteries `tools/round-69/mutation-check.py`,
`tools/round-69/contract-probe.py`, controls `tools/round-69/controls.py`.

## The arm seam, and what it kills

The five 2026-11-03 mutants survived every detector the lane ran: `identity_ok ≡ True`, recovery
self-comparison, detection without the section clause, `before_ok` self-comparison, and the control
arm dropped from the fold. All five were 13/13 green on the round-68 selftest because no case ever
evaluated an arm expression.

Round 69 moves every arm into one pure seam, `evaluate_carrier(model) -> {arms, ok}`, called by both
`score()` and `--selftest`. The selftest now runs 20 cases: the 13 helper cases plus `arm-pack-green`
and one false model per arm (`arm-pack-identity-false`, `-recovery-false`, `-detected-false`,
`-before-false`, `-control-false`) plus a refusal case. Measured at the landing with the frozen
battery:

| mutant | patch site | r68 selftest | r69 selftest |
|---|---|---|---|
| M1 identity | `identity_ok` expression → constant | 13/13 green (survivor) | killed by `arm-pack-identity-false` |
| M2 recovery | `recovery_ok` comparison → self-compare | 13/13 green (survivor) | killed by `arm-pack-recovery-false` |
| M3 detected | section clause dropped | 13/13 green (survivor) | killed by `arm-pack-detected-false` |
| M4 before | ceiling comparison dropped | 13/13 green (survivor) | killed by `arm-pack-before-false` |
| M5 control | control arm folded as `True` | 13/13 green (survivor) | killed by `arm-pack-control-false` |

A kill counts only when the selftest's `failed` list names the declared case; a mutant that breaks
syntax exits non-zero without that name and is reported `killed_wrong_case`, never a kill.

## The typed contract, and the enforced pin

The round-68 docstring promised exit 2 for a missing tool and a refused `--work`; the code raised
`FileNotFoundError` / `PermissionError` with exit 1 instead, accepted any packer, and recorded the
packer pin without testing it. Round 69's preflight, before any REA call, refuses with exit 2 and a
JSON `unevaluable` naming the class:

| class | trigger | exit-2 message |
|---|---|---|
| missing node / git / readelf / upx | `shutil.which` absent, or the upx path not executable | `missing_tool: <name>` |
| unusable work root | not a directory, or `mkdtemp` inside it raises OSError | `work_unusable: not writable (<path>: <error class>)` |
| packer version | `upx --version` first line ≠ `upx 5.2.0` | `packer_mismatch: version ...` |
| packer sha256 | the upx bytes ≠ `cf2f6e7c…` | `packer_mismatch: sha256 ...` |

The pin is enforced, not recorded: a different packer build is refused rather than described. The
`--upx <path>` seam exists so the refusal can be exercised (a fake 5.1.0 script, a real upx with one
appended byte) and so a host with a legitimate repack can be named explicitly. Every receipt carries
`packer.sha256_pin`, `packer.version_pin`, `packer.pin_enforced: true`, and every carrier record now
names `name`, `kind`, `format` (from `readelf -h`: class, data, type, machine), `packing_mode`
(`upx --best`, corroborated by the run's own pack argv) and `pin`.

## The carrier table at the landing

| carrier | kind | pin (sha256) | original procs/segments/strings | packed stub | ceiling (stub ≤) | ratio |
|---|---|---|---|---|---|---|
| `/usr/bin/jq` | executable | `e8156675…` | 167 / 30 / 190 | 3 / 3 / 3 | 10 | 0.0599 |
| `/usr/bin/xxd` | executable | `7b1e5d0c…` | 99 / 29 / 103 | 3 / 3 / 3 | 10 | 0.1010 |
| `/usr/lib/libz.so.1.3.2` | shared-object | `6c78c5e5…` | 184 / 29 / 199 | 98 / 6 / 136 | 120 | 0.6522 |

The shared-object stub is not the executables' 3-procedure stub: a packed `.so` keeps an export table,
so REA still resolves 98 procedures. The ceiling is therefore declared per carrier class and checked
against the original inventory (`ratio ≤ 0.75`); a ceiling looser than three quarters of the original
would make `before_ok` vacuous, and the counter rejects it. The unpacked copy equals the original's
inventory on all three counts (184/29/199), and byte identity is measured with `sha256sum`.
[inference] Because the unpacked bytes are the pinned original and the receipt is content-keyed, the
recovered inventory describes the program the packed file ships; the route still measures count
equality only, never semantic equality.

## Limits

UPX 5.2.0 only, default packing mode (`upx --best`), linux/amd64 ELF only; one shared-object carrier
(`libz.so.1.3.2`) and two executables; REA 6.5.0 with its 120 s per-verb limit; a packer other than
UPX, an anti-UPX stub whose magic or entry is altered, packed PE/Mach-O, packed static binaries and
semantic equality of a recovered inventory stay Frontier (`PROVINCE.md` round-69 note). A receipt is
evidence for the revision it names: the carrier pins and the packer pin are host facts, and the
before/after arms are re-derived with the frozen battery, never from this table.

## Final round-69 correction — measured, not promoted

The genuine runs above are retained as observations, not admission of C2/C3.
Both frozen receipt counters accept fabricated evidence (CriticClaims.md); the
later provenance gate does not repair their frozen admission rule. Shared-object
promotion is withdrawn: this carrier remains **measured Frontier** pending a new
freeze. Do not pass untrusted `--upx` paths: preflight executes them before checking
the sha256 pin (SentinelScope S-1). Hash-before-execution is outstanding.
