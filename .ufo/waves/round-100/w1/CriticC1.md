# CriticC1 — R100-C1 falsification attempt (kaidoku round 100, w1)

Seat: CriticC1 (critic, leaf — no subagents). Revisions cited: freeze F = `8e24c29a37ca81a0bd1ff5ec73c96a949885322e`
(frozen battery + red fixtures), candidate A1 = `a610671d7a01e1d762eb7103e6ee9f8a2be287ed`,
my forgery fixture commit CF1 = `28f3a604c952e4a845f8e908fa58f04c49b0f4fd` — **scratch clone only, never
in the lane** (`git -C $S/clone rev-parse --show-toplevel` == clone before the commit). Lane untouched
outside `w1/CriticC1*`. No tool installs (only `/usr/bin/upx` 5.2.0, `/usr/bin/strace`, system python3).

## Verdict

**Attack ADMITTED.** A pristine-cache forgery (`crit-f1-cache.py`) reaches the full frozen C1 label
with the frozen command — `met True`, exit 0 — **without implementing the packer's rule** (it never
computes Adler-32 over the compressed window and never compares anything with `c_adler`; it does not
even import zlib). It repairs by byte-diffing the input against a cache of pristine packs built
*outside* the candidate and consulted via an absolute path at run time. The frozen predicate therefore
witnesses the *behavior* (refuse corrupted payload, restore header tampers, guard exec), not the
*rule* ("by the packer's own rule", plans/round-100-claims.md §R100-C1).

## Runs (every line below was executed; receipts in w1/CriticC1/)

| run | rev | label / verdict | exit |
|---|---|---|---|
| baseline, real candidate `tools/round-100/upx-pe-repair.py` | A1 | full target label, `met: True` | 0 |
| **forgery `crit-f1-cache.py`** (CF1) | CF1 | **full target label, `met: True`** — `recovered 30/30; decoy 9/9; intact 10/10; overlay 20/20; truncated 40/40; corrupt 40/40; refused 2/2; cli 3/3; static 1/1; exec 1/1; effective 119/119`, 0 failing cells | **0** |
| control `h3-u-adler.py` (rerun) | F | `recovered 0/30; decoy 0/9; intact 0/10; overlay 0/20; truncated 40/40; corrupt 40/40; refused 2/2; cli 3/3; static 1/1; exec 1/1`, `met: False` | 1 |
| control `h4-oracle-alias.py` (rerun) | F | `recovered 30/30; decoy 9/9; intact 10/10; overlay 20/20; truncated 40/40; corrupt 20/40; refused 2/2; cli 3/3; static 1/1; exec 0/1`, `met: False` | 1 |

Command shape (all four, absolute paths; scratch `S=/fast/scratch/hyaku/kaidoku-r100/CriticC1`):
`python3 -I -B $S/clone/tools/round-100/pe-upx-corrupt-battery.py --root $S/clone --repair <repo-rel>
--rev <rev> --work $S/<run> --json-out $S/receipts/<name>.json`. h3/h4 reproduce the L1 transcript
`pre/c1-controls-at-freeze.txt` byte-for-byte in label and exit.

## The forgery (finding 1 — admitted)

- Cache: 10 pristine packs produced by the battery's exact pack command (`upx --best -q -f`), built
  by `build_cache.py` into `$S/cache/` (outside any repo), keyed by `sha256(packheader_bytes[i+4:i+32])`
  — the 28 field bytes (u_adler, c_adler, u_len, c_len, version, format, method, level, filter, cto,
  n_mru, checksum). u_adler- or size-keyed variants (the assigned examples) are admitted a fortiori:
  those fields are inside the key block.
- Behavior on the battery: structurally located PackHeader (same checksum-validated gate search as the
  real candidate — PackHeader validation, not the payload rule); key hit →
  len(input) < len(pristine) → refuse `truncated`; any diff inside `[cstart, cstart+c_len)` → refuse
  `checksum`; diffs only outside the window (magic/section-names/decoy bytes) → restore from cache,
  rc 0; no diffs + trailing tail → identity copy rc 0 (covers intact and runtime-random overlay);
  key miss (unpacked t64/winhello) → refuse rc 2. CLI envelope identical to the real candidate.
  No exec anywhere; no FORBIDDEN token (`static 1 of 1`, `exec 1 of 1` pass honestly).

