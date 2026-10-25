# ExecPermuteAudit — round 34 / r34b / wave 1

Seat: `L1Kaidoku34-2.ExecPermuteAudit` (leaf executor). Claim under attack: **R34-C2**
(capability acquisition, axis depth) — pre-freeze structure-blind shortcut-replay gate.
Instruments pinned at lane commit **c79bbe7b0959132b9873ff3431cf5eb313b58b33**
(`git rev-parse HEAD` → `c79bbe7b…`, read-only check at 07:22:17Z).
R34-C1 (GNU version-needs) untouched: its production reader and twelve carriers were **not**
executed or scored here. Only python fixtures/readers of the pinned mini set were used; no ELF
carrier was executed.

Verification window: 2026-10-25T07:18:12Z → 07:22:40Z. Host python3 = `/usr/bin/python3` 3.14.8.
**No tool installed, upgraded or removed** (nothing needed; pacman untouched, no `uv`/`npx`/`cargo`).

## 1. Assignment and headline

For each of the eight `mini-fix` fixtures, import `permute()` from
`tools/round-34/mini-fix/mini-counter.py`, permute with 20 random seeds, and check
(i) total size stays 512, (ii) decoded records via the pinned structural reader equal the
pristine decode, (iii) sha256 differs from pristine, (iv) name-pool byte multiset preserved.

**Result: 159 / 160 (fixture, seed) cases pass all four invariants; 1 case fails, and it fails
only (iii).** Decoded-output invariance — the property the counter's predicate actually relies
on — held in **160/160** cases. The single failure is `beta.mrec` at seed 18, where `permute()`
returned the pristine bytes *verbatim* (byte-for-byte equal, not merely equal sha256), i.e. the
"opaque permuted copy" was not perturbed at all. Decoding was still correct, so no green/red
verdict flips.

Seeds used: **integers 0–19 with `random.Random(seed)`** (stated explicitly because the counter's
own default seed is the *string* `"kaidoku-r34-mini-v1"`, and `Random(int)` ≠ `Random(str)`;
both families were probed separately in §5).

## 2. Method and reproduction

Scratch root `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecPermuteAudit` (`$S` below). Instruments
were **copied** (never mutated in the lane) and the copies were verified identical to the lane
files:

```
43ef669f…4b52  $S/round-34/mini-fix/mini-counter.py   == lane tools/round-34/mini-fix/mini-counter.py
2f399cab…b4b6  $S/round-34/mini-fix/readers/structural.py == lane …/readers/structural.py
```

Pristine fixture digests (lane, mode 0644, 512 bytes each), also reproduced in scratch:

```
alpha   d1de0e6f50eca499d70fc619bfa0bba52d9d789e36d2fba31109ffd6a922ad44
beta    a8547fcf1764611f5aec0b869e4560a14c6f3e995b7b3ee703bba09826d7665d
delta   79ff7036235a026355c9281ffb845e7d2ffebe7f54982d82f36b49fb0ae4b781
epsilon 82f03f991a99b73001f160ae2d8d8f9dd327de2b7d4954dbbdb40a99d148738e
eta     5bcabeb2711ead28066d17db4a79ab2351a23d390c887fc009187f39f6ddbc2e
gamma   ffb57ecdad76f6246e2aa2e8179e1effcfd49bbe9ef4c77b1959435b8937cc0a
theta   b1f87d7cb8147c5cb02f2f7f4f3212bfd8147c0025b765e70a8341ee09b274e3
zeta    19ff407420ab8028319b97e4bacc976eba3644b167bf0e235f7db5014078ea09
```

(All 64 hex; authoritative copies in `$S/pristine.sha256` and
`$S/audit-out/audit.json → fixtures.*.pristine_sha256`.)

Decoded-record comparison used the **pinned structural reader as python**, in exactly the
invocation shape the counter itself uses (`sys.executable -I -B readers/structural.py <file>` with
`env={"PATH": "/usr/bin:/bin", "HOME": <scratch>}`), on the permuted copies written to disk. A
second, independent path re-decoded the same copies through the counter's own
`decode_fixture()` + `name_at()` (record-array order preserved, not sorted), so a permutation that
silently reordered the record array would have been caught.

Per-case checks actually evaluated (all recorded per seed in `audit.json`):

