# RV-3 — chain c2, reviewer (arc3-loop1-round4)

Seat RV-3 · chain c2 · role **reviewer** · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (unchanged through this seat's work;
`git rev-parse HEAD` re-checked at write time). Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback recorded in
`claims-frozen.md:11-15` after the hyper lane returned 402 out-of-credits on all
48 seats.

**Task as frozen:** review each repair patch for **ACCURACY** — the new text must
match admitted evidence in the corpus; no overreach into unverified claims.

Writes by this seat: this report + `claims/c2/RV-3/**` only. No git mutation.
Custody paths never opened for write (not touched at all by this seat). The real
`PROVINCE.md` / `SKILL.md` / `SCORECARD.md` / `.ufo/gates/c1-census-v10.py` were
only ever **read**; every apply ran on a `/var/tmp/rv3-round4/` scratch copy
(never `/tmp` — standing EDQUOT rule).

---

## 1. Work performed (evidence pointers)

### 1.1 Independent ground truth built BEFORE any patch was read

`/var/tmp/rv3-round4/frontier-census.md` — this seat's own bullet-by-bullet
census of every PROVINCE Frontier bullet and surface-summary claim against
admitted corpus state, derived from `PROVINCE.md` sha256
`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 lines)
and the 83-file `corpus/knowledge/` set. Derived independently of VZ-2's and
RV-4's instruments (I read neither before writing it).

Instrument baseline re-derived first-hand:
`python3 .ufo/gates/c1-census-v10.py --root .` at HEAD →
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0.

**My independent stale set (3 stale bullets / 4 claims + 1 soft-stale):**

| id | location | claim | verdict | falsifier |
|---|---|---|---|---|
| F5b | :91-93 | "real solc/vyper-compiled bytecode untested" | STALE (the freeze's named debt) | `2026-10-19-arc3-r1-evm-real-solc.md`; `2026-10-19-arc3-r3-evm-optimizer-shapes.md` |
| F3 | :87-88 | "JEB (unprobed)" | STALE | `2026-10-14-r14-01-queue-b-residual.md:141-148,226` — live typed `capability_unavailable` refusal |
| R2 | :139-144 | the "Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` …" action | STALE | r6 mid-rung + r7 mitigated hold + r8 natural control; `SCORECARD.md:1217` "Retired: the 91.6MB wall thread" |
| X1a | :157-158 | "`compare-application-versions` still probe-refused since r2" | STALE | `2026-10-14-r12-02-queue-b-ledger.md:213-218,254-260` (L203 drained) |
| X1b | :158 | "multi-version pacman pairs beyond expac unexercised" | STALE | `2026-10-13-r4-10-real-version-pair.md:15-20` |
| F1b | :82-83 | "Reserve: 91MB Godot ARM64 template" | SOFT-STALE | same r6/r7/r8 chain; `corpus/README.md:179` already dropped it |
| C1 | :62 | "absent: `7z`, … `xxd`, radare2/rizin, strace/ltrace, upx …" | STALE (Core row, not Frontier) | first-hand `command -v` + `pacman -Qi` (below) |

### 1.2 First-hand re-derivations (not seat text)

- **Vyper leg.** `CarrierV-hex-6.4.0.json` → 15 functions, `dispatch:"abi"` ×15,
  decoded `bytecode.sha256 57d6fd0ae0da…`; **set-equal to EX-04's planted K=15**
  (0 missing / 0 extra, recomputed by this seat as a set difference). Rerun
  re-derives `ev_d1792f57…`.
- **Vyper offset semantics.** Recomputed against `runtime.bin` (1,562 B):
  **0/15** reported offsets land on `0x5b`; **15/15** are preceded by `0x57`
  (JUMPI). EX-06's "the JUMPDEST reading does not hold for this class" is
  confirmed — any repair that kept the unscoped JUMPDEST reading would overreach.
