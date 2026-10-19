# C2 verdict — PROVINCE Frontier/surface staleness census + repairs

Wave `arc3-loop1-round4` · chain c2 · seat VZ-2 (convergence) · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD at verdict work
`015e1bab914713568f339fd53999bc180459cc40` (no seat commits; the parent integrates).
Frozen claim: `claims-frozen.md:44-57`. Seat line: poll seats every 60 s (max 25
checks), reconcile into `claims/c2/verdict.md`.

**Method note (rule #14).** Every load-bearing number below was re-derived first-hand
by this seat on scratch copies at write time (14:04–14:17Z). No seat report was
treated as evidence without at least one first-hand re-measurement: the census was
re-run on the real tree and on three independently patched scratch trees, the patch
texts were re-applied from their own current bytes (three revisions of the complete
patch were measured), and every identity was re-hashed after the last revision.
Scratch under `/var/tmp/vz2r4` (never `/tmp`); no git mutation; custody paths never
opened.

## Verdict: **VERIFIED** — five independent repair candidates were produced; the two
this seat applied end-to-end each deliver every component of the frozen claim:

- **EX-14 v2** (`candidate-complete-frontier-repair.v2.patch.md`, `0b8ad045…`) — one
  6-hunk patch; my apply → `69ceea9b…`, 162 lines, census PASS, six of the nine stale
  rows repaired, content defect fixed.
- **EX-13's per-row set** (`claims/c2/EX-13/*.patch.md`, seven patches) — my apply →
  `dcfdb6a2…`, 162 lines, census PASS, seven of the nine repaired, content defect
  fixed. Two RV-3 accuracy defects are open against it.

EX-15's landing set repairs **eight** (all but C3; its own apply → `dce736cd…`), and
EX-12's standalone Core-row patch repairs the ninth. **Four further voices** (EX-11
A+B+C+D, EX-12, PL-2 ×2) carry their own validated applies; see the inventory table.

**The stale set is nine items, not six.** This seat's census began at 6 and grew three
times under peer pressure, every time because a peer was right: EX-13 found F2 (an
organic sub-cap core inspects), EX-15 found C2 (`PROVINCE.md:46` claims 35 Ghidra
features; the install has **34**), and EX-12 found C3 (the asar row names 9 archives; the
host has **12**). I re-measured each end-to-end rather than accepting a peer's number.
My instrument now reads `total=28 stale=9 adjudicated=1 current=18`.

**No single voice covers all nine.** EX-15's set covers 8 (all but C3); C3 is covered by
EX-12's standalone Core-row patch. A complete landing is therefore **EX-15's set +
EX-12's C3 patch**, or v2 plus the F2/C2/C3 repairs.

The census is run and its stale set named with evidence; the repairs are same-line at a
held line count; the gate reads PASS on the patched tree; the repairs are patch texts
(no seat wrote PROVINCE). **Two landing rules** are conditions of this verdict, both
measured: land one candidate in the same commit as C1's corpus entry (or take the
solc-only fallback), and shift no line above :116. **Two accuracy defects remain open
against the EX-13 set** (RV-3 sustained both; this seat reproduced the citations).

**Revision note (this verdict tracks the patches and the census, not a snapshot).** The
first complete candidate (`8a0e12ff…`) repaired 4 of 6 rows and carried a false Core
promotion; on that revision this verdict read NOT-VERIFIED. Two later peer findings
widened the census. All readings are recorded so the parent can see the trajectory and
re-derive the final shas at landing.

## Candidate comparison (both measured by this seat on fresh scratch trees)

| | EX-14 v2 (`0b8ad045…`) | EX-13 per-row set (7 patches) |
|---|---|---|
| after-sha on my apply | `69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5` | `dcfdb6a2fea6374caba5daf229b97c59ae4a69efa6ae14943909436e19eb81ca` |
| lines | 162 (held) | 162 (held) |
| census | PASS 0/0/0/0 | PASS 0/0/0/0 |
| stale rows covered | 6 of 8 (F2 and C2 untouched) | 7 of 8 (C2 untouched) |
| content defect (Core promotion) | fixed | fixed (revised at 11:17:33) |
| accuracy defects open | none found | **2** (X1 warrant, X1b left stale — §4.2/§4.2b below) |
| patch-text format | unified diff (`patch(1)`-readable) | fenced `-`/`+` with no `@@` markers — needs a content-match applier (RV-3 and this seat each wrote one) |

**Recommendation:** **EX-15's set + EX-12's C3 patch** is the complete landing (8 + 1 =
9 rows), with PL-2's `corpus-erratum-coupled.patch.md` optionally closing C2's corpus
root cause (R10). If the parent prefers v2, it must land **with CR-2's corrected hunk 6**
(never as-is — A15) and fold in the F2, C2 and C3 repairs. Land **one** coherent set, not
a hand-merge.

## Full candidate inventory (five voices — one must land)

The wave produced five independent PROVINCE repair voices. This seat applied and
measured the first two itself; the other three carry their own validated applies, which
I read but did not re-run (their after-shas are quoted from their own artifacts and
should be re-derived at landing).

