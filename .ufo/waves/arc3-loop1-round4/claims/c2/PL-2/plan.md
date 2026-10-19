# PL-2 — C2 plan: PROVINCE Frontier/surface staleness census + same-line repairs

Seat PL-2 · chain c2 · role planner · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (unchanged throughout; no git
mutation issued by this seat). Lane: devin (`devin/deepseek-v4-1-flash-max`),
the declared fallback recorded in `claims-frozen.md:11-15` after the hyper lane
returned 402 out-of-credits on all 48 seats. Scratch under `/var/tmp/pl2-r4`
(never `/tmp` — standing EDQUOT rule). Custody paths opened read-only (the
crashpad probe read a dumped copy, never a custody path). The real `PROVINCE.md`,
`SKILL.md`, `SCORECARD.md`, `corpus/**` and the instruments were only ever
**read**; every apply ran on a fresh scratch tree.

Frozen claim under plan (`claims-frozen.md:44-57`): every PROVINCE Frontier
bullet and surface-summary claim census-checked against admitted corpus state;
every stale item repaired same-line (line count held) or adjudicated NO-CHANGE
with cause; the census instrument reads PASS at the records commit; repairs land
as patch texts applied by the parent.

Base identities (re-derived at write time, rule #14):

| object | sha256 | size |
|---|---|---|
| `PROVINCE.md` (real, throughout) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | 162 lines / 19498 B |
| `SKILL.md` (real) | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | 390 lines |
| `SCORECARD.md` (real) | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` | 1580 lines |
| census instrument `.ufo/gates/c1-census-v10.py` | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | 610 lines |

Artifacts in this directory (identities re-derived after the final revision):

| file | what | sha256 |
|---|---|---|
| `plan.md` | this plan | not self-hashable — digest in the seat report |
| `gen-and-measure.py` | generator + measurement harness (rebuilds every patch text and every measurement from the real tree) | `125be8409f4c2f3bf14906877591d8b59b6016be990555649fe6dc6adb8140e4` |
| `candidate-repairs.patch.md` | the recommended repair set, 21 hunks | `0ccb7f2dfb3e2ee5c054a7a1df6466380afcfb91f1962b9f1f9c0f68976f68f9` |
| `candidate-with-s5.patch.md` | 21 hunks + the optional S5 pointer refresh | `0c28db8f7e95f23d803bcbfcfc78014c22d4057f7185da12055caa50aec9105b` |
| `candidate-coupled-vyper.patch.md` | 21 hunks + the Vyper-naming coupling hunk | `a98df66c8274ddd3eaeec069e9adcd06b9a4bd6e9a36ec86d232ab5ab5b90199` |
| `corpus-erratum-coupled.patch.md` | the corpus erratum coupled to hunk C46 | `12a7ceb3a62a526c9a04c33c114da1e2e466797f7d649d25723ab910e1832ca2` |
| `evidence/` | every measurement transcript quoted below | — |

Candidate identities (patched `PROVINCE.md`, measured by the harness):

| variant | sha256 | lines |
|---|---|---|
| baseline (scratch copy of the real file) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | 162 |
| `candidate-repairs` | `8cb86b35050f09b6fa4581f140e47ceb3ef97ce0c9fa6e2d2091b203016cc995` | 162 |
| `candidate-with-s5` | `9e5dab4dc5fa54b62d37bca9fbe371555053b6291ecab5760723b8aa9d1dab8e` | 162 |
| `candidate-coupled-vyper` | `6fd9059f3186f5b399e874cf62cf37df7e4029f2463e5a85186453dfd141fa36` | 162 |

## 0. Verdict

The census unit (line-keyed, needle-based) and the staleness unit (prose-truth)
are **different units**, and the frozen claim needs both. This plan separates
them explicitly, because two of this wave's instruments conflate them:

1. **Gate unit — the census instrument.** It grades version/pin/pointer *loci*
   and is structurally blind to prose (RV-4's §4.2 blindness proof; re-derived
   here: the EVM bullet matches no `REA_GATE` needle, so it yields zero
   detections on both sides of any repair). Its job here is narrower and
   absolute: **the repair set must not move the gate.** Measured: PASS
   `0/0/0/0` before and after, 16/16 assertions byte-identical (all five
   verdict-surface captures in RV-4 §3.5 agree; this seat's own differ run
   agrees again on the final bytes).
2. **Staleness unit — the claim's own census.** Prose-vs-corpus truth. Measured
   here by a per-item adjudication (below), independently of VZ-2's row set.

Result: **9 items repaired same-line in 21 hunks** (6 Frontier items — F1b, F2,
F3, F5b, R2, X1 — in 18 hunks; 3 Core-sweep rows — C46, C50, C62 — in 3 hunks),
**2 items adjudicated NO-CHANGE with cause** (S5's dead pointer, default voice
with a measured refresh variant; F5c's Vyper deferral, with a measured coupling
variant), and **2 coupling rules** (C1's entry ↔ the Vyper hunk; the corpus
erratum ↔ C46). Every repair holds the line count at 162, introduces **zero**
`rea-agents@` pins, zero bare `6.x.y` versions, zero `path:line` pointers in the
new text (token sweep, `evidence/residual-and-token-sweep.txt`), and removes
every stale literal the wave's three censuses independently named:

```
Reserve: 91MB Godot ARM64 template                      gone
all 3 organic cores                                     gone
JEB (unprobed)                                          gone
real solc/vyper-compiled bytecode untested              gone
Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`             gone
probe-refused since r2                                  gone
pacman pairs beyond expac unexercised                   gone
absent: `7z`                                            gone
35 features incl. PyGhidra/BSim                         gone
```

**The one sentence the parent should not miss:** two of the wave's rival patch
voices (EX-15's A6a/A6b and EX-14's demo/complete) write `(Core, arc3-r1/r3)` /
`held` into the EVM bullet. Both corpus entries disclaim exactly that
(`2026-10-19-arc3-r1-evm-real-solc.md:1,33` and
`2026-10-19-arc3-r3-evm-optimizer-shapes.md:1,35`: "RESULT-class, no Core
promotion"), and `PROVINCE.md:75-76` requires a `LOG.md` promotion entry that
does not exist. This plan's wording says "recovered K/K (arc3-r1/r3,
RESULT-class)" — true, promotion-neutral. **Do not land a Core-promotion claim
into a scoped file** (RV-4 §4.1/§4.1b sustained; VZ-2's re-apply concurs).

## 1. Method (the plan's first deliverable)

### 1.1 The census unit, precisely

Two independent axes; a row is only *stale* when the second fails:

- **Axis 1 — gate conformance (mechanical, mandatory).** After any repair:
  `python3 .ufo/gates/c1-census-v10.py --root .` must read PASS and the
  locus-level differ (`claims/c2/RV-4/census-diff.py`) must read CLEAN against
  the baseline capture. Constraints that follow, each measured (RV-4 §4.3,
  re-derived here in §4):
  - the repaired region (72-118, 132-162) is **UNDECLARED** in the scope table;
    a version/pin/pointer token there reads `undeclared=1` FAIL — proven live
    by this seat's planted-pin control (`VERDICT: FAIL undeclared=1`);
  - the line count must stay 162 — an insertion shifts the `:119` DATED marker
    and fails `SCOPE-ERRORS` (RV-4 plant D);
  - bare-version tokens are the **silent** class (RV-4 plant C: reads PASS);
    the token sweep in §4 covers what the gate cannot.
- **Axis 2 — prose truth (adjudicated, per item).** Each checked item resolves
  to one of: **current** (evidence re-derived this round), **stale→repair**
  (with the falsifying evidence), **adjudicated NO-CHANGE** (with cause), or
  **deferred** (coupled to a same-commit landing). §2 is the per-item table.

### 1.2 What "census-checked" can and cannot be mechanized

Measured this round, so the parent lands with eyes open:

- **Mechanizable:** gate conformance (above); the removal of named stale
  literals (the residual sweep); token-freedom of new text.
- **Not mechanizable in this wave's instruments:** prose truth. VZ-2's
  `province-staleness-census.py` carries its verdicts as **corpus-keyed
  constants** — its `--province` argument feeds only the phantom-row check, not
  the verdicts. Measured: on all three patched trees the SUMMARY line is
  *invariant* (`stale=9`), while its `claim_not_found` list flips from `[]`
  (baseline) to exactly the repaired anchors (candidate). **Its useful signal
  on a patched tree is the phantom list, not the STALE list.** The chain's
  verdict must therefore rest on reviewer adjudication (RV-4, EX-15, this
  plan) plus the two mechanical axes — and the round record should say so
  rather than implying the gate certifies prose.

### 1.3 Adjudication rules (for the parent and for RV-5)

1. **Evidence outranks text.** An item is repaired only when a corpus path or a
   re-run command contradicts it. Live-state items (env keys, tool presence,
   catalogs) are re-derived live, never trusted from a corpus entry.
2. **Repair same-line, token-free, citation-preserving.** The replacement keeps
   the line's citation furniture (`[r5-audit C1: …]`, `(Core, r3-07)`) unless
   the citation itself is false; never introduce a token (Axis 1).
3. **No promotion via Frontier prose.** A RESULT-class corpus entry does not
   become Core by being cited in a bullet; only a `LOG.md` entry does
   (`PROVINCE.md:75-76`). Wording must not assert `held`/`(Core, …)` for a
   RESULT-class leg.
4. **Unvisited ≠ absent.** "untested" claims must be narrowed, not deleted,
   when only part of the class moved (Vyper stays named until C1 lands).
5. **NO-CHANGE is a first-class verdict** and needs the same evidence bar as a
   repair; it is recorded in the round report, not silently dropped.
6. **Coupling is declared, not assumed.** Any repair whose truth depends on
   another chain's same-commit landing is emitted as a separate variant with
   the dependency named (here: the Vyper naming, and C46's corpus erratum).
7. **Adjudicate, don't smooth.** Where two seats disagree (VZ-2 F2 "adjudicated"
   vs EX-15 A4 "repair"; EX-15 D1 NO-CHANGE on JEB vs this plan's repair), the
   disagreement and the ruling are both recorded.

## 2. Per-item census and dispositions

Checked set: all 5 Frontier bullets (`:82-93`), the 9 post-unlock Frontier
bullets (`:133-162`), the surface-summary/drift-prone blocks (`:8-26`), and the
Core table rows the seat line's sweep reaches (`:46`, `:50`, `:62`). Evidence
abbreviations: **r1** = `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`,
**r3** = `…-arc3-r3-evm-optimizer-shapes.md`, **r7** =
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`, **r8** = its r8 erratum
(same file) + `.ufo/waves/arc2-loop1-round8/E2.md`, **r10** = r7's r10 erratum,
**r12-02** = `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md`,
**r4-10** = `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`, **crash** =
`corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md`.

### 2.1 Frontier 73-93 (the frozen claim's letter)

| id | item (`PROVINCE` line) | verdict | evidence / cause |
|---|---|---|---|
| F1a | PE subtypes both held (82-83) | current | r3-08 entry present |
| F1b | "Reserve: 91MB Godot ARM64 template" (83) | **stale→repair** | `corpus/README.md:175` "CLOSED, not frontier"; r7 held it (75,218 procs); r8 control OOM at 9G |
| F2 | "all 3 organic cores" (84-86) | **stale→repair** | live `coredumpctl`: 72 non-godot rows; a sub-cap organic core exists (below) |
| F2b | "Needs a cap-raising knob … neither exists" (85-86) | **stale→repair (premise)** | cap knob still absent (crash:22) — kept; but the *universal* is false: PID 1857 `chrome_crashpad_handler` dumps 17,608,704 B < 33,554,432 and `inspect-recorded-crash` completed on it, exit 0, `ev_813eed97…` (this seat's probe, `evidence/crashpad-probe-ev813eed97.json`; EX-17's probe agrees) |
| F3 | "IDA …, Hopper (absent), JEB (unprobed)" (87-88) | **stale→repair (JEB word)** | `r2-provider-capability-matrix.md:99` records `inspect-jeb-client` → `capability_unavailable` — JEB **was** probed. IDA/Hopper halves current (env unset, no binary). EX-15 D1 adjudicated NO-CHANGE on the word; this plan repairs it — see §5 A3 |
| F4 | macOS-only surfaces (89-90) | current | `r2-provider-capability-matrix.md:26-41` (10 `unsupported_host` ops); synth carriers exercise ops, not the host gate |
| F5a | synthetic-dispatcher selectors held (91-92) | current | r3-07 |
| F5b | "real solc/vyper-compiled bytecode untested" (92) | **stale→repair** | r1 recovered K/K on real solc-0.8.37 (5/5, 6/6, 11/11); r3 extended (optimizer on/off). **The named debt** (`claims-frozen.md:45-47`) |
| F5c | "selectors stay bare hashes" (93) | current (with the Vyper split) | no signature DB exists; the Vyper leg is C1's this-round claim → variant hunk, §3 |

### 2.2 Post-unlock Frontier 133-162

| id | item | verdict | evidence |
|---|---|---|---|
| R1 | RISC-V: "full 29 MB EXEC … 10,766 functions @900 s cap" (135-137) | current | `2026-10-13-r5-01-riscv-bypass.md` (10,766) |
| R2 | ">90 MB PE scale wall … Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` …" (139-144) | **stale→repair** | r7 (mitigated hold, validated analyzer-disable recipe), r8 (no-disable control OOM-killed at 9G), r10 (rerun id-stability **STABLE**, not unknown), `corpus/README.md:175` |
| R3 | `.jsc`→source mapping (145-146) | current | r4-07 (Ignition held); no mapper exists |
| R4 | sasquatch (147-148) | current | `2026-10-13-r4u-03-unblob-extract.md`; `command -v sasquatch` absent (re-checked) |
| R5 | adb 22/24 verbs (149-150) | current | `2026-10-13-r4u-06-adb-surface.md` (2 serial-free) |
| R6 | signal/1Password scale (151-156) | current | r4-05 (38.5 MB, 1,866 entries), r4-06, r4-14 |
| X1 | "`compare-application-versions` still probe-refused since r2" (157-158) | **stale→repair** | r12-02: L203 discharged both classes (`ev_7a8d0ec4…` JS verdict; `ev_b5fc998f…` managed) |
| X2 | "multi-version pacman pairs beyond expac unexercised" (158-159) | **stale→repair** | r4-10: `op` 2.34.1→2.40.0 (41–43 MB Go ELF) is a cached pacman pair, already in Core row 52 — the Frontier clause contradicts Core |
| X3 | `[r5-audit C1: …]` citation furniture (159-160) | repair (wording) | kept, compressed to hold the line count |

### 2.3 Surface summary + drift-prone (8-26) and the Core sweep

| id | item | verdict | evidence / cause |
|---|---|---|---|
| S1 | per-client pins (8-11, 15-18) | current | live: devin `:7`, omp `:8` = 6.5.0; kimi 6.7.0 (one occurrence) |
| S2 | 6.7.0 207/153, `af39310c…` (10-11) | current | live `rea doctor` 6.7.0: 207/153/`af39310c` (`evidence/doctor-670.txt`) |
| S3 | 6.5.0 207/153, `805433f1…` (9-10, 19-21) | current | live doctor 6.5.0: 207/153/`805433f1` |
| S4 | 6.4.0 historical 170/127, `25802f6d…` (12, 22-23) | current | live doctor 6.4.0: 170/127/`25802f6d` |
| S5 | `~/.kimi-code/config.toml:3298` pointer (18) | **adjudicated NO-CHANGE** (refresh optional) | live file `bc66d543…` is 3570 lines; the pin sits at `:3546`, stanza `:3544`; `:3298` holds `max_context_size`. The clause is receipt-stamped ("at the 17:55:49Z receipt") and names its own supersession chain; the named receipt exists in-repo. EX-15 A1 drafted the same repair. Both voices measured (§3, variant); this plan's default is NO-CHANGE because the pointer is self-declared perishable — but the variant is one apply away |
| S6 | installed shared skill v42/207, `c8639823…` (24) | current | `sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md` → `c8639823…` (re-derived) |
| S7 | Ghidra/JDK reverify block (25) | current | `application.version=12.1.4`, build `2026-Sep-21 1613 UTC`; `java -version` 21.0.12.1 (re-derived) |
| C46 | "35 features incl. PyGhidra/BSim" (`:46`) | **stale→repair** | live `ls -1 Ghidra/Features | wc -l` = 34; the r1 corpus entry's own list holds 34 names and matches the directory exactly — the "35" is a miscount propagated from that entry's claim line. **Coupled**: corpus erratum required same-commit (`corpus-erratum-coupled.patch.md`) |
| C50 | "pacman … corpus 1556 signed archives" (`:50`) | **stale→repair (as-of)** | live `ls … | wc -l` = 1350 (cache churns); repaired to "1556 … at the 2026-10-13 scan (1350 today)". EX-15 D3 adjudicated NO-CHANGE; this plan repairs — see §5 A4 |
| C62 | "absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib" (`:62`) | **stale→repair** | live `command -v`: `7z` (=`7zip 26.03-1`), `xxd` (=`tinyxxd 1.3.16-1`), `radare2` (6.2.0-1), `strace` (7.0-1), `upx` (5.2.0-1) all present, all installed 2026-10-13 13:52 — after the r1 scan. Absent now: `cabextract`, `rizin`, `ltrace`, `pacman-contrib` |

Also re-checked and current (no hunk): Core row 52's `op` pair clause (r4-10 —
it is the *Core* row that already carries the pair, which is why X2 is
contradictory), row 48's jq numbers (crash-free; corpus `2026-10-13-rea-live-jq-e2e.md`
agrees: 30 segments / 167 procedures / 190 strings), row 47 "sole Java on host"
(re-checked: `/usr/lib/jvm` holds only `java-21-openjdk` + two symlinks to it).

### 2.4 Items deliberately NOT repaired (named, not smoothed)

- **Row 49's host-asar inventory** ("obsidian ×2, signal, 1Password, electron39/43
  stubs, typora ×3"): live sweep adds `/usr/lib/chatgpt/resources/app.asar`
  (mtime 2026-10-16, i.e. post-r1) and `/usr/lib/obsidian/obsidian.asar`. The
  cell's own prose ("asar archives pinned on host") is a scan record, not a
  count; the r4u-03-style "as of" repair was judged low-value churn on a DATED
  row. **Recorded for the next scan round.**
- **The r4u-06 "22/24"** and other DATED-row counts: untouched (DATED rows are
  historical by construction; the census asserts their markers).
- **`MINT.md` drift** (`npx -y rea-agents@6.4.0 mcp`, the mint-era pin):
  MINT.md is outside the census scope and outside this claim; noted for the
  round report only.

## 3. Repair texts (delivered artifacts)

Format: prose patch, fenced `-`/`+` hunks, target named by backticked path —
the format `claims/c2/RV-4/prose-apply.py` consumes (and EX-15 uses). Every
hunk is same-line; the `@@ line N @@` markers are informational (the applier
matches by content). All four files were generated from the real bytes by
`gen-and-measure.py` and measured (§4).

- **`candidate-repairs.patch.md`** (recommended) — 21 hunks: 18 Frontier
  (`:83-93`, `:139-144`, `:157-160`) + 3 Core-sweep (`:46`, `:50`, `:62`).
  Hunk C46 (the `34` fix) must land with `corpus-erratum-coupled.patch.md` in
  the same commit, or neither.
- **`candidate-with-s5.patch.md`** — the same 21 + the `:18` pointer refresh
  (`:3298`→`:3546`). Take this voice if the parent prefers EX-15 A1-repair's
  semantics; the clause keeps its 17:55:49Z receipt stamp either way
  (the pointer-table's `prov18-stamp-named` / `prov18-pin-value` predicates were
  re-checked HIT on all three variants, `evidence/pointer-table-check.txt`).
- **`candidate-coupled-vyper.patch.md`** — the 21 + the `:93` Vyper-naming hunk
  ("the Vyper leg landed same-commit (arc3-r4)"). **Land only if C1's
  `corpus/knowledge/2026-10-19-arc3-r4-*` entry lands in the same commit**;
  otherwise the base variant's "the Vyper leg is this round's C1 claim" is the
  true text.
- **`corpus-erratum-coupled.patch.md`** — the append-only corpus erratum for
  `2026-10-13-ghidra-install.md` (34, not 35), coupled to C46.

Line-count proof for all variants: 162 → 162 (`wc -l`, §4 table). No hunk
touches `:40-45`, `:119` or any DATED marker line.

## 4. Before → after measurement (the claim's falsifiable unit)

Runner: `gen-and-measure.py` (rebuilds each variant from the real file, applies
to a fresh scratch tree, runs the census instrument, the locus differ, VZ-2's
instrument, the residual/token sweep, and the planted-pin control). Full
transcript `evidence/measure-run.txt`; harness re-run of the delivered patch
text through RV-4's own `apply-and-census.sh`: `evidence/rv4-harness-run.log`
(21/21 hunks applied, `CONFORMANT — census PASS, no new gated locus`).

| measurement | baseline | candidate | candidate-s5 | candidate-coupled |
|---|---|---|---|---|
| `PROVINCE.md` lines | 162 | **162** | **162** | **162** |
| sha256 | `d075a3c6…` | `8cb86b35…` | `9e5dab4d…` | `6fd9059f…` |
| census verdict | PASS 0/0/0/0 | **PASS 0/0/0/0** | **PASS 0/0/0/0** | **PASS 0/0/0/0** |
| differ vs baseline | — | **CLEAN** | **CLEAN** | **CLEAN** |
| assertions (differ) | 16 | 16 | 16 | 16 |
| new/removed/moved loci | — | 0/0/0 | 0/0/0 | 0/0/0 |
| residual literals (§0 list) | 9 present | **0 present** | 0 present | 0 present |
| token sweep on new text | — | **empty** | empty | empty |
| VZ-2 phantom rows | `[]` | F1b,F2,F2b,F5a,F5b,F5c,X1,X2,R2 | +S5 | +F5c-coupling |
| pointer-table PROVINCE predicates | 2 HIT | 2 HIT | 2 HIT | 2 HIT |
| SHONEN `shonen-province-range` (88-116 clause) | HIT | HIT | HIT | HIT |
| planted-pin control | — | **FAIL undeclared=1** (gate live) | — | — |

Reading of the two columns that matter: the gate column is **byte-identical**
to the baseline (the differ prints every verdict row with no `CHANGED` flag),
and the prose column removes exactly the stale anchors while VZ-2's phantom
list proves *which* anchors left. `stale N → 0` in the claim's sense is
established by §2 (11 repairs + 4 adjudications, every one evidenced), not by
VZ-2's constant SUMMARY — §1.2 records why.

## 5. Attacks / refutations attempted (verdicts)

| # | attack | verdict |
|---|---|---|
| A1 | "the repair set moves the gate" | **refuted** — PASS/CLEAN on all three variants; 16/16 assertions unchanged; RV-4's five-capture byte-identity result and this seat's differ agree |
| A2 | "the gate is vacuous here (a blind run would PASS anyway)" | **refuted** — planted-pin control on the repaired text reads `FAIL undeclared=1`, exit 1; RV-4's plants A/B/D/F reproduce four further caught classes |
| A3 | "the bare-version class is covered by the gate too" | **refuted** — RV-4 plant C (a bare `6.x.y` inside the Frontier) reads PASS, loci unchanged. Hence the explicit token sweep; hence rule 2 in §1.3 |
| A4 | "EX-15's NO-CHANGE on JEB is right; 'unprobed' is only a wording nit" | **partially sustained, overruled** — the operative claim (no engine) does hold, and EX-15's cause is sound. But "unprobed" is falsified by `r2-provider-capability-matrix.md:99`, and the repair is one same-line word at zero gate cost; a census whose unit is "every bullet checked" should not leave a falsified word when the fix is free. Ruling: **repair** (F3), disagreement recorded per rule 7 |
| A5 | "EX-15's D3 NO-CHANGE on the 1556 count is right (cache churn is not lane state)" | **partially sustained, overruled** — the cause is real; but the row presents 1556 as the live corpus ("pacman `.pkg.tar.zst` corpus 1556 signed archives") and the live number is 1350. The "as of" repair keeps the receipted number *and* states the live one; it changes no pin and no count the census grades. Ruling: **repair** (C50) |
| A6 | "VZ-2's `adjudicated` on F2 settles it" | **refuted** — VZ-2's adjudication is about the *exemplar pointer* (waybar rows now `missing`); this plan's F2/F2b repairs are about a *different falsified universal*: "all 3 organic cores exceed the cap". A 17.6 MB organic core now dumps, and `inspect-recorded-crash` completed on it (exit 0, `ev_813eed97…`) — the bullet's premise "no organic core fits the cap" is false, which no exemplar-pointer reading reaches. Recorded as a distinct row (rule 7) |
| A7 | "the Vyper half of F5b can be repaired now (C1 measured it in the wave tree)" | **refuted at HEAD** — `corpus/knowledge/` holds 83 files and no arc3-r4 entry; `corpus/README.md:38` lists only r1/r3. The naming variant exists precisely so the parent can couple the landing; the base variant is true without C1 |
| A8 | "the `35`-features repair is safe alone (it only touches PROVINCE)" | **refuted** — the falsified number originates in `2026-10-13-ghidra-install.md`'s own claim line; repairing PROVINCE alone leaves the corpus self-contradictory in the same commit. Coupled erratum emitted (rule 6) |
| A9 | "S5's dead pointer is caught by the census" | **refuted** — `classify()` collects pointer loci only when a block carries no `@`-pin, so `ptr_check` never runs on `:18` (EX-15's direct call: `ptr_check('~/.kimi-code/config.toml', 3298, …)` → `('stale', …)`, unreached). Named as a reviewer-enforced residual in §2.3 and §6 |
| A10 | "the patch text cannot be applied by the parent's tooling" | **refuted** — the delivered file was run through RV-4's independent `apply-and-census.sh`/`prose-apply.py`: 21/21 hunks applied by content match, patched sha `8cb86b35…` (identical to this seat's own tree), verdict CONFORMANT |

## 6. Residuals and blockers (named)

1. **No prose-truth instrument exists.** The gate cannot see prose; VZ-2's
   instrument grades the *before* text against corpus constants. The claim's
   "census-checked" half is reviewer-enforced (RV-4, EX-15, this plan), and the
   round report should say so. A future round could add a `--candidate` mode to
   VZ-2's instrument that re-evaluates verdicts against the patched text — out
   of scope here (not this seat's instrument).
2. **S5's dead pointer** is gate-invisible by construction (A9). The variant
   exists; if NO-CHANGE is taken, the round report carries EX-15's
   A1-nocause text as the cause.
3. **Row 49 host-asar inventory** — new asars since the r1 scan (chatgpt,
   obsidian.asar) unrecorded; deferred with cause (§2.4).
4. **Coupling is a landing-order constraint, not a blocker:** C46 ↔ corpus
   erratum; the Vyper hunk ↔ C1's entry; both variants measured so either
   order is executable with a known-true text.
5. **Seat-poll note:** at this seat's last poll the seats dir held 45/48
   reports; all c2 claim dirs relevant here (EX-14, EX-15, EX-16, RV-4, VZ-2,
   SC-2's drafts) were present and read. RV-5/CR-2 had not landed; this plan
   needs neither.

## 7. Application recipe for the parent

```bash
# 1. verify the base identity (refuse to apply to a moved base)
sha256sum PROVINCE.md    # expect d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad

# 2. apply the chosen voice on the real tree (or through the harness first)
python3 .ufo/waves/arc3-loop1-round4/claims/c2/RV-4/prose-apply.py \
  .ufo/waves/arc3-loop1-round4/claims/c2/PL-2/candidate-repairs.patch.md .

# 3. re-derive and measure at the landing tree
wc -l PROVINCE.md        # expect 162
sha256sum PROVINCE.md    # expect 8cb86b35050f09b6fa4581f140e47ceb3ef97ce0c9fa6e2d2091b203016cc995
python3 .ufo/gates/c1-census-v10.py --root .                    # expect PASS 0/0/0/0, exit 0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .           # expect findings=0 exit=0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict  # expect clean findings=0 exit=0

# 4. if hunk C46 is in the voice, land the coupled corpus erratum in the SAME commit
# 5. re-run command A at the work commit; PROVINCE is outside its read set — expect no change
```

## 8. Identity discipline (rule #14)

Every identity above was re-derived **after** the last revision of the object it
describes: the five patch-text/generator digests and the three candidate-tree
digests were taken at 2026-10-19 11:29 -03:00 (14:29Z) from the final bytes;
the real tree's
three scoped files and the instrument were re-hashed at the same sitting and
are unchanged from §0's table. The harness run in `evidence/` was re-executed
after the last wording edit (log sha `5e9057ea…`). No artifact records its own
digest inline.