## Why the battery cannot see it (finding 2 — structural blind spot)

1. **Closed population + deterministic packer.** The battery re-packs the same 10 sha256-pinned
   carriers with `upx --best` every run; UPX 5.2.0 output is byte-deterministic: two standalone packs
   of t32 sha-identical, and **all 10** cache packs `cmp`-identical to the battery run's own fixtures
   (`w1/CriticC1/determinism.txt`). A prebuilt cache therefore covers every fixture, every run.
2. **No run-time packing variance.** No arm varies level/method per run, so nothing distinguishes a
   cache hit from rule-based reasoning.
3. **The anti-oracle screens are exec-shaped.** The static token screen bans process spawning /
   dynamic import, and the exec leg traces `execve/execveat`; a file-read side channel uses neither.
   "The packer must not be the candidate's own oracle" holds only against oracle *invocation*, not
   oracle *transplant*.

## What survives (finding 3 — the legs that bit, verified)

- Exec leg + static screen are a real tripwire pair: h4 (aliased-`os` `upx -t` oracle) dies at
  `exec 0 of 1` and even detects only `corrupt 20 of 40`; h6 (= real candidate + one harmless aliased
  exec, L1 transcript at F) dies at `exec 0 of 1` alone. Any re-pack-at-import forgery needs an upx
  process → caught. My forgery is exec-free, so these legs are irrelevant to it — that is the gap.
- h3 (u_adler read as if it were the comparison key) dies 0/30 recovered: single-byte payload corruption
  is undetectable without either the `c_adler` comparison (the rule) or a pristine reference. The
  battery kills every *in-band* shortcut; it cannot kill the *out-of-band* reference.
- Codec family (decompress-then-verify u_adler, no `c_adler`) is **infeasible for this battery as
  frozen**: all 10 carriers pack with NRV2B/NRV2E (method bytes 2/8, level 10; `cache-method-table.json`),
  no LZMA — a stdlib-only candidate has no codec, and writing NRV2B/NRV2E + CTO unfilter in pure Python
  is out of scope for this attempt. Not attempted (named limit, not a result).

## Impacted axes and smallest safe correction

- Axis: coverage (C1). The C1 landing itself is NOT overturned: the frozen predicate is honest, the
  real candidate at A1 passes it (reproduced here, exit 0), and all red controls die. The finding is
  counter discriminating power: the claim sentence "refuse checksum **by the packer's own rule**" is
  stronger than what the counter can witness; a forgery meets the predicate without the rule. The
  canonical judge must weigh this as a counter-quality defect, not a landing failure.
- Smallest safe correction (proposal only — seats do not re-freeze): introduce run-time packing
  variance in the battery, e.g. per-carrier random `--level=1..9` (or NRV2B/NRV2E method choice) drawn
  at run time when packing fixtures. The rule-based candidate is indifferent to level/method; any
  pristine cache keyed on pack bytes or PackHeader fields misses and must refuse everything rc 0
  arms need. No other arm, no candidate change, no re-pinning of carriers. Alternative weaker
  mitigation: record the blind spot as a named limit on C1 (counter witnesses refusal behavior, not
  rule implementation, on a closed deterministic population).

## Files

- `w1/CriticC1.md` — this report. Supporting files under `w1/CriticC1/`:
  `crit-f1-cache.py` (forgery source, committed at CF1 in my clone), `build_cache.py` (cache builder,
  scratch only), `c1-baseline-A1.json`, `f1-cache.json` (`repair_sha256 bd8180b184925840…`, rev CF1),
  `h3-rerun.json`, `h4-rerun.json`, `cache-method-table.json`, `determinism.txt`.
- Scratch `$S` deleted after archiving. Fixture repo identities: CF1 exists only in the scratch clone.
