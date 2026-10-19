# frontier-census — PROVINCE Frontier/surface staleness census (part 1: every Frontier bullet vs the corpus)

SEAT EX-11 | chain c2 | executor | wave `arc3-loop1-round4`.
Repo HEAD at work: `015e1bab914713568f339fd53999bc180459cc40` (re-derived: `git rev-parse HEAD`).
`PROVINCE.md` measured at sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. Scratch `/var/tmp/ex11` (never `/tmp`). PROVINCE read-only; no git mutations.

This is **part 1** of the C2 census — the `## Frontier` + `### Round-4 frontier`
bullets. Part 2 (the surface-summary claims, lines 8–26) is a sibling seat's
scope; where the two touch (the S-row style) I note the overlap rather than
claim it.

## The instrument

Every bullet is checked as a (claim, contradicting-or-supporting evidence,
verdict) triple. Evidence is a corpus path plus the exact string, or a live
command re-run in this seat. Verdicts: **STALE** (the bullet's text asserts
something the admitted corpus state contradicts), **CURRENT** (corpus supports
it as written), **ADJUDICATE** (the text is defensible but reads as a live
claim when it is a historical/design statement, or a mixed bullet where one
half is stale and the other true — the ruling is recorded, not silently
repaired).

Companion instruments (both already landed by siblings, used here read-only):
- `.ufo/waves/arc3-loop1-round4/claims/c2/VZ-2/evidence/province-staleness-census.py`
  — VZ-2's independent row set (its anchors overlap mine on F1b/F2/F3/F5b/X1/X2).
- `.ufo/gates/c1-census-v10.py` — the chain's gate; it checks version/pin loci,
  **not** Frontier prose, so a PASS from it is not a certificate for this census.

## Verdict table — `## Frontier` (lines 73–93)

