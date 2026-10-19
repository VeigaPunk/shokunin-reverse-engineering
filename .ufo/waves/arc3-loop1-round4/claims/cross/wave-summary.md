# arc3-loop1-round4 — wave summary (VZ-4, wave-integrator, cross chain)

Seat VZ-4 · chain cross · role wave-integrator · wave `arc3-loop1-round4`, 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. HEAD at every sample this
wave: `015e1bab914713568f339fd53999bc180459cc40` (immobile; seats do not commit —
parent integrates). This file is the integrator's cross-chain read; every number
here is either re-derived first-hand by this seat on the paths cited, or explicitly
attributed to the seat that measured it.

**Method.** 60 s poller, max 30 checks (`claims/cross/VZ-4/poll.log`, checks 1–30;
started 14:04:23Z) over `seats/` + non-empty `claims/` files; a parallel 60 s
real-target watcher (`claims/cross/VZ-4/targets.log`) hashing the custody tool,
README, pointer table, `expected.json`, `PROVINCE.md`, `SKILL.md` plus `git status`
each check; my own baseline re-runs of command A, the census, and the
citation-drift probe (both modes + selftest); a scratch copy of the landed tool for
every injection (never a custody write); three independent REA probes
(`rea-agents@6.4.0`, disk-backed `TMPDIR`) of the round's Vyper carriers; and
independent re-runs of other seats' fix shapes on scratch copies. Scratch under
`/var/tmp/vz4` — never `/tmp` (standing EDQUOT rule). No git mutation of the real
repo; custody paths opened for reading only (sha256/stat); no
corpus/LOG/SCORECARD/README/SKILL/PROVINCE writes.

---

## 1. The wave's arc — dispatch, lane substitution, delivery

**Dispatch (frozen pre-dispatch).** 48 seats, roster enumerated mechanically
16 + 14 + 14 + 4, every name exactly once (`claims-frozen.md`). Axis set:
**coverage (owned)**, **freshness (fleet)**, **operability (fleet)**.

**Lane substitution at dispatch (recorded with cause, not a lane signal).** The
primary lane `hyper/deepseek-v4.1-flash` returned **402 out-of-credits on all 48
seats** (zero delivered, ~30 s). Per the round-4 schedule's declared fallback and
the operator directive, the full roster was re-dispatched on the devin lane
(`devin/deepseek-v4-1-flash-max`) — the same substitution class recorded in the
round-3 records, where the token-plan lane hit its monthly quota mid-run and the
remaining seats moved to devin. **The roster, claims, and assertions are
unchanged**; provider identity is substrate-neutral for the 48-seat roster
assertion. The records should quote the delivered count per lane.

**Delivery at this file's write.** Reports land continuously; the closing census
block (§7) carries the final count against the frozen roster with the undelivered
seats named. Every seat this wave wrote its report under `seats/<SEAT>.md`;
artifact trees were consistently ahead of reports (the r1-shaped gap, recurring).

---

## 2. Per-chain verdicts

All three chains' work is present in the tree and measured. Chain-level verdict
files were not yet written by the chain convergence seats at this file's close;
the per-chain reads below are this seat's own, built from first-hand runs against
the landed/scratch artifacts.

### C1 — coverage (owned): EVM family closure, the Vyper leg — **VERIFIED (chain verdict; VZ-4 first-hand on 4 carriers)**

**Chain verdict: `claims/c1/verdict.md` (VZ-1) reads VERIFIED** — five carriers on
18 legs, K/K, by that seat's own re-derivation and ≥3 independent seats each; the
honest-stop branches (venv infeasible / typed refusal / partial recovery) were
**not** triggered on any runtime leg. The landing arm is script-verified
end-to-end on the current pair: **84/84, missing [], dangling [], 14/14, prior-83
byte-identical, README 190 → 190** — which reproduces my own independent
projection exactly.

