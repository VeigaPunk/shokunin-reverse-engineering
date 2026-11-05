# CriticClaims — round 90, pre-landing falsification of R90-C1 and R90-C2

Seat: `CriticClaims` (critic). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the tree: this seat wrote only its own seat dir and
`/fast/scratch/hyaku/kaidoku-r90/CriticClaims/`; the scratch dir was removed after
the receipts below were copied into `receipts/`.
No tool installs were needed (`upx 5.2.0`, `bwrap`, `node`, REA 6.5.0 all present and
pin-matching); no pacman transaction was attempted.

Measured tree: HEAD `18b21f092` ("round-90: freeze the two claims …"), declared base
`fc52cc9dc` (verified ancestor of HEAD; 6 commits between). Frozen inputs read:
`plans/round-90-claims.md`, `.ufo/waves/round-90/claims.json`,
`tools/round-90/upx-later-block-battery.py` (528 lines),
`tools/round-90/upx-break-repair.py` (445 lines),
`tools/round-90/control-cheat-repack.py`, `tools/round-89/depth-blocks-v2.py`.

Instrument pins from `claims.json` re-hashed and **all match**:

```
84664f52…8206  tools/round-90/upx-later-block-battery.py
aaf3536e…590b  tools/round-90/upx-break-repair.py
faafc982…b826  tools/round-90/control-cheat-repack.py
359f15e1…f18f  tools/round-89/depth-blocks-v2.py
```

Environment pins: `/usr/bin/upx` `cf2f6e7c…c969` and `upx 5.2.0`; REA package.json
`a5003023…0a6c` (version 6.5.0); carriers `/usr/bin/jq` `e8156675…7806`,
`/usr/bin/xxd` `7b1e5d0c…ae65`, `/usr/lib/libz.so.1.3.2` `6c78c5e5…5ca9`,
`/usr/bin/docker-init` `0bd49c8d…e115` — all four carrier pins match the counter's table.

---

## 0. Commands run (every number below carries one of these)

| # | command | exit | receipt |
|---|---|---|---|
| R1 | `python3 -I -B tools/round-90/upx-later-block-battery.py --root . --rev fc52cc9dc --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <scratch>/work-rea --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out <scratch>/battery-rea.json` | **0** (5 m 02.132 s) | `receipts/battery-rea.json` |
| R2 | same command **+ `--no-rea`**, `--work <scratch>/work-norea` | **0** (3.385 s) | `receipts/battery-norea.json` |
| R3 | same as R2 with `--rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | **0** | `receipts/battery-bogusrev.json` |
| R4 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev fc52cc9dc --expect-blocks 30` | **1** (`blocks 29 resolved 29 unresolved 0`) | `receipts/depth-fc52cc9dc.json` |
| R5 | same, `--rev 54c277868` | **1** (`29/29`) | `receipts/depth-54c277868.json` |
| R6 | same, `--rev 18b21f092` | **1** (`29/29`) | `receipts/depth-18b21f092.json` |
| R7 | `--rev` omitted | **2** (`--rev (or --worktree) is required`) | — |
| R8 | `python3 -I -B tools/round-90/upx-later-block-battery.py --selftest` | **0** (`cases=8 failures=0`) | — |
| R9 | `python3 -I -B tools/round-90/upx-break-repair.py --selftest` | **0** (`cases=17 failures=0`) | — |
| R10 | `python3 -I -B tools/round-89/depth-blocks-v2.py --selftest` | **0** (`cases=10 failures=0`) | — |
| R11 | `python3 -I -B tools/round-87/upx-magic-repair.py --selftest` | **0** (`cases=33 failures=0`) | — |
| R12 | `python3 -I -B tools/round-88/upx-chain-battery.py --selftest` | **0** (`cases=6 failures=0`) | — |
| R13 | `python3 -I -B tools/round-89/upx-field-battery.py --selftest` | **0** (`cases=9 failures=0`) | — |
| R14 | `... tools/round-88/upx-chain-repair.py --selftest` | **0** (`cases=11 failures=0`) | — |
| R15 | `... tools/round-89/upx-field-value-repair.py --selftest` | **0** (`cases=22 failures=0`) | — |
| R16 | layout / tamper / route harness over the four carriers (scratch) | 0 | `receipts/routing-and-limits.json` |
| R17 | C2 fixture repos (3 variants), `depth-blocks-v2.py --root <fixture> --rev HEAD --expect-blocks 30` | **0, 0, 0** | `receipts/c2-fixture-*.json` |

R1/R2 ran concurrently in separate work roots; both repacked all four carriers from the
pinned sources under the pinned packer.

---