| # | bullet (line) | claim as written | evidence | verdict |
|---|---|---|---|---|
| F1a | PE subtypes (82) | "x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136 procedures)" | `corpus/knowledge/2026-10-13-r3-pe-arm64.md:59` — `analyze cli-arm64.exe` → `ev_f4e02f93…`, 7 segs / 136 procs / 77 strings | **CURRENT** |
| F1b | PE subtypes (83) | "Reserve: 91MB Godot ARM64 template, ARM64X hybrids" | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` — same target (sha256 `7a2ccd68…`) HELD, 75,218 procs; `corpus/README.md:175` "CLOSED, not frontier" | **STALE** |
| F2a | Recorded crashes (84) | "mechanism held (Core)" | `corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md` — full provisioning recipe + e2e evidence | **CURRENT** |
| F2b | Recorded crashes (84–85) | "all 3 organic cores exceed the cap (waybar 434MB)" | live: `core.chrome_crashpad…1857` = 17,608,704 B < 33,554,432 B cap, `inspect-recorded-crash` RC=0, `ev_cde93acb…` (`evidence/crash-probe-crashpad-under-cap.json`); waybar core no longer in the store (`ls /var/lib/systemd/coredump \| grep -c waybar` → 0) | **STALE** |
| F2c | Recorded crashes (85) | "Needs a cap-raising knob or partial-core intake — neither exists" | live `inspect-recorded-crash --schema` → only `path` + `debuggerContext`; oversize refused typed `out_of_range` "exceeds 33554432 bytes" (`evidence/oversize-refusal-33554432.json`) | **CURRENT** |
| F2d | Recorded crashes (86) | "Retention decays oldest-first" | live: the waybar/localsearch cores cited by r2 are absent from the store while newer godot cores remain — consistent | **CURRENT** (weak; single-store observation) |
| F3 | Alternate providers (87–88) | "IDA (unset), Hopper (absent), JEB (unprobed)" | r2 matrix `:99` records the **live** JEB refusal probe (`capability_unavailable`/`unsupported_provider`, "fetch failed"); r12-02 L201 re-verified. Live this wave: `:8425` closed, `REA_JEB_MCP_URL` unset, `/opt/hopper/bin/Hopper` absent | **STALE** (JEB half only) |
| F4 | macOS-only surfaces (89–90) | "Mach-O/plist/LLDB/asset-catalog ops report `unsupported_host` on Linux" | live `capabilities --format json` (6.7.0): `native-macos` groups all `available:false`, `availability_code:"unsupported_host"` (`evidence/capabilities-6.7.0.json`); `corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md:142` refusal class | **CURRENT** |
| F5a | EVM (91) | "selectors held on synthetic dispatcher (Core, r3-07)" | `corpus/knowledge/2026-10-13-r3-evm-interface.md` Summary — 3 planted ERC-20 selectors recovered | **CURRENT** |
| F5b | EVM (92) | "real solc/vyper-compiled bytecode untested" | solc: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` + `…arc3-r3-evm-optimizer-shapes.md` (K/K, optimizer on/off). vyper: this wave `claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json` — vyper 0.4.3 carrier, **15/15 K/K**, `ev_405e2a2a…`, decoded runtime sha256 `57d6fd0a…`; 6.7.0 `ev_470be5f5…`; raw `ev_83a6f336…`; planted K=15 pre-compile (`planted-K.json`) | **STALE** (both halves; the frozen claim's named debt) |
| F5c | EVM (92–93) | "selectors stay bare hashes (no signature DB → no name resolution)" | `corpus/knowledge/2026-10-13-r3-evm-interface.md:142` — same statement; no corpus entry claims a signature DB | **CURRENT** |

## Verdict table — `### Round-4 frontier (post-unlock)` (lines 133–162)

| # | bullet (line) | claim as written | evidence | verdict |
|---|---|---|---|---|
| R1 | RISC-V analysis (135–138) | "`target_unavailable` gate pinned (`binaryTarget.js:105` ELF e_machine allowlist), bypassed via e_machine patch + language override"; full 29 MB EXEC via direct `analyzeHeadless` (10,766 functions @900 s) | entry's own numbers reproduce (`corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md`). **But the gate wording is r5-01-pin-specific**: the pin it measured has `binaryTarget.js` 237 lines / md5 `b7f89a09…` with no 243 case; the live pin's copy is 379 lines / md5 `1ff13b45…`, branches on `architecture === "riscv"` (`:118`), and `elfFixedHeader.js:63` returns `"riscv"`. Live end-to-end, **no override**: a RISC-V ET_EXEC with the double-float ABI analyzes RC=0, `ev_a572363e…`, `architecture:"riscv"`, 31 segments (`evidence/r1-live-pin-riscv-exec.json`); soft-float ABI and PIE are refused at the **provider** layer with typed specific reasons. Direct-`analyzeHeadless` leg unaffected | **STALE** (parse-gate half; direct-Ghidra half CURRENT) |
| R2 | >90 MB PE scale wall (139–144) | "hits REA's ~900s internal session deadline … still progressing at kill (r4-12). **Next:** raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a 2-5MB PE." | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` — the wall **FALLS**: 75,218 procs, 1424.663 s, 9 G cap, analyzer-disable recipe, `ev_a4aa9b0d…`; r8 erratum — natural control OOM-killed at 9 G in 4m42.945s ("no natural hold exists at this cap"); `corpus/README.md:175` "CLOSED, not frontier"; `LOG.md:1363` rerun id-stability closed at r10 | **STALE** (the "Next:" plan is superseded; the r4-12 mechanism is retained as historical) |
| R3 | `.jsc` → source mapping (145–146) | "Ignition disassembly held; a View8/jsc2js-style mapper is the next frontier" | `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md:208` — same next-step; no later entry claims a mapper | **CURRENT** |
| R4 | sasquatch (147–148) | "unblob's squashfs recursion extractor (AUR-only); 7z fallback covers the carved-image path today" | `corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md:176-177` — carve-then-7z pipeline verified; live: `command -v sasquatch` absent, `/usr/bin/7z` = 7zip 26.03-1, `7z i` lists SquashFS, `pacman -Ss sasquatch` empty | **CURRENT** |
| R5 | adb device surface (149–150) | "22/24 verbs need a live device/emulator; `collect-adb-bugreport` blocks ~10min on dead serial" | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` Summary — 19/22 `unsupported_target`, bugreport 600 s bound; live: `adb devices` → empty list, daemon killed, `:5037` closed | **CURRENT** |
| R6 | Signal/1Password-scale asar (151–156) | 1Password 40.7 MB asar + 188 MB core mapped; signal 38.5 MB (1,866 entries) mapped via scoped directory run; stripped Rust `.node` addons down to neon registration | `corpus/knowledge/2026-10-13-r4-06-1password-asar.md` (40,708,328 B); `…r4-05-signal-asar.md` (1,866 entries; `ev_f9b4493a…`); `…r4-14-libsignal.md` (neon-1.1.1 attribution); live: signal asar present, 38,465,187 B; 1Password asar at `/opt/1Password/resources/app.asar` | **CURRENT** |
| X1 | Cross-version residuals (157–160) | "`compare-application-versions` still probe-refused since r2; multi-version pacman pairs beyond expac unexercised" | `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md:213` — "WAS TRULY-OPEN, **NOW EXERCISED**" (JS-graph diff 10 changed / 208 unknown); `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:15` — pacman pairs `op` 2.34.1→2.40.0 and `qpdf` 12.3.2→12.4.1 exercised | **STALE** |
| X2 | Cross-version residuals (158) | "multi-version pacman pairs beyond expac unexercised" | same r4-10 evidence as X1 | **STALE** (subsumed by X1) |
| G1 | Operator-gated (161–162) | "IDA, Hopper, JEB — all absent" | live: `REA_IDA_MCP_CONFIG` unset, `HOPPER_LAUNCHER_PATH` unset, `/opt/hopper/bin/Hopper` absent, no JEB install, `:8425` closed | **CURRENT** |

## Tally

**STALE: 7** — F1b, F2b, F3, F5b, R1, R2, X1/X2 (X2 is a sub-clause of X1's unit).
**CURRENT: 11 bullets** — F1a, F2a, F2c, F2d, F4, F5a, F5c, R3, R4, R5, R6, G1 (plus R1's direct-Ghidra half, retained in the repair).
**ADJUDICATE: 1** — F2d, see below.

Stale count at the census: **7**. After the four patch texts in this directory:
**0** (see "Before → after" below).

## The one adjudication

**F2d "Retention decays oldest-first."** The claim is consistent with what the
store shows today (the r2-cited waybar/localsearch cores are gone while newer
godot cores remain), but this seat has **one** observation and no retention
policy to read — `systemctl show systemd-coredump -p MemoryMax` reports
`infinity`, `/etc/systemd/coredump.conf` carries no `MaxUse`, and the store
holds 90 files / 510 MB. Retention order is not stated anywhere on the host.
**Ruling: ADJUDICATE — keep the sentence, do not strengthen it.** It is a
design-consequence note the lane wrote for itself, and the evidence supports it
weakly. A repair would need a policy document this seat did not find; writing
one would be invention. Flagged for the parent, not patched.

## Before → after (the chain's falsifiable form)

| unit | before | after (A+B+C+D applied to a scratch tree) | evidence |
|---|---|---|---|
| stale bullets | **7** (F1b, F2b, F3, F5b, R1, R2, X1/X2) | **0** | this table; `evidence/` |
| PROVINCE line count | 162 | **162** | `wc -l` on `scratch4` |
| PROVINCE sha256 | `d075a3c6…` | **`e23354000fac054b2434ba410ce8c6bdc40c108ccd627b6941be03199f4ab03a`** | `sha256sum` |
| census verdict | PASS exit 0 (stale=0 …) | **PASS exit 0 (stale=0 ambiguous=0 undeclared=0 unresolved=0)**, SCOPE-ERRORS `[]`, UNREADABLE `[]`, declared fail classes `[]`, G2 floor 17/14/3 | `evidence/census-after-A-B-C-D.txt` |
| census differ vs baseline | — | **CLEAN — no new gated locus, no regression** (16 assertions both sides, 0 new / 0 removed / 0 disposition moves) | `evidence/census-diff-vs-baseline-D.txt` |
| hunks applied | — | 3 (A) + 2 (B) + 1 (C) + 1 (D) = **7 hunks, 0 failures** | `evidence/apply-and-census-D.log` |

The intermediate state (A+B+C only, before the R1 finding) is preserved as
`evidence/census-after-A-B-C.*` — sha256 `83c2da8f…`, same PASS verdict.

The repair patches are line-neutral **and** needle-free: the Frontier region
(lines 73–118) is UNDECLARED in the census scope table, so a `rea-agents@x.y.z`
or bare `6.x.y` needle written there would flip the gate to FAIL undeclared. The
patched lines introduce no such token; the census confirms it (`undeclared=0`).
Patch D was authored under this constraint by hand-checking the new lines against
the gate's own `PIN`/`VER`/`PTR` regexes before writing them.

## Reproduction

```
# 1. fresh scratch tree with all three scoped files (the gate needs PROVINCE + SKILL + SCORECARD)
mkdir -p /var/tmp/ex11/scratch4 && cd /var/tmp/ex11/scratch4
cp <repo>/{PROVINCE,SKILL,SCORECARD}.md .

# 2. apply this directory's four patch texts (content-anchored; each hunk its own fence)
python3 /var/tmp/ex11/harness/apply_patches.py --root . \
  --patch <repo>/.ufo/waves/arc3-loop1-round4/claims/c2/EX-11/frontier-repair-A.patch.md \
  --patch <repo>/.ufo/waves/arc3-loop1-round4/claims/c2/EX-11/frontier-repair-B.patch.md \
  --patch <repo>/.ufo/waves/arc3-loop1-round4/claims/c2/EX-11/frontier-repair-C.patch.md \
  --patch <repo>/.ufo/waves/arc3-loop1-round4/claims/c2/EX-11/frontier-repair-D.patch.md

# 3. census on the patched tree — expect PASS exit 0, 162 lines, sha256 e2335400…
python3 <repo>/.ufo/gates/c1-census-v10.py --root .
```

`apply_patches.py` is EX-14's chain applier, copied read-only to
`/var/tmp/ex11/harness/`; the same applier RV-4's `prose-apply.py` semantics
define. Both were used: EX-14's applier for the run above, and the patch format
is compatible with RV-4's. One format rule matters and cost this seat a
correction: the applier treats **each fenced block as one hunk**, so multiple
hunks per file must each get their own fence (an early draft put three hunks in
one fence and the applier read all `-` lines as a single search string).

## Attacks / refutations attempted

| # | attack | expected | measured | verdict |
|---|---|---|---|---|
| 1 | "the census gate already covers Frontier prose, so this census is redundant" | refuted | the gate's `classify()` keys on `REA_GATE` (pins/versions/pointers) and its SCOPE table stops at PROVINCE `:131`; the Frontier block is UNDECLARED and needle-free, so it is invisible to the gate — baseline census reads PASS while 7 bullets are stale | **attack succeeds** — the two instruments measure different things; recorded, not smoothed |
| 2 | "F2b is stale only because a new core appeared; the bullet's *intent* (all organic cores are big) may still hold" | refuted | the bullet says "all 3 organic cores exceed the cap"; the store now holds 90 files including under-cap ones, and one under-cap organic core **inspects** with a sealed id. The literal claim is false; intent is not the claim | **bullet STALE** |
| 3 | "C1's vyper leg is in flight, so F5b's vyper half should be CURRENT-as-untested" | refuted | the probe envelopes are sealed on disk with planted-K recorded pre-compile; 15/15 K/K at two pins. "Untested" is contradicted by landed evidence, not by a promise | **F5b STALE** |
| 4 | "R2 may still be a live wall — r7's hold used a caller-arranged disable" | partially survives | correct that it is not a *plain-cap* hold; but the bullet's text is "hits the deadline … Next: raise X" — both falsified. The honest residual (caller-arranged recipe) is written into the repair, not hidden | **bullet STALE; residual preserved in patch text C** |
| 5 | "a patch that adds no needle cannot be verified as applied" | refuted | the applier logs per-hunk `applied (n - / m +)` and the after-sha256 changes (`d075a3c6…` → `e2335400…`) while line count holds at 162 | **attack fails; repair verified** |
| 6 | "the Frontier repairs might break a DATED marker elsewhere" | refuted | the marker at PROVINCE `:119` sits below the Frontier region — a line-count change anywhere above 119 would break it. All four patches are line-neutral; SCOPE-ERRORS `[]` after apply | **attack fails** |
| 7 | "the R1 bullet is current because r5-01's entry reproduces" | **refuted by this seat's own first pass** | my initial R1 verdict was CURRENT on the strength of the entry's citations. Re-reading the *live* caches' `binaryTarget.js` showed the cited `:105` line is the r5-01 pin's copy (237 lines, md5 `b7f89a09…`), not the live one (379 lines, md5 `1ff13b45…`), which has a `riscv` branch at `:118`. A live no-override ET_EXEC run then succeeded (`ev_a572363e…`) | **verdict flipped to STALE; patch D authored.** The lesson is in the census: an entry reproducing at its own pin is not evidence that its *present-tense* wall wording still holds at the live pin |
| 8 | "a mislabeled x86-64 carrier cannot prove anything about RISC-V admission" | partially survives | correct — the run proves only that the **parse gate** admits EM_RISCV and the provider lane succeeds when its declared requirements are met. The carrier caveat is written into patch D; a genuine-RV64 end-to-end leg remains open | **attack recorded; claim scoped honestly** |

## Reconciliation with the chain's convergence verdict (VZ-2, `claims/c2/verdict.md`)

The convergence seat's verdict landed while this census was being finalized. Read
against it, my census agrees on every row it graded **except one**, and the
disagreement is a *later measurement*, not a contradiction:

| row | VZ-2 verdict | this census | reconciliation |
|---|---|---|---|
| F1b, F2, F3, F5b, R2, X1/X2 | stale | stale | agree |
| R1 | **current** (`verdict.md:182`, citing the r5-01 entry) | **STALE** | VZ-2's row cites the entry's own 10,766-functions line — true and unaffected by my finding. My finding targets the bullet's *other* clause, the present-tense parse-gate wording. Patch D is dated after the verdict (verdict mtime 11:23:41; D written 11:23) and the verdict's candidate inventory does not mention it (`grep -c 'repair-D' verdict.md` → 0). **This is an open decision for the parent, not a settled row.** |
| C2 (`PROVINCE.md:46`, 35 vs 34 Ghidra features) | stale (found by EX-15) | **not in scope** | C2 is a **Core** row, not a Frontier bullet; my part-1 scope is Frontier-only. Named as a gap, not silently omitted. |
| F2 | VZ-2 revised adjudicated → **stale** on EX-13's evidence | stale (independently, on my own live run) | agree — and our two measurements are independent (different seats, same 17,608,704 B / RC=0 result). |

**Landing implication.** The parent's candidate choice (EX-14 v2 / EX-13 set /
EX-15 set / PL-2) covers F1b, F2, F3, F5b, R2, X1/X2 and C2. **None of the
inventoried voices repairs R1**, because none of them measured it — the row read
CURRENT to every census that ran before patch D. If the parent wants R1 repaired,
patch D is the only text that does it; if the parent prefers the "land exactly one
voice" rule to hold strictly, R1 stays stale and should be recorded as a named
residual rather than a repaired row.

## Blockers / gaps named

1. **Part 2 (surface-summary, lines 8–26) is not this seat's scope.** VZ-2's
   row set covers the S-rows; I did not duplicate it. If no sibling lands part 2,
   the chain's "every … surface-summary claim is census-checked" clause is only
   half-discharged.
2. **F2d's retention policy is unlocatable** — adjudicated, not repaired.
3. **X2 is subsumed** — I did not author a separate repair for the pacman
   sub-clause; patch B covers it in the X1 hunk. If the parent prefers
   independent patches per clause, X2 needs its own file.
4. **The Vyper leg's *entry* is not yet in `corpus/knowledge/`** — my F5b
   verdict rests on the seat artifacts (`claims/c1/EX-04/evidence/probe/`), not
   on an admitted corpus entry. If C1's entry fails review, F5b's vyper half
   reverts to stale-by-default and patch B's wording should be reverted with it.
   **This is the one dependency that could invalidate a repair**; named, not
   papered over.
5. **No genuine-RISC-V end-to-end leg on the live pin.** Patch D's admitted
   carrier is synthetic (jq's bytes, patched headers), so it proves admission,
   not RISC-V analysis quality. The live-pin Ghidra RISC-V lane's behavior on
   real RV64 code is **untested by this seat**; the r5-01 entry's direct-
   `analyzeHeadless` leg remains the only real-code RISC-V evidence in the
   corpus, and it bypasses REA entirely.
6. **The live-pin RISC-V lane's exact admission rule is inferred, not read from
   source.** The typed rejections name two conditions (ET_EXEC; double-float ABI)
   and the successful run satisfies both, but this seat did not read the
   provider's admission code. The repair's wording ("ET_EXEC + double-float ABI,
   no override needed") follows the measured rejections; if the parent wants
   source-level certainty, that is an open reading task.