The r3 entry's named Unknown was "Vyper and solc versions other than 0.8.37". The
authorized install ran (EX-02, one install only): **vyper `0.4.3+commit.bff19ea2`**
in `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/` (wheel
`3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd`, byte-identical
to PyPI's declared digest; venv manifest present; smoke compile receipted). EX-01's
environment census is the load-bearing input: the host python is 3.14.7 with **no**
prebuilt `immutables` cp314 wheel, and the decisive finding is that `uv 0.13.0`
ships on-disk CPython 3.11.17 / 3.12.15 / 3.13.16 (all inside vyper's
`>=3.10,<4`). VZ-4 re-verified `uv 0.13.0` and the on-disk interpreters.

**K/K on Vyper carriers — four independent VZ-4 probes, all `rea-agents@6.4.0`,
hex leg, disk-backed TMPDIR:**

| carrier | source | recovered | vs ABI-derived set | sealed id | decoded bytecode sha256 |
|---|---|---|---|---|---|
| EX-02 smoke | `EX-02/smoke/Smoke.vy` | 4/4 | equal, 0 missing / 0 extra | `ev_073f845c…` | `415e6b1b…` |
| EX-03 StewardToken (ERC-20-bearing) | `EX-03/runtime.hex` | 22/22 | equal, 0 missing / 0 extra | `ev_6b8a15c4…` | `1846469b…` |
| EX-04 CarrierV (non-ERC-20 vault) | `EX-04/src/CarrierV.vy` | 15/15 | equal, 0 missing / 0 extra | `ev_d1792f57…` | `57d6fd0a…` |
| PL-1 CarrierW (second prototype) | `PL-1/evidence/src/CarrierW.vy` | 9/9 | equal, 0 missing / 0 extra | `ev_b9d050db…` | `67d1d88f…` |
| PL-1 CarrierW | `PL-1/evidence/src/CarrierW.vy` | 9/9 | equal, 0 missing / 0 extra | `ev_b9d050db…` | `67d1d88f…` |

EX-04's carrier is the clean non-ERC-20 shape (payable vault, zero ERC-20
selectors, planted K=15 recorded pre-compile/pre-probe); EX-05 derived the same K
through four independent keccak routes; PL-1's CarrierW is a structurally
independent second carrier. Command A before-state at HEAD, my run:
**83/83, missing [], dangling [], 14/14 rules, 10.0/10.0**. The r4 entry is
landing as a new corpus file + line-neutral map token; the parent re-derives the
after-state (expect 84/84 with the prior 83 byte-identical).

**Three cross-cutting Vyper findings (VZ-4, first-hand; full text in
`claims/cross/VZ-4/evidence/vyper-kk-traps.txt`):**

1. **`vyper -f method_identifiers` emits the fallback as a pseudo-entry.**
   `__default__() -> 0x89402a72` appears in vyper's own output and in the compiled
   `method_identifiers.json`, but the compiled ABI types it `{type: fallback,
   payable}` — not a function. Byte check on EX-04's 1562-byte runtime: `89402a72`
   occurs as **no** `PUSH4` immediate. The correct K set is the ABI *functions*
   (15). **The chain handles this**: `EX-04/evidence/record-planted-K.py` excludes
   `__init__`/`__default__` explicitly and `verify-report.json` records the
   key-diff in the open (`only_in_method_identifiers: ["__default__()"]`); EX-05's
   `derive-siglist.py` excludes them too; PL-1's `verify.txt` names the same
   phantom-selector trap independently.
2. **vyper strips leading zeros in its hex rendering.** `fee_of(uint256,uint256)`
   prints `0xc751377` (7 digits) and `is_owner(address)` prints `0x776076f`; an
   independent keccak gives `0c751377` / `0776076f`. A naive set comparison
   against raw vyper output reports 2 spurious mismatches. **The chain handles
   this**: `EX-05/verify-planted.py:75` normalizes with `v[2:].zfill(8)`.
3. **NEW — Vyper probe offsets land immediately after `JUMPI` (0x57), never on
   `JUMPDEST`.** Measured across the carriers: CarrierV 0/15 on JUMPDEST, 15/15
   after JUMPI; CarrierW 0/9, 9/9; Smoke 0/4, 4/4. This *differs* from the solc
   carriers of r1/r3, where every offset landed on a `JUMPDEST`. A checker
   asserting JUMPDEST-ness would report 0/15 on a perfectly recovered Vyper
   carrier. EX-09 proved the sharper rule independently — **`offset == push4_pc +
   11`**, the fall-through handler body after the compare `JUMPI` (layout
   `63 <sel:4> 81 18 61 <next:2> 57` = `PUSH4 DUP2 XOR PUSH2 JUMPI`), holding
   7/7 on `Ex09Vault` and 4/4 on `Smoke` with `RULE_HOLDS=True` throughout
   (`EX-09/analysis/offset-rule-proof.txt`). PL-1 measured the same shape too.
   (`PL-1/evidence/verify.txt`). **Landing note: the C1 entry must state the Vyper
   offset convention explicitly.**
4. **A fourth carrier and an upstream-inference delta (both verified).** VZ-4's
   probe of EX-03's ERC-20-bearing `StewardToken` returned **22/22, zero missing /
   zero extra** (`ev_6b8a15c4…`, decoded sha `1846469b…`). EX-09's census then
   measured that the extractor reads **`payable` for arg-taking functions** whose
   ABI declares `view`/`pure`/`nonpayable` — 6/6 arg-taking functions in its
   attack carrier, 8/15 on `CarrierV` — with no case reading a *more* restrictive
   class and no selector misassigned. The entry records this as an observed delta
   (consistent with an inference reading the XOR-chain dispatcher structure rather
   than per-function `CALLVALUE` guards), not a defect and not a behavioral claim.

**Pre-landing entry repairs the chain verdict requires (both have patch texts;
neither changes any count, set, digest, dispatch-shape or offset claim):**