- **C1 tool inventory.** `command -v`: `7z /usr/bin/7z`, `xxd /usr/bin/xxd`,
  `radare2 /usr/bin/radare2`, `r2 /usr/bin/r2`, `strace /usr/bin/strace`,
  `upx /usr/bin/upx` all PRESENT; `cabextract`, `rizin`, `ltrace`,
  `pacman-contrib` ABSENT. `pacman -Qi 7zip tinyxxd radare2 strace upx` → all
  five installed `Tue 13 Oct 2026 01:52:22 PM -03` (one batch). The row is
  falsified.
- **Census scope map.** Re-derived from the instrument's own `SCOPE` table:
  PROVINCE declared rows 8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131;
  **UNDECLARED: 72-118 (Frontier + Adjacent) and 132-162 (post-unlock frontier)**
  plus 1-7, 14, 27-39, 63. G6 makes any locus there UNDECLARED → FAIL.
  Matches RV-4's `scope-gap-map.txt` exactly.
- **Patch application.** All seven EX-13 patches applied by this seat's own
  content-match applier to a fresh scratch copy (`/var/tmp/rv3-round4/apply13.py`
  — content match on the `-` lines, since the patches carry `# file:` headers
  and no `---`/`+++` lines). Result: **7/7 applied, 162 → 162 lines**, sha256
  `f951f161d8a7526ed0043eb41e9d92ee3b65b5c1dda51146e637aadd6d0ddcc5`; census on
  the patched scratch tree → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, exit 0, G2 floor 17/14/3 unchanged.
- **EX-14 demo patch re-derived.** Applied → sha256
  `1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2`, matching
  EX-14's claimed identity byte-for-byte.

### 1.3 Patch texts reviewed (identity re-derived at write time)