## 1. Predicate identity — is the same sentence in plan, code and receipt?

### 1.1 R90-C1

Plan (`plans/round-90-claims.md`, Kill rule + §C1): "A candidate is written only when
it accounts for exactly the declared `u_len` and, where the stored chain is intact,
strictly more than the stored chain does — **a filter, not a rank key (QUALITY 171)**."
Counter docstring: "The PackHeader `u_len` is enforced as a *filter* inside the repair
for this class, not as a rank key (QUALITY 171)."

**Divergence (quoted).** `tools/round-90/upx-break-repair.py`, module docstring:

> "… take `derived = successor - (block + 12)` bounded by that block's `sz_unc`, and
> among the survivors **prefer the candidate that accounts for the most declared bytes
> (the PackHeader `u_len` is a preference, never a filter -- QUALITY 171)**, ties to the
> smaller derived value."

That is the negation of the frozen sentence. The code is in fact a filter —
`derive_break`:

```python
total = accounted(dd, r88, b0, ph_off, method, ph, info)
if total != require_total:      # exact-u_len FILTER
    continue
if min_total is not None and total <= min_total:   # strictly more than stored
    continue
key = (total <= ph["u_len"], total, -derived)      # inert rank key
```

so the docstring is wrong, not the code. But the *rank key QUALITY 171 names* is still
present verbatim: Row 171 at the base says "the code keys on
`(total <= u_len, total, -derived)`, so an over-`u_len` candidate is ranked last, not
rejected". It is now dead (every survivor has `total == u_len`, so the first two key
components are constant and only `-derived` discriminates), which is provable only by
reading four lines up; the receipt carries none of this. Row 171's own remedy is
"implement it as a filter **and report the refusal** or state the bound as a preference
with the fallback named"; the code reports the refusal, the docstring states a
preference. That is the Row-162 docstring-vs-code defect, inside the instrument.

**Receipt divergence.** The label is `P1 6 of 6; P2 4 of 4; P3 4 of 4` — counts only.
The receipt has no field recording filter-vs-rank; `pins` records the four *composed*
module hashes but not the declared instrument pins, and the battery's own hash is not
(and cannot be) in its own receipt. The "same sentence in plan, code and receipt label"
claim is therefore unverifiable from the receipt alone.

**Minor.** Battery docstring says the isolation control "holds exactly `["in"]`"
(`in`, `out`); the code accepts `["in"]` **or** `["in","out"]`, and all 14 scored cells
recorded `["in","out"]`. Same intent, different sentence.

### 1.2 R90-C2

Plan §C2 Claim: block 30 is "the guard-and-control set a *superseding instrument
revision* must inherit, **as a decision table whose rows route each revision defect
class to the guard that answers it, each row citing the base-revision criterion it
restates (QUALITY 161/163/167/168/169/170/171 and `corpus/lessons/round-89.md`)**."

Counter code, `depth-blocks-v2.py`:

```python
PATTERN = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
```

`resolve()` requires ≥1 match of that pattern, resolves each against
`corpus/knowledge/<name>.md` at the revision, and `shape()` requires ≥25 words and ≥2
backticked spans. **No table check, no row count, no QUALITY token check, no
`corpus/lessons/` check.** The label `blocks 30, resolved 30` encodes none of the claim.

**Demonstrated (R17).** Three fixture repos, each the base's 173 knowledge files + the
base SKILL.md (29 blocks) + one appended block 30, committed at the fixture's own HEAD
(`git rev-parse --show-toplevel` asserted equal to the fixture dir before every mutation):

| block 30 variant | result | met | exit |
|---|---|---|---|
| plain prose sentence, no table, one `corpus/knowledge/2026-10-13-asar-surface.md` citation | `blocks 30 resolved 30 expect 30 unresolved 0` | **true** | **0** |
| same prose **+ `corpus/QUALITY.md:99999-100000`** (a range that cannot exist) **+ `corpus/lessons/round-89.md:1-2`** | same | **true** | **0** |
| genuine decision table (3 `\|`-rows, QUALITY 171/168/167 tokens) | same | true | 0 |

The middle row is the decisive one: a block that omits every table row and carries a
*citation to a nonexistent QUALITY range* still yields the frozen target. The predicate
does not entail the claim.

---

## 2. Vacuity

### 2.1 Is P1 reachable with the claimed work skipped?

- **No-work repair: not reachable.** The discriminating arm is `identity` (output bytes
  == intact packed bytes). The unchanged round-89 repair returns the tampered input, so
  `identity` is false; `controls.no_work` is `0` of 6 in both R1 and R2. Confirmed by
  code: `row["recovered"] = all(arms except None)`.