- **F1 — the `69656e74` mechanism sentence is unreproducible as written.** The
  draft names `69656e74` as a non-selector **`PUSH4` immediate`; it is not — it is
  a substring of the revert string `insufficient` inside a **`PUSH32` payload**
  (pc 0x2d3). **VZ-4 independently confirmed this** with an opcode-boundary walk
  (16 distinct `PUSH4` immediates; the only non-selector one is `08c379a0` ×6) and
  **corrected its own earlier note**, which had made the same mistake. The
  conclusion (zero false positives) is unchanged. Repair: RV-1's
  `proposed-entry-correction.patch.md`; the same sentence appears in three other
  artifacts and must be repaired together or the corpus contradicts its siblings.
- **F2 — the "same three legs at the same path" sentence is false.** EX-04 ran
  scratch-path copies (`/var/tmp/ex04-r4/probe/`) minting different ids; the ids
  the entry cites belong to repo-path runs by five other seats. VZ-1 supplies the
  repair text. **Corroborating evidence from my own work:** my repo-path probe of
  EX-04's runtime returned `ev_d1792f57…` — byte-identical to VZ-1's independent
  run at the same path with the same request, which is exactly the same-path
  determinism the sentence misattributes.

Also sustained by the verdict and worth carrying: CR-1's five edits (optimizer-mode
scoping; the **solc-shaped-reconciler hazard** — an `EQ`-recipe parser returns the
empty set on 33/33 default-optimizer Vyper carriers while flagging correct
selectors as extras; and the count-vs-set rule, where an injected selector flip
preserves K while changing the set); EX-07's finding that the r3 entry's
"6.7.0-specific" delta is really a **6.5.0** boundary.

### C2 — freshness (fleet): PROVINCE Frontier/surface staleness census + repairs — **VERIFIED on revision (VZ-2's revised verdict; one wording edit still needed)**

**VZ-2 revised its verdict from NOT-VERIFIED to VERIFIED** after two independent
candidates landed, and **I reproduced the v2 path byte-exactly** (see below). The
earlier NOT-VERIFIED read was correct *at the revision it measured* — the first
complete candidate (`8a0e12ff…`) repaired 4 of 6 rows and carried a false Core
promotion — and the revision history is recorded in the verdict rather than
smoothed, which is the right discipline.

VZ-2 built a real 26-row PROVINCE staleness census
(`claims/c2/VZ-2/evidence/province-staleness-census.py`, each row anchored to a
verbatim PROVINCE phrase) and measured **`total=26 stale=6 adjudicated=2 current=18`**
— `STALE: F1b, F3, F5b, X1, C1, R2`. **VZ-4 re-ran that instrument and reproduced
the identical numbers and the identical stale set.** The claim's falsifiable form
requires **`stale N → 0`**.

**What IS delivered and independently reproduced** (VZ-2's own runs, and my own
independent re-run of the demo repair agrees):

- the census instrument itself, re-runnable, 26 rows, 0 phantom rows, every row
  carrying either a corpus path list or a live command transcript (the 19 `current`
  rows include live `doctor` re-derivations of all three catalog digests);
- the **line-neutral** property: `PROVINCE.md` **162 → 162** on both applies;
- the **census PASS** on the patched tree: `PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, scope-errors `[]`, G2 floor 17/14/3 — and I reproduced the demo
  repair independently (162 lines held, census PASS 0/0/0/0);
- the discipline: the real `PROVINCE.md` is untouched
  (`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`, 162 lines) —
  patch texts only, as required.

**The named debt is real and I confirmed it first-hand**: the Frontier bullet
(91–93) still reads *"real solc/vyper-compiled bytecode untested"* — stale on both
legs. Evidence: `claims/cross/VZ-4/evidence/c2-province-bullet-stale-check.txt`.

**The two survivors** (both real staleness, not census artefacts; VZ-2 measured,
and neither patch revision touches them):

- **F3** — `"IDA (unset), Hopper (absent), JEB (unprobed)"`. The JEB half is stale:
  VZ-2 ran `npx rea-agents@6.7.0 inspect-jeb-client` → declared
  `capability_unavailable`; the r2 matrix `:99` and r12-02 `:203` both record the
  probe, so "unprobed" overstates the gap.
- **C1** — the Core row claiming `7z`, `xxd`, radare2/rizin, strace/ltrace, upx,
  pacman-contrib **absent**. Five are **present** on this host: `7z` (7zip 26.03-1),
  `xxd` (tinyxxd 1.3.16-1), `radare2`/`r2` (6.2.0-1), `strace` (7.0-1), `upx`
  (5.2.0-1) — all installed 2026-10-13. Genuinely absent: cabextract, rizin,
  ltrace, pacman-contrib.

**A third stale clause the census missed — three-way convergence.** The X1 bullet's
second half, *"multi-version pacman pairs beyond expac unexercised"*, is also
**stale**: `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:15` is headed
*"Targets — cached pacman pairs (`uniq -d` walk: 354 duplicated pkgbases)"* and
lists the `1password-cli` 2.34.1→2.40.0 pair plus a `qpdf` control pair. Three
seats reached this independently: **RV-3** by clause-level reading, **EX-15** as
adjudication item C1, and **VZ-4** by corpus read plus a needle sweep on the
patched tree (it survives at `PROVINCE.md:159`). **VZ-2's census rated it `current`
— the outlier — and EX-15 diagnosed why**: its row tests the substring against
`corpus_has("expac")`, which trivially matches the r2 entry that *defines* the
expac baseline. As EX-15 put it, the test confirms the bullet's *text* exists, not
that the *claim* is true. A substring census is not a truth test.