EX-13 (the chain's real per-row repair set), all under
`claims/c2/EX-13/`:

| patch | sha256 (16) | target |
|---|---|---|
| `province-frontier-evm-solc-held.patch.md` | `66df2d6cf096f101` | :91-93 |
| `province-frontier-alternate-providers-jeb.patch.md` | `203fd3acb383bfdb` | :87-88 |
| `province-frontier-pe-subtypes-reserve.patch.md` | `25de1d22c2f88826` | :82-83 |
| `province-round4-frontier-pe-wall-closed.patch.md` | `1ce9b5a2a4017b54` | :139-144 |
| `province-round4-frontier-cross-version-residuals.patch.md` | `8db47d240fc6027b` | :157-160 |
| `province-frontier-recorded-crashes-organic.patch.md` | `c16fd02bf2804587` | :84-86 |
| `province-core-fallback-readers-inventory.patch.md` | `1913e11ed5aa967f` | :62 |

EX-14 (complete candidates):
`demo-frontier-repair.patch.md` (`507b0061…`),
`candidate-complete-frontier-repair.patch.md` (`8a0e12ff…` at review time),
`candidate-complete-frontier-repair.v2.patch.md` (`0b8ad045…`).

**Revision pin (rule #14).** Every sha in §1.3 was re-derived at write time
(14:19Z) and all eight patch texts were re-checked for stability after this
report's final revision: **unchanged**, mtimes 11:14:53–11:17:33. If a patch
text is revised again, the verdicts below attach to the shas named here, not to
whatever lands later.

---

## 2. Proposed changes

**None by this seat** (reviewer; this seat writes no real target). The findings
below are for the parent's landing decision.

---

## 3. Before → after measurement for the chain's claim

Frozen claim: *every PROVINCE Frontier bullet and surface-summary claim is
census-checked against the admitted corpus state; every stale item is repaired
same-line (line count held) or adjudicated NO-CHANGE with cause; the census
instrument reads PASS at the records commit; the repairs land as patch texts
applied by the parent.*

| | before | after (EX-13's 7 patches, this seat's own apply) |
|---|---|---|
| PROVINCE.md sha256 | `d075a3c6…` | `f951f161d8a7526ed0043eb41e9d92ee3b65b5c1dda51146e637aadd6d0ddcc5` |
| lines | 162 | **162 (held)** |
| census | PASS 0/0/0/0 | **PASS 0/0/0/0** (G2 17/14/3) |
| stale rows (my census) | F5b, F3, R2, X1a, X1b, C1 (+F1b soft) | F5b(solc), F3, R2, C1, F1b repaired; **X1a repaired but mis-cited** (§4.2); **X1b left stale** (§4.2b) |
| overreach clauses | — | **1 sustained** (§4.2), 1 under-reach (§4.2b), 2 minor (§4.3) |

**Every repair is line-neutral and needle-free, and none introduces a gated
locus.** That part of the claim verifies. The census PASS is, however,
**satisfiable without the repairs being true** (the Frontier region is
UNDECLARED and the EVM bullet carries no needle) — so the PASS is not evidence
for accuracy, which is why this seat's verdict rests on clause-level reading
against admitted corpus state.

---

## 4. Attacks / refutations attempted, with verdicts

### 4.1 Core-promotion overreach — **sustained, then discharged by revision**

EX-14's demo and v1 complete candidate wrote `real solc-0.8.37 carriers
(Core, arc3-r1)` / `(Core, arc3-r1/r3)`. Both arc3 EVM entries read
"RESULT-class, no Core promotion" at `:1` and `:33`/`:35`; the Core EVM row
(`PROVINCE.md:54`) cites only `(r3-07)`; `arc3` appears **zero** times in
PROVINCE.md outside the patched bullets; `PROVINCE.md:75-76` requires a
`LOG.md` entry for promotion and `LOG.md:1396-1415` records none.

**Verdict: sustained against demo + v1; discharged.** EX-13's per-row patch and
EX-14's v2 both now read `(RESULT-class, arc3-r1)` / `(RESULT-class)`. This seat
re-read the current bytes of all three to confirm (the v1 file was revised
mid-wave — see 4.4).

### 4.2 X1's "all three input classes" — **SUSTAINED (accuracy defect, not yet fixed)**

`province-round4-frontier-cross-version-residuals.patch.md` (`8db47d24…`) adds:

> `compare-application-versions` exercised since r12 (**all three input
> classes**; the r2 refusal is historical)

The admitted corpus supports **two** classes, not three, and explicitly names a
residual:

- `2026-10-14-r12-02-queue-b-ledger.md:213-218` — "NOW EXERCISED (this lane,
  **both classes**; candidates 1–3)" + "**Residual open sub-class**: the
  runtime-reconciliation input class (`reconcile_javascript_runtime` Evidence) —
  **untested**, needs a held reconcile evidence composed as input."
- `2026-10-14-r14-01-queue-b-residual.md:19-25` — r14-01 then **closed** that
  residual ("the input class r12-02 left open … **succeeds** (exit 0, 0.75 s,
  325,009 B): `ev_8f0ac46c…`").

So the count "three" is arguably right *against r14-01*, but the patch cites
`r12` as its warrant, and r12-02's own text says "both classes". The clause
overstates what the cited entry admits. **Correct form:** either cite r14-01
(`exercised across all three input classes since r14`) or write
`exercised since r12 (two classes; the reconcile-input sub-class closed at
r14-01)`. Note also r14-01 records a **directional coverage law** and a
"paired-items-stay-unknown" law — so "exercised" must not be read as "correct".
Verdict: **sustained; the repair text must be re-worded or re-cited before
landing.**

### 4.2b X1's second half is left stale — **SUSTAINED (the repair under-reaches)**

The same patch (`8db47d24…`) repairs only the first half of the bullet. It
**carries the second half through verbatim**:

> `… multi-version pacman pairs beyond expac unexercised …`

That clause is also false against admitted state, and I re-verified it
first-hand: `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:15` is headed
"Targets — **cached pacman pairs** (`uniq -d` walk: 354 duplicated pkgbases)" and
`:19-20` list the `1password-cli` 2.34.1-1 → 2.40.0-2 pair (41,210,040 →
43,475,106 B) plus the `qpdf` 12.3.2-2 → 12.4.1-1 control pair, with `:22`
recording the `tar -xOf <pkg>` extraction from the pacman cache. "Beyond expac
unexercised" was true at r2 (which used `expac`/`bwrap`); r4-10 falsified it.

My applied tree confirms it: the literal
`pacman pairs beyond expac unexercised` survives at line 159
(`grep -n` on `/var/tmp/rv3-round4/ex13/PROVINCE.md`). So the X1 row is
**half-repaired** — the patch closes one stale claim while leaving the adjacent
stale claim in the same bullet untouched, and the claim requires every stale item
repaired or adjudicated with cause.

**Verdict: sustained.** Correct form:
`multi-version pacman pairs exercised since r4-10 (1password-cli, qpdf controls)`.
Note VZ-2's census rates this same clause `current` with the note "no corpus
entry claims a further pacman version pair" — that reading is not supported:
r4-10's own section header says "cached pacman pairs", and its pairs are pacman
packages, not a different provenance.

### 4.3 Two minor accuracy issues

**(a) R2's "Residual: rerun id-stability (r7 erratum)" — STALE.**
`province-round4-frontier-pe-wall-closed.patch.md` (`1ce9b5a2…`) closes the
bullet and then names a residual that the same entry already resolved:
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:41-52` (the r10 erratum) reads
"Rerun id-stability is therefore **STABLE** at the 91.6MB scale point".
Repairing one stale claim by importing another is a defect. **Correct form:**
drop the residual clause, or write `id-stability STABLE (r7 erratum, r10)`.

**(b) F2's "an organic 17.6MB core inspects" — evidence is real but the
adjective is unadmitted.**
`province-frontier-recorded-crashes-organic.patch.md` (`c16fd02b…`) repairs
`:84-86`. I re-derived the underlying measurement: EX-11's envelope
`crash-probe-crashpad-under-cap.json` is genuine — `ev_cde93acb…`, 17,608,704 B
ELF core, `format:"elf-core"`, 53 segments, 3 threads × 27 registers, and its
`NT_PRPSINFO` carries `chrome_crashpad` / `chrome_crashpad_handler
--monitor-self-…`. The patch's own "Note for the parent" already discloses that
clause 1 is wave-tree-only (no arc3-r4 crash entry in the 83-file corpus), which
is honest.

But the *word* "organic" is a defined term in this lane's corpus: r1/r2 count
"Only 3 **organic** non-chromium crashes" and contrast them with 39 deliberate
`crash-godot` **self-kills** (`2026-10-13-crash-evidence.md:22`) — that entry's
enumerated set is *non-chromium* crashes, so a chromium-derived core is neither
in it nor excluded by it; the word's admitted sense is "not a deliberate
test self-kill", and a crashpad-handler core is unclassified under it. The r2
entry's standing claim is the one the repair touches: "every *organic* core on
this host … exceeds the cap, so REA
currently cannot inspect a real application crash here"
(`2026-10-13-r2-crash-inspect-probe.md:66`). A crashpad-handler core is
machinery, not an application crash, and whether it is "organic" in the corpus's
sense is **not admitted anywhere**. Landing it as "organic" silently narrows the
r2 entry's standing claim. **Correct form:** `a 17.6MB crashpad-handler core
inspects (wave-tree measurement, not yet admitted)`, leaving the "organic"
classification to the entry that measures it.

### 4.4 Patch-revision churn — **sustained (process finding)**

The complete candidate carried **four** published shas inside one wave
(`16b878d3…` → `928cfbc5…` → `8a0e12ff…` → `0b8ad045…`); RV-4's report pins
`16b878d3…` and VZ-2's re-apply log pins `928cfbc5…`, while the file on disk at
this seat's read was `8a0e12ff…` and then `0b8ad045…`. Measured consequence: a
reviewer's recorded identity can name bytes that no longer exist, so a "reviewed"
verdict can be attached to an unreadable revision.

Worse, the **v1 revision at `8a0e12ff…` carried a corrupt hunk** — its X1 leading
context line read `… is no longer` where the base reads `… still`. Under
`--fuzz=0` the hunk is rejected; GNU patch's default fuzz=2 papers over it and
applies the replacement against the **base** line, yielding the
self-contradictory sentence `compare-application-versions still refused since
r2: r12-02 drained the row with two success legs`. I reproduced this
independently (`/var/tmp/rv3-round4/v2b/`): applied output reads `still refused
since r2: r12-02 drained the row`, sha256 `69ceea9b…`. **This defect persists in
the current `0b8ad045…` revision** — I re-extracted the fenced block from the
current file and re-applied: 6/6 hunks, 162 lines, and the X1 line still reads
`still` + `refused since r2: r12-02 drained the row`. RV-4 recorded the same
defect against `8a0e12ff…`; it was not fixed in the revision that supersedes it.
**Verdict: sustained.** EX-13's per-row X1 patch (`8db47d24…`) does **not** have
this defect — its leading context line is the base text verbatim.

### 4.5 Attacks refuted

| # | attack | verdict |
|---|---|---|
| A1 | "the census PASS validates the repairs" | **refuted** — the Frontier region is UNDECLARED and the EVM bullet carries no needle; the census reads byte-identical PASS before and after. I reproduced this: my patched tree's census output is the same PASS line as the baseline. |
| A2 | "the repairs shift the DATED marker at :119" | **refuted** — 7/7 patches are exactly line-neutral (162 → 162); I re-derived `wc -l` and sha256 on my own applied tree. |
| A3 | "the repairs inject a gated token into the UNDECLARED region" | **refuted** — `solc-0.8.37` is not a needle (VER requires a literal `6.`); no patch adds `rea-agents@x.y.z` or a `~`/`/`-absolute `path:line`. Census `undeclared=0` on my applied tree. |
| A4 | "EX-13's C1 inventory repair is an opinion, not a measurement" | **refuted** — `command -v` + `pacman -Qi` reproduce all five present / four absent exactly, with a single install timestamp. |
| A5 | "the vyper leg is a wave-tree rumor" | **refuted** — envelope re-read first-hand: 15 functions, K=15 set-equal, decoded `57d6fd0a…`. |
| A6 | "EX-06's offset claim is a seat assertion" | **refuted (claim verified)** — 0/15 on JUMPDEST, 15/15 preceded by JUMPI, recomputed from the runtime bytes. |
| A7 | "the EX-13 EVM patch still carries the Core overreach" | **refuted** — current bytes read `(RESULT-class, arc3-r1)`; `grep -c "(Core, arc3-r1)"` → 0. |

---

## 5. Blockers

**None for this seat.** Named gaps for the parent:

1. **The X1 clause is defective on both halves.** (§4.2) the first half cites
   `r12` for a three-class count that r12-02 itself records as "both classes";
   (§4.2b) the second half — `multi-version pacman pairs beyond expac
   unexercised` — is left **stale in the applied tree**, so the X1 row is
   half-repaired. This is the chain's own real patch text (`8db47d24…`) and the
   only place the X1 debt is repaired; it must be re-worded and extended before
   landing. The landing decision is the parent's.
2. **The v2 hunk-6 corruption (§4.4) persists** in
   `candidate-complete-frontier-repair.v2.patch.md` (`0b8ad045…`). If the parent
   lands the *complete* candidate rather than EX-13's per-row set, the X1 line
   lands self-contradictory. EX-13's per-row patch is the safe carrier for X1.
3. **The R2 residual clause (§4.3a) imports a stale claim** into a repair whose
   purpose is removing stale claims.
4. **The F2 "organic" adjective (§4.3b)** rests on wave-tree-only evidence that
   the patch itself discloses; the classification word is the unadmitted part.
5. **Cross-chain coupling, still live:** the F5b repair cites the Vyper leg,
   whose corpus entry is **not admitted** (`corpus/knowledge/` is at 83 files;
   `corpus/README.md:38` lists only the r1/r3 EVM entries). EX-13 handled this
   correctly — its patch repairs the **solc half only** and leaves
   `vyper-compiled bytecode untested` standing, which is true against admitted
   state. EX-14's v2 instead writes `Vyper 0.4.3 (r4) legs held K/K` and names
   the coupling in its own "Landing dependency" block. **The two patch sets
   therefore encode different landing orders**; landing both would double-apply
   the same bullet (fails closed) and, if v2 lands alone, would assert an
   unadmitted leg. The parent must pick one.
6. **Reviewer identity drift (§4.4):** recorded patch shas in RV-4's and VZ-2's
   reports no longer match the files on disk. Rule #14 applies to patch texts
   too — any landing receipt should pin the sha it actually applied.