- **No-op tamper: impossible by construction.** `value = blk["sz_cpr"] + delta`,
  `DIRECTIONS = (-7, 7)`, and an out-of-range value `continue`s (which would shorten
  the population and fail `== 6`). Every constructed cell differs from the intact bytes.
- **Exact-`u_len` is a filter in code, not a rank key** — see 1.1. Verified empirically:
  `derive_break` refuses libz's block-1 tamper (`class intact`, bytes unchanged) rather
  than ranking an over-`u_len` candidate first.
- **Cheap rule:** a paker-validated brute force over `1..sz_unc` would also score these
  cells and is *declared* out of scope ("this claim is the capability, not the
  mechanism", QUALITY 152). I did not run it; the admission is explicit and the counter
  cannot force the mechanism.
- **`met` requires every control** — `all(arms_ok.values())` over the 8 keys
  `N1, N2, N3, isolation, carrier_blind, no_work, cheat_live, cheat_killed`. All true in
  R1 and R2.

### 2.2 The REA arm can be silently skipped — **found**

`rea_recover` is **not** in `arms_ok`; it is per-cell and `None` when `--no-rea`.
`met` has no dependency on `rea_on`. R2 (`--no-rea`) returned
`met_target: true, exit 0, label "P1 6 of 6; P2 4 of 4; P3 4 of 4"`, with
`arms.rea_recover: null` in all 14 cells and `pins.rea_pkg: null` — byte-identical label
and `met` against the declared run R1. So the predicate sentence "REA 6.5.0 reports the
original's own procedure/segment/string counts" can be dropped with no signal in the
label or `met`.

R1 shows the arm does work when enabled: `rea_recover: true` in all 14 cells, 5 m 02 s
(REA `analyze` dominates: 46 m user). But the arm is **logically redundant**: `identity`
already requires the output packed bytes to equal the intact packed file, and
`unpack_pin` requires `upx -d` of that file to hash to the carrier pin; the unpacked
bytes are then the original's bytes, so any deterministic analyzer must return the same
counts. The REA clause cannot fail unless REA itself is nondeterministic — it cannot
discriminate a wrong repair. Likewise `field_only`, `test_ok` and `unpack_pin` are all
implied by `identity`; the five-arm cell is effectively the single `repair_rc0 AND
identity` conjunction.

### 2.3 Receipt provenance is not bound to a revision — **found**

`--rev` is a free string echoed into the receipt. R3 passed a hash that is not a
revision (`deadbeef…`) and still produced `met_target: true, exit 0` with
`revision: "deadbeef…"`. The battery loads every module from `--root .` (the moving
worktree), never from the revision it names, and never records a dirty-tree flag. The
C1 receipt's freshness rests entirely on an external checker.

### 2.4 C2 kill rule has no referent

`claims.json` C2 kill rule: "the block text changed after this declaration". At the
declaration revision there is no block-30 text: R4/R5/R6 all report `blocks 29` at
`fc52cc9dc`, `54c277868` and `18b21f092`. The rule cannot be evaluated.

---

## 3. Causality and separability

- **C2 without C1: yes.** R4 runs the depth counter at `fc52cc9dc`, where
  `tools/round-90/` does not exist (`git cat-file -e fc52cc9dc:tools/round-90/…` →
  absent), and returns `29/29/exit 1`. The counter reads `SKILL.md` and
  `corpus/knowledge/*` from git at the named rev.
- **C1 without C2: yes.** The battery loads `tools/round-87/`, `-88/`, `-89/`, `-90/`
  and the four carriers; it never opens `SKILL.md`.
- **Shared artifact:** `claims.json` / the wave, and the base revision. No shared code.
- **Separability sentence is false as written (C2).** The claim requires a row citing
  `corpus/lessons/round-89.md`; that file is **absent at the declared base**:

  ```
  git cat-file -e fc52cc9dc:corpus/lessons/round-89.md   -> fatal: … not in 'fc52cc9dc'
  ```
  It landed in `c40a36f21` (round-89 wave), which is *after* `fc52cc9dc`. The plan's
  "Block 30 cites only documents present at the base — no round-90 artifact" is
  contradicted by its own citation list (a round-**89** artifact, still absent at the
  base). `QUALITY.md` itself is present at the base and rows 161, 163, 167, 168, 169,
  170, 171 all exist there (verified by `grep -nE '(161|163|167|168|169|170|171)'`
  against `git show fc52cc9dc:corpus/QUALITY.md`).
  The kill rule only polices "a `corpus/knowledge` document absent at the base", so this
  cannot fire.
- **Base-arm provenance.** `pre/c2-depth-at-base.json` records
  `"revision": "54c277868…"`, not the declared base `fc52cc9dc`. I reproduced `29/29/
  exit 1` at `fc52cc9dc` (R4), so the substance holds, but the committed receipt does
  not evidence the revision the plan attributes to it.

---

## 4. Harm — do the older classes survive?

### 4.1 Scored arms (R1)

`P2-first-block` 4 of 4, `P3-zeroed` 4 of 4, each with `rea_recover: true`.

### 4.2 Older selftests (R11–R15)

r87 repair 33/0, r88 chain battery 6/0, r89 field battery 9/0, r88 repair 11/0,
r89 repair 22/0. The composed modules are unchanged (sha pinned and matching), and the
older batteries score the older repairs, so no regression is possible there *by
construction*; the risk is only in the new repair's decision order.

### 4.3 Routing on real carriers (R16)

| carrier | blocks in prefix | `u_len` | intact chain accounts | b1−7 / b1+7 | b0±1, ±7, ±64, 0 |
|---|---|---|---|---|---|
| jq | 5 | 30,800 | 30,800 | `break-point`, restored byte-exact | `field-value` / `chain-geometry`, restored |
| xxd | 5 | 38,928 | 38,928 | `break-point`, restored | restored |
| dinit | 5 | 851,288 | 851,288 | `break-point`, restored | restored |
| libz | 3 | 108,560 | **98,592** | `intact`, bytes returned unchanged | restored |

The declared libz limit is exact (98,592 of 108,560, as written). `stored_accounted`
beats the filter's margin on the P1 cells: jq 14,527, xxd 11,899, dinit 17,683 against
`u_len` totals of 30,800 / 38,928 / 851,288 — "strictly more than the stored chain"
holds in the recorded info, not just in prose.

Class admission is real for all six P1 cells (independent of the battery): the tampered
file answers `upx -t` rc **1** with `Exception: compressed data violation`, `upx -d` rc
**1**, and the round-87 anchor path returns it unchanged (rc 0). This matches the plan's
class sentence exactly.

### 4.4 Harm found: the round-89 refusal contract regressed on the write path

Round-89, bad `--out` (`..` component), real packed ELF input:

```
refused: --out carries a '..' component: …/escape2.bin      rc=2
```

Round-90, same input and `--out`:

```
Traceback (most recent call last):
  … in write_atomic  full = checked_target(path, what)
  … in checked_target  raise Refused(...)
Refused: --out carries a '..' component: …/escape3.bin      rc=1
```

`main()` wraps `read_input` and `repair` in `try/except Refused` but calls
`write_atomic(args.dst, out, "--out")` **outside** it, so the module's own `Refused`
escapes as an uncaught traceback. Round-89 wraps its writes (`try: write_atomic(...);
write_atomic(info) except Refused: … return 2`). This is verbatim the defect QUALITY
Row 169 names ("the round-87 `Refused` escaped as an uncaught traceback (rc 1)") and the
repair's docstring claims: "the input guards and typed refusals of the round-89 revision
are inherited (QUALITY 169), and output writes are atomic through `mkstemp`". The input
guards *are* inherited (verified: directory / FIFO / `/dev/zero` / 257 MiB / missing /
`MZ` all give rc 2 with a typed `refused` JSON). The counter cannot see the write-path
defect: every box it builds has a valid `out` path, and `N1` only feeds a plain ELF
(which `read_input`/the ELF gate rejects).

### 4.5 Out-of-class boundaries (not defects, but the claim should not be read wider)

- **Double defect** (block 0 −7 *and* block 1 −7): rc 0, class `field-value`, output
  still fails `upx -t` (rc 1). The block-0 path is not re-walked after composition. This
  is consistent with the declared single-defect class and with Row 167 ("exit code means
  I changed the field I own"), but it means rc 0 on this tool does not imply a valid
  file.
- **Anchor probe:** replacing all four `UPX!` words in packed jq also mutated three
  bytes at offset 10,971 that lie in a region r87 does not own (three header anchors
  restored; `upx -t` rc 0; one `KDK!` remains). That probe was out of class, not a
  fill-in for the r87 class.

---

## 5. Strongest surviving objections and verdicts

### Objection O1 (decisive, C2) — the predicate does not entail the claim

C2's frozen Target is a block count and a citation-shape floor. A 25-word prose
paragraph with two backticks and one `corpus/knowledge` citation scores
`blocks 30 resolved 30 met true exit 0` (R17, variant 1), and it still scores when it
carries `corpus/QUALITY.md:99999-100000`, a range that cannot resolve (variant 2). The
claim's core — a decision table routing each defect class to its guard, each row citing
QUALITY 161/163/167/168/169/170/171 or the round-89 lesson — is unmeasured. Evidence:
`receipts/c2-fixture-prose-with-false-QUALITY-citation.json` (`met: true, exit 0`).

### Objection O2 (C1) — the shipped instrument regresses a guard it claims to inherit

`write_atomic` outside the `try` turns a typed refusal into an uncaught traceback
(rc 1 vs round-89's rc 2). The scored predicate is unaffected, but the instrument's
stated QUALITY-169 contract is false as shipped, and it is not observable from any
receipt.

### Objection O3 (C1) — a green receipt is obtainable without the declared evidence

`--no-rea` (R2) and a bogus `--rev` (R3) each produce `met_target: true, exit 0` with
the declared label. Neither is visible in `label`, `met_target` or `controls_ok`; only
`cases[*].arms.rea_recover` and `pins.rea_pkg`/`revision` differ, and the revision is
whatever string was passed. The declared command does not use either flag, so the
landed receipt *can* be correct — but the counter does not make it so.

### Objection O4 (C1) — the filter sentence is contradicted by the instrument's own prose

The repair docstring says `u_len` is "a preference, never a filter"; the code filters.
QUALITY Row 171 exists precisely to forbid this mismatch, and the claim cites 171 as the
criterion it satisfies.

### Objection O5 (C2) — the claim's citation list names a document absent at the base

`corpus/lessons/round-89.md` did not exist at `fc52cc9dc`; separability as written is
false, and the kill rule cannot catch it (it polices `corpus/knowledge` only).

### Verdicts

- **R90-C1 — holds on the frozen predicate as the counter measures it; weakened.**
  Reproduced the declared label, `met_target: true`, exit 0 and all eight controls with
  REA on (R1) and off (R2). The class is real (six cells: `upx -t` rc 1), the derivation
  is exact (three carriers account `u_len` fully), the libz limit is exact, the
  composition is byte-exact on P2/P3 and across ±1/±7/±64 on all four carriers, and
  no-work scores 0/6. Weakened by O2 (refusal-contract regression), O3 (`--no-rea` and
  unverified `--rev` both yield green), O4 (docstring vs filter), and by four of the
  five arms being implied by `identity` (so the predicate overstates its own breadth).
  Not falsified: no no-work, no-op or cheap path scores the six P1 cells.

- **R90-C2 — falsified as written; holds only under a narrowed restatement.**
  The stated predicate (count + shape + `corpus/knowledge` citations) is satisfiable
  with the claimed work entirely skipped and with a false QUALITY citation (O1), and the
  claim's own citation set includes a document absent at its base (O5). The measured
  predicate itself is sound (base arm red at `fc52cc9dc` — 29/29/exit 1 — and the
  counter's selftest green, R4/R10), but it does not measure the claim.

### Smallest safe corrections

C1 — (a) wrap both `write_atomic` calls in `try/except Refused` (round-89 parity) and
re-pin the repair in `claims.json` with a recorded instrument revision, or record the
defect as accepted with a named follow-up; (b) make `met` depend on `rea_on` (or refuse
`--no-rea` when `--expect` carries the full label); (c) assert
`git -C <root> rev-parse HEAD == --rev` and record the dirty flag; (d) delete the
"preference, never a filter" sentence and either remove the inert
`(total <= u_len, total, -derived)` key or state in the receipt that it is inert.

C2 — (a) restate the Target to what the test measures and move the decision-table
sentence into a separately checked arm, or (b) extend the counter with a row check
(≥1 `|`-row per named guard, each row's `QUALITY <n>` token resolved against
`corpus/QUALITY.md` at the measured rev) — which must be **re-declared**, because the
kill rule forbids a post-declaration counter change; and (c) either drop the
`corpus/lessons/round-89.md` citation or restate the base as a revision where it exists
(`c40a36f21` or later).

---

## 6. Receipts (absolute)

```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/battery-rea.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/battery-norea.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/battery-bogusrev.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/depth-fc52cc9dc.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/depth-54c277868.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/depth-18b21f092.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/c2-fixture-prose-only.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/c2-fixture-prose-with-false-QUALITY-citation.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/c2-fixture-real-table.json
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/CriticClaims/receipts/routing-and-limits.json
```

`routing-and-limits.json` holds every carrier's block table, `u_len`, intact-chain
accounting, the ±7 P1 cells, the ±1/±7/±64 block-0 grid, the block-0-zeroed cell, the
double-defect probe and the `--out` escape result. Scratch
(`/fast/scratch/hyaku/kaidoku-r90/CriticClaims/`) is removed on exit; nothing outside
the seat dir and scratch was written.