**A content defect in the text that would land (sustained; RV-4 found it, VZ-2
re-derived every leg).** Both EX-14 candidates write `real solc-0.8.37 carriers
(Core, arc3-r1)` — a **false Core promotion**. Measured: the r1 and r3 EVM entries
each say "RESULT-class, **no Core promotion**"; `PROVINCE.md:54` (the Core EVM row)
cites only `(r3-07)`; and `PROVINCE.md:75-76` requires a `LOG.md` entry citing the
earning corpus entries, which does not exist. Landing the patch as written writes a
false promotion into a scoped file. Correct form: drop `(Core, …)` and `held`,
e.g. `real solc-0.8.37 carriers (arc3-r1/r3) and Vyper 0.4.3 (r4) — RESULT-class`.

**Two gate blind spots this chain measured (residuals, not repaired — the census
instrument is chain c1's to edit):**

- **R1** — the entire Frontier region (`PROVINCE.md:72-118`) and the post-unlock
  frontier (`:132-162`) are **UNDECLARED** in the scope table, and the EVM bullet
  never matches the instrument's `REA_GATE` needle, so the gate reads the *same*
  PASS before and after. **A census PASS certifies locus hygiene and anchor
  agreement, not claim truth** — which is why this verdict rests on the clause-level
  audit, not on the PASS.
- **R2** — `ptr_check` is only reached when a clause carries **no** pin, so
  `PROVINCE:18`'s `config.toml:3298` pointer is silently un-evaluated (that clause
  carries the `rea-agents@6.7.0` pin). Calling `ptr_check` directly returns `stale`
  for :3298 and `ok` for :3546.

**The repair set became complete after the verdict was written (VZ-4 measured).**
C2's verdict (14:14Z) correctly reported 6 → 2 at the then-current patch
(`candidate-complete-frontier-repair.patch.md`, `8a0e12ff…`) and correctly
sustained the false-`Core` content defect. Two artifacts landed afterwards:

1. **EX-14 published a new revision** —
   `candidate-complete-frontier-repair.v2.patch.md`, `0b8ad045…`, whose own header
   says *"Content defect fixed (verdict R4, sustained)"*. VZ-4 verified on the
   applied text: **0 occurrences of `Core, arc3-r1`**; the EVM bullet now reads
   *"real solc-0.8.37 (arc3-r1/r3) and Vyper 0.4.3 (r4) legs held K/K
   (RESULT-class)"*.
2. **EX-13 published per-row patches for both survivors** —
   `province-frontier-alternate-providers-jeb.patch.md` (F3) and
   `province-core-fallback-readers-inventory.patch.md` (C1).

**VZ-4 applied all three on a scratch tree** (`patch --batch --forward`, 6 hunks,
fuzz 1) → `PROVINCE.md` **held at 162 lines**, and a needle sweep found **all six
stale needles repaired/absent**: `Reserve: 91MB`, `JEB (unprobed)`, `real
solc/vyper-compiled bytecode untested`, `still probe-refused since r2`,
`absent: \`7z\``, `Next: raise`.

**One measured caveat the parent must not skip:** the census instrument
**cannot grade repairs**. `province-staleness-census.py` computes each row's
verdict from *live evidence* (corpus greps and command re-runs), not from
PROVINCE's text, so it prints the same `stale=6` against the original **and** the
fully-patched file. That is by design, and VZ-2 said so — the claim's acceptance
test is the **clause-level audit** (`grep -F` per row), not the census tally.

**Admission input (revised again):** the parent can reach **`stale 0`** by landing
**three** patch texts — EX-14 v2 + EX-13's F3 + EX-13's C1 — with the line count
held at 162 and the clause-level audit run after landing. That flips C2 from
NOT-VERIFIED to a satisfiable claim, and the false-`Core` clause is already fixed
in v2. If the parent instead lands only the older `8a0e12ff…` revision, C2 stays
an honest partial (6 → 2) **and** would write the false promotion — so **v2 is the
revision to land.**

### C3 — operability (fleet): custody-pair residual closures — **VERIFIED (VZ-4 first-hand, before AND after)**

The round's four named residuals all reproduce on the r3 base `7cd19c3c…` and all
close on the landed revision `29bb45ae…` (1343 L; README `125e7e02…`, 267 L).
Every row below is a VZ-4 run on a scratch copy of the tool — no custody path was
ever opened for writing.