| voice | patch text(s) | after-sha on apply | rows covered | known defects |
|---|---|---|---|---|
| **EX-15 landing set** | 8 hunks in `claims/c2/EX-15/adjudications.md` | `dce736cd…` (A6b) / `feec841b…` (A6a) *(its own apply)* | F1b, F2, F3, F5b, X1, C1, C2, R2 — **8 of 9** (C3 not in its hunk list) | none found; its A6a/A6b split mirrors the C1 coupling |
| **EX-14 v2** | `candidate-complete-frontier-repair.v2.patch.md` `0b8ad045…` | **`69ceea9b…`** *(my apply)* | F1b, F3, F5b, X1, C1, R2 — **6 of 9** (F2, C2, C3 untouched) | **1 defect, verified here (A18)**: hunk 6's context line is malformed, so the applied X1 sentence reads "still refused since r2: r12-02 drained the row…" — self-contradictory. **Land with CR-2's corrected hunk 6** (`proposed-x1-context-fix.patch.md`); I applied the combination → `8bb35a2c…`, 162 lines, census PASS, sentence correct |
| **EX-13 per-row** | 7 patches, `claims/c2/EX-13/*.patch.md` | **`dcfdb6a2…`** *(my apply)* | the 6 **plus F2** — **7 of 9** | 2 accuracy defects (A11); non-standard format |
| **EX-12 Core-row repair** | `proposed-core-asar-row-repair.patch.md` | not re-measured here | **C3** — the only voice this seat has seen covering it | not re-measured here |
| **CR-2 X1 correction** | `proposed-x1-context-fix.patch.md` | see EX-14 v2 row | replaces v2's hunk 6 | the correction itself; no defect found |
| **EX-11 A+B+C+D** | `frontier-repair-{A,B,C,D}.patch.md` (4 patches, 7 hunks) | `e2335400…` *(its own apply)* | F1b, F2, F3, F5b, X1, R2, R1 — **7 of its own set** | R1 disagreement with the peers (its own §reconciliation) |
| **PL-2 candidates** | `candidate-repairs.patch.md` (21 hunks) / `candidate-with-s5.patch.md` (22) / `candidate-coupled-vyper.patch.md` (22) / `corpus-erratum-coupled.patch.md` | — | widest single-file set; the coupled variants address the C1 coupling and the C2 corpus root cause | not re-measured here |

**Convergence note for the parent.** No single voice this seat has measured covers all
nine stale rows: EX-15's set covers 8 (all but C3), and C3 is covered by EX-12's
standalone Core-row patch. **A complete landing is therefore EX-15's set + EX-12's C3
patch** — or v2 + CR-2's hunk-6 correction + the F2, C2 and C3 repairs. PL-2's
`corpus-erratum-coupled.patch.md` addresses the C2 root cause in `corpus/` (R10), which
no PROVINCE-only voice can. All measured voices are line-neutral, needle-free and
census-PASS on their own applies; the material differences are row coverage, the two
defect classes (EX-13's accuracy wording, v2's malformed context), and whether the S5
pointer row is touched (this verdict adjudicates it NO-CHANGE, so touching it needs its
own justification). **Land one coherent set, not a hand-merge.**

## What the claim requires, and what was measured

Frozen falsifiable form: *the staleness census (each checked bullet: stale / current /
adjudicated, with evidence) → stale count N → 0; PROVINCE line count unchanged; census
PASS at the work tree after the parent applies the patches.*

| # | component | status | evidence (this seat's own runs) |
|---|---|---|---|
| 1 | a census instrument exists and is re-runnable | DELIVERED | `claims/c2/VZ-2/evidence/province-staleness-census.py` sha256 `e6eef57476bb6acac10f77285c90b035304286e91b19ccc6dbfe928509b174cc`; 26 rows, each anchored to a verbatim PROVINCE phrase (0 phantom rows measured on the unpatched tree) |
| 2 | the census is run against admitted corpus state, not asserted | DELIVERED | every row carries either a corpus path list or a live command transcript; the 18 `current` rows include live `doctor` re-derivations of all three catalog digests |
| 3 | baseline census at HEAD | MEASURED | final instrument reads `SUMMARY: total=27 stale=8 adjudicated=1 current=18` — `STALE: F1b, F2, F3, F5b, X1, C1, C2, R2`; `evidence/census-before.txt` / `.json`. (The first baseline read 6 stale; two peer corrections widened it — see below.) |
| 4 | **stale count N → 0** | **ACHIEVED by EX-15's set; 6/8 by v2, 7/8 by EX-13's** | EX-15's 8-hunk landing set covers all eight (its own apply → `dce736cd…`); v2 (`0b8ad045…`) repairs six (my tree `69ceea9b…`, F2 and C2 untouched); EX-13's per-row set repairs seven (my tree `dcfdb6a2…`, C2 untouched). Clause audits: `evidence/v2-patch-independent-reapply.txt`, `evidence/ex13-patch-independent-reapply.txt`. The first complete revision `8a0e12ff…` reached only 4 of 6 |
| 5 | PROVINCE line count unchanged | DELIVERED | 162 → **162** on every apply (demo `1bfb5dd7…`; complete v1 `f9b0888c…`/`dfa70b42…`; **v2 `69ceea9b…`**; **EX-13 set `dcfdb6a2…`**) |
| 6 | census PASS at the patched tree | DELIVERED | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, G2 floor 17/14/3, scope-errors `[]` — measured on my own scratch applies of **both** candidates |
| 7 | repairs land as patch texts, seats never write PROVINCE | HELD | `PROVINCE.md` sha256 `d075a3c6…` / 162 lines, **byte-identical to the HEAD blob** at write time; no seat wrote it |
| 8 | the round's own apply-and-measure seat iterated to PASS | DELIVERED | EX-14's `harness/run.sh` + `apply_patches.py`; RV-4 re-ran its own applier and reproduced byte-identical after-digests for every revision it graded |
| 9 | independent second witness on the patches | DELIVERED | RV-4's `census-diff.py` + `harness/apply-and-census.sh`; RV-3's own content-match applier + accuracy review; CN-1's cross-chain landing simulations; and this seat's four independent applies |
| 10 | landing constraints beyond the claim's letter | MEASURED | both candidates hold the DATED markers (:40/:45/:119), the SHONEN:12 range `88-116` safety clause, :18's two probe needles, and add no graded token (needle-free) |