| id | check |
|---|---|
| I1 | `len(permuted) == 512` |
| I2 | sorted records from pinned `structural.py` == pristine's |
| I2b | array-order records from `decode_fixture()`/`name_at()` == pristine's |
| I2c | header `names_off` unchanged |
| I3 | `sha256(permuted) != sha256(pristine)` |
| I4 | `Counter(permuted[names_off:]) == Counter(pristine[names_off:])` (pool byte multiset) |
| I4b | multiset of decoded names preserved |
| I5 | every differing byte outside `names_off` lies in a record's u16 `name_off` field (16+8·i, 17+8·i) |

Commands (all exit codes are the *run's* exit code):

```
07:18:36Z  sha256sum round-34/mini-fix/fixtures/*.mrec                     exit 0  → $S/pristine.sha256
07:18:52Z  python3 permute_audit.py                                        exit 1  → 160 cases, 1 failure
07:19:16Z  python3 probes.py                                               exit 0  → identity / latent-defect probes
07:19:33Z  mini-counter.py --root . --control-reader …/structural.py --seed {0,1,18,19,kaidoku-r34-mini-v1}
                                                                           exit 0 each (matched=8)
07:20:20Z  python3 probes2.py                                              exit 0  → census + leak reader sweep
07:20:43Z  python3 probes3.py                                              exit 0  → counter-stream census + e2e leak
07:22:10Z  python3 probes4.py                                              exit 0  → red-surface seed sweep
07:22:28Z  mini-counter.py on a scratch fixture with a non-NUL-terminated pool
                                                                           exit 3  (typed refusal, §6)
```

## 3. Per-fixture result (seeds 0–19, `random.Random(int)`)

Fixture shape facts recomputed from the bytes (`count`, header `records_off`, `names_off`,
pool entries = NUL count):

| fixture | count | records_off | names_off | pool entries | seeds passed | I1 | I2/I2b/I2c | I3 | I4/I4b | I5 max outside-diff |
|---|---|---|---|---|---|---|---|---|---|---|
| alpha.mrec | 3 | 16 | 40 | 445 | 20/20 | ok | ok | ok | ok | 0 |
| **beta.mrec** | 1 | 16 | 24 | 474 | **19/20** | ok | ok | **1 fail (seed 18)** | ok | 0 |
| delta.mrec | 2 | 16 | 32 | 452 | 20/20 | ok | ok | ok | ok | 0 |
| epsilon.mrec | 1 | 16 | 24 | 468 | 20/20 | ok | ok | ok | ok | 0 |
| eta.mrec | 3 | 16 | 40 | 436 | 20/20 | ok | ok | ok | ok | 0 |
| gamma.mrec | 5 | 16 | 56 | 392 | 20/20 | ok | ok | ok | ok | 0 |
| theta.mrec | 6 | 16 | 64 | 378 | 20/20 | ok | ok | ok | ok | 0 |
| zeta.mrec | 4 | 16 | 48 | 410 | 20/20 | ok | ok | ok | ok | 0 |

Pass matrix (`.` pass, `X` fail), from `$S/audit-out/audit.json`:

```
fixture     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19   pass
alpha       . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
beta        . . . . . . . . . .  .  .  .  .  .  .  .  .  X  .   19/20
delta       . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
epsilon     . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
eta         . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
gamma       . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
theta       . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
zeta        . . . . . . . . . .  .  .  .  .  .  .  .  .  .  .   20/20
```

**Seeds where decoded output changed: none.** No (fixture, seed) pair produced a decoded record
set differing from pristine, through either decode path — including the one case where the bytes
were unchanged.

Evidence: `$S/audit-out/audit.json` (sha256 `891ec9fb63b0d38a…`) holds all 160 rows with every
check, the permuted sha256 and the reader exit code; the 160 permuted copies themselves are
`$S/audit-out/<fixture>.s<NN>` (160 files, each 512 bytes).

## 4. Root cause of the single failure (depth)

`permute()` builds the string list from the whole tail `data[names_off:]`, which for synthetic
fixtures is the real name(s) followed by **zero padding**, and it treats every padding NUL as an
extra *empty* string (beta: 1 real string + 473 empties = 474 entries). It then shuffles indices
and re-emits `strings[i] + b"\x00"`, so the byte layout is reproduced **iff** the real string
lands back in its original slot:

- one distinct non-empty name ⇒ `P(identity bytes) = 1 / pool_entries` = **1/474** (beta),
  **1/468** (epsilon);
- k ≥ 2 distinct names ⇒ requires all k to return to their slots (≈ 1/Lᵏ) — never observed.

Measured (fresh `Random(int)` per fixture, 5000 seeds — `$S/audit-out/probes.json`,
`probes2.json`):

| fixture | identity seeds / 5000 | rate | theory |
|---|---|---|---|
| alpha, delta, eta, gamma, theta, zeta | 0 / 5000 | 0 | ≈ 0 for k ≥ 2 |
| beta | 10 / 5000 | 0.0020 | 1/474 = 0.00211 |
| epsilon | 13 / 5000 | 0.0026 | 1/468 = 0.00214 |

beta identity seeds (int): 18, 1415, 2004, 2187, 2347, 2771, 2796, 3164, 4599, 4848.
epsilon identity seeds (int, first 12 of 13): 562, 1265, 1406, 1737, 2004, 2187, 2347, 2709,
2771, 3164, 4578, 4599. Seed 18 is an identity for beta only, which is exactly the failing cell.

**Consequence, stated at its true weight.** The counter writes the transformed copy as
`opaque-<sha256(transformed)[:20]>.data`, i.e. it relies on the transform to make the input
unrecognizable. For the two single-record fixtures that guarantee does not hold: with p ≈ 1/474
per run the copy *is* the pinned fixture, so a structure-blind reader that had memorized the true
pristine digest scores on it. This does **not** threaten the target-8 conjunction (it can lift a
shortcut to at most 1, or 2 if both single-record identities hit in one stream — probability
≈ 4.6e-6; 0/5000 observed), but it is a real opacity leak and a *per-fixture* falsifier of the
predicate's phrase "opaque permuted copies".

## 5. Counter-level (shared-RNG) reproduction and the leak end-to-end

`score()` creates **one** `random.Random(seed)` and feeds the same stream to all eight fixtures in
sorted order, so a fixture's permutation depends on the earlier fixtures' pool sizes. Reproducing
that stream exactly for string seeds `"0".."4999"` (`$S/probes3.py`,
`$S/audit-out/probes3.json`):

- **20 / 5000 seeds produce an identity permutation**, always for exactly one single-record
  fixture (beta ×13, epsilon ×7). Seeds: 28, 161, 244, 682, 692, 910, 1481, 1855, 2490, 2621,
  2711, 3346, 3867, 3957, 4233, 4320, 4396, 4479, 4649, 4884. No seed made both hit.
- On six of those seeds I ran the pinned counter end-to-end against a scratch, **non-registered**
  leak-aware reader (digest-memorized on the eight true pristine sha256 values,
  `$S/leak_digest_reader.py`, sha256 `61a32217bf2e3b51…`): `matched=1`, `met_target=false`,
  exit 1 on every one (seeds 28, 161, 244, 682, 692, 910), with the failing fixture being the
  identity-collided one; the structural reader scored `matched=8` on the same seeds.
- With the frozen default seed `kaidoku-r34-mini-v1`: counter → `matched=8`, `met_target=true`,
  exit 0 (scratch copy, 07:19:33Z) and **no** transformed digest equals a pristine digest on any
  of the 12 seeds swept through the counter in that probe (`identity_collisions: []` for all 12 in
  `probes2.json`), i.e. the production green clause is reproduced and is not resting on a leak.

## 6. Latent defects in `permute()` — proven, not triggered by the eight fixtures

All three were reproduced on **scratch-only synthetic 512-byte fixtures** (`$S/probe-out/`,
`$S/audit-out/probes.json`, `probes2.json`, `probes3.json`). None fires on the pinned set, because
all eight fixtures have `records_off == 16` and NUL-terminated pools and every record's `name_off`
lands on a string boundary.

1. **`records_off != 16` silently corrupts the file.** `decode_fixture()` accepts any
   `records_off >= 16`, but `permute()` writes the new u16 `name_off` at the hardcoded
   `16 + 8*index` instead of `records_off + 8*index`. Fixture `(records_off=24, names_off=40,
   count=2)`: pristine decodes `[(liba.so,0,17), (libb.so,0,34)]`; after `permute(seed 3)` the
   pinned reader **still exits 0** but decodes `[("",0,34), (libb.so,0,17)]` — it reads record 0
   out of the shifted slot and the write also lands in header padding (byte 16). Differing
   positions were exactly `{16, 24}`; the out-of-record-array diff at byte 16 is the proof.
   Verification then reports a *changed decode*, not a refusal — a silent, wrong-answer failure
   shape inside the very transform that is supposed to be decode-preserving.
2. **`name_off` off a string boundary raises an uncaught `KeyError`.** Patch alpha's first record
   `name_off` to 1 (still `decode_fixture`-legal): `permute()` raises `KeyError: 1`,
   `isinstance(error, Unevaluable) == False`. The CLI still refuses cleanly, because `main()`
   wraps `score()` and prints `unevaluable:KeyError:1` (exit 3), so this is a type-discipline
   defect, not a verdict defect.
3. **Pool without a trailing NUL raises an uncaught `ValueError`.** Set beta's last byte to `X`:
   `permute()` raises `ValueError: subsection not found`. Confirmed end-to-end on a scratch root
   at 07:22:28Z: the pinned counter printed
   `{"finding": "unevaluable:ValueError:subsection not found", "met_target": false, …}` and
   **exited 3** — the refusal path is honest here, but it degrades the whole eight-fixture run to
   unevaluable rather than skipping one fixture.

Non-defects verified (so they are not reported as findings): two records sharing one `name_off`
(20/20 seeds invariant); the same name string present at two different pool offsets (20/20
invariant); a name that is a suffix of another name adjacent in the pool, `libz.so.1` / `z.so.1`
(20/20 invariant); `names_off` never moves; only the rewritten u16 `name_off` bytes ever differ
(I5 outside-diffs = 0 in all 160 audit cases).

## 7. Adjacent bounded probe — red surface is seed-stable (not my gate verdict)

Because my failure mode is a *seed-dependent* transform, I checked whether the frozen red surface
moves with the seed. Pinned counter, scratch root, 7 registered shortcuts × seeds `"0".."19"` +
`"kaidoku-r34-mini-v1"` (147 runs, 07:22:10Z, `$S/audit-out/probes4.json`):

| class | max matched | met target | exits |
|---|---|---|---|
| all-false | 0 | never | 1 |
| size-keyed | **1** (alpha, every seed — all fixtures are 512 B) | never | 1 |
| fixed-slice | 0 | never | 1 |
| digest-keyed | 0 | never | 1 |
| string-scan | 0 | never | 1 |
| record-order-replay | 0 | never | 1 |
| label-memorization | 0 | never | 1 |

Every class stays strictly below target 8 in all 21 seeds; the only non-zero cell is `size_keyed`
matching alpha by the deliberate 512-byte size collision, which is a designed control, not drift.
Structural reader on the same seeds: 8/8, `met_target=true`, exit 0.

Cross-observation for whoever owns the counter/gate control audit (**not** my verdict, offered as
evidence): the registered `digest_keyed.py` memorizes digest prefix `e1c4d1d5`, which matches
**none** of the eight pristine fixture digests (`d1de0e6f, a8547fcf, 79ff7036, 82f03f99, 5bcabeb2,
ffb57ecd, b1f87d7c, 19ff4074`, checked 07:22:36Z). As registered it is therefore vacuous — it
would score 0 even on byte-identical inputs. Its 0/21 result is not evidence that digest-keyed
memorization is defeated; §5's leak-aware reader is the evidence for what that class can actually
do (max 1/8, and only on leak seeds).

## 8. Assessment against R34-C2

- The property the counter's predicate needs — *decoded records are invariant under the
  permutation transform* — **holds**: 160/160, via two independent decode paths, with header,
  flags, value, `names_off` and pool byte multiset unchanged in every case.
- The transform's *opacity* claim ("opaque permuted copies") is **not an invariant**: it is
  byte-identity with probability ≈ 1/pool-entries for each single-record fixture, measured at
  0.20–0.26 % and confirmed end-to-end (a digest-memorized structure-blind reader scores 1/8 on
  such seeds). The target-8 conjunction absorbs it; a future per-fixture or ≥1 floor would not.
- `permute()` is **shape-dependent, not general**: three uncaught exception classes and one
  silent-corruption path exist for fixture shapes the decoder itself accepts (`records_off > 16`,
  mid-string `name_off`, un-terminated pool). Today's eight fixtures all sit in the safe corner
  (`records_off == 16`, boundary-aligned offsets, NUL-terminated pool), so the frozen result is
  not wrong — but the transform carries no guard that would keep a ninth fixture honest, and the
  `records_off` case fails *silently with exit 0*.

Risks/holes I did not close (out of my scope, stated so they are not mistaken for clean): whether
`replay-gate.py` itself forwards a seed or pins one (a forwarded seed would let a shortcut shop
pick a leak seed — still capped at ≤2 < 8, so not a refusal bypass); the registered
`digest_keyed.py` vacuity noted in §7.

Blockers: none.

## 9. Draft doc text (for the L1 to land; not written to LOG/SCORECARD by me)

> **R34-C2 — permutation invariance (independent audit).** `mini-counter.permute()` was replayed
> over the eight pinned fixtures × 20 integer seeds (160 cases) on a scratch copy of the frozen
> instruments (`mini-counter.py` sha `43ef669f…`, `readers/structural.py` sha `2f399cab…`).
> Decoded output was invariant in 160/160 cases through both the pinned structural reader and the
> counter's own decoder; size stayed 512, pool byte and name multisets were preserved, and only
> the rewritten u16 `name_off` bytes changed. One case failed the "sha256 differs" leg: beta at
> seed 18 is a **byte-identical** permutation, because a single-record fixture has one non-empty
> name among 474 pool entries, so the transform is the identity with probability 1/474 (1/468 for
> epsilon; measured 10/5000 and 13/5000). A structure-blind digest-memorized reader therefore
> scores 1/8 on such seeds (20/5000 counter-stream seeds), never 8 — the target-8 conjunction
> holds, per-copy opacity does not. Latent, non-triggered: `records_off > 16` makes `permute`
> silently misalign records (reader still exits 0); mid-string `name_off` → `KeyError`;
> un-terminated pool → `ValueError` (counter then refuses with exit 3).

## 10. Evidence index

| path | sha256 | content |
|---|---|---|
| `$S/permute_audit.py` | `437222b0eccbc784…` | 160-case invariance harness (§3) |
| `$S/audit-out/audit.json` | `891ec9fb63b0d38a…` | all 160 rows, every check, permuted sha256 |
| `$S/audit-out/<fixture>.s<NN>` | — | 160 permuted copies, 512 B each |
| `$S/probes.py` / `probes.json` | `9cb7c979…` / `894c0e2b…` | identity census, records_off/mid-string/shared/suffix probes |
| `$S/probes2.py` / `probes2.json` | `ed5afed6…` / `d389ff3d…` | shape facts, un-terminated pool, leak-reader sweep |
| `$S/probes3.py` / `probes3.json` | `ed49d284…` / `9826f461…` | counter-stream identity census, end-to-end leak, duplicate-offset case |
| `$S/probes4.py` / `probes4.json` | `b8a59172…` / `48081fdf…` | red-surface 147-run seed sweep |
| `$S/leak_digest_reader.py` | `61a32217bf2e3b51…` | scratch-only structure-blind leak reader (§5) |
| `$S/pristine.sha256` | — | pristine fixture digests |
| `$S/probe-out/*.mrec` | — | 65 scratch synthetic fixtures/permuted copies |

Only two lane paths were authored by me: this report, and nothing else. No lane VCS operation was
performed; `git status --porcelain` (read-only, 07:22:17Z) shows only the pre-existing untracked
`.ufo/waves/round-34/r34b/**` wave material.

VERDICT: PASS_WITH_ONE_FALSIFIED_LEG — decoded-output invariance holds 160/160 (both decode paths), size/multiset invariants hold 160/160, but the "sha256 differs" leg is falsified for beta.mrec at seed 18 by a byte-identity permutation (structural probability 1/474 for any single-record fixture, measured 10/5000 beta and 13/5000 epsilon), which leaks per-copy opacity to digest-memorized shortcuts at ≤1/8 and never breaches the target-8 gate; plus three latent, non-triggered `permute()` shape defects (`records_off>16` silent corruption, mid-string `name_off` KeyError, un-terminated pool ValueError).