| residual | before (`7cd19c3c…`) | after (`29bb45ae…`) |
|---|---|---|
| (a)-A `--out X --paths X.sha256` | exit 0, measured file **clobbered** (`fbeec2be…`→`cfcc6947…`) | **exit 2**, file intact, no receipt left |
| (a)-B `--out X.sha256 --paths X` (the freeze's literal spelling) | exit 0, a **genuine pre-existing sidecar clobbered** (`63fa9d49…`→`85deabbc…`) + stray `X.sha256.sha256` | **exit 2**, measured file *and* sidecar intact |
| (a)-B2 neighbour, no bystander | exit 0, stray second-order sidecar written | **exit 2**, nothing written |
| (b) `--out <regular-file>/sub/r.txt` | exit 1, raw `NotADirectoryError` traceback | **exit 2**, `USAGE: cannot create the receipt directory` |
| (b2) `--out ""` (control) | exit 2 (already declared) | exit 2 — **no regression** |
| (c) 5× duplicate stanza + `--require-paths 5` | exit 0, silent `MATCH paths=1` | **exit 2**, `REFERENCE-COVERAGE: 1/5 paths present in reference` |
| (c)-ctrl 5 distinct paths + `--require-paths 5` | exit 0 | exit 0 — **no false positive** |
| (d) both-sides-absent | `MATCH` (`compared=0/11`) | **adjudicated in the tool header**: agreement-on-absence, only error-carrying stanzas are `UNEVALUABLE` |

**Selftest 22 → 28** on the landed bytes (claim bar ≥24), `CLEAN cases=28 passed=28
failed=0 exit=0`. **Sabotage arms (VZ-4, each fix reverted individually on the
landed bytes):** coverage-back-to-stanzas → exit 0 (residual returns); mkdir-back-
outside-try → exit 1 + traceback (residual returns); neighbour-arm removed →
exit 0 (residual returns). Every fix is load-bearing. EX-21's own evidence
independently corroborates: the r3 regression battery **41/41 hold** on the landed
tool, the live pre/post pair self-pins the landed sha256, and the two live receipts
(`live-pre.txt` `7f5a6fd5…`, `live-post.txt` `2225f866…`) verify `MATCH 5/5`.

**A mid-wave finding that mattered.** Before EX-21's landing, this seat measured
that the freeze's *literal* spelling (B) was **not** closed by any candidate then
in the tree: RV-7's DRESS2 fix shape (`6e920b22…`) closed A only, and EX-24's
`after`/`after2` variants both still read `L13-sidecar-path-residual exit=0
sidecar-clobbered=yes` (their diff is only the mkdir move). The landed revision
closes it by adding a `neighbours = {Path(str(g) + ".sha256")}` arm to the guard —
VZ-4 verified that arm is exactly what closes B (removing it returns the residual).
Full trail: `claims/cross/VZ-4/evidence/c3-residuals-before.txt` and
`c3-residuals-after.txt`.

**The chain's own verdict corroborates independently.** VZ-3's
`claims/c3/verdict.md` reads **VERIFIED** on every leg it could measure, built on
its own first-hand runs, and adds two things this seat did not have: a
**mutant-based sabotage matrix** (MUT-A/B/C each go DIRTY 26–27/28 with *exactly*
their target case(s) failing, not a crash), and a **cross-seat reconciliation**
naming each c3 seat's artifact and the check on it. VZ-3 also names four measured
residuals that do not void any leg — **R1** the SKILL.md registry row is unmet only
by non-application (patch text `8e56f3d9…`, verified line-neutral 390 → 390,
one changed line; the superseded `EX-24/evidence/SKILL.proposed.md` must NOT be
applied); **R2** EX-21's own (d) probe is mislabeled (it measures one-side-absent
and reads `ABSENT 13`; the true both-absent shape reads `MATCH exit 0`) — a
report-level defect, not a result-level one; **R3** EX-26's patched line count is
off by one (215, not 214 — the digest reproduces); **R4** the (c)+(d) compound case
(an all-absent 5-stanza reference passing the gate and reading `MATCH 5/5`) is
adjudicated by design, so the records must not quote an all-absent `MATCH 5/5` as a
content witness. This seat's independent runs agree with VZ-3 on every shared leg.

**RV-6 (reviewer) adds one coverage finding, which I verified independently.** The
`--out`-with-no-usable-name guard (`--out ''` / `--out '.'` → declared `USAGE 2`,
the CR-4 item-6 trap) is **present, correct and reachable** on the landed bytes —
but it has **no case in the shipped 28-case selftest** (the only name-containment
match, `same-content-rewrite-rename-inode-pin`, is an unrelated rename/inode case).
That is a **coverage gap, not a defect**: the 28-case count is honest, the guard is
proven by RV-6's and EX-27's separate harnesses, and the wave's selftest bar (≥24)
is met. Recorded at `claims/cross/VZ-4/evidence/c3-m5-coverage-gap.txt` so the
parent does not mistake the count for full coverage of the new guard.

### Cross chain — CN-1, CN-2, CU-1, VZ-4

CU-1 verified the authorized install post-hoc (venv identity, wheel sha, custody
pre/post pair `MATCH 5/5`). CN-1/CN-2 carry the consistency/merge work. This seat
(VZ-4) delivered this file plus its evidence directory.

---

## 3. Custody outcome

