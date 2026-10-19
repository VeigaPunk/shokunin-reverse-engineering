# RV-4 — seat report (chain c2, reviewer), wave `arc3-loop1-round4`

Seat RV-4 · chain c2 · role **reviewer** · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
HEAD `015e1bab914713568f339fd53999bc180459cc40` (unchanged throughout; no git mutation issued).

**Task as frozen:** review each patch for census-conformance — apply them myself on a fresh
scratch copy and run the census; any new gated locus is a defect; list them.

Writes by this seat: this report + `claims/c2/RV-4/**` only. No git mutation. Custody paths
read-only (hash/stat only; never opened for write). The real `PROVINCE.md` / `SKILL.md` /
`SCORECARD.md` / `.ufo/gates/c1-census-v10.py` were only ever **read** — every apply ran on a
fresh scratch copy. Scratch under `/var/tmp/rv4-scratch/` (never `/tmp` — standing EDQUOT rule).
Lane: devin (`devin/deepseek-v4-1-flash-max`), the declared fallback recorded in
`claims-frozen.md:11-15` after the hyper lane returned 402 out-of-credits on all 48 seats.

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round4/claims/c2/RV-4/`.

### 1.1 Review instruments built by this seat

| instrument | what | sha256 |
|---|---|---|
| `census-diff.py` | locus-level differ between two `--json` census captures: new / removed / disposition-moved assertions + every verdict-row delta (scope-errors, unreadable, g2, declared fail classes, g11, g7, per-file floor, counts). Exit 1 on any new gated locus or regression. | `d7ab95902282d86481666092a0ff3dcb434c1983f771349f0460381ffad1d32e` |
| `harness/apply-and-census.sh` | one command: fresh scratch copy of the 3 scoped files + instrument → apply (unified diff *or* prose `.patch.md`) → sha256/wc before+after → census → differ. Real tree read-only. | `8fb48dd0e759fe99e905722de9ec6650e3b0e30b48f651ff52c96b9f5648e01f` |
| `prose-apply.py` | applies the round-3/4 prose patch format (fenced `-`/`+` hunks) by **content match**, so a stale author line number still lands; refuses on ambiguous/absent search text. | `9fbe257400005dae8c3d86fcab7b089491256795f82611ef40ca4218425a2a54` |

Both harness bugs found by self-test and fixed before use: (i) relative patch paths broke after
`cd` to the scratch tree — now resolved to absolute before the cwd moves; (ii) `patch` prompted
interactively and hung — now `--batch --forward`.

### 1.2 Baseline (before) — the real tree, measured

```
$ python3 .ufo/gates/c1-census-v10.py --root .        → VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit 0
PROVINCE.md 162 lines  d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad
SKILL.md    390 lines  5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f
SCORECARD.md 1580 lines 21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7
instrument  .ufo/gates/c1-census-v10.py  d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5
```
Evidence: `evidence/census-baseline-realtree.txt`, `evidence/census-baseline.json`.
Scratch copy reproduces the same verdict byte-for-byte (control).

### 1.3 Every round-4 patch text, classified against the census file set

The census opens exactly `{PROVINCE.md, SKILL.md, SCORECARD.md}` (`c1-census-v10.py` `SCOPE`;
the file-open surface at `:518` joins only those names to `--root` — no `.ufo/**` path is read).
`claims/c2/EX-31/census.md` in round 3 established this structurally; re-derived here.

| patch | target | in census scope? | applied + measured |
|---|---|---|---|
| `c2/EX-14/evidence/demo-frontier-repair.patch.md` (`507b0061…`) | `PROVINCE.md` | **yes** | ✅ CONFORMANT (§3.1) |
| `c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md` (`16b878d3…`) | `PROVINCE.md` | **yes** | ✅ CONFORMANT (§3.2) |
| `c3/EX-21/patch/skill-registry-row.patched.md` (`8e56f3d9…`) | `SKILL.md` | **yes** | ✅ CONFORMANT (§3.3) |
| `c3/EX-24/evidence/skill-row.diff` (`c369f73d…`) | `SKILL.md` | **yes** | ✅ CONFORMANT (§3.4) |
| `c3/EX-24/evidence/readme.diff` | `custody-pair/README.md` | no | not applicable — file never read |
| `c3/EX-26/proposed-readme-ruling.patch.md` | `custody-pair/README.md` | no | not applicable (prose patch carries no fenced hunk; target out of scope either way) |
| `c1/EX-06/proposed-corpus-note-vyper-dispatch.patch.md` | `corpus/knowledge/` | no | not applicable |
| `c1/EX-07/proposed-r3-unknowns-correction.patch.md` | `corpus/knowledge/` | no | not applicable |
| `c3/EX-25/proposed-{hardlink-inode-key,verify-key-resolved}.patch.md` | `custody-pair.py` | no | not applicable |
| `c3/EX-21/tools/{r3-to-r4,readme-r3-to-r4}.diff` | tool + README | no | not applicable |
| `c2/EX-13/province-frontier-{alternate-providers-jeb,evm-solc-held,pe-subtypes-reserve,recorded-crashes-organic}.patch.md` | `PROVINCE.md` | **yes** | ✅ CONFORMANT (§3.7) |
| `c2/EX-13/province-round4-frontier-cross-version-residuals.patch.md` | `PROVINCE.md` | **yes** | ✅ CONFORMANT (§3.7) |
| `c2/EX-13/province-round4-frontier-pe-wall-closed.patch.md` (`32f6052d…`) | `PROVINCE.md` | **yes** | ⚠️ census-PASS but **NOT line-neutral** (§4.1d) |

**No patch text was found that introduces a new gated locus.** See §4 for the four content-level
defects and the structural findings the census cannot express.

### 1.4 Scope-gap map (measured from the instrument's own `SCOPE`)

Evidence: `evidence/scope-gap-map.txt`.

| file | declared rows | **UNDECLARED gaps** |
|---|---|---|
| `PROVINCE.md` (162) | 8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131 | **72-118 (47 lines — the entire Frontier section)**, **132-162 (31 lines — the post-unlock frontier)**, 1-7, 14, 27-39, 63 |
| `SKILL.md` (390) | 10-16, 18-20 | **21-390 (370 lines — includes the registry row at :390)**, 1-9, 17 |
| `SCORECARD.md` (1580) | 56-60, 273-326, 417-466, 467-502, 503-533, 534-560, 619, 620, 636-702, 703-768, 769-855 | **856-1580 (725 lines)**, 1-55, 61-272, 327-416, 561-618, 621-635 |

Creep audit on the current instrument vs the round-3 baseline (`git show 015e1ba:…`) via the
round-1 CR-5 tool: `rows before=20 after=20 / ADDED 0 / REMOVED 0 / CHANGED 0 / CREEP FLAGS []`.

## 2. Proposed changes

**None by this seat** (reviewer; this seat writes no real target). Two patch-text-level
recommendations for the parent, both advisory:

- **P-1 (content, not locus):** EX-14's candidates and EX-13's `evm-solc-held` should not be
  landed as written — their added text asserts Core membership the corpus disclaims (§4.1); the
  complete candidate also asserts a Vyper leg with no admitted entry (§4.1b). A scope-true form
  such as `real solc-0.8.37 carriers held (arc3-r1/r3, RESULT-class)` avoids the promotion claim.
  Two independent seats produced this overclaim, so the parent may want to correct the bullet's
  own framing rather than only the two patches.
- **P-2 (structural):** any future repair that must carry a version/pointer token into
  `PROVINCE.md:72-118` or `SKILL.md:21-390` requires a **same-commit re-key of the census scope
  table** (`.ufo/gates/c1-census-v10.py`) — chain c1's instrument, not a c2 seat's to edit. The
  round-3 `EX-31/proposed-census-ptr-redaction.patch.md` precedent is the correct shape (patch
  text, owner lands).
- **P-3 (unrepaired rows) — now largely satisfied:** `PROVINCE.md:62` ("absent: `7z`, `cabextract`,
  `xxd`, radare2/rizin, strace/ltrace, upx`, `pacman-contrib`") was falsified by measurement —
  VZ-2's census and this seat's own sweep both find five of those tools **present** (installed
  2026-10-13 in one batch). EX-13's `province-core-fallback-readers-inventory` patch
  (`1913e11e…`) repairs it and measures CONFORMANT (§3.7). Remaining unrepaired row: `F3` (the
  JEB "unprobed" wording), a nit, not a staleness defect.
- **P-4 (patch hygiene):** EX-14's revised candidate carries a malformed hunk-4 context line
  (§4.1c). Apply it with `patch --fuzz=0` — or with an applier that requires exact context
  matches — so the defect fails loudly instead of producing a self-contradictory sentence. The
  wave's prose-patch format has no such check today; my `prose-apply.py` skips a leading context
  line rather than validating it, which is exactly how this defect stayed invisible until the
  byte-comparison in §4.1c.
- **P-5 (new — line-neutrality is unenforced):** EX-13's `pe-wall-closed` breaks the claim's
  "line count unchanged" invariant undetected (§4.1d). The gap is structural: the census asserts
  only the marker at `PROVINCE.md:119`, so a **deletion below 119** — anywhere in the undeclared
  `132-162` region — trips nothing, while an insertion above it does. A cheap repair is to make
  the instrument assert the scoped files' total line counts (or the undeclared tail's length) as
  part of the verdict rather than merely reporting them in `counts`; that is chain c1's
  instrument, so this is a patch-text-level recommendation for the parent.

## 3. Before → after measurement (the chain's claim)

The C2 claim is: *every PROVINCE Frontier bullet and surface-summary claim is census-checked;
every stale item repaired same-line (line count held) or adjudicated NO-CHANGE with cause; the
census instrument reads PASS at the records commit.*

### 3.1 EX-14 `demo-frontier-repair.patch.md` — CONFORMANT

`507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51`
Transcript `runs/ex14-demo-apply-census.out`; census `evidence/census-after-ex14-demo.json`.

| | before | after |
|---|---|---|
| `PROVINCE.md` sha256 | `d075a3c6…` | `1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2` |
| lines | 162 | **162 (held)** |
| census verdict | PASS 0/0/0/0 | **PASS 0/0/0/0** |
| assertions | 16 | 16 |
| new gated loci | — | **0** |
| differ | — | **CLEAN** |

This independently reproduces EX-14's own claimed after-digest `1bfb5dd7…` exactly.

### 3.2 EX-14 `candidate-complete-frontier-repair.patch.md` — CONFORMANT

`16b878d3d4af61040b036772c9b31d721070a4143b5e0a92d147e222c112db5e`
Transcript `runs/ex14-complete-apply-census.out`; census `evidence/census-after-ex14-complete.json`.

A four-hunk candidate repairing F1b (`:82-83`), F5b (`:91-93`), R2 (`:139-144`) and X1
(`:157-160`). It landed on the same scope constraints the wave established: **line-neutral**
(162 → 162), so DATED row `119-131` keeps its marker line, and **needle-free**, so no
`undeclared` locus appears in the 72-118 gap.

| | before | after |
|---|---|---|
| `PROVINCE.md` sha256 | `d075a3c6…` | `f9b0888c2b60b0b3cabed299b5b83271d7b91c33cc33968bdbe502a40718eb4b` |
| lines | 162 | **162 (held)** |
| census verdict | PASS 0/0/0/0 | **PASS 0/0/0/0** |
| assertions | 16 | 16 |
| new gated loci | — | **0** |
| differ | — | **CLEAN** |

Its F1b repair is **evidence-grounded and verified**: it replaces "Reserve: 91MB Godot ARM64
template" with "the 91MB scale wall is closed (arc2-r7)", which matches the authority it cites —
`corpus/README.md:175` reads ">90MB PE scale — CLOSED, not frontier". This closes the `:82-83`
staleness this seat independently identified in §3.5.

**Review note (not a census defect):** my `prose-apply.py` initially treated this patch as a
single hunk and failed to apply it. Fixed to split fenced blocks on `@@` sections and to carry
context lines inside the search text; regression-tested against the single-hunk demo patch
(§3.1), which still reads CONFORMANT after the change. A patch that cannot be applied cannot be
reviewed — the applier fix is what made this section possible.

### 3.2b EX-14 `candidate-complete-frontier-repair.patch.md` REVISED — CONFORMANT on the census, but DEFECTIVE

The candidate was revised after §3.2 was written: `16b878d3…` → `8a0e12ff…`. Rule #14 requires
re-review after a revision, so the revised bytes were re-applied and re-measured.

| | revised `8a0e12ff…` |
|---|---|
| apply (fuzz-tolerant) | OK |
| `PROVINCE.md` sha256 | `dfa70b42b51dd45bd82bbf3037b707c0e1f10518ec9b0d5f68d72dbda652d27e` |
| lines | **162 (held)** |
| census verdict | **PASS 0/0/0/0** |
| new gated loci | **0** — census capture byte-identical to baseline |
| **hunk 4 validity** | **REJECTED — malformed context line (§4.1c)** |

The census result is unchanged from §3.2; the defect is content-level, not locus-level.

### 3.3 EX-21 `skill-registry-row.patched.md` — CONFORMANT, all three self-claims verify

Transcript `runs/ex21-landing-census.txt`; census `evidence/census-after-ex21-landing.json`;
identities `evidence/ex21-landing-identities.txt`.

| | before | after |
|---|---|---|
| `SKILL.md` sha256 | `5eec51c0…` | `8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf` (EX-21's claim — **reproduced exactly**) |
| lines | 390 | **390 (held)** |
| census verdict | PASS 0/0/0/0 | **PASS 0/0/0/0** |
| assertions | 16 | 16 |
| new gated loci | — | **0** |
| differ | — | **CLEAN** |

Rule-#14 re-derivation of EX-21's row identity: `sha256(row_line + LF)` =
`8f8e5408648c7aacfb0c161eee54c86514f35570f3a8e332526ca5fec136fa0e` — **equals the claimed
value**. The real tree's `SKILL.md` is still `5eec51c0…`, confirming EX-21 did not write the
seat-forbidden file. EX-21's real target moved as claimed: tool `7cd19c3c…`/1155 lines →
`29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`/1343 lines;
README `f30df42e…` → `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186`.

### 3.4 EX-24 `skill-row.diff` — CONFORMANT

`c369f73d21bc7ae2ddf62b33c3a14f70cba0d9260251862bf65da3ad984c766f`
Transcript `runs/ex24-skillrow-apply-census.out`; census `evidence/census-after-ex24-skillrow.json`.

| | before | after |
|---|---|---|
| `SKILL.md` sha256 | `5eec51c0…` | `68435482ea041704f91af0536ef86f56457e964374abd160067d731a022ce565` |
| lines | 390 | **390 (held)** |
| census verdict | PASS 0/0/0/0 | **PASS 0/0/0/0** |
| new gated loci | — | **0** |
| differ | — | **CLEAN** |

The edited row carries only the pin columns as gated tokens (`devin=6.5.0`, `omp=6.5.0`,
`kimi=6.7.0`, all `current-ok`); the edit itself adds selftest counts 22→24 and a mkdir-guard
clause, introducing no version or pointer token.

### 3.5 The strongest form of the result: all fourteen conformance captures are byte-identical

Every patch that measured CONFORMANT produced **the same 7197 bytes** as the baseline:

```
7cb9b513412f47b07d56e085a68f3eaf8b0028d20768bd7b38ac94cead93807d  (×14)
  census-baseline.json
  census-after-ex14-demo.json            census-after-ex14-complete.json
  census-after-ex14-complete-v2.json     census-after-ex21-landing.json
  census-after-ex24-skillrow.json
  census-after-ex13-{alternate-providers-jeb,evm-solc-held,pe-subtypes-reserve,
                     recorded-crashes-organic}.json
  census-after-ex13-province-round4-frontier-cross-version-residuals.json
  census-after-ex13b-{province-round4-frontier-pe-wall-closed,
                      province-core-fallback-readers-inventory}.json
```

The four captures that differ are exactly the intentional plants/defects, each with its expected
signature:

| capture | digest | verdict | signature |
|---|---|---|---|
| `plantA-undeclared` | `07b223b9…` | FAIL | `undeclared=1` |
| `plantB-linemove`, `plantD-insert-linemove` | `669ba0ac…` | FAIL | `scope_errors=1` (`:119` marker), 163 lines |
| `plantE-append-silent` | `08af8de8…` | PASS | 164 lines — silent (growth past the bound is not a locus) |
| `ex13-pe-wall-closed` **rev 1** | `6b4101f4…` | PASS | 161 lines — the §4.1d defect, census-invisible |

Byte-identity across the fourteen conformance runs is stronger than "no new gated locus": the
census's **entire verdict surface** — every locus, every disposition, every counter, the G2
per-file floor, the `counts` line — is unchanged to the byte across every repair that conforms.
`stale=0 ambiguous=0 undeclared=0 unresolved=0` before and after, with `PROVINCE.md=17,
SCORECARD.md=14, SKILL.md=3` current-ok assertions on every run.

**The converse is the important half.** Because the census surface is *invariant* to these
repairs, byte-identity is also the proof that the census **cannot grade** them: it reads the same
PASS on the correct revision (`16b878d3…`) and on the defective one (`8a0e12ff…`, §4.1c), on the
161-line tree and the 162-line one (§4.1d), and on the bullet whose text it never parses at all
(§4.2). "Census PASS" is a necessary but insufficient certificate for a C2 repair.

### 3.6 The chain claim's *staleness* half — independent Frontier census

> **CORRECTION (added after EX-13's patches landed).** My original census below adjudicated
> `:84-86` ("all 3 organic cores exceed the cap (waybar 434MB)") as **current**, on the strength
> of the r2 corpus entry. **That was wrong.** EX-13 falsified it, and I reproduced both legs
> first-hand: `coredumpctl dump 1857` → **17,608,704 B** (under the 33,554,432 cap), and
> `inspect-recorded-crash` on it → **exit 0**, `format: elf-core`, 53 segments, 4 threads,
> `ev_78c885047ca0be39801fd1890de4db057e807b9bc8a79196acd18cc8fbbe2e9a`; separately,
> `ls /var/lib/systemd/coredump/ | grep -i waybar` is **empty** and `coredumpctl list` shows both
> waybar entries as **`missing`** — retention decayed them. So the bullet is falsified twice over,
> and the stale set is **five** rows, not four. EX-13 is right and this seat's first pass was
> incomplete; the corrected census is below.

The census instrument grades **loci** (version/pin/pointer tokens), never staleness of prose.
This seat therefore ran an independent content census of all five Frontier bullets
(`PROVINCE.md:82-93`) against admitted corpus state:

| bullet | claim | verdict | evidence |
|---|---|---|---|
| `:82-83` PE subtypes | "Reserve: 91MB Godot ARM64 template" | **STALE** | the reserve was **consumed** — `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:3` "the scale wall falls", 9 segments / 75,218 procedures, envelope `a77ebee8…` |
| `:84-86` crashes >32 MiB | mechanism held; "all 3 organic cores exceed the cap (waybar 434MB)" | **STALE (corrected — see note above)** | `coredumpctl dump 1857` → 17,608,704 B under cap; `inspect-recorded-crash` → exit 0, `ev_78c88504…`; waybar cores `missing` in `coredumpctl list`. Falsified by EX-13, reproduced by this seat |
| `:87-88` alternate providers | "JEB (unprobed)" | current (wording nit) | `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99` — JEB *was* probed (`inspect-jeb-client` → `capability_unavailable`, exit 0). The operative claim (no engine) holds; "unprobed" is inaccurate but not a staleness defect |
| `:89-90` macOS-only | `unsupported_host` on Linux | current | `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:11-15` — the 10 `unsupported_host` ops; synth carriers exercise the *ops*, not the host gate |
| `:91-93` EVM extended | "real solc/vyper-compiled bytecode untested" | **STALE (solc half)** | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` — K/K on 0.8.37 (5/5, 6/6, 11/11). Vyper half is this round's C1 claim |

**Stale count N = 5 → 0 is NOT achieved at HEAD.** No single patch repairs all five; the repairs
are spread across EX-14's candidates and EX-13's per-bullet texts, and two of the five (`C1`, the
`:62` absent-tools list, and `F3`, the JEB wording) are addressed by EX-13's `:87-88` patch and
by nothing else respectively. **This is the gap I report to the parent.**

### 3.7 EX-13's seven per-bullet patches — all CONFORMANT (one fixed mid-review)

Applied individually, each on a fresh scratch copy. Transcripts
`runs/ex13-<name>-apply-census.out`; captures `evidence/census-after-ex13-*.json`.

| patch | lines after | census | differ |
|---|---|---|---|
| `province-frontier-alternate-providers-jeb` (`203fd3ac…`) | 162 | PASS | CLEAN |
| `province-frontier-evm-solc-held` (`a9515f74…`) | 162 | PASS | CLEAN |
| `province-frontier-pe-subtypes-reserve` (`25de1d22…`) | 162 | PASS | CLEAN |
| `province-frontier-recorded-crashes-organic` (`c16fd02b…`) | 162 | PASS | CLEAN |
| `province-round4-frontier-cross-version-residuals` (`8db47d24…`) | 162 | PASS | CLEAN |
| `province-core-fallback-readers-inventory` (`1913e11e…`) | 162 | PASS | CLEAN |
| `province-round4-frontier-pe-wall-closed` — rev 1 (`32f6052d…`) | **161** | PASS | CLEAN — **not line-neutral, see §4.1d** |
| `province-round4-frontier-pe-wall-closed` — rev 2 (`1ce9b5a2…`) | **162** | PASS | CLEAN — **defect FIXED** |

All seven current revisions hold 162 lines and introduce no gated locus.

**The line-neutrality defect was fixed mid-review.** Rev 1 carried 6 minus / 5 plus (−1 net); the
revised bytes carry **6 minus / 6 plus (net 0)**, and the applied tree measures 162 lines as the
patch claims. This is the rule-#14 loop working as intended: a reviewer measurement (`32f6052d…`
→ 161 lines) was corrected by the author in a new revision (`1ce9b5a2…` → 162 lines). §4.1d is
retained as the record of the rev-1 defect.

**`province-core-fallback-readers-inventory` is a new, well-evidenced finding.** It repairs the
Core table's `:62` row — the `C1` stale row this seat independently flagged in §3.6/P-3 and
believed unrepaired. Its evidence reproduces first-hand:

```
7z → /usr/bin/7z      xxd → /usr/bin/xxd      radare2 → /usr/bin/radare2
strace → /usr/bin/strace   upx → /usr/bin/upx
cabextract, rizin, ltrace, paccheck → ABSENT
pacman -Qi: all five Install Date = Tue 13 Oct 2026 01:52:22 PM -03
```

Every element of its sweep matches: the five present tools, the four genuinely absent, and the
single batch install timestamp. So `C1` **is** repaired — my P-3 should be read as satisfied by
this patch, and the "unrepaired rows" list shrinks to `F3` alone.

**Two content observations on this set:**
- `province-frontier-evm-solc-held` writes `real solc-0.8.37 carriers (Core, arc3-r1)` — the
  **same Core-promotion defect** as EX-14's patches (§4.1). The defect is not confined to one
  seat; two independent executors produced it, which suggests the stale bullet's own wording
  invites the overclaim.
- `province-frontier-recorded-crashes-organic` cites `claims/c2/EX-13/evidence/crashpad-probe.json`.
  **No `evidence/` directory exists** under `claims/c2/EX-13/` (measured: the seven patch texts
  only). The measurement itself reproduces first-hand (§3.6 correction), but the cited transcript
  is absent — a citation that cannot be followed to the artifact it names (B-7).

## 4. Attacks / refutations attempted, with verdicts

### 4.1 SUBSTANTIVE DEFECT — EX-14's patches assert a Core promotion the corpus disclaims

**Both** EX-14 candidates write `real solc-0.8.37 carriers (Core, arc3-r1)` (demo) and
`(Core, arc3-r1/r3)` (complete).

Measured, all legs:
- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:1,33` — `RESULT-class, no Core
  promotion, no availability→holding claim`. The r3 sibling says the same at `:1,35`.
- `PROVINCE.md:54` (the Core EVM row) cites **only** `(r3-07)`; `arc3-r1` appears nowhere in
  PROVINCE.md outside EX-14's own added text (measured: `grep -n "arc3-r1" PROVINCE.md` → the
  only hits are inside the patched bullets).
- `PROVINCE.md:75-76` states the promotion rule: "Each moves to Core by a `LOG.md` entry citing
  the corpus entries that earned it." `LOG.md:1396-1415` (the arc3-loop1-round1 entry) records
  the entry landing and the map row; it records **no Core promotion**.

**Verdict: sustained, in both candidates.** The patches would write a false promotion into a
scoped file. It is a *content* defect the census structurally cannot catch (§4.2), so it is
reported as a review finding rather than a census failure.

### 4.1b SUBSTANTIVE DEFECT (extension) — the complete candidate also cites an unadmitted leg

The complete candidate adds `and Vyper 0.4.3 (r4) held` to the same bullet, asserting a leg
whose corpus entry does not exist:

- `ls corpus/knowledge/ | grep -c "arc3-r4"` → **0**; the directory holds 83 files, matching
  EX-14's own count.
- `corpus/README.md:38` (the EVM row) lists only the r1 and r3 arc3 EVM entries.

EX-14's patch names this itself under "Open dependency (named, not hidden)" and specifies the
fallback wording. **Verdict: sustained as a landing hazard** — the patch is safe only if the
parent lands C1's entry in the same commit; landed alone, that clause asserts what the corpus
cannot back. This seat did not verify C1's entry will land; the coupling is the parent's call.

### 4.1c SUBSTANTIVE DEFECT — the revised candidate's hunk 4 has a nonexistent context line

In the revision `8a0e12ff…`, hunk 4's leading line is a **context line** (space prefix) that
does not occur in the base document:

```
patch hunk 4 :  - **Cross-version residuals** — `compare-application-versions` is no longer
base PROVINCE:157 :  - **Cross-version residuals** — `compare-application-versions` still
```

Measured: I byte-compared every context line in the patch against the base file. Hunks 1, 2 and
3 match (`True`); **hunk 4 does not** (`False`). Under `patch --fuzz=0` all four hunks are
rejected (`4 out of 4 hunks FAILED`); GNU patch's default fuzz=2 papers over it
(`Hunk #4 succeeded at 157 with fuzz 1`).

**Consequence, measured on the applied tree.** Because the context line matches fuzzily, the
replacement is written against the base line, which still reads `still` — while the patch's own
first `+` line begins `refused since r2:`. The applied result reads:

```
- **Cross-version residuals** — `compare-application-versions` still refused since r2:
  r12-02 drained the row with two success legs; multi-version
```

i.e. **"still refused since r2: r12-02 drained the row with two success legs"** — a
self-contradictory sentence asserting both the stale r2-era refusal and its own falsification.
The X1 repair, whose entire purpose is to remove that stale wording, leaves `still refused since
r2` in place while appending the evidence against it.

**Verdict: sustained; hunk 4 should be rejected.** The correct context line is
``- **Cross-version residuals** — `compare-application-versions` still`` (base `:157`). The
earlier revision `16b878d3…` carried the **correct** context line and applied cleanly under
fuzz=0; this revision introduced the defect. Evidence:
`evidence/defect-ex14-v2-malformed-hunk4.txt`, transcript `runs/ex14-complete-v2-apply-census.out`.

Note the census reads PASS with zero new loci on the defective tree too — so this defect is
invisible to the gate, and would have landed as a silent content regression.

### 4.1d SUBSTANTIVE DEFECT — EX-13's `pe-wall-closed` patch is NOT line-neutral, and the census cannot see it

The patch's own "Census conformance" section claims: *"Line-neutral: 6 → 6 lines; `PROVINCE.md`
stays at 162 lines."*

Measured on its own bytes: the fenced hunk carries **6 minus lines and 5 plus lines — net −1**.
Applied on a scratch copy, `PROVINCE.md` lands at **161 lines**, not 162.

Why the census still reads PASS — and this is the important part:

- The only declared `PROVINCE.md` row carrying a line-number assertion is
  `("PROVINCE.md", 119, 131, "DATED", 119, r"verified 2026-10-13")` — its marker is asserted **at
  line 119**.
- The edited bullet sits at **139-144**, i.e. *below* 119, so deleting a line there does not move
  the marker. Every declared PROVINCE row ends at or before 131; the entire region **132-162 is
  UNDECLARED**, so nothing is asserted about it.
- Measured: `census --root <scratch>` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, and my differ reports `CLEAN — 0 new, 0 removed, 0 moved`. The census's
  `counts` row **does** record `PROVINCE.md lines 162 → 161`, but that row is not part of the
  PASS/FAIL predicate — a consumer reading only `VERDICT: PASS` would not see it.

The asymmetry is the finding: an **insertion above** line 119 trips the marker assertion
(measured, my plant D: `SCOPE-ERRORS ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from
''"]`, FAIL exit 1), while a **deletion below** line 119 trips nothing. The claim's own
falsifiable form is "PROVINCE line count unchanged"; this patch breaks it undetected.

**Verdict: sustained against rev 1 (`32f6052d…`); FIXED in rev 2 (`1ce9b5a2…`).** The revised
bytes carry **6 minus / 6 plus (net 0)** and the applied tree measures 162 lines as claimed —
re-measured after the revision landed. §4.1d is retained as the record of the rev-1 defect and of
the detection method (count the fenced hunk's `-`/`+` lines; do not trust the patch's own
line-neutrality prose). Evidence: `evidence/defect-ex13-pe-wall-false-line-neutrality.txt`,
transcripts `runs/ex13-province-round4-frontier-pe-wall-closed-apply-census.out` (rev 1) and
`runs/ex13b-province-round4-frontier-pe-wall-closed-apply-census.out` (rev 2).

### 4.2 The census is structurally blind to that entire bullet — measured, not asserted

`evidence/census-blindness-proofs.txt`:

```
BASELINE       unit 91-93  REA_GATE=False  detections=NONE
EX-14 PATCHED  unit 91-93  REA_GATE=False  detections=NONE
BASELINE   EVM-bullet loci: NONE
EX-14      EVM-bullet loci: NONE
```
The bullet never matches the instrument's `REA_GATE` needle, so `classify()` emits zero
detections and the block produces no locus in any bucket. The census reads the **same PASS
before and after** — it neither validates nor refutes the repair. The `(Core, arc3-r1)` phrase
carries no pin, no bare version, and no `path:line` pointer, so even a gated block would not
flag it.

### 4.3 Gated-token plants — the classes the census DOES catch (and the ones it misses)

Each planted on a fresh scratch copy of the real tree; full captures in `evidence/`.

| # | plant | location | measured verdict | class |
|---|---|---|---|---|
| A | `(rea-agents@6.7.0 gate)` | `PROVINCE.md:91` (Frontier, undeclared) | **FAIL `undeclared=1`** exit 1 | caught |
| B | pointer `see ~/.kimi-code/config.toml:3298` | `PROVINCE.md:91` | **FAIL `undeclared=1`** exit 1 | caught |
| C | bare version `…untested since 6.7.0` | `PROVINCE.md:91` | **PASS, loci unchanged** | **silent miss** |
| D | one-line **insertion** at `:75` | `PROVINCE.md` | **FAIL** `scope_errors: "PROVINCE.md:119 marker 'verified 2026-10-13' absent from ''"` | caught (line-count) |
| E | append past the declared bound | `PROVINCE.md` tail | **PASS `undeclared=0`** | silent (growth is not itself a locus) |
| F | `(rea-agents@6.7.0)` in the **SKILL.md registry row** (`:390`) | `SKILL.md` | **FAIL `undeclared=1`**; differ: `SKILL.md:390 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause) block 390-390 scope None` | caught |

Findings from the matrix:
- **C is a real blind spot for C2's claim.** A stale-version repair written as a bare `6.x.y`
  inside a Frontier bullet reads PASS. The C2 repairs must therefore avoid bare version tokens
  in the Frontier, or the census cannot certify them.
- **F matters because it is the wave's own hot row.** The SKILL.md `custody-pair` row that
  EX-21/EX-24/EX-30 all patch sits at `:390`, inside the 370-line undeclared gap. Any version
  token landing there fails the census — so a future registry-row revision that pins a version
  inline (rather than only in the `:18-20` pin block) will FAIL the very gate the wave relies on.
  Neither this round's row patch does that; both were verified token-free (§3.2, §3.3).

### 4.4 FINDING — the chain's own staleness census (VZ-2) cannot grade a repair

The frozen C2 claim names two instruments: the staleness census and the census gate
(`.ufo/gates/c1-census-v10.py`). This seat ran VZ-2's census
(`claims/c2/VZ-2/evidence/province-staleness-census.py`) against EX-14's **repaired** tree:

```
SUMMARY: total=26 stale=6 adjudicated=2 current=18
STALE: F1b, F3, F5b, X1, C1, R2
```

It still reports **F1b, F5b, X1, R2** as STALE — the exact four rows the complete candidate
edits. Cause, measured in the tool's own source: each row's verdict is a **literal string**
passed at construction (`add("F1b", …, "stale", …)`; 10 literal `"stale"` occurrences), and the
only post-construction pass sets `claim_present` by substring match and then *filters*
(`stale = [r for r in rows if r["verdict"] == "stale"]`) — it never recomputes a verdict from
document content. So the tool censuses the document it was written against and is invariant to
repairs. Its `stale=6` therefore cannot be read as "the repaired tree still has 6 stale rows".

Two consequences for the chain claim:
- **VZ-2's exit code cannot certify "stale → 0".** The claim's falsifiable form ("stale count
  N → 0") has no instrument-enforced reading; only the independent content census in §3.6
  distinguishes repaired from unrepaired.
- **The two rows VZ-2 reports stale that EX-14 did not touch are genuine separate findings.**
  `C1` ("absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib`)
  is contradicted by the tool's own measurement: five of the claimed-absent tools are now
  **present** (`7z`, `xxd`, … installed 2026-10-13). That is a real PROVINCE Core-table
  staleness (`PROVINCE.md:62`) outside the Frontier scope EX-14 worked. `F3` (JEB wording) is
  the nit this seat also flagged in §3.6.

This is reported as a **finding about the instrument**, not a defect in VZ-2's authoring: its
docstring is explicit that it "MEASURES" and that "the claim's repair is judged separately".
The gap is that no instrument in the wave actually performs that separate judgment.

### 4.5 Attacks on the review instruments themselves

- **Differ false-negative check:** baseline vs baseline → `CLEAN`, 0 new / 0 removed / 0 moved.
  A no-op must not read as a defect; it does not.
- **Differ detection check:** plant A vs baseline → `NEW gated loci — 1`, verdict row
  `PASS → FAIL` flagged `CHANGED`, `RESULT: DEFECT`, exit 1. The differ is load-bearing.
- **Harness self-test:** legal same-line repair → `CONFORMANT` exit 0; identical repair with a
  gated token → `DEFECT` exit 1. Both arms exercised on the same diff shape, so the difference
  is attributable to the token, not to the harness.
- **Applier parity:** `prose-apply.py` and EX-14's independently written `apply_patches.py`
  consume the same fenced `-`/`+` format; cross-checked by EX-14 on the r3 reference patch with
  identical per-hunk outcome. Two independent appliers agreeing reduces the chance that a
  "clean apply" is an artifact of one tool's leniency.
- **Line-neutrality is load-bearing, confirmed by D:** EX-14's and EX-21's patches both hold
  line count (162 / 390). A repair that inserted a line would trip the `:119` marker assertion —
  which is why the two landed repairs are safe and any future multi-line repair is not.

## 5. Blockers

- **B-1 (chain-level, reported not resolved):** the C2 claim's "stale count N → 0" is not met at
  HEAD, and no instrument in the wave can certify it either way. The stale set at HEAD is
  `{F1b (:82-83 Godot reserve), F2 (:84-86 organic-core inventory — corrected upward after
  EX-13's falsification), F5b (:91-93 solc half), C1 (:62 absent-tools list), F3 (JEB wording)}`
  — **five** rows. EX-13 now supplies repair texts for **all five** (each census-CONFORMANT,
  §3.7), and EX-14's complete candidate covers F1b/F5b/R2/X1 but its X1 hunk is defective
  (§4.1c). So the repairs exist; what is missing is a landing that (a) picks one text per row,
  (b) avoids the Core-promotion overclaim (§4.1/§4.1b), and (c) couples C1's Vyper entry. The
  parent owns that decision.
- **B-2 (ownership boundary):** the Frontier region is undeclared in the census scope table. A
  same-commit scope re-key is required for any gated repair there, and `.ufo/gates/c1-census-v10.py`
  is chain c1's instrument — not this seat's, and not chain c2's, to edit. Patch text only (P-2).
- **B-3 (landing hazard):** the complete candidate's `Vyper 0.4.3 (r4) held` clause asserts a leg
  with no admitted corpus entry (0 `arc3-r4` files). Safe only if C1's entry lands in the same
  commit (§4.1b).
- **B-6 (patch churn):** the complete candidate was revised mid-review (`16b878d3…` →
  `8a0e12ff…`) and the revision introduced the hunk-4 defect. Any further revision invalidates
  §3.2/§3.2b/§4.1c and must be re-reviewed per rule #14; the `prose-apply.py` identity in §6 is
  stable across it.
- **B-4 (timing):** no C2 patch text existed when I began; the wave's scoped-file patches arrived
  from EX-14 and EX-13 (c2) and EX-21/EX-24 (c3). I reviewed everything that landed and named the
  gaps rather than waiting further. `seats/` at my last poll held 35 of 48 reports.
- **B-5 (not a blocker, recorded):** a fourth npx cache `9b9809298fe40d2c` holds `rea-agents`
  6.7.0 and is uncited in PROVINCE; the pinned `a1722018f28f9df2` is unchanged, so this is not
  version drift — but PROVINCE's "both versions have separate npx cache installs" wording
  undercounts the caches now present (4 hold rea-agents: 6.7.0 ×2, 6.5.0, 6.4.0).
- **B-7 (unfollowable citation):** EX-13's `recorded-crashes-organic` patch cites
  `claims/c2/EX-13/evidence/crashpad-probe.json`, but no `evidence/` directory exists in that
  seat's tree. The measurement reproduces first-hand (§3.6 correction); the cited transcript does
  not exist. Not a blocker for the repair's correctness, but the citation cannot be verified as
  written.

## 6. Identity discipline (rule #14)

Every identity below was re-derived **after** the final revision of the artifact it describes.
No artifact records its own digest inline.

| object | sha256 |
|---|---|
| `.ufo/gates/c1-census-v10.py` (instrument) | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` |
| `PROVINCE.md` (real tree, throughout) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` |
| `SKILL.md` (real tree, throughout) | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` |
| `SCORECARD.md` (real tree, throughout) | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` |
| `custody-pair.py` (r4 landed) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` |
| `custody-pair/README.md` (r4 landed) | `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186` |
| EX-14 demo patch | `507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51` |
| EX-14 complete candidate (rev 1) | `16b878d3d4af61040b036772c9b31d721070a4143b5e0a92d147e222c112db5e` |
| EX-14 complete candidate (rev 2, current) | `8a0e12ffc8c48a809d60b06e7c13a4e93f3e1af131f08e9b7914fef86b06b1b2` |
| EX-21 patched-row file | `8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf` |
| EX-24 `skill-row.diff` | `c369f73d21bc7ae2ddf62b33c3a14f70cba0d9260251862bf65da3ad984c766f` |
| EX-13 `province-frontier-*` (4) | `203fd3ac…` / `a9515f74…` / `25de1d22…` / `c16fd02b…` |
| EX-13 `province-round4-frontier-{cross-version-residuals,pe-wall-closed rev2}` | `8db47d24…` / `1ce9b5a2…` |
| EX-13 `province-round4-frontier-pe-wall-closed` rev 1 (defective) | `32f6052d92de6816bd647ec89197e604be4f659f67ae42729e3bbe945f3aaea5` |
| EX-13 `province-core-fallback-readers-inventory` | `1913e11e…` |
| VZ-2 staleness census tool | `.ufo/waves/arc3-loop1-round4/claims/c2/VZ-2/evidence/province-staleness-census.py` (read-only; run, not modified) |
| RV-4 `census-diff.py` | `d7ab95902282d86481666092a0ff3dcb434c1983f771349f0460381ffad1d32e` (re-derived after final edit) |
| RV-4 `harness/apply-and-census.sh` | `8fb48dd0e759fe99e905722de9ec6650e3b0e30b48f651ff52c96b9f5648e01f` (re-derived after final edit) |
| RV-4 `prose-apply.py` | `123d868326fa31bf68288fccd5715a5de6bcf9ccd2f0815ca29d28f6fd471d06` (re-derived after the multi-hunk fix) |
| the fourteen conformance `census-*.json` captures | all `7cb9b513412f47b07d56e085a68f3eaf8b0028d20768bd7b38ac94cead93807d` — **byte-identical**, 7197 B each; `diff` against baseline = 0 lines for every one |
| the four plant/defect captures | `07b223b9…` (plantA), `669ba0ac…` (plantB, plantD), `08af8de8…` (plantE), `6b4101f4…` (ex13-pe-wall rev 1) — each with its expected signature (§3.5) |

The three scoped files and the instrument were re-hashed at the end of the run and are unchanged
from the baseline above — this seat wrote none of them.

## 7. Files written by this seat

48 files total: this report, 3 review instruments, 29 evidence artifacts, 16 run transcripts.

- `.ufo/waves/arc3-loop1-round4/seats/RV-4.md` — this report
- `claims/c2/RV-4/{census-diff.py,prose-apply.py}` + `claims/c2/RV-4/harness/apply-and-census.sh`
  — the three review instruments (identities in §6)
- `claims/c2/RV-4/evidence/` (29 files) — baseline + every patched-tree census capture, the
  scope-gap map, the census-blindness proofs, the six plant captures, the two defect write-ups
  (`defect-ex14-v2-malformed-hunk4.txt`, `defect-ex13-pe-wall-false-line-neutrality.txt`), the
  rev1-vs-rev2 line-neutrality record, the EX-21 identity re-derivation, and the SKILL.md gated
  token attack pair
- `claims/c2/RV-4/runs/` (16 files) — harness transcripts: one per applied patch (EX-13 ×8,
  EX-14 ×3, EX-21, EX-24, EX-26) plus the synthetic detect arm

Nothing outside `seats/RV-4.md` and `claims/c2/RV-4/` was written. No git mutation. Scratch
confined to `/var/tmp/rv4-scratch/` and `/var/tmp/rv4-crashcheck/` (never `/tmp`).