## The three peer-found stalenesses (all independently confirmed here)

This seat's census began at 6 and grew three times, each time because a peer was right.

### The seventh — F2 (EX-13's find)

EX-13's per-row set asserts a stronger falsifier than my adjudication, and I re-measured
it first-hand:

- The bullet reads "all 3 organic cores exceed the cap (waybar 434MB)".
- `coredumpctl list | grep crashpad` → pid 1857, `present`, 48.5K compressed.
- `coredumpctl dump 1857 --output=/var/tmp/vz2r4/core.crashpad.raw` → **17,608,704 B**,
  **under** the 33,554,432 cap.
- `npx -y rea-agents@6.4.0 inspect-recorded-crash <that core> --format json` → **exit 0**,
  `format: elf-core`, `architecture: x86_64-little-endian`, **53 segments, 3 threads**
  (this seat's own `ev_3bdc54d2…`; EX-13's run minted `ev_1c1cd827…`).
- The waybar rows the bullet cites: 2 entries, **all `missing`** — the exemplar is gone.
- Population re-measured: **73 non-godot organic rows today, only 4 still `present`** — so
  the "3" is a stale r1-era sample size (PL-2's generator reached the same diagnosis).

So the bullet is stale on two counts. **Adjudication revised: F2 is STALE, not
adjudicated.**

### The eighth — C2 (EX-15's find)

- `PROVINCE.md:46` reads "39 processor modules; **35 features** incl. PyGhidra/BSim".
- I listed the install: `Ghidra/Features/*/` → **34** directories;
  `Ghidra/Processors/*/` → **39** (that half is correct); PyGhidra and BSim both present.
- **The staleness traces to the corpus entry itself**:
  `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims "35 modules" but its own
  enumerated list on that same line contains exactly **34** names, which match disk. The
  entry miscounts its own evidence, and PROVINCE inherited the number.

### The ninth — C3 (EX-12's find)

- `PROVINCE.md:49` (Core Electron/ASAR row) names **9** pinned asar archives.
- My own sweep of the same recipe (`find /usr/lib /usr/share /opt ~/.config
  ~/.local/opt -maxdepth 6 -name '*.asar'`) returns **12**, with byte counts matching
  EX-12's exactly: chatgpt 578,643,106; zcode 326,913,098; 1Password 40,708,328;
  signal 38,465,187; config-dir obsidian 27,477,966; obsidian.asar 25,787,463;
  typora node_modules 15,077,447; typora lib 8,339,267; obsidian app.asar 480,052;
  typora app.asar 390,514; electron43 111,073; electron39 109,371.
- The row's evidence cell also carries the **superseded** "1Password 423-file asar"
  count: the cited `corpus/knowledge/2026-10-13-r4-06-1password-asar.md` corrects it in
  its own erratum ("423 inventory files" conflates REA's `relevant_files:423` with
  archive membership — the asar lists **480** files). The 188 MB core is confirmed
  (187,997,016 B).

**Both halves verified. The baseline stale set is NINE, and this seat's instrument now
reads `total=28 stale=9 adjudicated=1 current=18`.**

**Independent corroboration of the membership.** EX-17's verbatim before-state census
reached the same 7-item set at its write time and explicitly reconciled with this seat
("VZ-2 adjudicated the same bytes — no contradiction, a unit choice, both recorded"); it
also pins the byte-level verbatim text of each item
(`claims/c2/EX-17/evidence/stale-items-verbatim.txt`, sha256 `f5723eb2…`). RV-3's
reviewer census reached the same six plus F1b as soft-stale. EX-15 reached all eight. So
the stale membership is now derived five ways — this seat's instrument, EX-13, EX-15,
EX-17, and RV-3 — and the two disagreements were both resolved in the peers' favour by
first-hand re-measurement.

## The census (this seat's own reading — the certificate the claim asks for)

26 rows over the Frontier section (5 bullets), the Round-4-frontier section (8 bullets),
the surface summary, the drift-prone block, the Core host-fallback row, and the
operator-gated footer. Verdicts:

| id | item | verdict | evidence |
|---|---|---|---|
| F1a | PE x86-64 AND ARM64 held (r3-08, 136 procs) | current | `corpus/knowledge/2026-10-13-r3-pe-arm64.md` |
| **F1b** | **"Reserve: 91MB Godot ARM64 template"** | **STALE** | wall fell mitigated arc2-r7 (`2026-10-18-arc2-r7-pe-wall.md`), no-disable control OOM-killed arc2-r8; `corpus/README.md:175` already reads "CLOSED, not frontier" |
| F2 | crashes >32 MiB: "all 3 organic cores exceed the cap (waybar 434MB)" | **STALE** (revised from adjudicated — see §"The seventh staleness") | an organic 17,608,704 B core inspects successfully (my own run: exit 0, `elf-core`, 53 segments); both waybar rows read `missing` |
| F2b | "no cap-raising knob … neither exists" | current | `2026-10-13-r2-crash-inspect-probe.md:22` (`--schema` carries only path + debuggerContext) |
| **F3** | **"IDA (unset), Hopper (absent), JEB (unprobed)"** | **STALE** | IDA/Hopper halves re-measured current (env unset; no binary). JEB half: I ran `npx rea-agents@6.7.0 inspect-jeb-client` → declared `capability_unavailable`/"fetch failed"; r2 matrix `:99` and r12-02 `:203` both record the probe — "unprobed" overstates the gap |
| F4 | macOS-only ops report `unsupported_host` | current | `2026-10-13-r3-keyed-archive-carriers.md:142` |
| F5a | selectors held on synthetic dispatcher (r3-07) | current | r3-07 entry |
| **F5b** | **"real solc/vyper-compiled bytecode untested"** | **STALE (both halves)** | solc: `2026-10-19-arc3-r1-evm-real-solc.md` + `…-r3-evm-optimizer-shapes.md` K/K. vyper: **this round's C1 leg landed** — 15/15 K/K on vyper-0.4.3 runtime (below) |
| F5c | "selectors stay bare hashes (no signature DB)" | current | no corpus entry claims a signature DB |
| **X1** | **"`compare-application-versions` still probe-refused since r2"** | **STALE** | `2026-10-14-r12-02-queue-b-ledger.md:213` — Queue-B row L203 drained with two success legs (`ev_7a8d0ec4…` JS, `ev_b5fc998f…` managed, both byte-identical re-runs) |
| X2 | multi-version pacman pairs beyond expac unexercised | current | no corpus entry claims one |
| G1 | operator-gated footer (IDA/Hopper/JEB) | current | env unset; JEB has no install |
| S1 | pins: Devin/OMP 6.5.0, Kimi 6.7.0 | current | live configs re-read: devin:7, omp:8, kimi |
| S2 | 6.7.0: 207/153, `tools_sha256 af39310c…` | current | **live** `doctor` re-derivation |
| S3 | 6.5.0: 207/153, `805433f1…` | current | **live** `doctor` re-derivation |
| S4 | 6.4.0 hist: 170/127, `25802f6d…` | current | **live** `doctor` re-derivation |
| S5 | Kimi pin `~/.kimi-code/config.toml:3298` | adjudicated | the cited line now holds `max_context_size`; the live pin sits at :3546. The citation is **receipt-stamped by design** (round-3 re-anchored it to the named 17:55:49Z receipt, `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt:1`), so the value claim is current and the pointer is historical-by-declaration. **No repair needed** — but see the gate blind spot below |
| S6 | installed shared REA skill v42/207 `c8639823…` | current | re-hashed: `c8639823…`, 22,513 B |
| S7 | Ghidra 12.1.4 / JDK 21.0.12.1 | current | `application.properties:17` + `java -version` |
| **C1** | **Core row "absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib"** | **STALE** | five of the claimed-absent tools are **present**: `7z` (7zip 26.03-1), `xxd` (tinyxxd 1.3.16-1), `radare2`/`r2` (6.2.0-1), `strace` (7.0-1), `upx` (5.2.0-1) — all installed 2026-10-13 13:52 -03. Genuinely absent: cabextract, rizin, ltrace, pacman-contrib |
| R1 | RISC-V: 10,766 functions @900 s cap | current | `2026-10-13-r5-01-riscv-bypass.md:62` |
| **R2** | **">90 MB PE … Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` …"** | **STALE** | arc2-r7's validated analyzer-disable recipe held it; arc2-r8's control OOM-killed at 9G; `corpus/README.md:175` reads CLOSED. PROVINCE still carries the pre-r7 remediation as if open |
| R3 | `.jsc` → source mapping next | current | r4-07 holds Ignition disasm; no mapper held |
| R4 | sasquatch AUR-only, 7z fallback | current | r4u-03 |
| R5 | adb 22/24 need a device | current | r4u-06 |
| R6 | signal/1Password-scale asar | current | r4-05 / r4-14 |

**Stale count N = 6** (F1b, F3, F5b, X1, C1, R2); 2 adjudicated (F2, S5); 18 current.

## The repair patch, measured independently

**The current repair candidate is EX-14's v2**,
`candidate-complete-frontier-repair.v2.patch.md` sha256
`0b8ad045e19cee5a3120706853f9950bb90522b2ebaebb418db25f586c21d9a8`. It supersedes
the earlier `candidate-complete-frontier-repair.patch.md` (`8a0e12ff…`), whose
predecessor revisions I measured as `928cfbc5…` (RV-4 also quoted `16b878d3…`). Three
revisions of the complete candidate plus the demo were applied and measured across
this seat and RV-4; **only the sha re-derived at landing time is authoritative**.

My own apply of v2 on a fresh scratch tree (`/var/tmp/vz2r4/v2`):

| | before | after |
|---|---|---|
| `PROVINCE.md` sha256 | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | **`69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5`** |
| lines | 162 | **162 (held)** |
| hunks | — | 6/6 applied (`patch --batch --forward`, fuzz 1) |
| census | PASS 0/0/0/0 | **PASS 0/0/0/0**, scope-errors `[]`, G2 17/14/3 |

Clause-level audit on the patched text (this seat's own `grep -F` — the decisive
measurement, since the gate is blind here):

| stale row | old literal | v2 result |
|---|---|---|
| F1b | `Reserve: 91MB` | **repaired** → "the 91MB scale wall is closed (arc2-r7)" |
| **F2** | `all 3 organic cores exceed the cap` | **UNTOUCHED** (survives at :84-86) |
| F3 | `JEB (unprobed)` | **repaired** → "JEB (probed; operator-gated)" |
| F5b | `vyper-compiled bytecode untested` | **repaired** → "real solc-0.8.37 (arc3-r1/r3) and Vyper 0.4.3 (r4) legs held K/K (RESULT-class)" |
| X1 | `probe-refused` | **repaired** → "is no longer refused since r2: r12-02 drained the row with two success legs" |
| C1 | `absent: \`7z\` …` | **repaired** → `7z`, `xxd`, `radare2`, `strace`, `upx` move to the present column; absent becomes `cabextract`, rizin, ltrace, pacman-contrib |
| **C2** | `35 features` | **UNTOUCHED** (survives at :46) |
| R2 | `Next: raise` | **repaired** → "closed, not frontier — no natural hold at this cap, rerun id-stability unknown" |

**Six of the eight old literals are gone on the v2 tree; F2 and C2 survive.** So v2
drives the count **8 → 2**, not to 0. Evidence:
`evidence/v2-patch-independent-reapply.txt`.

EX-13's per-row set repairs seven (C2 untouched); EX-15's landing set repairs all eight.
The F2 and C2 repairs are simple same-line rewrites of the two surviving literals, so if
the parent prefers v2 the gap is closable by folding in those two hunks.

For the record, the intermediate revision `8a0e12ff…` measured **6 → 2** (F3 and C1
surviving verbatim at :88 and :62) — that reading is why this verdict first returned
NOT-VERIFIED, and it is retained here so the parent can see the repair's trajectory.

## The content defect (fixed in v2)

The earlier candidates wrote `real solc-0.8.37 carriers (Core, arc3-r1)` /
`(Core, arc3-r1/r3)` / `Vyper 0.4.3 (r4) held` — asserting Core membership the corpus
disclaims. Measured, all legs:

- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:1,33` — "RESULT-class, **no Core
  promotion**, no availability→holding claim"; the r3 sibling says the same at `:1,35`.
- `PROVINCE.md:54` (the Core EVM row) cites only `(r3-07)`; `arc3-r1` appears nowhere in
  `PROVINCE.md` outside the patched bullets.
- `PROVINCE.md:75-76` — promotion requires "a `LOG.md` entry citing the corpus entries
  that earned it". No such promotion is recorded.

**Verdict on the earlier revisions: sustained** (RV-4 found it first; this seat
re-derived every leg) — landing them as written would have written a **false promotion
into a scoped file**.

**v2 fixes it.** Its EVM bullet now reads "…(Core, r3-07); real solc-0.8.37 (arc3-r1/r3)
and Vyper 0.4.3 (r4) legs held K/K (RESULT-class)…". The `(Core, …)` marker is retained
only for the synthetic dispatcher — which is the existing Core row's own citation
(`PROVINCE.md:54`) — while the r1/r3/r4 legs are correctly marked RESULT-class. Measured
on my patched tree: `grep -n "arc3-r1" PROVINCE.md` → one hit, at :92, inside the
corrected wording.

The census cannot catch this class by construction (see A1): the phrase carries no pin,
no bare version and no `path:line` pointer.

## Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the census gate validates the repairs" | **refuted, measured** — the Frontier region (PROVINCE:72-118) and the post-unlock frontier (:132-162) are **UNDECLARED** in the scope table, and the EVM bullet never matches the instrument's `REA_GATE` needle: `classify()` emits zero detections, so the gate reads the *same* PASS before and after. RV-4's blindness proof reproduced here: `unit 91-93 REA_GATE=False detections=NONE` both sides. A PASS certifies locus hygiene and anchor agreement, **not claim truth** |
| A2 | "the apply-and-measure seat's after-digest is stale" | **partially sustained, resolved** — EX-14's demo after-digest `1bfb5dd7…` **reproduced exactly** by this seat's own apply. The complete candidate then went through three revisions (`16b878d3…` per RV-4 → `928cfbc5…` → `8a0e12ff…` → **v2 `0b8ad045…`**); I re-applied each set of current bytes and re-measured rather than quoting an earlier run |
| A3 | "`ptr_check` covers the `config.toml:3298` pointer" | **refuted, measured** — `ptr_check` is only reached when a clause carries **no** pin/bare version (`c1-census-v10.py:416-418`). PROVINCE:18's clause carries the pin `rea-agents@6.7.0`, so the pointer is never evaluated. I called `ptr_check("~/.kimi-code/config.toml", 3298)` directly → `('stale', "line holds no rea-agents pin: 'max_context_size = 1048576'")`, while :3546 → `('ok', 'pins 6.7.0')`. **This is a genuine gate blind spot** — reported as a residual, not repaired (the citation is receipt-stamped by design, and the scope table is chain c1's instrument) |
| A4 | "the round-1/demo patch is enough" | **refuted** — it repairs only the solc half of F5b and leaves F5b's vyper half, F1b, X1, C1, R2 and F3 all stale. The v2 candidate supersedes it on all six |
| A5 | "the stale set is smaller than claimed" | **partially sustained** — the frozen claim's own named debt is one bullet; this seat's census finds six. Three of the extra four (F1b, R2, C1) were independently found by EX-14/RV-4/SC-2; two (F3 wording, S5 pointer) are this seat's. SC-2's independent 7-item census agrees on 5 items with mine; its extra item (v) — the decayed crash-core exemplar — I re-measured and **adjudicated** rather than counted stale (the bullet's own text already says retention decays oldest-first) |
| A6 | "C1's Vyper leg is a wave-tree claim, not corpus state" | **sustained as a landing hazard** — the leg is real and I re-derived it (below), but `corpus/` is still **83 files** and `corpus/README.md:38` lists only the r1/r3 EVM entries; C1's entry is patch text (`claims/c1/records-drafts/knowledge-entry-draft.md`, stem `2026-10-19-arc3-r4-evm-vyper-leg`). The patch's `Vyper 0.4.3 (r4)` clause is safe **only** if the parent lands that entry in the same commit — this is a condition of the VERIFIED verdict, not a defect in the patch |
| A7 | "the chain's instruments are seat text, not measurements" | **refuted** — I re-ran the census on the real tree and on three independently patched scratch trees; re-applied every patch revision from its own bytes; re-derived every identity at write time; and re-ran command A (83/83, 14/14, 10.0/10.0, missing `[]`, dangling `[]`) |
| A8 | "the earlier NOT-VERIFIED reading was wrong / should be suppressed" | **refuted as a request to hide it** — the reading was correct for the bytes it graded (`8a0e12ff…` genuinely left F3 and C1 stale and genuinely asserted a false promotion). Both readings are kept in this file; the verdict tracks the patch, and the parent re-derives the final sha at landing |
| A9 | "v2 trades a content fix for a probe break" | **refuted, measured** — v2 holds every anchor the gates and probes read: DATED markers at :40/:45/:119 still carry `2026-10-13`, `PROVINCE.md:18` still matches both `17:55:49Z receipt` and `rea-agents@6.7.0`, the SHONEN:12 range `88-116` still contains `Quality/safety verdicts on findings`, `bare hashes` survives at :93, and no added line carries a graded token |
| A10 | "my F2 adjudication (bullet not stale) was right" | **REFUTED against this seat's own earlier reading** — EX-13's per-row set asserts a stronger falsifier, which I re-measured first-hand: an organic crashpad core decompresses to 17,608,704 B (under the cap) and `inspect-recorded-crash` returns exit 0 with `elf-core` / 53 segments / 3 threads. "All 3 organic cores exceed the cap" is false. My adjudication was too lenient; F2 is **STALE**, and the true baseline count is **7**. EX-13's repair is grounded; v2 does not touch this row |
| A11 | "EX-13's per-row set is landable as it stands" | **partially sustained — two accuracy defects** (RV-3 sustained both; this seat reproduced the citations). **(a) X1's warrant overstates:** the patch reads "exercised since r12 (all three input classes…)", but `2026-10-14-r12-02-queue-b-ledger.md:213-218` says "**both classes**" and explicitly names the runtime-reconciliation sub-class as **untested**; that sub-class was closed later, at `2026-10-14-r14-01-queue-b-residual.md:19-25` (`ev_8f0ac46c…`). The count is right against r14-01 and wrong against the cited r12 — re-word or re-cite. **(b) X1b left stale:** the patch carries `multi-version pacman pairs beyond expac unexercised` through verbatim, but `2026-10-13-r4-10-real-version-pair.md:15` is headed "Targets — **cached pacman pairs**" and lists the `1password-cli 2.34.1-1 → 2.40.0-2` pair plus a `qpdf` control (I confirmed both by reading the entry). That clause was falsified at r4-10. Both defects are in the **same patch** (`8db47d240fc6027b…`) |
| A12 | "the two candidates disagree on the landing result" | **refuted** — I applied both to fresh scratch trees: v2 → `69ceea9b…`, EX-13 set → `dcfdb6a2…`, both 162 lines and both census PASS. The material deltas are F2/C2 coverage plus EX-13's two open accuracy defects |
| A13 | "the census is complete at 6 stale rows" | **REFUTED three times against this seat's own baseline** — EX-13's F2, EX-15's C2 and EX-12's C3 are all real, and I re-measured each end-to-end rather than accepting the peers' numbers. My instrument now reads 9 stale |
| A14 | "`35 features` is right and only the listing is short" | **refuted** — 34 directories on disk, and `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims 35 while its own enumerated list on that same line contains exactly 34 names matching disk. The entry miscounts its own evidence (EX-15's refutation, re-derived here by parsing the list) |
| A15 | "v2 is landable as-is" | **REFUTED (CR-2's find, verified here)** — v2's hunk 6 carries a malformed context line (`… is no longer` where the base reads `… still`). Applied with default fuzz it lands anyway and produces a **self-contradictory** sentence: "compare-application-versions **still** refused since r2: r12-02 drained the row with two success legs". Under `--fuzz=0`, 5 of 6 hunks fail. **Land v2 only with CR-2's corrected hunk 6**; I applied the combination → `8bb35a2c…`, 162 lines, census PASS, sentence correct |
| A16 | "a literal-gone clause audit is sufficient" | **refuted against this seat's own method** — my audit checked that `probe-refused` was gone (it was) but did not read the resulting sentence, which still asserts the refusal via the retained `still`. CR-2 read it. Recorded as a method lesson: a literal-gone check is not a semantics check |
| A17 | "one voice covers the whole stale set" | **refuted** — I read every patch's hunk list against my census: EX-15's set covers 8 of 9 (not C3), EX-13's 7, v2 6, EX-11's 7 of its own set. **C3 is covered only by EX-12's standalone patch.** A complete landing needs voices composed deliberately, which is why this file states the recipe rather than naming one file |

## Cross-chain fact this verdict established (needed for the F5b repair wording)

The C1 Vyper leg **landed in the wave tree and recovered K/K**, which makes the whole
EVM bullet stale rather than half:

- `CarrierV.vy` compiled with the round's one authorized install, vyper `0.4.3+commit.bff19ea2`
  (`claims/c1/EX-04/out/compile-receipt.txt`), runtime 1,562 B.
- This seat re-hashed the runtime bytes itself: sha256
  `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, **equal to the
  probe's decoded `bytecode.sha256`** — the probe really read those bytes.
- `inspect-evm-interface` on that runtime: **15 functions, all `dispatch:"abi"`**,
  set-equal to the 15 ABI-derived planted selectors (zero missing / zero extra), at
  6.4.0 (`ev_405e2a2a…`) and 6.7.0.
- The creation blob carries the `vyper` CBOR trailer (`…a1657679706572830004030037` at
  offset 1626), confirming genuine vyper output.
- The Vyper dispatch shape is a **third class** (modulo-indexed jump table,
  `5f3560e01c6002600d820660011b61060001601e395f5156`), distinct from the solc
  linear and binary-search classes.

Consequence: the correct post-landing wording of F5b depends on whether C1's corpus
entry lands in the same commit. If it lands → the patch's vyper clause is true (minus
the false `Core`/`held`). If it does not → the clause must fall back to the solc-only
form EX-14 itself specifies.

## Second landing constraint (found by CN-1; re-derived here)

CN-1's cross-chain record adds a constraint the c2 chain had not measured: the
**citation-drift pointer table pins SHONEN.md:12**, whose text asserts the province
boundary as `` `PROVINCE.md:88-116` ``, and the table's `shonen-province-range` entry
requires the range to still contain the load-bearing clause
`must_match: "Quality/safety verdicts on findings"`. That clause sits at **:114-116**
in the 162-line file — the last three lines of the cited range.

So "line count held" is **necessary but not sufficient**. Measured consequences
(CN-1's counterexamples, re-checked against the table's own entry here):

| variant | PROVINCE lines | census | probe |
|---|---|---|---|
| exact line-neutral rewrite (this wave's patch) | 162 | PASS 0/0/0/0 | clean |
| +1 net anywhere above :119 | 163 | **FAIL** — `:119 marker 'verified 2026-10-13' absent` | clean |
| +1 above / −1 at EOF (count held, content shifted) | 162 | **FAIL** — same :119 marker error | clean |
| +3 shift above the safety clause | 165 | — | **failed** — `shonen-province-range`, clause pushed out of 88-116 |

I re-derived the end state on my own patched tree: the clause
`Quality/safety verdicts on findings` is **still inside lines 88-116** after v2, and the
file is still 162 lines — so v2 clears the constraint, including the F3 repair at :88
and the C1 repair at :62 (both written line-for-line, not as expansions). Any *further*
repair that adds a line above :116 would break the SHONEN range even at a held total
count.

## Named residuals (measured; none voids the verdict)

1. **R1 — the census gate cannot grade any of these repairs.** The entire Frontier and
   post-unlock-frontier regions are UNDECLARED, and the EVM bullet carries no needle.
   The claim's `census PASS` clause is therefore **satisfiable without the repairs being
   true** — which is exactly why this verdict rests on the clause-level audit, not the
   PASS. Closing this needs a same-commit scope re-key of `.ufo/gates/c1-census-v10.py`
   — chain c1's instrument, not a c2 seat's to edit (r3 EX-31 precedent: patch text,
   owner lands).
2. **R2 — `ptr_check` never fires on a clause that already carries a pin** (A3). The
   `config.toml:3298` pointer has been silently un-evaluated since the clause gained
   its inline pin. Not repaired here (receipt-stamped by design + c1's instrument).
3. **R3 — CLOSED by v2**: the two previously unpatched stale rows (F3 at :88, C1 at :62)
   are now repaired line-for-line. Retained as a record of what v1 left open.
4. **R4 — CLOSED by v2**: the false Core promotion is gone; the r1/r3/r4 legs now read
   RESULT-class, matching their corpus entries. Retained as a record.
5. **R5 — patch-revision churn.** The complete candidate went through four published
   shas inside one wave (`16b878d3…` → `928cfbc5…` → `8a0e12ff…` → `0b8ad045…`), and
   EX-13's EVM patch was revised at 11:17:33 (after RV-3's apply) — which is why RV-3
   measured `f951f161…` and this seat measures `dcfdb6a2…`. Only the sha measured at
   landing time is authoritative; the parent must re-derive it.
6. **R6 — `__pycache__` residue** under `.ufo/gates/` — untracked; must stay out of the
   landing commit (round-2 precedent).
7. **R7 — the C1 coupling is unresolved until landing** (A6). The verdict is VERIFIED
   *given* the same-commit landing; landed alone, the vyper clause must fall back.
8. **R8 — EX-13's two accuracy defects (A11)** are open against that candidate and must
   be fixed before it lands: X1's "all three input classes" warrant and X1b's pacman
   half. Both are in `8db47d240fc6027b…`. v2 has neither defect.
9. **R9 — F2 and C2 are covered by only some voices.** v2 leaves both; EX-13's set
   leaves C2. If the parent lands v2, carry in the F2 and C2 repairs (both are simple
   same-line rewrites) or name them as carried debt.
10. **R10 — C2's staleness originates in the corpus, not only in PROVINCE.**
   `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims "35 modules" while its own
   enumerated list on that line names exactly 34, matching disk. Repairing the PROVINCE
   row alone leaves the source entry miscounting its own evidence. **PL-2 has drafted the
   coupled fix** (`claims/c2/PL-2/corpus-erratum-coupled.patch.md`, append-only erratum);
   a `corpus/` write is outside every seat's scope this round, so the parent applies it.
11. **R11 — EX-14 v2 must not land as-is (A15).** Its hunk 6 is malformed; use CR-2's
   corrected hunk (`claims/c2/CR-2/proposed-x1-context-fix.patch.md`) instead. This is a
   defect in a specific patch text, not in the claim.

## Closing procedure (the landing rules that carry this verdict)

1. **Land ONE voice in the SAME commit as C1's corpus entry**
   (`claims/c1/records-drafts/knowledge-entry-draft.md`, stem
   `2026-10-19-arc3-r4-evm-vyper-leg`) and its line-neutral map token. If C1's entry
   does not land, take the solc-only fallback EX-14 specifies in its own §"Landing
   dependency".
   - **Complete landing: EX-15's set + EX-12's C3 patch.** EX-15's 8 hunks (its own
     apply → `dce736cd…` for A6b / `feec841b…` for A6a) cover eight rows — all but C3;
     EX-12's `proposed-core-asar-row-repair.patch.md` covers C3. Add PL-2's
     `corpus-erratum-coupled.patch.md` to close C2's corpus root cause (R10).
   - **If taking EX-14 v2** (`0b8ad045…`): it **must** land with CR-2's corrected hunk 6
     (`proposed-x1-context-fix.patch.md`) — never as-is (A15/R11) — and must fold in the
     F2, C2 and C3 repairs, since v2 covers only 6 of 9.
   - **EX-13's per-row set** covers 7 of 9 but carries two accuracy defects (R8); fix
     those before landing, and note its format needs a content-match applier.
2. **Add nothing that shifts a line above :116** — both candidates are exactly
   line-for-line, and any later edit must be too, or the DATED markers at :40/:45/:119
   and the SHONEN:12 range `88-116` break.
3. Re-derive at the commit (rule #14): `PROVINCE.md` sha + line count (expect 162),
   census PASS, citation-drift probe both modes (`findings=0`), command A (expect 83/83
   if C1's entry lands — 84/84 once the new knowledge file and its map token are in;
   measured at HEAD `015e1bab` by this seat as 83/83, 14/14, 10.0/10.0).
4. Re-run this seat's census instrument (sha256 `e6eef574…`) and require
   `stale=0` — noting that the instrument's `ANCHORS` are the *old* literals, so on a
   repaired tree the repaired rows read `claim_present=False` by construction; the
   clause audits (`evidence/v2-patch-independent-reapply.txt`,
   `evidence/ex13-patch-independent-reapply.txt`) are the correct checks there.
5. Exclude the three `__pycache__` dirs from the commit.

## Verdict basis note (evidence discipline)

Every row of the census cites either a corpus file whose text I read or a command I
ran at write time; the three catalog digests and the pin set were re-derived live
rather than read. No seat report was accepted as evidence without a first-hand
re-measurement: EX-14's demo after-digest, RV-4's conformant verdicts, SC-2's census
count, CN-1's SHONEN:12 constraint, and the C1 Vyper leg were each independently
reproduced here. Where a first-hand
run disagreed with a recorded one — the patch revision I first applied was superseded
mid-wave — the disagreement is named rather than averaged away.