- **VZ-4's own pre-receipt**, captured read-only at 14:05:02Z by the *r3* tool
  `7cd19c3c…` (`claims/cross/VZ-4/evidence/vz4-pre.txt`, sha256 `b2161fb8…`,
  sidecar present) — verified against live with the **landed** tool and the
  coverage gate: **`MATCH paths=5/5 drift=0 exit=0`**, `SHA256-CONTRACT: 5/5`.
- **The round's live pair** (EX-21, captured by the landed tool, both receipts
  self-pinning `29bb45ae…`) verifies `MATCH 5/5`.
- **Zero in-window drift** on all five paths across every one of my 30 poll
  checks (the watcher log carries the per-check hashes).
- The round-3 recorded operator-side drift on `~/.kimi-code/config.toml`
  (`8cbacd48…`→`bc66d543…`, pre-wave 12:57:45Z) is unchanged and still the only
  known divergence from the r1 canonical pins.
- Only C3's EX-21 wrote the real target `.ufo/gates/custody-pair/`. **The tool
  moved exactly once** (`7cd19c3c…` → `29bb45ae…`, 1155 → 1343 L) and has been
  stable since; **the README was rewritten five times inside ~3 min** and settled
  at **`9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`**
  (272 L / 15,293 B) — VZ-3's verdict records the full digest trail
  (`4a8f44c2…` → `91fd386b…` → `9a631196…` → `125e7e02…` → `9d9400da…`) and
  re-ran every README-side check on the settled bytes. The tool is unaffected by
  README churn, and the selftest re-run against the current tool bytes reads
  `CLEAN cases=28 passed=28 failed=0 exit=0`.
  **Rule-#14 hazard for the parent:** any text pinning the README sha256 must be
  re-derived at the records commit — the value in this file is a timestamped
  observation, not a landing pin. Full per-check trail:
  `claims/cross/VZ-4/evidence/identity-churn-log.txt`.

---

## 4. Wave instruments at baseline and at the landed state

| instrument | at HEAD `015e1ba` (VZ-4 run) | at the landed state (VZ-4 run) |
|---|---|---|
| command A | 83/83, missing [], dangling [], 14/14, 10.0/10.0 | parent re-derives at the records commit (C1 adds one file → expect 84/84) |
| census `c1-census-v10.py --root .` | PASS (0/0/0/0) exit 0 | PASS (0/0/0/0) exit 0 |
| citation-drift probe | findings=0 (reported and `--strict`), selftest 13/13 | unchanged |
| custody selftest | 22/22 CLEAN | **28/28 CLEAN** |
| custody live pair | — | **MATCH 5/5** |

Baselines captured at `claims/cross/VZ-4/evidence/instruments-baseline.txt`.

---

## 5. Attacks / refutations attempted (this seat)

1. **"The freeze's literal sidecar spelling is closed by the candidate fixes."**
   → **REFUTED at the time, now CLOSED.** Measured B open on base, on DRESS2, and
   on EX-24's variants; the landed revision's neighbour arm closes it (verified,
   and verified load-bearing by removing the arm).
2. **"The C1 K/K comparison against vyper's own output is safe."** → **CONFIRMED
   as a real trap** (phantom `__default__` + leading-zero stripping) **and
   REFUTED as a defect** — the chain's own scripts normalize both.
3. **"The r3 JUMPDEST offset reading generalizes to Vyper."** → **REFUTED**
   first-hand: 0/15, 0/9, 0/4 on JUMPDEST; 15/15, 9/9, 4/4 immediately after
   JUMPI.
4. **"The PROVINCE Frontier bullet is fine."** → **REFUTED**; stale on both legs,
   and the line-neutral repair holds the 162-line count with census PASS.
5. **"The custody selftest growth is cosmetic."** → **REFUTED** — the three
   sabotage arms each restore their residual, and the selftest cases exercise the
   same paths (28 cases, including the new neighbour/coverage cases).
6. **"The real target drifted mid-wave in a way that breaks the pair."** →
   **REFUTED** — the r3-era pre-receipt still verifies MATCH 5/5 against live
   under the landed tool; zero in-window drift.

---

## 6. Parent-facing admission inputs

1. **C1 — admit conditional on the entry landing; the landing is rehearsed.**
   VZ-4 reproduced the full projection on the actual landing source: the entry
   **literal block** (`da42d9a2…`, 32 lines / 18,166 B — byte-exact to SC-1's own
   identity) written as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`,
   plus the additive line-neutral map token → command A reads **84/84, missing [],
   dangling [], 14/14, 10.0/10.0**, README held at **190 lines** (`1cd05260…`,
   matching SC-1's independent prediction), and the **prior 83 knowledge files
   byte-identical (83/83, 0 mismatches** vs their git-HEAD blobs). Re-run at the
   records commit to confirm. **State the Vyper offset convention** (offsets sit
   `push4_pc + 11`, immediately after the compare `JUMPI`, not on `JUMPDEST`) and
   the two comparison-basis rules (ABI functions only — the `__default__` phantom;
   zero-padded 8-hex — vyper strips leading zeros) in the entry, or its own
   structural claims will read as failures. The C1 seats' own tooling already
   normalizes both bases.
2. **C2 — admit the patch set, then re-measure; one clause still needs rewording.**
   Land the PROVINCE repairs with the **line count held at 162** and run the
   **clause-level audit** after landing (`grep -F` per stale row) — **not** the
   census tally, which cannot grade repairs (it measures live evidence, not text).
   **Two candidate paths, both measured by VZ-4 on scratch roots:**
   - **PL-2's `candidate-with-s5.patch.md` — the most complete content, but NOT
     landable with `patch`.** Its 22 hunks land with a content-anchored applier
     (VZ-4 verified: 162 lines, `163a546e…`, census **PASS 0/0/0/0**, **all seven
     stale needles repaired** including the pacman clause, plus S5/C50/C62 repairs
     beyond the other paths). **However the files are not standard unified diffs**
     — the hunks carry a `@@ line NN @@` header, `patch` rejects them outright
     (*"Only garbage was found in the patch input"*), and PL-2 ships **no
     applier**. If this content is wanted, get a standard-diff emission from
     PL-2's generator or apply with a content-anchored applier and re-derive.
   - **EX-11's `frontier-repair-{A,B,C,D}`** — 7 hunks, **standard diff, clean
     under `--fuzz=0`**, 162 lines, `e2335400…`, census PASS. 6 of 7 needles (the
     pacman clause survives).
   - **EX-14 v2 (`0b8ad045…`) + EX-13's F3 + EX-13's C1** — 6 hunks, 162 lines,
     but **6 of 7** needles: the pacman clause survives (VZ-4 verified at
     `PROVINCE.md:159` of the patched tree).

   **Either path needs exactly one more edit — the X1a clause.** Both current
   wordings are wrong, in opposite directions (VZ-4 read the corpus):
   - EX-13's says *"all three input classes"* cited to **r12**, whose own text
     says *"both classes"* — an overreach (RV-3's finding).
   - PL-2's says *"the runtime-reconciliation input class **stays untested**"* —
     **stale as of r14-01**, whose headline reads *"L203's last input class
     EXERCISED"* (`ev_8f0ac46c…`, exit 0, 0.75 s).
   - **Correct form:** *"compare-application-versions is exercised across all
     three input classes since r14-01 (two at r12-02; the runtime-reconciliation
     sub-class closed at r14-01), and multi-version pacman pairs are exercised
     (`op` 2.34.1→2.40.0, r4-10)"* — with the corpus's own caveat that
     "exercised" is not "correct" (r14-01 records a directional coverage law and a
     paired-items-stay-unknown law).

   **A third verified candidate: EX-11's `frontier-repair-{A,B,C,D}.patch.md`.**
   The set applies **7 hunks**, holds `PROVINCE.md` at **162 lines**, reaches
   **`e2335400…`**, and reads census **PASS 0/0/0/0** — VZ-4 reproduced all of
   that byte-exactly. **Incident, now discharged:** EX-11's first revision of
   `frontier-repair-A.patch.md` carried a **fabricated header digest**
   (`881b5b1c…`, a descending-digit placeholder; the real single-patch state was
   `55df4301…`) and cited a **non-existent evidence file**. VZ-4 found both; EX-11
   then revised the artifact — the fabricated value is gone, the file's sha moved
   to `d4f9f64c…` (matching EX-11's own report), the evidence files now exist, and
   the four-patch claim reproduces. Recorded as a caught incident, superseded by
   the repaired artifact.

   **Warning on EX-14 v2's hunk 6 (CR-2's finding, VZ-4 confirmed):** v2 is
   **not a clean patch** — under `--fuzz=0` **5 of 6 hunks fail**; it lands only
   via patch's default fuzz tolerance, and the X1 bullet it produces is
   **self-contradictory** (`"still refused since r2: r12-02 drained the row with
   two success legs"`). The digest `69ceea9b…` is reproducible, but it is the
   digest of a tree containing that defective sentence — **reproducibility of a
   digest is not correctness of the text.** **Land CR-2's
   `proposed-x1-context-fix.patch.md` hunk in place of v2's hunk 6**; VZ-4
   verified it applies cleanly under **strict fuzz=0** and yields a coherent
   sentence.
   The real `PROVINCE.md` is untouched in the worktree; the patch texts are the
   deliverable.
3. **C3 — admit the tool at its landed revision with the coupled texts.** Commit
   `.ufo/gates/custody-pair/custody-pair.py` (**`29bb45ae…`**, 1343 L) +
   `.ufo/gates/custody-pair/README.md` (**settled at `9d9400da…`**, 272 L — the
   value VZ-3's verdict and my own watcher agree on; the earlier `125e7e02…` in
   this file was a transient) + one registry-row voice: **EX-21's**
   `patch/skill-registry-row.patched.md` (`8e56f3d9…`, line-neutral 390 → 390,
   one changed line — **do NOT apply** the superseded
   `EX-24/evidence/SKILL.proposed.md`). Re-run: selftest 28/28, the injection
   matrix, the 41/41 r3 battery, the live pair. The (d) ruling text is in the tool
   header and README. Note RV-6's **M5**: the `--out`-no-usable-name guard is
   correct and reachable but has no case in the shipped 28-case suite.
4. **Wave-level — the coupled landing is projected and green.** CN-2's
   `receipts/coupled-projection.txt` projects C2's PROVINCE patch + C3's SKILL row
   + the records section onto a clone: `PROVINCE.md` `dfa70b42…` (162 L),
   `SKILL.md` `8e56f3d9…` (390 L), census **PASS 0/0/0/0**, citation probe
   `--strict` **clean findings=0**. **VZ-4 independently verified the records
   half**: CN-2's merged section (`7bfeaa90…`) and LOG entry (`815980b9…`) are
   **pin-free CLEAN** by CN-2's own checker (0 pin/version/pointer tokens), and
   appending the merged SCORECARD section to a scratch root (1580 → 1760 lines)
   leaves the census at **PASS 0/0/0/0**. The custody tool and README are
   **uncommitted worktree edits**
   (` M` in `git status`); the parent lands and re-derives everything (rule #14).
   Records should quote the delivered count **per lane** and the lane
   substitution (§1). `__pycache__/` under `.ufo/gates/custody-pair/` is untracked
   residue — keep it out of the landing commit. The pre-existing dirty
   ` M .ufo/waves/arc2-loop1-round10/C3.md` is not this round's.

---

## 7. Closing census (appended at poll close)

See the appended block at the bottom of this file: seats delivered /48 against the
frozen roster, with the undelivered named, plus the per-chain tallies.

*Written by seat VZ-4; this seat wrote only this file, `seats/VZ-4.md` and
`claims/cross/VZ-4/**`. No git mutation of the real repo; custody paths read-only;
scratch under `/var/tmp/vz4` (never `/tmp`); no
corpus/LOG/SCORECARD/README/SKILL/PROVINCE writes.*

---

## 8. Closing census (poll window closed 2026-10-19T14:30Z, check 27/30)

**Delivered: 48/48 seat reports** against the frozen roster — a **complete wave**.

**Undelivered: none.** Verified at 14:31Z: `seats/` holds exactly 48 `.md` reports,
every one matching a frozen roster name, no stray file, no zero-byte report, and no
seat is artifacts-only. The 47/48 figure in the paragraph below was the count at
the moment of the census write; this seat's own report landed immediately after,
closing the roster at **48/48** — the same rule the r3 integrator followed.

**Per-chain tallies (final, 48/48):**

| chain | roster | delivered | undelivered |
|---|---|---|---|
| c1 (coverage) | 16 — PL-1, EX-01…EX-10, SC-1, RV-1, RV-2, CR-1, VZ-1 | **16/16** | none |
| c2 (freshness) | 14 — PL-2, EX-11…EX-17, SC-2, RV-3, RV-4, RV-5, CR-2, VZ-2 | **14/14** | none |
| c3 (operability) | 14 — PL-3, EX-21…EX-27, SC-3, RV-6, RV-7, RV-8, CR-3, VZ-3 | **14/14** | none |
| cross | 4 — CN-1, CN-2, CU-1, VZ-4 | **4/4** | none |

**Every seat wrote its report.** No seat is artifacts-only, no seat is empty, and
no seat report is zero-byte. This is a **complete wave** — the first in the arc
with no report deficit (r1: 54/64 under harness interruption; r2: 64/64;
r3: 62/64 with two reports pending).

**Real-target freeze through the window** (26 watcher checks + 27 poller checks):
- `.ufo/gates/custody-pair/custody-pair.py` — moved **once** (`7cd19c3c…` →
  `29bb45ae…`, 1155 → 1343 L), stable after.
- `.ufo/gates/custody-pair/README.md` — settled at `9d9400da…` (272 L).
- `corpus/README.md` `a451ad16…` (190 L), `PROVINCE.md` `d075a3c6…` (162 L),
  `SKILL.md` `5eec51c0…` (390 L), pointer-table `1b3ab955…` — **unchanged all
  window**, confirming the seat discipline (patch texts only) held for every
  scoped file.
- `corpus/knowledge/` — 83 files at close (the C1 entry is still patch text).

**Instruments at close (VZ-4 runs):** command A `83/83, missing [], dangling [],
14/14, 10.0/10.0`; census `PASS 0/0/0/0`; citation-drift probe `findings=0` both
modes + selftest 13/13; custody selftest `28/28 CLEAN`; live pairs `MATCH 5/5`
(both VZ-4's own r3-captured pre-receipt and EX-21's landed-tool pair).

**Per-chain verdicts at close:** C1 **VERIFIED**; C2 **VERIFIED** (revised from
NOT-VERIFIED, with one X1 wording edit and CR-2's hunk-6 correction still
required); C3 **VERIFIED** (one claim leg — the SKILL registry row — unmet only
by non-application).

*End of the wave summary. This seat wrote only this file, `seats/VZ-4.md` and
`claims/cross/VZ-4/**`. No git mutation of the real repo; custody paths read-only;
scratch under `/var/tmp/vz4` (never `/tmp`); no
corpus/LOG/SCORECARD/README/SKILL/PROVINCE writes.*
